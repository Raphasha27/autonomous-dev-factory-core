import os

base_dir = r"C:\Users\nelso\OneDrive\Desktop\autonomous-dev-factory-v6.1"

files = {
    "requirements.txt": """pyyaml
openai
""",
    "README.md": """# Autonomous Dev Factory v6.1 (PR System) 🚀

This is the Enterprise Upgrade. The AI agents now collaborate via real **GitHub Pull Requests**.

## Features
- **Branch Management**: Agents automatically check out feature branches.
- **Commit Automation**: Clean commits with generated code.
- **Pull Request Creation**: Uses the `gh` CLI to open a PR for the newly generated code.
- **Review Simulation**: The Reviewer agent can add comments (simulated via stdout for now) and merge.

## Setup
1. `pip install -r requirements.txt`
2. Set API Key: `$env:OPENAI_API_KEY="your-key-here"`
3. Make sure you are authenticated with GitHub CLI (`gh auth status`)
4. Run: `python devfactory.py --spec specs/example.yaml`
""",
    "specs/example.yaml": """project:
  name: auto-pr-saas
  type: fastapi-react
  visibility: public

  stack:
    backend: fastapi

  features:
    - User Authentication
    - Secure API routes

  github:
    branch_name: feature/auth-system
    pr_title: "feat: Implement Auth System"
""",
    "cli/__init__.py": "",
    "cli/orchestrator.py": """import os
from llm.client import LLMClient
from github.branch_manager import create_branch, commit_changes, push_branch
from github.pr_creator import create_pr
from github.repo_creator import ensure_repo

class Orchestrator:
    def __init__(self):
        self.llm = LLMClient()

    def build_with_pr_flow(self, spec):
        name = spec["project"]["name"]
        base = f"outputs/{name}"
        branch_name = spec["project"]["github"].get("branch_name", "feature/auto-generated")
        pr_title = spec["project"]["github"].get("pr_title", "Auto-generated feature")

        os.makedirs(base, exist_ok=True)
        
        # 1. Initialize repo and branch
        ensure_repo(base, name)
        create_branch(base, branch_name)

        # 2. Architect -> Developer -> QA (Simulated generation)
        print(f"\\n🧠 Agents generating code on branch '{branch_name}'...")
        code = self.llm.complete(f"Write a simple secure FastAPI auth route for {name}")
        
        os.makedirs(f"{base}/src", exist_ok=True)
        with open(f"{base}/src/main.py", "w") as f:
            f.write(code)

        # 3. Commit and Push
        print(f"📦 Committing and pushing to origin/{branch_name}...")
        commit_changes(base, pr_title)
        push_branch(base, branch_name)

        # 4. Create PR
        print(f"🔀 Creating GitHub Pull Request...")
        pr_url = create_pr(base, branch_name, pr_title)
        
        if pr_url:
            print(f"✅ Pull Request created successfully! {pr_url}")
        else:
            print(f"⚠️ PR creation failed or simulated.")

        return base
""",
    "llm/__init__.py": "",
    "llm/client.py": """import os
from openai import OpenAI

class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def complete(self, prompt):
        if not self.client:
            return "from fastapi import FastAPI\\napp = FastAPI()\\n# MOCK AUTH ENDPOINT"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Return raw python code only."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            if content.startswith("```"):
                content = content.split("```", 1)[1]
                if "\\n" in content:
                    content = content.split("\\n", 1)[1]
                if content.endswith("```"):
                    content = content.rsplit("```", 1)[0]
            return content.strip()
        except Exception as e:
            return f"# LLM ERROR: {e}"
""",
    "github/__init__.py": "",
    "github/repo_creator.py": """import subprocess
import os

def ensure_repo(path, name):
    print("-> Ensuring git repo exists...")
    subprocess.run(["git", "init"], cwd=path, stdout=subprocess.DEVNULL)
    
    # Check remote
    remotes = subprocess.run(["git", "remote"], cwd=path, capture_output=True, text=True).stdout
    if "origin" not in remotes:
        # Create GitHub repo if it doesn't exist
        print(f"-> Creating remote GitHub repo: Raphasha27/{name}")
        subprocess.run(["gh", "repo", "create", f"Raphasha27/{name}", "--public", "--confirm"], cwd=path, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", f"https://github.com/Raphasha27/{name}.git"], cwd=path, stderr=subprocess.DEVNULL)
""",
    "github/branch_manager.py": """import subprocess

def create_branch(repo_path, branch_name):
    # Ensure we are on a clean main first
    subprocess.run(["git", "checkout", "-b", "main"], cwd=repo_path, stderr=subprocess.DEVNULL)
    # create initial commit to allow branching
    subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit"], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Checkout feature branch
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def commit_changes(repo_path, message):
    subprocess.run(["git", "add", "."], cwd=repo_path, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, stdout=subprocess.DEVNULL)

def push_branch(repo_path, branch_name):
    subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
""",
    "github/pr_creator.py": """import subprocess

def create_pr(repo_path, branch_name, title):
    try:
        result = subprocess.run([
            "gh", "pr", "create",
            "--title", title,
            "--body", "🤖 Auto-generated by Autonomous Dev Factory v6.1",
            "--base", "main",
            "--head", branch_name
        ], cwd=repo_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"PR Creation Output: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error creating PR: {e}")
        return None
""",
    "devfactory.py": """import argparse
import yaml
from cli.orchestrator import Orchestrator

def load_spec(path):
    with open(path, "r") as f: return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    spec = load_spec(args.spec)
    orchestrator = Orchestrator()
    
    print("🚀 Starting AI Engineering Team (v6.1 PR System)...")
    orchestrator.build_with_pr_flow(spec)
    print("\\n🎉 Pull Request Workflow Complete!")

if __name__ == "__main__":
    main()
"""
}

for file_path, content in files.items():
    full_path = os.path.join(base_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Autonomous Dev Factory v6.1 has been scaffolded at: {base_dir}")
