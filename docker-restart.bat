# Stop and remove all containers
docker-compose down

# Build new image
docker-compose build --no-cache

# Start services
docker-compose up -d

echo "Digital Buddy restarted successfully!"
echo "Open: http://localhost:8501"
