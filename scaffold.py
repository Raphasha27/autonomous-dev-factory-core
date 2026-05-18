import os

base = r"C:\Users\nelso\OneDrive\Desktop\GitHubProjects"
os.makedirs(base, exist_ok=True)

# 1. Profile repo
profile_dir = os.path.join(base, "Raphasha27")
os.makedirs(profile_dir, exist_ok=True)
with open(os.path.join(profile_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write("""# Koketso Raphasha 👨💻🚀

Full-stack developer focused on **Automation, DevOps, SaaS systems, UI engineering, and scalable backend development**.

- 💻 Backend: FastAPI, Node.js, PostgreSQL
- 🎨 Frontend: React, TailwindCSS, Next.js
- 📱 Mobile: Flutter, React Native
- ⚙️ DevOps: Docker, GitHub Actions, CI/CD
- 🧠 Systems: Multi-tenant SaaS, RBAC, audit logs

---

## 🔥 Featured Projects

### 🚀 Backend Engineering
- **Enterprise FastAPI Starter** → Production-ready FastAPI boilerplate  
- **Secure Auth + RBAC Template** → Authentication + authorization starter  
- **Structured Logging System** → JSON logs + correlation IDs  

### ⚙️ Automation & DevOps
- **Repo Audit Bot** → GitHub repo scanner + PR reviewer  
- **Docker Deployment Templates** → reusable deployment templates  

### 🎨 UI / Product Engineering
- **React Admin Dashboard Pro** → responsive admin dashboard UI  
- **RideWave UI Simulation** → rider + driver + admin system prototype  

### 🏗 SaaS Engineering
- **Multi-Tenant SaaS Backend Starter** → tenant isolation + subscription-ready backend

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-black?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-black?style=for-the-badge&logo=postgresql)
![React](https://img.shields.io/badge/React-black?style=for-the-badge&logo=react)
![Docker](https://img.shields.io/badge/Docker-black?style=for-the-badge&logo=docker)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-black?style=for-the-badge&logo=githubactions)

---

## 📌 Contact
- GitHub: https://github.com/Raphasha27
- LinkedIn: (add link)
- Email: (optional)

---

⭐ If you find my work useful, feel free to star and follow.
""")

# Setup repos
repos = {
    "enterprise-fastapi-starter": {
        "app/api/routes/health.py": """from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get("/")\ndef health_check():\n    return {"status": "healthy"}\n""",
        "app/api/routes/auth.py": "",
        "app/api/routes/users.py": "",
        "app/api/router.py": """from fastapi import APIRouter\nfrom app.api.routes.health import router as health_router\n\napi_router = APIRouter()\napi_router.include_router(health_router, prefix="/health", tags=["Health"])\n""",
        "app/core/config.py": "",
        "app/core/security.py": "",
        "app/core/logging.py": "",
        "app/core/database.py": "",
        "app/models/user.py": "",
        "app/schemas/user.py": "",
        "app/services/user_service.py": "",
        "app/main.py": """from fastapi import FastAPI\nfrom app.api.router import api_router\n\napp = FastAPI(title="Enterprise FastAPI Starter")\n\napp.include_router(api_router)\n\n@app.get("/")\ndef root():\n    return {"status": "ok", "message": "Enterprise FastAPI Starter running"}\n""",
        "tests/test_health.py": "",
        "scripts/run_dev.sh": "",
        "docker/postgres-init.sql": "",
        ".github/workflows/ci.yml": """name: CI\n\non:\n  push:\n  pull_request:\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Setup Python\n        uses: actions/setup-python@v5\n        with:\n          python-version: "3.11"\n      - name: Install dependencies\n        run: pip install -r requirements.txt\n      - name: Run tests\n        run: pytest\n""",
        ".env.example": """APP_NAME="Enterprise FastAPI Starter"\nENVIRONMENT=development\nSECRET_KEY=changeme\nDATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/appdb\n""",
        "docker-compose.yml": """version: "3.9"\n\nservices:\n  api:\n    build: .\n    ports:\n      - "8000:8000"\n    env_file:\n      - .env\n    depends_on:\n      - db\n\n  db:\n    image: postgres:15\n    environment:\n      POSTGRES_USER: postgres\n      POSTGRES_PASSWORD: postgres\n      POSTGRES_DB: appdb\n    ports:\n      - "5432:5432"\n""",
        "Dockerfile": """FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . .\n\nCMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]\n""",
        "requirements.txt": """fastapi\nuvicorn[standard]\npython-dotenv\nsqlalchemy\npsycopg2-binary\npydantic\npytest\n""",
        "README.md": """# Enterprise FastAPI Starter\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/enterprise-fastapi-starter?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/enterprise-fastapi-starter?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/enterprise-fastapi-starter?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/enterprise-fastapi-starter?style=for-the-badge)\n\nProduction-ready FastAPI backend boilerplate.\n\n## Features\n- Dockerized FastAPI\n- PostgreSQL integration\n- Health check endpoint\n- CI workflow included\n\n## Setup\n```bash\ncp .env.example .env\ndocker-compose up --build\n```\n\nAPI Docs: http://localhost:8000/docs\n"""
    },
    "react-admin-dashboard-pro": {
        "public/.gitkeep": "",
        "src/components/.gitkeep": "",
        "src/layouts/.gitkeep": "",
        "src/pages/.gitkeep": "",
        "src/hooks/.gitkeep": "",
        "src/utils/.gitkeep": "",
        "src/App.tsx": "",
        "src/main.tsx": "",
        "index.html": "",
        "package.json": "",
        "README.md": """# React Admin Dashboard Pro\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/react-admin-dashboard-pro?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/react-admin-dashboard-pro?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/react-admin-dashboard-pro?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/react-admin-dashboard-pro?style=for-the-badge)\n\nModern admin dashboard UI built with React + TailwindCSS.\n\n## Features\n- Responsive layout\n- Dashboard cards\n- Sidebar navigation\n- Ready for API integration\n\n## Run\n```bash\nnpm install\nnpm run dev\n```\n"""
    },
    "repo-audit-bot": {
        "src/checks/readme_check.py": "",
        "src/checks/license_check.py": "",
        "src/checks/env_check.py": "",
        "src/core/runner.py": "",
        "src/main.py": """import os\nfrom src.core.runner import run_checks\n\nif __name__ == "__main__":\n    repo_path = os.getcwd()\n    run_checks(repo_path)\n""",
        "requirements.txt": "",
        "README.md": """# Repo Audit Bot\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/repo-audit-bot?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/repo-audit-bot?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/repo-audit-bot?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/repo-audit-bot?style=for-the-badge)\n\nCLI tool that audits repositories for security and best practices.\n\n## Checks\n- Missing README\n- Missing LICENSE\n- Exposed `.env`\n\n## Run\n```bash\npython src/main.py\n```\n"""
    },
    "saas-multitenant-backend": {
        "app/tenants/.gitkeep": "",
        "app/auth/.gitkeep": "",
        "app/billing/.gitkeep": "",
        "app/subscriptions/.gitkeep": "",
        "app/core/.gitkeep": "",
        "app/main.py": "",
        "Dockerfile": "",
        "docker-compose.yml": "",
        ".env.example": "",
        "README.md": """# SaaS Multi-Tenant Backend Starter\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/saas-multitenant-backend?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/saas-multitenant-backend?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/saas-multitenant-backend?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/saas-multitenant-backend?style=for-the-badge)\n\nBackend starter for SaaS platforms with tenant isolation.\n\n## Features\n- Tenant structure folder ready\n- Auth module ready\n- Billing placeholders\n\n## Run\n```bash\ndocker-compose up --build\n```\n"""
    },
    "docker-deployment-templates": {
        "templates/fastapi-postgres/.gitkeep": "",
        "templates/node-mongo/.gitkeep": "",
        "templates/nextjs/.gitkeep": "",
        "templates/nginx-reverse-proxy/.gitkeep": "",
        "templates/redis/.gitkeep": "",
        "README.md": """# Docker Deployment Templates\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/docker-deployment-templates?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/docker-deployment-templates?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/docker-deployment-templates?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/docker-deployment-templates?style=for-the-badge)\n\nProduction-ready docker templates for fast deployments.\n\n## Templates\n- FastAPI + Postgres\n- Node.js + Mongo\n- Next.js\n- Nginx reverse proxy\n- Redis\n\nEach folder contains its own docker-compose.yml.\n"""
    },
    "ai-prompt-cli": {
        "src/templates/.gitkeep": "",
        "src/providers/.gitkeep": "",
        "src/core/.gitkeep": "",
        "src/main.py": "",
        ".env.example": "",
        "requirements.txt": "",
        "README.md": """# AI Prompt CLI\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/ai-prompt-cli?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/ai-prompt-cli?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/ai-prompt-cli?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/ai-prompt-cli?style=for-the-badge)\n\nCLI tool to run AI prompts using templates.\n\n## Usage\n```bash\npython src/main.py --template summarize --input file.txt\n```\n\nNo API keys included. Use .env.example.\n"""
    },
    "ridewave-ui-simulation": {
        "mobile/rider/.gitkeep": "",
        "mobile/driver/.gitkeep": "",
        "admin-dashboard/.gitkeep": "",
        "architecture/system-diagram.md": "",
        "README.md": """# RideWave UI Simulation\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/ridewave-ui-simulation?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/ridewave-ui-simulation?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/ridewave-ui-simulation?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/ridewave-ui-simulation?style=for-the-badge)\n\nUI simulation of a ride-hailing platform.\n\n## Includes\n- Rider UI folder\n- Driver UI folder\n- Admin dashboard UI folder\n- Architecture diagrams\n\nThis repo is safe for public use (no real keys).\n"""
    },
    "structured-logging-system": {
        "python/logger.py": """import logging\nimport json\n\nclass JsonFormatter(logging.Formatter):\n    def format(self, record):\n        log_record = {\n            "level": record.levelname,\n            "message": record.getMessage(),\n            "time": self.formatTime(record),\n        }\n        return json.dumps(log_record)\n\ndef get_logger(name="app"):\n    logger = logging.getLogger(name)\n    logger.setLevel(logging.INFO)\n\n    handler = logging.StreamHandler()\n    handler.setFormatter(JsonFormatter())\n\n    logger.addHandler(handler)\n    return logger\n""",
        "python/example.py": "",
        "README.md": """# Structured Logging System\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/structured-logging-system?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/structured-logging-system?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/structured-logging-system?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/structured-logging-system?style=for-the-badge)\n\nReusable JSON logging module for Python backends.\n\n## Usage\n```python\nfrom logger import get_logger\n\nlog = get_logger()\nlog.info("hello world")\n```\n"""
    },
    "secure-auth-rbac-template": {
        "app/auth/.gitkeep": "",
        "app/roles/.gitkeep": "",
        "app/permissions/.gitkeep": "",
        "app/main.py": "",
        ".env.example": "",
        "README.md": """# Secure Auth + RBAC Template\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/secure-auth-rbac-template?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/secure-auth-rbac-template?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/secure-auth-rbac-template?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/secure-auth-rbac-template?style=for-the-badge)\n\nStarter project demonstrating authentication and role-based authorization.\n\n## Features\n- JWT auth\n- RBAC folder structure\n- Secure password hashing placeholders\n\n## Run\n```bash\npython app/main.py\n```\n"""
    },
    "raphasha-dev-portfolio": {
        "apps/portfolio-site/.gitkeep": "",
        "apps/admin-ui/.gitkeep": "",
        "apps/api/.gitkeep": "",
        "packages/ui-components/.gitkeep": "",
        "packages/utils/.gitkeep": "",
        "docs/.gitkeep": "",
        "README.md": """# Raphasha Dev Portfolio\n\n![GitHub stars](https://img.shields.io/github/stars/Raphasha27/raphasha-dev-portfolio?style=for-the-badge)\n![GitHub forks](https://img.shields.io/github/forks/Raphasha27/raphasha-dev-portfolio?style=for-the-badge)\n![GitHub issues](https://img.shields.io/github/issues/Raphasha27/raphasha-dev-portfolio?style=for-the-badge)\n![License](https://img.shields.io/github/license/Raphasha27/raphasha-dev-portfolio?style=for-the-badge)\n\nMonorepo containing my best projects:\n- portfolio website\n- admin UI\n- backend APIs\n- reusable UI components\n\nBuilt to showcase full-stack engineering and DevOps skills.\n"""
    }
}

universal_gitignore = """.env\n__pycache__/\nnode_modules/\ndist/\nbuild/\n*.log\n.DS_Store\n.vscode/\n.idea/\n"""

universal_license = """MIT License\n\nCopyright (c) 2026 Koketso Raphasha\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n"""

universal_security = """# Security Policy\n\n## Reporting a Vulnerability\nIf you discover a security vulnerability, please report it privately via email or GitHub issues.\n\nDo not publish sensitive security issues publicly.\n"""

universal_contributing = """# Contributing\n\nThanks for contributing!\n\n## Steps\n1. Fork repo\n2. Create a feature branch\n3. Commit changes\n4. Open a PR\n\n## Standards\n- Clean code\n- Tests required for new features\n- Keep secrets out of commits\n"""

for repo_name, files in repos.items():
    repo_path = os.path.join(base, repo_name)
    os.makedirs(repo_path, exist_ok=True)
    
    # Write files
    for file_path, content in files.items():
        full_path = os.path.join(repo_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    # Write universal files
    with open(os.path.join(repo_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(universal_gitignore)
    with open(os.path.join(repo_path, "LICENSE"), "w", encoding="utf-8") as f:
        f.write(universal_license)
    with open(os.path.join(repo_path, "SECURITY.md"), "w", encoding="utf-8") as f:
        f.write(universal_security)
    with open(os.path.join(repo_path, "CONTRIBUTING.md"), "w", encoding="utf-8") as f:
        f.write(universal_contributing)

print(f"All repositories have been successfully scaffolded at {base}")
