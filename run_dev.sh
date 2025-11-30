#!/bin/bash

# Colors for logging
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print with timestamp
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] ✅ $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ❌ $1${NC}"
}

# Stop execution if any command fails
set -e

echo ""
echo -e "${YELLOW}==============================================${NC}"
echo -e "${YELLOW}      🚀 Vibrain Development Launcher         ${NC}"
echo -e "${YELLOW}==============================================${NC}"
echo ""

log "Phase 1: Testing Environment Initialization..."
log "Spinning up test containers and running pytest..."

# Run tests using the test compose file
# Capture exit code to handle failure gracefully with custom message
if docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit; then
    echo ""
    success "Tests Passed Successfully!"
else
    echo ""
    error "Tests Failed. Aborting startup."
    error "Check the logs above for details."
    exit 1
fi

echo ""
echo -e "${YELLOW}----------------------------------------------${NC}"
echo ""

log "Phase 2: Application Startup..."
log "Starting production containers (Backend + Redis + Mongo)..."

# Start the main application in detached mode
docker-compose up -d --build

echo ""
success "Application started successfully!"
echo -e "${BLUE}📍 Backend:${NC} http://localhost:8000"
echo -e "${BLUE}📄 Docs:   ${NC} http://localhost:8000/docs"
echo ""
log "Streaming logs for 'backend' service (Ctrl+C to exit logs, app keeps running)..."
echo ""
docker-compose logs -f backend
