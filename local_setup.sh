#!/bin/bash

# Local development setup script for Customer Subscription

set -e  # Exit on error

echo "🚀 Starting local development setup..."

# Create symlink for docker-compose.yml to default to local
echo "🔗 Setting up docker-compose.yml symlink..."
if [ ! -L docker-compose.yml ]; then
  ln -s docker-compose.local.yml docker-compose.yml
fi

# Cleanup before setup
echo "🛑 Cleaning up existing containers, system, and volumes..."
docker compose down 2>/dev/null || true
echo "🧹 Pruning Docker system..."
docker system prune -a -f
echo "💾 Removing volumes..."
docker volume prune -a -f

# Create logs folder
echo "📁 Creating logs folder..."
mkdir -p logs
chmod 755 logs

# Build and start Docker containers
echo "🐳 Building and starting Docker containers..."
docker compose up -d --build

# Wait for backend container to be ready
echo "⏳ Waiting for backend container to be ready..."
sleep 10

# Run migrations
echo "🔄 Running migrations..."
docker compose exec -T web python manage.py migrate

echo "✅ Setup complete! Your application is ready."
echo "🌐 Access the app at: http://localhost:8000"
