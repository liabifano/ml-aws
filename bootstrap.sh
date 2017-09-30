#!/usr/bin/env bash
set -euo pipefail

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

echo "------------------------------------------------------------------------------------------"
echo "This script will create: "
echo "  1. A repository to save the docker images that will be created when the model in deployed"
echo "  2. Key-value pair to allow SSH into the instances"
echo "  3. Stack with a database Postgres9.6 to store input/outputs of the models"
echo "------------------------------------------------------------------------------------------"

echo
if [[ -z $(aws ecr describe-repositories | \
           jq -r --arg RN "${DOCKER_REPOSITORY_NAME}" '.repositories[] | select(.repositoryName==$RN)') ]];
    then
        echo "Creating docker repository ${DOCKER_REPOSITORY_NAME} in aws"
        aws ecr create-repository --repository-name ${DOCKER_REPOSITORY_NAME};
    else
        echo "The docker repository ${DOCKER_REPOSITORY_NAME} has already been created";
fi

echo "----------------------------------------------------------"
echo
if [[ -z $(aws ec2 describe-key-pairs | jq -r --arg KY "$KEY_VALUE_PAIR" '.KeyPairs[] | select(.KeyName==$KY)') ]];
    then
        echo "Creating key-value pair ${KEY_VALUE_PAIR} in aws"
        aws ec2 create-key-pair --key-name ${KEY_VALUE_PAIR} --output text --query 'KeyMaterial' >  `pwd`/secrets/${KEY_VALUE_PAIR}.pem
        chmod 400 `pwd`/secrets/${KEY_VALUE_PAIR}.pem
        echo "The key-value pair ${KEY_VALUE_PAIR} is in `pwd`/secrets/${KEY_VALUE_PAIR}.pem"
    else
        echo "The key-value pair ${KEY_VALUE_PAIR} has already been created";
fi

echo "----------------------------------------------------------"
echo
if [[ -z $(aws rds describe-db-instances | jq -r --arg DB "$DB_NAME" '.DBInstances[] | select(.DBName==$DB)') ]];
    then
        echo "Creating DB stack ${DB_NAME} in aws"
        aws cloudformation create-stack --stack-name db-${DB_NAME} \
                                        --template-body file://cf-db.json \
                                        --parameters ParameterKey=DBName,ParameterValue=${DB_NAME} \
                                                     ParameterKey=DBUsername,ParameterValue=${DB_USER} \
                                                     ParameterKey=DBPassword,ParameterValue=${DB_PASSWORD}
    else
        echo "The database ${DB_NAME} has already been created";
fi

echo "----------------------------------------------------------"
echo
echo ">>> The next step is to run train-and-deploy-it.sh"
echo "----------------------------------------------------------"