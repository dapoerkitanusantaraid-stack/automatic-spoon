#!/bin/bash
# ============================================
# PROJECT SERVER - DEPLOYMENT HELPER
# ============================================

set -e

echo "🚀 PROJECT SERVER DEPLOYMENT HELPER"
echo "===================================="

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "msys" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "🖥️  Detected OS: $OS"

# Function to check command
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed"
        return 1
    else
        echo "✅ $1 installed"
        return 0
    fi
}

# Function to install dependencies
install_deps() {
    echo ""
    echo "📦 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
}

# Function to setup environment
setup_env() {
    echo ""
    echo "⚙️  Setting up environment..."
    
    if [ ! -f .env ]; then
        echo "Creating .env file from .env.example..."
        cp .env.example .env
        echo "⚠️  Please edit .env with your configuration"
    else
        echo "✅ .env already exists"
    fi
}

# Function to init database
init_database() {
    echo ""
    echo "🗄️  Initializing database..."
    python server/main.py --init-db 2>/dev/null || python init_sample_data.py
    echo "✅ Database initialized"
}

# Function to run development server
run_dev() {
    echo ""
    echo "🚀 Starting development server..."
    echo "📍 Server running at http://localhost:8000"
    echo "📊 Admin dashboard at http://localhost:8000/admin-dashboard.html"
    echo ""
    cd server
    python main.py
}

# Function to run production server
run_prod() {
    echo ""
    echo "🚀 Starting production server..."
    
    if ! check_command gunicorn; then
        echo "Installing gunicorn..."
        pip install gunicorn
    fi
    
    cd server
    gunicorn main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
}

# Function to test API
test_api() {
    echo ""
    echo "🧪 Testing API..."
    
    check_command curl || return 1
    
    echo "Testing health endpoint..."
    curl -s http://localhost:8000/ | python -m json.tool
    
    echo ""
    echo "✅ API is responding"
}

# Main menu
show_menu() {
    echo ""
    echo "📋 COMMANDS:"
    echo "  1. setup        - Install dependencies & setup environment"
    echo "  2. dev          - Run development server"
    echo "  3. prod         - Run production server"
    echo "  4. test         - Test API endpoints"
    echo "  5. db-init      - Initialize database"
    echo "  6. db-reset     - Reset database (delete & recreate)"
    echo "  7. docker       - Build & run in Docker"
    echo "  8. docker-stop  - Stop Docker container"
    echo "  9. logs         - Show server logs"
    echo "  10. help        - Show this menu"
    echo ""
}

# Parse arguments
case "${1:-help}" in
    setup)
        check_command python3 || check_command python
        install_deps
        setup_env
        echo ""
        echo "✅ Setup complete! Run './deploy.sh dev' to start"
        ;;
    
    dev)
        run_dev
        ;;
    
    prod)
        run_prod
        ;;
    
    test)
        test_api
        ;;
    
    db-init)
        init_database
        ;;
    
    db-reset)
        echo "⚠️  RESETTING DATABASE - This will delete all data!"
        read -p "Are you sure? Type 'yes' to confirm: " confirm
        if [ "$confirm" = "yes" ]; then
            rm -f data.db
            echo "Database file deleted"
            init_database
        else
            echo "❌ Cancelled"
        fi
        ;;
    
    docker)
        if ! check_command docker; then
            exit 1
        fi
        
        echo "🐳 Building Docker image..."
        docker build -t project-server .
        
        echo "🚀 Running Docker container..."
        docker run -p 8000:8000 -v $(pwd)/data.db:/app/data.db project-server
        ;;
    
    docker-stop)
        if ! check_command docker; then
            exit 1
        fi
        
        echo "🛑 Stopping Docker container..."
        container_id=$(docker ps -q -f ancestor=project-server)
        if [ ! -z "$container_id" ]; then
            docker stop $container_id
            echo "✅ Container stopped"
        else
            echo "❌ No running container found"
        fi
        ;;
    
    logs)
        echo "📋 Checking for log file..."
        if [ -f server.log ]; then
            tail -f server.log
        else
            echo "❌ No log file found"
        fi
        ;;
    
    help|*)
        echo "🚀 PROJECT SERVER DEPLOYMENT HELPER"
        show_menu
        ;;
esac
