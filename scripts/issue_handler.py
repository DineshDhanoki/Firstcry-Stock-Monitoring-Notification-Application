import os, yaml
from github import Github

CONFIG_FILE = "config.yaml"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {"products": [], "delay_between_requests": 3}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

def handle_issue():
    body = os.environ["ISSUE_BODY"].strip()
    repo_name = os.environ["GITHUB_REPOSITORY"]
    issue_number = os.environ["ISSUE_NUMBER"]
    token = os.environ["GITHUB_TOKEN"]

    g = Github(token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(int(issue_number))

    cfg = load_config()
    updated = False

    if body.lower().startswith("/add"):
        lines = body.splitlines()
        title = next((l.split(":",1)[1].strip() for l in lines if l.lower().startswith("title:")), None)
        url = next((l.split(":",1)[1].strip() for l in lines if l.lower().startswith("url:")), None)
        pincode = next((l.split(":",1)[1].strip() for l in lines if l.lower().startswith("pincode:")), None)
        if title and url and pincode:
            pid = f"prod{len(cfg['products'])+1}"
            cfg["products"].append({"id": pid, "title": title, "url": url, "pincode": pincode})
            updated = True
            issue.create_comment(f"✅ Added product: **{title}** [{pincode}]")
            issue.edit(state="closed")

    elif body.lower().startswith("/remove"):
        lines = body.splitlines()
        title = next((l.split(":",1)[1].strip() for l in lines if l.lower().startswith("title:")), None)
        if title:
            cfg["products"] = [p for p in cfg["products"] if p["title"].lower() != title.lower()]
            updated = True
            issue.create_comment(f"❌ Removed product: **{title}**")
            issue.edit(state="closed")

    elif body.lower().startswith("/list"):
        if not cfg["products"]:
            issue.create_comment("📭 No products in watchlist.")
        else:
            msg = "\n".join([f"- **{p['title']}** [{p['pincode']}] → {p['url']}" for p in cfg["products"]])
            issue.create_comment("📋 Current Watchlist:\n" + msg)
        issue.edit(state="closed")

    if updated:
        if os.path.exists(CONFIG_FILE):
            sha = repo.get_contents(CONFIG_FILE).sha
            repo.update_file(CONFIG_FILE, "Update config via issue", yaml.safe_dump(cfg, sort_keys=False), sha)
        else:
            repo.create_file(CONFIG_FILE, "Create config via issue", yaml.safe_dump(cfg, sort_keys=False))
        save_config(cfg)

if __name__ == "__main__":
    handle_issue()
