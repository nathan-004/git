"""Modify the HEAD file by modifying its content"""

import os

def modify_head(branch_name:str, repo_path:str):
    """Modify the HEAD file by ref: refs/heads/<branch name>"""
    path = os.path.join(repo_path, "HEAD")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(f"ref: refs/heads/{branch_name}")

def get_latest_branch_path(repo_path:str) -> str:
    """Returns the path of the latest branch used"""
    with open(os.path.join(repo_path, "HEAD")) as f:
        content = f.read()
    if content.startswith("ref: "):
        return content[5:]
    
def get_latest_branch_content(repo_path:str) -> str:
    with open(get_latest_branch_path(repo_path)) as f:
        return f.read()
