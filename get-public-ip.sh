#!/bin/bash

set -e

CLUSTER_NAME="jbr-cluster"
PORT="8000"

echo "Fetching public IP..."

TASK_ARN=$(aws ecs list-tasks \
  --region eu-west-2 \
  --cluster "$CLUSTER_NAME" \
  --desired-status "RUNNING" \
  --query "taskArns[0]" \
  --output text)

echo "Found Task ARN: $TASK_ARN"

ENI_ID=$(aws ecs describe-tasks \
  --region eu-west-2 \
  --cluster "$CLUSTER_NAME" \
  --tasks "$TASK_ARN" \
  --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" \
  --output text)
  echo "Found ENI_ID: $ENI_ID"

PUBLIC_IP=$(aws ec2 describe-network-interfaces \
  --region eu-west-2 \
  --network-interface-ids "$ENI_ID" \
  --query "NetworkInterfaces[0].Association.PublicIp" \
  --output text)

echo ""
echo "=================================================="
echo "Deployed Public IP:"
echo "$PUBLIC_IP:$PORT"
echo "=================================================="