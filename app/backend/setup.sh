#!/bin/bash

# EchoCAD Setup Script - First Time Setup
# This script prepares your environment and starts all services

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🚀 EchoCAD Backend - First Time Setup                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check Docker
echo -e "${BLUE}[1/5] Checking Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found. Please install Docker${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

# Check Docker Compose
echo -e "${BLUE}[2/5] Checking Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not found. Please install Docker Compose${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found${NC}"

# Create .env if doesn't exist
echo -e "${BLUE}[3/5] Setting up environment variables...${NC}"
cd "$SCRIPT_DIR"

if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env created${NC}"
    echo -e "${YELLOW}  Note: Review .env for any needed adjustments${NC}"
else
    echo -e "${GREEN}✓ .env already exists${NC}"
fi

# Make docker-manage.sh executable
echo -e "${BLUE}[4/5] Setting up management script...${NC}"
if [ -f "docker-manage.sh" ]; then
    chmod +x docker-manage.sh
    echo -e "${GREEN}✓ docker-manage.sh is executable${NC}"
fi

# Start services
echo -e "${BLUE}[5/5] Starting services...${NC}"
echo ""

docker-compose down -v 2>/dev/null || true
docker-compose up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Services started successfully!${NC}"
else
    echo -e "${RED}✗ Failed to start services${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Wait for services to initialize (5-15 minutes for model download)"
echo "2. Check status: ${CYAN}./docker-manage.sh status${NC}"
echo "3. View logs: ${CYAN}./docker-manage.sh logs${NC}"
echo ""

echo -e "${YELLOW}Access Points:${NC}"
echo "  📖 API Docs: ${CYAN}http://localhost:8000/docs${NC}"
echo "  🗄️  MySQL: ${CYAN}localhost:3306${NC} (echocad_admin / echocad_admin_password)"
echo "  🤖 Ollama: ${CYAN}http://localhost:11434${NC}"
echo ""

echo -e "${YELLOW}Useful Commands:${NC}"
echo "  View all logs: ${CYAN}./docker-manage.sh logs${NC}"
echo "  View API logs: ${CYAN}./docker-manage.sh logs-api${NC}"
echo "  View model download: ${CYAN}./docker-manage.sh logs-ollama${NC}"
echo "  Stop services: ${CYAN}./docker-manage.sh stop${NC}"
echo "  Restart services: ${CYAN}./docker-manage.sh restart${NC}"
echo ""

echo -e "${YELLOW}📝 For more details, see:${NC}"
echo "  - ${CYAN}QUICKSTART.md${NC} - Quick reference guide"
echo "  - ${CYAN}DOCKER_SETUP.md${NC} - Detailed Docker documentation"
echo ""

# Show initial status
echo -e "${BLUE}Current Container Status:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}Setup complete! Services are initializing...${NC}"
echo -e "${YELLOW}⏳ Models may take 5-15 minutes to download on first run${NC}"
