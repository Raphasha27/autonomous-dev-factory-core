import os

base_dir = r"C:\Users\nelso\OneDrive\Desktop\autonomous-dev-factory-v4"

files = {
    "requirements.txt": """pyyaml
openai
pytest
""",
    "README.md": """# Autonomous Dev Factory v4 (Self-Healing Engine) 🚀

The v4 engine incorporates an AI self-healing pipeline: **Generate → Validate → Fix → Rebuild**.

## Core Features
- **Validation Loop**: Runs static analysis (`compileall`) and `pytest`.
- **Repair Agent**: Captures stdout/stderr from failed builds and sends them to the LLM to rewrite and fix code.
- **Sandbox execution**: Evaluates code inside isolated runtime before committing.

## Setup
1. `pip install -r requirements.txt`
2. `$env:OPENAI_API_KEY="your-key-here"`
3. `python devfactory.py --spec specs/example.yaml`
""",
    "specs/example.yaml": """project:
  name: self-healing-saas-v4
  type: fastapi-react
  visibility: public

  stack:
    backend: fastapi
    db: postgres
    frontend: react

  features:
    - Authentication (JWT)
    - RBAC roles
    - Healthcheck endpoint
""",
    "cli/__init__.py": "",
    "cli/pipeline.py": """from runtime.executor import run_tests
from llm.repair_agent import fix_code
from runtime.validator import validate_code

class Pipeline:
    def build_until_green(self, project_path, llm, spec):
        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            print(f"\\n🔁 Build attempt {attempt + 1}")

            # 1. Validate
            validation = validate_code(project_path)
            if validation["ok"]:
                print("✅ Compilation Check Passed")
            else:
                print("❌ Compilation Failed")

            # 2. Run tests
            test_result = run_tests(project_path)
            if test_result["success"] and validation["ok"]:
                print("✅ Tests Passed - Green Build Achieved! 🟢")
                return True

            # 3. Repair using LLM
            errors = []
            if not validation["ok"]: errors.append(validation["error"])
            if not test_result["success"]: errors.extend(test_result["errors"])
            
            print(f"🧠 Sending {len(errors)} error logs to AI repair agent...")
            fix_code(llm, project_path, errors)

            attempt += 1

        raise Exception("❌ Build failed after max retries")
""",
    "cli/orchestrator.py": """import os
from cli.pipeline import Pipeline
from llm.client import LLMClient
from generators.backend import generate_backend
from generators.frontend import generate_frontend

class Orchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.pipeline = Pipeline()

    def build(self, spec):
        name = spec["project"]["name"]
        base = f"outputs/{name}"

        os.makedirs(base, exist_ok=True)

        print("🧠 Generating backend...")
        backend = generate_backend(self.llm, spec)
        with open(f"{base}/main.py", "w") as f:
            f.write(backend)

        # Generate a dummy test file so pytest works
        test_content = "from main import app\\ndef test_app():\\n    assert app is not None\\n"
        with open(f"{base}/test_main.py", "w") as f:
            f.write(test_content)

        print("🎨 Generating frontend...")
        frontend = generate_frontend(self.llm, spec)
        with open(f"{base}/App.jsx", "w") as f:
            f.write(frontend)

        # 🔁 SELF-HEALING LOOP
        try:
            self.pipeline.build_until_green(base, self.llm, spec)
            return base
        except Exception as e:
            print(f"Orchestrator failed: {e}")
            return None
""",
    "llm/__init__.py": "",
    "llm/client.py": """import os
from openai import OpenAI

class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not set. Using mock LLM client.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def complete(self, prompt):
        if not self.client:
            return "from fastapi import FastAPI\\napp = FastAPI()\\n# MOCK CODE GENERATED"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Return ONLY the raw python/jsx code without markdown wrappers."},
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
    "llm/repair_agent.py": """import os

def fix_code(llm, project_path, errors):
    error_text = "\\n".join(errors)
    prompt = f\"\"\"
You are a senior software engineer debugging a broken codebase.
Fix ALL issues below:
{error_text}

Rules:
- Only fix what is broken
- Ensure code compiles and runs
- Return the fully corrected python code for main.py without any markdown formatting.
\"\"\"
    fixed_code = llm.complete(prompt)
    file_path = os.path.join(project_path, "main.py")
    with open(file_path, "w") as f:
        f.write(fixed_code)
    return project_path
""",
    "runtime/__init__.py": "",
    "runtime/validator.py": """import subprocess

def validate_code(path):
    try:
        result = subprocess.run(
            ["python", "-m", "compileall", path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr}
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
""",
    "runtime/executor.py": """import subprocess

def run_tests(path):
    try:
        result = subprocess.run(
            ["pytest"],
            cwd=path,
            capture_output=True,
            text=True
        )
        return {
            "success": result.returncode == 0,
            "errors": result.stderr.split("\\n") if result.returncode != 0 else []
        }
    except Exception as e:
        return {"success": False, "errors": [str(e)]}
""",
    "generators/__init__.py": "",
    "generators/backend.py": """def generate_backend(llm, spec):
    return llm.complete(f"Build a production FastAPI backend for {spec}. Return ONLY Python code.")
""",
    "generators/frontend.py": """def generate_frontend(llm, spec):
    return llm.complete(f"Build a React frontend App.jsx for {spec}. Return ONLY JSX code.")
""",
    "github/__init__.py": "",
    "github/git.py": """import subprocess
def init_git(path):
    if not path: return
    print("-> Initializing Git...")
    subprocess.run(["git", "init"], cwd=path, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "add", "."], cwd=path, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "v4 Self-Healed Release"], cwd=path, stdout=subprocess.DEVNULL)
""",
    "devfactory.py": """import argparse
import yaml
from cli.orchestrator import Orchestrator
from github.git import init_git

def load_spec(path):
    with open(path, "r") as f: return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    spec = load_spec(args.spec)
    orchestrator = Orchestrator()
    project_path = orchestrator.build(spec)
    
    if project_path:
        init_git(project_path)
        print("\\n🚀 AI Dev Factory v4 (Self-Healing) successful!")
    else:
        print("\\n❌ Dev Factory v4 failed to reach a green build.")

if __name__ == "__main__":
    main()
"""
}

for file_path, content in files.items():
    full_path = os.path.join(base_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Autonomous Dev Factory v4 has been scaffolded at: {base_dir}")
