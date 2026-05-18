import os

base_dir = r"C:\Users\nelso\OneDrive\Desktop\autonomous-dev-factory-v3-real"

files = {
    "requirements.txt": """pyyaml
openai
""",
    "README.md": """# Autonomous Dev Factory v3 (Real Architecture) 🚀

A spec-driven code synthesis pipeline with LLM orchestration and DevOps automation.

## Features
- **Orchestrator Pattern**: Manages the generation flow predictably.
- **LLM Client**: Dedicated API wrapper (using OpenAI).
- **Domain Generators**: Separate modules for Frontend, Backend, and Infra.
- **File Writer**: Manages output boundaries.

## Setup
1. `pip install -r requirements.txt`
2. Set your API Key: `$env:OPENAI_API_KEY="your-key-here"`
3. Run: `python devfactory.py --spec specs/example.yaml`
""",
    "specs/example.yaml": """project:
  name: saas-platform-v3
  type: fastapi-react
  visibility: public

  stack:
    backend: fastapi
    db: postgres
    frontend: react

  features:
    - Authentication (JWT)
    - RBAC roles
    - PostgreSQL models
    - Clean architecture
    - Docker-ready

  github:
    auto_create: false
    auto_push: false
    auto_release: false
    auto_pin: false
""",
    "cli/__init__.py": "",
    "cli/spec_loader.py": """import yaml

def load_spec(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)
""",
    "cli/orchestrator.py": """import os
from llm.client import LLMClient
from generators.backend_generator import generate_backend
from generators.frontend_generator import generate_frontend
from runtime.file_writer import write_file

class Orchestrator:
    def __init__(self):
        self.llm = LLMClient()

    def build_project(self, spec):
        name = spec["project"]["name"]
        base = f"outputs/generated_repos/{name}"
        os.makedirs(base, exist_ok=True)

        print(f"🧠 Orchestrator starting build for: {name}")

        # 1. Generate backend
        print("-> Synthesizing Backend...")
        backend_code = generate_backend(self.llm, spec)
        write_file(f"{base}/backend/main.py", backend_code)

        # 2. Generate frontend
        print("-> Synthesizing Frontend...")
        frontend_code = generate_frontend(self.llm, spec)
        write_file(f"{base}/frontend/App.jsx", frontend_code)

        # 3. Generate infrastructure
        print("-> Synthesizing Docker Config...")
        self.generate_docker(base, spec)

        # 4. Generate README
        print("-> Synthesizing README...")
        self.generate_readme(base, spec)

        return base

    def generate_docker(self, base, spec):
        docker = self.llm.complete(
            "Generate a production Docker setup (Dockerfile and docker-compose.yml combined in one response if needed, or just Dockerfile) for this stack: " + str(spec) + ". Return ONLY the raw Dockerfile content."
        )
        write_file(f"{base}/Dockerfile", docker)

    def generate_readme(self, base, spec):
        readme = self.llm.complete(
            f"Write a professional SaaS README for: {spec['project']['name']}. Include architecture overview and setup steps."
        )
        write_file(f"{base}/README.md", readme)
""",
    "llm/__init__.py": "",
    "llm/client.py": """import os
from openai import OpenAI

class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY is not set. Generation will fail or use mock data.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def complete(self, prompt):
        if not self.client:
            return f"# MOCK OUTPUT (Set OPENAI_API_KEY)\\n# Prompt received:\\n# {prompt}"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # using a standard available model
                messages=[
                    {"role": "system", "content": "You are a senior software architect. Return ONLY the requested code or file content without markdown blocks unless specifically asked."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            # Clean up markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```", 1)[1]
                if "\\n" in content:
                    content = content.split("\\n", 1)[1]
                if content.endswith("```"):
                    content = content.rsplit("```", 1)[0]
            return content.strip()
        except Exception as e:
            return f"# Error from LLM: {str(e)}"
""",
    "generators/__init__.py": "",
    "generators/backend_generator.py": """def generate_backend(llm, spec):
    prompt = f\"\"\"
Build a production FastAPI backend.

Requirements:
- Authentication (JWT)
- RBAC roles
- PostgreSQL models
- Clean architecture (routers, services, models)
- Docker-ready
- Based on spec: {spec}

Return ONLY Python code for the main backend entry file.
\"\"\"
    return llm.complete(prompt)
""",
    "generators/frontend_generator.py": """def generate_frontend(llm, spec):
    prompt = f\"\"\"
Build a React frontend for a SaaS system.

Requirements:
- Dashboard UI
- Login page
- API integration ready
- TailwindCSS styling
- Clean component structure

Spec:
{spec}

Return ONLY App.jsx code.
\"\"\"
    return llm.complete(prompt)
""",
    "runtime/__init__.py": "",
    "runtime/file_writer.py": """import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
""",
    "github/__init__.py": "",
    "github/repo_manager.py": """import subprocess

def create_repo(spec):
    name = spec["project"]["name"]
    user = "Raphasha27"
    print(f"-> Creating GitHub repo: {user}/{name}")
    subprocess.run([
        "gh", "repo", "create",
        f"{user}/{name}",
        "--public",
        "--confirm"
    ])
""",
    "github/git_manager.py": """import subprocess

def init_git(path):
    print("-> Initializing local git repository...")
    subprocess.run(["git", "init"], cwd=path, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "add", "."], cwd=path, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "Auto-generated by AI DevFactory v3"], cwd=path, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "branch", "-M", "main"], cwd=path, stdout=subprocess.DEVNULL)

def push_repo(path, spec):
    name = spec["project"]["name"]
    user = "Raphasha27"
    print(f"-> Pushing to GitHub: {user}/{name}")
    subprocess.run([
        "git", "remote", "add", "origin",
        f"https://github.com/{user}/{name}.git"
    ], cwd=path, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=path)
""",
    "devfactory.py": """import argparse
import sys
import os

from cli.spec_loader import load_spec
from cli.orchestrator import Orchestrator
from github.repo_manager import create_repo
from github.git_manager import init_git, push_repo

def main():
    parser = argparse.ArgumentParser(description="Autonomous AI Dev Factory v3")
    parser.add_argument("--spec", required=True, help="Path to your YAML spec file")
    args = parser.parse_args()

    spec = load_spec(args.spec)

    orchestrator = Orchestrator()
    project_path = orchestrator.build_project(spec)

    github_cfg = spec["project"].get("github", {})

    if github_cfg.get("auto_create"):
        create_repo(spec)

    init_git(project_path)

    if github_cfg.get("auto_push"):
        push_repo(project_path, spec)

    print("\\n🚀 AI Dev Factory v3 (Real Architecture) complete! Check outputs/generated_repos/")

if __name__ == "__main__":
    main()
"""
}

for file_path, content in files.items():
    full_path = os.path.join(base_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Real Autonomous Dev Factory v3 has been scaffolded at: {base_dir}")
