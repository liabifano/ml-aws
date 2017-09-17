#!/usr/bin/env bash


while getopts ":r:d:p:u:v:" opt; do
  case $opt in
    r) DOCKER_REPOSITORY_NAME="$OPTARG";;
    d) DB_NAME="$OPTARG";;
    u) DB_USER="$OPTARG";;
    p) DB_PASSWORD="$OPTARG";;
    v) VERSION="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done


STACK_NAME=modelapp-${VERSION}

echo "--------------------------------------------------------------------------------------------------------"
echo "This script will: "
echo "  1. Delete docker image ${VERSION} from ${DOCKER_REPOSITORY_NAME}"
echo "  2. Delete stack ${STACK_NAME}"
echo "  3. Delete tables inputs_${VERSION} and outputs_${VERSION} from database ${DB_NAME}"
echo "--------------------------------------------------------------------------------------------------------"

echo
echo "Deleting docker image ${VERSION} from ${DOCKER_REPOSITORY_NAME}"
echo "---------------------------------------------------------------------------------"
aws ecr batch-delete-image --repository-name ${DOCKER_REPOSITORY_NAME} --image-ids imageTag=$VERSION

echo
echo "Deleting stack ${STACK_NAME}"
echo "---------------------------------------------------------------------------------"
aws cloudformation delete-stack --stack-name ${STACK_NAME}

DB_INFOS=$(aws rds describe-db-instances \
           | jq -r --arg DB "${DB_NAME}" '.DBInstances[] | select(.DBName==$DB)')
DB_ENDPOINT=$(echo $DB_INFOS | jq '.Endpoint.Address' | sed 's/"//g')
DB_PORT=$(echo $DB_INFOS | jq '.Endpoint.Port')

echo
echo "Deleting tables inputs_${VERSION} and outputs_${VERSION} from database ${DB_NAME}"
echo "---------------------------------------------------------------------------------"
PGPASSWORD=${DB_PASSWORD} psql --host=${DB_ENDPOINT} \
                               --port=${DB_PORT} \
                               --username=${DB_USER} \
                               --dbname=${DB_NAME} \
                               -c "DROP TABLE IF EXISTS inputs_${VERSION}, outputs_${VERSION}"
