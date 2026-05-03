#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   EchoCAD Docker Compose Manager      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Function to display usage
usage() {
    echo -e "${YELLOW}Usage: $0 {start|stop|restart|status|logs|clean}${NC}"
    echo ""
    echo "Commands:"
    echo "  start       - Start all containers"
    echo "  stop        - Stop all containers"
    echo "  restart     - Restart all containers"
    echo "  status      - Show container status"
    echo "  logs        - Show live logs (all containers)"
    echo "  logs-api    - Show API logs"
    echo "  logs-mysql  - Show MySQL logs"
    echo "  logs-ollama - Show Ollama logs"
    echo "  clean       - Stop and remove containers + volumes"
    echo "  build       - Build and start with fresh containers"
    exit 1
}

# Function to start containers
start() {
    echo -e "${BLUE}Starting EchoCAD services...${NC}"
    cd "$SCRIPT_DIR"
    
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Services started successfully!${NC}"
        echo ""
        echo -e "${YELLOW}Waiting for services to be ready...${NC}"
        sleep 5
        
        echo -e "${BLUE}Service Status:${NC}"
        docker-compose ps
        
        echo ""
        echo -e "${GREEN}✓ EchoCAD is starting up:${NC}"
        echo "  - MySQL:    localhost:3306"
        echo "  - Ollama:   localhost:11434"
        echo "  - Backend:  localhost:8000"
        echo "  - API Docs: http://localhost:8000/docs"
        echo ""
        echo -e "${YELLOW}Note: Models may take 5-15 minutes to download. Check progress with: $0 logs-ollama${NC}"
    else
        echo -e "${RED}✗ Failed to start services${NC}"
        exit 1
    fi
}

# Function to stop containers
stop() {
    echo -e "${BLUE}Stopping EchoCAD services...${NC}"
    cd "$SCRIPT_DIR"
    
    docker-compose down
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Services stopped successfully!${NC}"
    else
        echo -e "${RED}✗ Failed to stop services${NC}"
        exit 1
    fi
}

# Function to restart containers
restart() {
    echo -e "${BLUE}Restarting EchoCAD services...${NC}"
    stop
    sleep 2
    start
}

# Function to show status
status() {
    echo -e "${BLUE}EchoCAD Service Status:${NC}"
    echo ""
    cd "$SCRIPT_DIR"
    docker-compose ps
    
    echo ""
    echo -e "${BLUE}Container Resource Usage:${NC}"
    docker stats --no-stream $(docker-compose ps -q) 2>/dev/null || echo "No containers running"
}

# Function to show logs
logs() {
    echo -e "${BLUE}Live logs (press Ctrl+C to exit):${NC}"
    cd "$SCRIPT_DIR"
    docker-compose logs -f --tail=50
}

# Function to show specific logs
logs_service() {
    local service=$1
    echo -e "${BLUE}Live logs for $service (press Ctrl+C to exit):${NC}"
    cd "$SCRIPT_DIR"
    docker-compose logs -f --tail=100 "$service"
}

# Function to clean everything
clean() {
    echo -e "${RED}This will remove all containers and volumes!${NC}"
    read -p "Are you sure? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Cleaning up...${NC}"
        cd "$SCRIPT_DIR"
        docker-compose down -v
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Cleanup completed!${NC}"
        else
            echo -e "${RED}✗ Cleanup failed${NC}"
            exit 1
        fi
    else
        echo "Cleanup cancelled"
    fi
}

# Function to build and start
build() {
    echo -e "${BLUE}Building and starting fresh containers...${NC}"
    cd "$SCRIPT_DIR"
    
    docker-compose up -d --build
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build completed and containers started!${NC}"
        sleep 5
        docker-compose ps
    else
        echo -e "${RED}✗ Build failed${NC}"
        exit 1
    fi
}

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ docker-compose not found. Please install Docker and docker-compose${NC}"
    exit 1
fi

# Main command handling
case "${1:-}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    logs-api)
        logs_service "api-backend"
        ;;
    logs-mysql)
        logs_service "mysql"
        ;;
    logs-ollama)
        logs_service "ollama_puller"
        ;;
    clean)
        clean
        ;;
    build)
        build
        ;;
    *)
        usage
        ;;
esac
