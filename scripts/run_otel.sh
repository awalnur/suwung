# /scripts/run_monitoring.sh
#!/bin/bash

# Get the absolute path to the project root directory
PROJECT_ROOT=$(pwd)

# Stop existing containers
docker compose -f ${PROJECT_ROOT}/config/docker-compose.yml down

# Start the services
docker compose -f ${PROJECT_ROOT}/config/docker-compose.yml up -d

# Check if services are running
docker compose -f ${PROJECT_ROOT}/config/docker-compose.yml ps


