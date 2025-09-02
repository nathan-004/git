from git.trees.tree import Tree
from git.utils import get_last_commit

author = "test"

class Commit:
    """Contains the current tree, the parent tree, the author, the date and the message"""
    
    def __init__(self, file_path, repo_path):
        self.file_path = file_path
        self.repo_path = repo_path
    
def main():
    pass