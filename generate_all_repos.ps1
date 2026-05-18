param(
  [string]$GitHubUsername = "Raphasha27",
  [string]$BasePath = "C:\Users\nelso\OneDrive\Desktop\GitHubProjects",
  [switch]$PushToGitHub
)

$ErrorActionPreference = "Stop"

$repos = @(
  "enterprise-fastapi-starter",
  "react-admin-dashboard-pro",
  "repo-audit-bot",
  "saas-multitenant-backend",
  "docker-deployment-templates",
  "ai-prompt-cli",
  "ridewave-ui-simulation",
  "structured-logging-system",
  "secure-auth-rbac-template",
  "raphasha-dev-portfolio"
)

function Ensure-Folder($path) {
  if (!(Test-Path $path)) {
    New-Item -ItemType Directory -Path $path | Out-Null
  }
}

function Write-File($path, $content) {
  $dir = Split-Path $path
  Ensure-Folder $dir
  Set-Content -Path $path -Value $content -Encoding UTF8
}

function Git-Init-Commit($repoPath, $repoName) {
  Push-Location $repoPath

  git init | Out-Null
  git add . | Out-Null
  git commit -m "Initial commit - $repoName" | Out-Null
  git branch -M main | Out-Null

  if ($PushToGitHub) {
    $remote = "https://github.com/$GitHubUsername/$repoName.git"
    git remote add origin $remote
    git push -u origin main
  }

  Pop-Location
}

# Universal files
$gitignore = @"
.env
__pycache__/
*.pyc
node_modules/
dist/
build/
*.log
.DS_Store
.vscode/
.idea/
coverage/
"@

$license = @"
MIT License

Copyright (c) 2026 $GitHubUsername

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
"@

$security = @"
# Security Policy

## Reporting a Vulnerability
Please report vulnerabilities privately via GitHub or email.
Do not publish security issues publicly.
"@

$contributing = @"
# Contributing

## Workflow
1. Fork repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

## Rules
- Keep secrets out of commits
- Follow clean code principles
- Add tests where applicable
"@

$ci_python = @"
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
"@

$ci_node = @"
name: CI

on:
  push:
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm install
      - run: npm run build
"@

# Base folder
Ensure-Folder $BasePath

foreach ($repo in $repos) {
  $repoPath = Join-Path $BasePath $repo
  Ensure-Folder $repoPath

  Write-Host "Generating: $repo"

  Write-File "$repoPath\.gitignore" $gitignore
  Write-File "$repoPath\LICENSE" $license
  Write-File "$repoPath\SECURITY.md" $security
  Write-File "$repoPath\CONTRIBUTING.md" $contributing
  Ensure-Folder "$repoPath\.github\workflows"

  # Repo-specific scaffolding
  switch ($repo) {

    "enterprise-fastapi-starter" {

      Write-File "$repoPath\README.md" @"
# Enterprise FastAPI Starter

Production-ready FastAPI starter with Docker, PostgreSQL, and CI.

## Run
````bash
cp .env.example .env
docker-compose up --build
````

## Docs
http://localhost:8000/docs
"@

      Write-File "$repoPath\.env.example" @"
APP_NAME=EnterpriseFastAPIStarter
ENVIRONMENT=development
SECRET_KEY=changeme
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/appdb
"@

      Write-File "$repoPath\requirements.txt" @"
fastapi
uvicorn[standard]
python-dotenv
sqlalchemy
psycopg2-binary
pydantic
pytest
"@

      Write-File "$repoPath\docker-compose.yml" @"
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
"@

      Write-File "$repoPath\Dockerfile" @"
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
"@

      Ensure-Folder "$repoPath\app\api\routes"
      Ensure-Folder "$repoPath\app\api"
      Ensure-Folder "$repoPath\app\core"
      Ensure-Folder "$repoPath\tests"

      Write-File "$repoPath\app\main.py" @"
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Enterprise FastAPI Starter")

app.include_router(api_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Enterprise FastAPI Starter running"}
"@

      Write-File "$repoPath\app\api\router.py" @"
from fastapi import APIRouter
from app.api.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["Health"])
"@

      Write-File "$repoPath\app\api\routes\health.py" @"
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": "healthy"}
"@

      Write-File "$repoPath\tests\test_health.py" @"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health/")
    assert res.status_code == 200
"@

      Write-File "$repoPath\.github\workflows\ci.yml" $ci_python
    }

    "repo-audit-bot" {

      Write-File "$repoPath\README.md" @"
# Repo Audit Bot

CLI tool that audits repos for missing security files and best practices.

## Run
````bash
python src/main.py
````
"@

      Write-File "$repoPath\requirements.txt" @"
pytest
"@

      Ensure-Folder "$repoPath\src\checks"
      Ensure-Folder "$repoPath\src\core"

      Write-File "$repoPath\src\checks\readme_check.py" @"
import os

def check_readme(repo_path: str):
    return os.path.exists(os.path.join(repo_path, "README.md"))
"@

      Write-File "$repoPath\src\checks\env_check.py" @"
import os

def check_env(repo_path: str):
    return not os.path.exists(os.path.join(repo_path, ".env"))
"@

      Write-File "$repoPath\src\core\runner.py" @"
from src.checks.readme_check import check_readme
from src.checks.env_check import check_env

def run_checks(repo_path: str):
    results = {
        "README.md": check_readme(repo_path),
        ".env not committed": check_env(repo_path),
    }
    for k, v in results.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
"@

      Write-File "$repoPath\src\main.py" @"
import os
from src.core.runner import run_checks

if __name__ == "__main__":
    run_checks(os.getcwd())
"@

      Write-File "$repoPath\.github\workflows\ci.yml" $ci_python
    }

    "structured-logging-system" {

      Write-File "$repoPath\README.md" @"
# Structured Logging System

Reusable JSON logging module for Python backends.
"@

      Ensure-Folder "$repoPath\python"

      Write-File "$repoPath\python\logger.py" @"
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record),
        })

def get_logger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger
"@

      Write-File "$repoPath\python\example.py" @"
from logger import get_logger

log = get_logger()
log.info("Structured logging active")
"@
    }

    "secure-auth-rbac-template" {

      Write-File "$repoPath\README.md" @"
# Secure Auth + RBAC Template

Starter repo demonstrating secure authentication architecture.
"@

      Ensure-Folder "$repoPath\app"

      Write-File "$repoPath\.env.example" @"
SECRET_KEY=changeme
"@

      Write-File "$repoPath\app\main.py" @"
from fastapi import FastAPI

app = FastAPI(title="Secure Auth + RBAC Template")

@app.get("/")
def root():
    return {"message": "Auth + RBAC Template"}
"@

      Write-File "$repoPath\requirements.txt" @"
fastapi
uvicorn[standard]
python-dotenv
pytest
"@

      Write-File "$repoPath\.github\workflows\ci.yml" $ci_python
    }

    "docker-deployment-templates" {

      Write-File "$repoPath\README.md" @"
# Docker Deployment Templates

Collection of reusable docker-compose templates.
"@

      Ensure-Folder "$repoPath\templates\fastapi-postgres"
      Ensure-Folder "$repoPath\templates\node-mongo"
      Ensure-Folder "$repoPath\templates\nextjs"

      Write-File "$repoPath\templates\fastapi-postgres\docker-compose.yml" @"
version: "3.9"
services:
  api:
    image: tiangolo/uvicorn-gunicorn-fastapi:python3.11
    ports:
      - "8000:80"
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: appdb
"@
    }

    "ridewave-ui-simulation" {

      Write-File "$repoPath\README.md" @"
# RideWave UI Simulation

UI simulation for Rider + Driver + Admin.
This is a safe public demo repo (no real keys).
"@

      Ensure-Folder "$repoPath\mobile\rider"
      Ensure-Folder "$repoPath\mobile\driver"
      Ensure-Folder "$repoPath\admin-dashboard"
      Ensure-Folder "$repoPath\architecture"

      Write-File "$repoPath\architecture\system-diagram.md" @"
# RideWave Architecture Diagram

Components:
- Rider App
- Driver App
- Admin Dashboard
- Backend API
- Database
"@
    }

    "ai-prompt-cli" {

      Write-File "$repoPath\README.md" @"
# AI Prompt CLI

CLI tool to run prompt templates.

No secrets included. Use .env.example.
"@

      Write-File "$repoPath\.env.example" @"
AI_PROVIDER=openai
API_KEY=changeme
"@

      Ensure-Folder "$repoPath\src"

      Write-File "$repoPath\src\main.py" @"
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', required=True)
    args = parser.parse_args()

    print(f'Prompt received: {args.prompt}')
    print('Provider integration placeholder.')

if __name__ == '__main__':
    main()
"@

      Write-File "$repoPath\requirements.txt" @"
python-dotenv
"@
    }

    "saas-multitenant-backend" {

      Write-File "$repoPath\README.md" @"
# SaaS Multi-Tenant Backend Starter

FastAPI SaaS backend scaffold with tenant module structure.
"@

      Ensure-Folder "$repoPath\app\tenants"
      Ensure-Folder "$repoPath\app\auth"
      Ensure-Folder "$repoPath\app\billing"
      Ensure-Folder "$repoPath\app\core"

      Write-File "$repoPath\app\main.py" @"
from fastapi import FastAPI

app = FastAPI(title="Multi-Tenant SaaS Backend")

@app.get("/")
def root():
    return {"message": "SaaS backend scaffold"}
"@

      Write-File "$repoPath\requirements.txt" @"
fastapi
uvicorn[standard]
pytest
"@

      Write-File "$repoPath\.github\workflows\ci.yml" $ci_python
    }

    "react-admin-dashboard-pro" {

      Write-File "$repoPath\README.md" @"
# React Admin Dashboard Pro

Frontend admin dashboard template.

## Run
npm install
npm run dev
"@

      Write-File "$repoPath\package.json" @"
{
  "name": "react-admin-dashboard-pro",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "vite": "^5.4.0"
  }
}
"@

      Write-File "$repoPath\index.html" @"
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Admin Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"@

      Ensure-Folder "$repoPath\src"

      Write-File "$repoPath\src\main.jsx" @"
import React from 'react'
import ReactDOM from 'react-dom/client'

function App() {
  return (
    <div style={{ padding: 20 }}>
      <h1>React Admin Dashboard Pro</h1>
      <p>Starter template ready.</p>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
"@

      Write-File "$repoPath\.github\workflows\ci.yml" $ci_node
    }

    "raphasha-dev-portfolio" {

      Write-File "$repoPath\README.md" @"
# Raphasha Dev Portfolio (Monorepo)

Monorepo containing my best work:
- portfolio-site
- backend API
- UI components
"@

      Ensure-Folder "$repoPath\apps\portfolio-site"
      Ensure-Folder "$repoPath\apps\api"
      Ensure-Folder "$repoPath\packages\ui-components"
      Ensure-Folder "$repoPath\docs"

      Write-File "$repoPath\apps\api\README.md" "# API placeholder"
      Write-File "$repoPath\apps\portfolio-site\README.md" "# Portfolio placeholder"
    }
  }

  # git init + commit + push
  Git-Init-Commit $repoPath $repo
}

Write-Host ""
Write-Host "DONE. All repos generated in: $BasePath"
Write-Host "Push enabled: $PushToGitHub"
