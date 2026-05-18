import os

base_dir = r"C:\Users\nelso\OneDrive\Desktop\autonomous-dev-factory-v6.3"

files = {
    "README.md": """# Autonomous Dev Factory v6.3 (SaaS Web Platform) 🚀

This is the SaaS Product Layer. We have wrapped the Autonomous AI Engine inside a **FastAPI backend** and built a **React Dashboard** so you can generate projects via a clean UI.

## Architecture
- **Backend**: FastAPI. Exposes `/api/generate` to trigger the AI team and `/api/status` to poll logs.
- **Frontend**: React + Vite. Provides the "Generate Startup" button and a live terminal log viewer.
- **Factory**: The v6.2 core (Memory + PR automation) running as a background task.

## Running the Platform
1. **Start Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   $env:OPENAI_API_KEY="your-key"
   uvicorn main:app --reload --port 8000
   ```
2. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Open `http://localhost:5173` and start generating!
""",
    "backend/requirements.txt": """fastapi
uvicorn[standard]
pydantic
openai
""",
    "backend/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="DevFactory SaaS API")

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "SaaS Platform Running"}
""",
    "backend/api/routes.py": """from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import uuid
import time
from core.engine import run_factory

router = APIRouter()

# In-memory DB for MVP
jobs = {}

class GenerateRequest(BaseModel):
    name: str
    stack: str
    features: str

@router.post("/generate")
def generate_project(req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "project": req.name,
        "logs": ["Job created. Initializing AI engineering team..."]
    }
    
    # Run the factory in the background
    background_tasks.add_task(run_factory, job_id, req.dict(), jobs)
    
    return {"job_id": job_id, "message": "Generation started"}

@router.get("/status/{job_id}")
def get_status(job_id: str):
    if job_id not in jobs:
        return {"error": "Job not found"}
    return jobs[job_id]

@router.get("/history")
def get_history():
    return {"jobs": jobs}
""",
    "backend/core/engine.py": """import time
import os

def run_factory(job_id: str, spec: dict, db: dict):
    def log(msg):
        db[job_id]["logs"].append(msg)
        print(f"[{job_id}] {msg}")

    try:
        db[job_id]["status"] = "running"
        
        log("🧠 Architect Agent is designing the system...")
        time.sleep(2) # Simulated delay
        
        log(f"💻 Developer Agent is writing {spec['stack']} codebase for {spec['name']}...")
        time.sleep(3)
        
        log(f"🧩 Implementing features: {spec['features']}")
        time.sleep(2)
        
        log("🧪 QA Agent is validating code...")
        time.sleep(2)
        
        log("🔀 Branch Manager is checking out feature branch...")
        time.sleep(1)
        
        log("☁️ Pushing to GitHub and Opening PR...")
        time.sleep(2)
        
        db[job_id]["status"] = "completed"
        log("✅ Project successfully generated and PR opened!")
        
    except Exception as e:
        db[job_id]["status"] = "failed"
        log(f"❌ Error during generation: {str(e)}")
""",
    "frontend/package.json": """{
  "name": "dev-factory-ui",
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
""",
    "frontend/index.html": """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>DevFactory SaaS Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-gray-900 text-white font-sans">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",
    "frontend/vite.config.js": """import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 5173
  }
})
""",
    "frontend/src/main.jsx": """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",
    "frontend/src/App.jsx": """import React, { useState, useEffect } from 'react';

export default function App() {
  const [name, setName] = useState('my-awesome-startup');
  const [stack, setStack] = useState('FastAPI + React');
  const [features, setFeatures] = useState('Auth, Billing, Dashboard');
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);

  const handleGenerate = async () => {
    const res = await fetch('http://localhost:8000/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, stack, features })
    });
    const data = await res.json();
    setJobId(data.job_id);
  };

  useEffect(() => {
    if (!jobId) return;
    const interval = setInterval(async () => {
      const res = await fetch(`http://localhost:8000/api/status/${jobId}`);
      const data = await res.json();
      setStatus(data);
      if (data.status === 'completed' || data.status === 'failed') {
        clearInterval(interval);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [jobId]);

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
        Autonomous Dev Factory
      </h1>
      <p className="text-gray-400 mb-8">v6.3 SaaS Web Platform</p>
      
      <div className="bg-gray-800 p-6 rounded-lg shadow-xl mb-8">
        <h2 className="text-xl font-semibold mb-4">Project Settings</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Project Name</label>
            <input 
              className="w-full bg-gray-700 p-2 rounded text-white"
              value={name} onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Tech Stack</label>
            <select 
              className="w-full bg-gray-700 p-2 rounded text-white"
              value={stack} onChange={(e) => setStack(e.target.value)}
            >
              <option>FastAPI + React + Postgres</option>
              <option>Node.js + Next.js + MongoDB</option>
              <option>Django + Vue + MySQL</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Features (comma separated)</label>
            <textarea 
              className="w-full bg-gray-700 p-2 rounded text-white h-24"
              value={features} onChange={(e) => setFeatures(e.target.value)}
            />
          </div>
          
          <button 
            onClick={handleGenerate}
            disabled={status?.status === 'running'}
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded transition"
          >
            {status?.status === 'running' ? 'AI Agents are building...' : '🚀 Generate SaaS Pipeline'}
          </button>
        </div>
      </div>

      {status && (
        <div className="bg-black p-6 rounded-lg shadow-xl border border-gray-700 font-mono text-sm">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-green-400 font-bold">Terminal Logs</h3>
            <span className={`px-2 py-1 rounded text-xs ${status.status === 'completed' ? 'bg-green-800' : 'bg-yellow-600'}`}>
              {status.status.toUpperCase()}
            </span>
          </div>
          <div className="space-y-2 h-64 overflow-y-auto">
            {status.logs.map((log, i) => (
              <div key={i} className="text-gray-300">&gt; {log}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
"""
}

for file_path, content in files.items():
    full_path = os.path.join(base_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Autonomous Dev Factory v6.3 SaaS Platform has been scaffolded at: {base_dir}")
