import os
from typing import Optional

from git.objects.commits import Commit
from git.head import modify_head

class Branche:
    """Fichier dans `.git/refs/heads`"""

    def __init__(self, repo_path:str, branch_name:str = "main", commit_sha1:Optional[str] = None, folder_path:Optional[str] = None):
        if commit_sha1 is None and folder_path is None:
            raise ValueError("Il faut que le folder_path ou le commit_sha1 soit spécifié")
        
        self.branch_name = branch_name
        if commit_sha1 is None:
            commit = Commit(folder_path, repo_path)
            commit_sha1 = commit.sha1
        self.create_file(commit_sha1, repo_path)

    def create_file(self, commit_sha1: str, repo_path: str):
        """Crée un fichier dans `.git/refs/heads` pointant vers un commit"""
        path = os.path.join(repo_path, "refs", "heads", self.branch_name)
        modify_head(self.branch_name, repo_path)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            f.write(commit_sha1.strip() + "\n")


def main():
    Branche("example/.git", folder_path="example")
