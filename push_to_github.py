import os
import subprocess

repos = [
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
]

base_path = r"C:\Users\nelso\OneDrive\Desktop\GitHubProjects"
github_username = "Raphasha27"

screenshots_readme = """# Screenshots Folder

Add UI screenshots here:

- dashboard.png
- login.png
- mobile-view.png

Keep images optimized (<500kb recommended)
"""

for repo in repos:
    repo_path = os.path.join(base_path, repo)
    if not os.path.exists(repo_path):
        print(f"Skipping {repo}, directory not found.")
        continue

    print(f"==========================================")
    print(f"Processing {repo}...")
    
    # 1. Add screenshots
    screenshots_dir = os.path.join(repo_path, "assets", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    with open(os.path.join(screenshots_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(screenshots_readme)

    # 2. Commit the new folder
    subprocess.run(["git", "add", "."], cwd=repo_path)
    subprocess.run(["git", "commit", "-m", "Add screenshots placeholder"], cwd=repo_path)

    # Check if remote origin already exists
    remotes = subprocess.run(["git", "remote"], cwd=repo_path, capture_output=True, text=True).stdout
    if "origin" not in remotes:
        subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{github_username}/{repo}.git"], cwd=repo_path)

    # 3. Create repo and push
    print(f"Creating repo {repo} on GitHub...")
    res = subprocess.run(["gh", "repo", "create", f"{github_username}/{repo}", "--public", "--source", ".", "--push"], cwd=repo_path)
    
    # Ensure push to main
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path)

    # 4. Create tags and release
    print(f"Creating release for {repo}...")
    subprocess.run(["git", "tag", "-a", "v1.0.0", "-m", "Initial release"], cwd=repo_path)
    subprocess.run(["git", "push", "origin", "v1.0.0"], cwd=repo_path)
    subprocess.run(["gh", "release", "create", "v1.0.0", "--title", "Initial Release", "--notes", f"Automated first release for {repo}"], cwd=repo_path)

    # 5. Set topics
    print(f"Adding topics for {repo}...")
    subprocess.run(
        ["gh", "api", "-X", "PUT", f"repos/{github_username}/{repo}/topics", "--input", "-"], 
        input=b'{"names":["featured","portfolio"]}', 
        cwd=repo_path
    )

print("All repos successfully pushed to GitHub!")
