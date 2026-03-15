#!/bin/bash

# Configuration
REPO_URL="https://github.com/Sani-varda/alfred.git"
GIT_DIR="/home/ubuntu/.openclaw/workspace"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "ERROR: GITHUB_TOKEN is not set."
    exit 1
fi

# Clean up URL to insert token
AUTH_URL=$(echo $REPO_URL | sed "s/https:\/\//https:\/\/alfred:$GITHUB_TOKEN@/")

cd $GIT_DIR

# Check if git is initialized
if [ ! -d ".git" ]; then
    git init
    git remote add origin $AUTH_URL
else
    git remote set-url origin $AUTH_URL
fi

# Configuration
git config user.email "contact@moonlitarc.com"
git config user.name "Alfred (MoonLIT Arc)"

# Add and commit
git add .
git commit -m "chore: alfred system bootstrap and project initialization"

# Push
git push origin master --force
