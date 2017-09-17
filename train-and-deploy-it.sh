#!/usr/bin/env bash
set -eo pipefail

while getopts ":r:k:d:u:p:" opt; do
  case $opt in
    r) DOCKER_REPOSITORY_NAME="$OPTARG";;
    k) KEY_VALUE_PAIR="$OPTARG";;
    d) DB_NAME="$OPTARG";;
    u) DB_USER="$OPTARG";;
    p) DB_PASSWORD="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

VERSION=`cat VERSION`
THIS_PATH=$(dirname `realpath $0`)
STACK_NAME=modelapp-${VERSION}
DOCKER_PREFIX=$(aws ecr get-login --no-include-email | awk 'match($0, /https*/) {print substr($0, RSTART+8)}')
DOCKER_REPOSITORY_PATH=${DOCKER_PREFIX}/${DOCKER_REPOSITORY_NAME}:${VERSION}

echo "--------------------------------------------------------------------------------------------------------"
echo "This script will: "
echo "  1. Check if there is already a docker image or a stack with the current version"
echo "  2. Train the model and save the model's output in resourses/model"
echo "  3. Build a docker image with all the dependencies of your application"
echo "  4. Push this image created to the repository previously created in bootstrap.sh"
echo "  5. Create a stack with a cluster of machines running the service specified in the pushed docker image"
echo "--------------------------------------------------------------------------------------------------------"

echo
echo "Checking if the stack is available"
echo "---------------------------------------------------------------------------------"
if [[ ! -z $(aws ecr describe-images --repository-name ${DOCKER_REPOSITORY_NAME} \
             | jq -r --arg V "${VERSION}" '.imageDetails[].imageTags[] | select(.==$V)') ]];
    then
        echo "The docker ${VERSION} has already been created, please bump your version or run revert-deploy.sh";
        exit 1
fi

if [[ ! -z $(aws cloudformation describe-stacks \
             | jq -r --arg S "${STACK_NAME}" '.Stacks[] | select(.StackName==$S)') ]];
    then
        echo "The stack ${STACK_NAME} has already been created, please bump your version or run deploy.sh";
        exit 1
fi



echo
echo "Train model version ${VERSION}"
echo "---------------------------------------------------------------------------------"
bash ${THIS_PATH}/modelapp/bootstrap-python-env.sh && \
. ${THIS_PATH}/modelapp-python-env/bin/activate && \
python3 ${THIS_PATH}/modelapp/src/modelapp/train.py

echo
echo "Building the image ${DOCKER_REPOSITORY_PATH}"
echo "---------------------------------------------------------------------------------"
eval $(docker-machine env default)
docker build -t ${DOCKER_REPOSITORY_PATH} .

echo
echo "Pushing the image ${DOCKER_REPOSITORY_PATH} to aws"
echo "---------------------------------------------------------------------------------"
eval $(aws ecr get-login --no-include-email)
docker push ${DOCKER_REPOSITORY_PATH}

echo
echo "Creating stack with a cluster of machines running the application"
echo "---------------------------------------------------------------------------------"
DB_INFOS=$(aws rds describe-db-instances \
           | jq -r --arg DB "${DB_NAME}" '.DBInstances[] | select(.DBName==$DB)')
DB_ENDPOINT=$(echo $DB_INFOS | jq '.Endpoint.Address' | sed 's/"//g')
DB_PORT=$(echo $DB_INFOS | jq '.Endpoint.Port')
DB_HOST="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_ENDPOINT}:${DB_PORT}/${DB_NAME}"

AMI_ID=$(aws ec2 describe-images --owners amazon --filters Name=root-device-type,Values=ebs Name=state,Values=available \
         | jq '.Images[] | select(.Name | contains("amazon-ecs-optimized"))' \
         | jq -s 'sort_by(.CreationDate)[-1].ImageId' \
         | sed 's/"//g')

aws cloudformation create-stack --template-body file://cf-ecs-cluster.json \
                                --stack-name $STACK_NAME  \
                                --parameters ParameterKey=KeyName,ParameterValue=${KEY_VALUE_PAIR} \
                                             ParameterKey=DBHost,ParameterValue=${DB_HOST} \
                                             ParameterKey=DBSecurityGroup,ParameterValue=rds-launch-wizard \
                                             ParameterKey=AMIImageId,ParameterValue=${AMI_ID} \
                                             ParameterKey=ImageECRId,ParameterValue=${DOCKER_REPOSITORY_PATH}