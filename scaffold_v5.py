import os

base_dir = r"C:\Users\nelso\OneDrive\Desktop\autonomous-dev-factory-v5"

files = {
    "requirements.txt": """pyyaml
openai
""",
    "README.md": """# Autonomous Dev Factory v5 (Multi-Agent System) 🚀

Welcome to v5. This is no longer a code generator; it is a **Simulated Software Engineering Company**.

## The AI Engineering Team
- 🧠 **Architect Agent**: System design and architecture planning.
- 💻 **Developer Agent**: Writes the actual production codebase.
- 🧪 **QA Agent**: Writes unit and integration tests.
- 🔍 **Reviewer Agent**: Audits code for security and performance.
- 📦 **DevOps Agent**: Sets up Docker, CI/CD, and deployment infrastructure.
- 📚 **Docs Agent**: Authors comprehensive documentation.

They communicate via a shared **Project Memory**.

## Setup
1. `pip install -r requirements.txt`
2. Set your API Key: `$env:OPENAI_API_KEY="your-key-here"`
3. Run: `python devfactory.py --spec specs/example.yaml`
""",
    "specs/example.yaml": """project:
  name: multi-agent-saas-v5
  type: fastapi-react
  visibility: public

  stack:
    backend: fastapi
    db: postgres
    frontend: react

  features:
    - User Authentication (JWT)
    - Role-Based Access Control
    - Subscription billing placeholders
""",
    "cli/__init__.py": "",
    "cli/agent_router.py": """class AgentRouter:
    def __init__(self, agents):
        self.agents = agents

    def execute(self, spec):
        print("\\n🧠 Architect is designing the system...")
        architecture = self.agents["architect"].run(spec)
        
        print("💻 Developer is writing the code...")
        code = self.agents["developer"].run(architecture)
        
        print("🧪 QA is writing tests...")
        tests = self.agents["qa"].run(code)
        
        print("🔍 Reviewer is checking the code...")
        review = self.agents["reviewer"].run(code)
        
        print("📦 DevOps is building the infrastructure...")
        infra = self.agents["devops"].run(spec)
        
        print("📚 Tech Writer is creating documentation...")
        docs = self.agents["docs"].run(code)

        return {
            "architecture": architecture,
            "code": code,
            "tests": tests,
            "review": review,
            "infra": infra,
            "docs": docs
        }
""",
    "cli/orchestrator.py": """import os
from llm.client import LLMClient
from memory.project_memory import ProjectMemory
from agents.architect import ArchitectAgent
from agents.developer import DeveloperAgent
from agents.qa import QAAgent
from agents.reviewer import ReviewerAgent
from agents.devops import DevOpsAgent
from agents.docs import DocsAgent
from cli.agent_router import AgentRouter
from workflow.pipeline import Pipeline
from runtime.file_writer import write_file

class Orchestrator:
    def build(self, spec):
        llm = LLMClient()
        memory = ProjectMemory()

        agents = {
            "architect": ArchitectAgent(llm, memory),
            "developer": DeveloperAgent(llm, memory),
            "qa": QAAgent(llm, memory),
            "reviewer": ReviewerAgent(llm, memory),
            "devops": DevOpsAgent(llm, memory),
            "docs": DocsAgent(llm, memory),
        }

        router = AgentRouter(agents)
        pipeline = Pipeline()
        
        # Execute the multi-agent pipeline
        result = pipeline.run(spec, router)

        # Write results to disk
        name = spec["project"]["name"]
        base = f"outputs/{name}"
        os.makedirs(base, exist_ok=True)
        
        print(f"\\n💾 Writing generated assets to {base}/ ...")
        
        write_file(f"{base}/docs/ARCHITECTURE.md", result["architecture"])
        write_file(f"{base}/src/main.py", result["code"])
        write_file(f"{base}/tests/test_main.py", result["tests"])
        write_file(f"{base}/docs/REVIEW_REPORT.md", result["review"])
        write_file(f"{base}/Dockerfile", result["infra"])
        write_file(f"{base}/README.md", result["docs"])
        
        return base
""",
    "memory/__init__.py": "",
    "memory/project_memory.py": """class ProjectMemory:
    def __init__(self):
        self.state = {
            "architecture": None,
            "code": {},
            "tests": {},
            "errors": [],
            "decisions": []
        }

    def update(self, key, value):
        self.state[key] = value

    def append_log(self, message):
        self.state["decisions"].append(message)

    def get_context(self):
        return self.state
""",
    "llm/__init__.py": "",
    "llm/client.py": """import os
from openai import OpenAI

class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not set. Using mock responses.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def complete(self, prompt):
        if not self.client:
            return f"# MOCK RESPONSE\\n# Processed by AI agent"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are part of an elite AI engineering team. Output only the requested content."},
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
    "agents/__init__.py": "",
    "agents/base_agent.py": """class BaseAgent:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory

    def run(self, task):
        raise NotImplementedError
""",
    "agents/architect.py": """from agents.base_agent import BaseAgent

class ArchitectAgent(BaseAgent):
    def run(self, spec):
        prompt = f\"\"\"
You are a senior software architect.
Design a full system architecture for:
{spec}
Return:
- folder structure
- tech stack
- API design
- database schema
\"\"\"
        design = self.llm.complete(prompt)
        self.memory.update("architecture", design)
        return design
""",
    "agents/developer.py": """from agents.base_agent import BaseAgent

class DeveloperAgent(BaseAgent):
    def run(self, architecture):
        prompt = f\"\"\"
You are a senior backend/frontend engineer.
Build production code based on:
{architecture}
Rules:
- clean architecture
- no pseudo-code
- production-ready python code only
\"\"\"
        code = self.llm.complete(prompt)
        self.memory.update("code", code)
        return code
""",
    "agents/qa.py": """from agents.base_agent import BaseAgent

class QAAgent(BaseAgent):
    def run(self, code):
        prompt = f\"\"\"
You are a QA engineer.
Write pytest tests for this code:
{code}
Include: unit tests and edge cases.
\"\"\"
        tests = self.llm.complete(prompt)
        self.memory.update("tests", tests)
        return tests
""",
    "agents/reviewer.py": """from agents.base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    def run(self, code):
        prompt = f\"\"\"
You are a senior code reviewer.
Review this code for:
- security issues
- bad patterns
- performance problems
Code:
{code}
\"\"\"
        review = self.llm.complete(prompt)
        if "critical" in review.lower() or "security" in review.lower():
            self.memory.append_log("Security issue detected")
        return review
""",
    "agents/devops.py": """from agents.base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    def run(self, spec):
        prompt = f\"\"\"
Generate a Dockerfile for this system:
{spec}
\"\"\"
        infra = self.llm.complete(prompt)
        self.memory.update("infra", infra)
        return infra
""",
    "agents/docs.py": """from agents.base_agent import BaseAgent

class DocsAgent(BaseAgent):
    def run(self, project):
        prompt = f\"\"\"
Write professional documentation for this project.
Include: setup guide, API docs, and architecture explanation.
\"\"\"
        docs = self.llm.complete(prompt)
        return docs
""",
    "runtime/__init__.py": "",
    "runtime/file_writer.py": """import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
""",
    "workflow/__init__.py": "",
    "workflow/pipeline.py": """class Pipeline:
    def run(self, spec, router):
        result = router.execute(spec)

        # Feedback loop simulation
        if "security" in result["review"].lower():
            print("\\n⚠️ REVIEWER flagged security issues! Re-routing back to Developer...")
            result["code"] = router.agents["developer"].run(
                result["architecture"] + "\\nFix these security issues:\\n" + result["review"]
            )
            print("✅ Developer applied security patches.")

        return result
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
    
    print("🚀 Starting AI Engineering Team (v5)...")
    orchestrator.build(spec)
    print("\\n🎉 Multi-Agent Software Engineering Factory run complete!")

if __name__ == "__main__":
    main()
"""
}

for file_path, content in files.items():
    full_path = os.path.join(base_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Autonomous Dev Factory v5 has been scaffolded at: {base_dir}")
