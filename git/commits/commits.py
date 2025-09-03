import zlib
from hashlib import sha1
import time

from git.trees.tree import Tree
# from git.utils import get_last_commit

author = "Test Name"
email = "Test@example.fr"
message = "Test Message"

class Commit:
    """Contains the current tree, the parent tree, the author, the date and the message"""
    
    def __init__(self, file_path, repo_path):
        self.file_path = file_path
        self.repo_path = repo_path
        content = self._get_content()
        header = f"commit {len(content)}\0".encode()
        content = header + content.encode()
        self.sha1 = sha1(content)
        self.encoded_content = zlib.compress(content)

    def _get_content(self) -> str:
        """Returns the content of the commit file"""
        current_tree = Tree(self.file_path, self.repo_path)
        timestamp = int(time.time())
        timezone = time.strftime("%z")
        
        lines = [
            f"tree {current_tree.sha1}",
            f"author {author} <{email}> {timestamp} {timezone}",
            f"commiter {author} <{email}> {timestamp} {timezone}",
            "",
            message
        ]

        return "\n".join(lines)

def main():
    pass