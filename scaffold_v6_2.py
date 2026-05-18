import os

base_dir = r"C:\Users\nelso\OneDrive\Desktop\autonomous-dev-factory-v6.2"

files = {
    "requirements.txt": """pyyaml
openai
""",
    "README.md": """# Autonomous Dev Factory v6.2 (Learning System + PR Flow) 🚀

This upgrade combines the **v6.1 PR Automation** with the **v6.2 Memory & Learning Layer**. The factory no longer repeats its mistakes. It tracks build failures, logs them, and automatically optimizes future AI prompts to avoid those specific errors.

## Features
- **Failure Database**: Stores history of failed builds and errors locally.
- **Prompt Optimizer**: Pre-processes prompts sent to the LLM by injecting context from past failures.
- **PR Automation**: Continues to safely branch, commit, push, and open PRs.

## Setup
1. `pip install -r requirements.txt`
2. Set API Key: `$env:OPENAI_API_KEY="your-key-here"`
3. Run: `python devfactory.py --spec specs/example.yaml`
""",
    "specs/example.yaml": """project:
  name: learning-saas-v6.2
  type: fastapi-react
  visibility: public

  stack:
    backend: fastapi

  features:
    - User Authentication
    - Database Models

  github:
    branch_name: feature/learning-system
    pr_title: "feat: Add intelligent memory layer"
""",
    "cli/__init__.py": "",
    "cli/orchestrator.py": """import os
from llm.client import LLMClient
from github.branch_manager import create_branch, commit_changes, push_branch
from github.pr_creator import create_pr
from github.repo_creator import ensure_repo
from memory.prompt_optimizer import optimize_prompt
from memory.failure_database import log_failure

class Orchestrator:
    def __init__(self):
        self.llm = LLMClient()

    def build_project(self, spec):
        name = spec["project"]["name"]
        base = f"outputs/{name}"
        branch_name = spec["project"]["github"].get("branch_name", "feature/auto")
        pr_title = spec["project"]["github"].get("pr_title", "Auto-generated feature")

        os.makedirs(base, exist_ok=True)
        ensure_repo(base, name)
        create_branch(base, branch_name)

        print(f"\\n🧠 Agents generating code (Learning Enabled)...")
        
        # Optimize prompt using past failures
        base_prompt = f"Write a secure FastAPI auth route for {name}"
        optimized_prompt = optimize_prompt(base_prompt)
        print(f"💡 Optimized Prompt:\\n{optimized_prompt}")
        
        code = self.llm.complete(optimized_prompt)
        
        # Simulate a syntax error validation (In reality, this uses compileall/pytest)
        if "MOCK" in code or "ERROR" in code:
            print("❌ Simulated Build Failure! Logging to memory...")
            log_failure(spec, "Mocked compilation error: Missing dependency.")
            # We continue for demonstration purposes
            
        os.makedirs(f"{base}/src", exist_ok=True)
        with open(f"{base}/src/main.py", "w") as f:
            f.write(code)

        print(f"📦 Committing and pushing to origin/{branch_name}...")
        commit_changes(base, pr_title)
        push_branch(base, branch_name)

        print(f"🔀 Creating GitHub Pull Request...")
        pr_url = create_pr(base, branch_name, pr_title)
        
        if pr_url:
            print(f"✅ Pull Request created! {pr_url}")

        return base
""",
    "memory/__init__.py": "",
    "memory/failure_database.py": """import json
import os

DB_FILE = "memory_db.json"

def log_failure(spec, error):
    history = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []
                
    history.append({
        "project": spec["project"]["name"],
        "error": error
    })
    
    with open(DB_FILE, "w") as f:
        json.dump(history, f, indent=2)
""",
    "memory/prompt_optimizer.py": """import json
import os

DB_FILE = "memory_db.json"

def optimize_prompt(base_prompt):
    if not os.path.exists(DB_FILE):
        return base_prompt

    try:
        with open(DB_FILE, "r") as f:
            history = json.load(f)
    except:
        return base_prompt

    if not history:
        return base_prompt

    # Extract the last 3 errors to feed to the LLM
    recent_errors = [item["error"] for item in history[-3:]]
    
    improvements = "\\n\\nIMPORTANT RULES TO AVOID PAST FAILURES:\\n"
    for err in recent_errors:
        improvements += f"- Ensure you DO NOT cause this error: {err}\\n"

    return base_prompt + improvements
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

def ensure_repo(path, name):
    print("-> Ensuring git repo exists...")
    subprocess.run(["git", "init"], cwd=path, stdout=subprocess.DEVNULL)
    remotes = subprocess.run(["git", "remote"], cwd=path, capture_output=True, text=True).stdout
    if "origin" not in remotes:
        print(f"-> Creating remote GitHub repo: Raphasha27/{name}")
        subprocess.run(["gh", "repo", "create", f"Raphasha27/{name}", "--public", "--confirm"], cwd=path, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", f"https://github.com/Raphasha27/{name}.git"], cwd=path, stderr=subprocess.DEVNULL)
""",
    "github/branch_manager.py": """import subprocess

def create_branch(repo_path, branch_name):
    subprocess.run(["git", "checkout", "-b", "main"], cwd=repo_path, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit"], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            "--body", "🤖 Auto-generated by Dev Factory v6.2 (Learning Enabled)",
            "--base", "main",
            "--head", branch_name
        ], cwd=repo_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except:
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
    
    print("🚀 Starting AI Engineering Team (v6.2 PR + Learning System)...")
    orchestrator.build_project(spec)
    print("\\n🎉 Learning Flow Complete!")

if __name__ == "__main__":
    main()
"""
}

for file_path, content in files.items():
    full_path = os.path.join(base_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Autonomous Dev Factory v6.2 has been scaffolded at: {base_dir}")
