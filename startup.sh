#!/bin/bash
# Kill old containers
echo "Kill all previous homie-timeout builds..."

CONTAINER_IDS=$(docker ps -a -q --filter name='^homie-timeout')

if [ -z "$CONTAINER_IDS" ]; then
	echo "No containers matching 'homie-timeout' were found."
else
	COMMAND_OUTPUT=$(docker stop $CONTAINER_IDS 2>&1)
	if [ $? -eq 0 ]; then
		echo "Containers stopped: "
		echo "$COMMAND_OUTPUT"
		KILLED_CONTAINERS=$(docker rm $CONTAINER_IDS 2>&1)
		if [ $? -eq 0 ]; then
			echo "Containers removed: "
			echo "$KILLED_CONTAINERS"
		else
			echo "Error killing containers"
			echo "Error details:"
			echo "$KILLED_CONTAINERS"
		fi
	else
		echo "Error stopping containers"
		echo "Error details:"
		echo "$COMMAND_OUTPUT"
	fi
fi

# Generate unique build id
echo "generating timestamp"
TIMESTAMP=$(date +%s)
STAMP=$(printf '%x' "$TIMESTAMP")
BASE_NAME="homie-timeout"
DOCKER_NAME="${BASE_NAME}-${STAMP}"

# Build and Deploy
echo "Building $DOCKER_NAME container..."
docker build -t $DOCKER_NAME /home/service/discord-timeout-vote/
echo "Running $DOCKER_NAME..."
docker run -d --name $DOCKER_NAME --env-file /home/service/discord-timeout-vote/.env -it $DOCKER_NAME
echo "$DOCKER_NAME deployed. Homie of Timeouts is now online"
