# deploy.sh
#!/bin/bash

# Deploy script
echo "Deploying agent system..."

# Create dist directory
mkdir -p dist

# Clean previous build
rm -rf dist/*

# Copy source files
# Updated from "cp -r src dist/" to "cp -r cmate dist/"
cp -r cmate dist/
cp -r config dist/

# Copy requirements
cp requirements/prod.txt dist/requirements.txt

# Create necessary directories
mkdir -p dist/logs
mkdir -p dist/temp
mkdir -p dist/workspace

echo "Deployment completed"
