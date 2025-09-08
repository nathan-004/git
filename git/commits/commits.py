import zlib
from hashlib import sha1
import time
import os

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
        self.sha1 = sha1(content).hexdigest()
        self.encoded_content = zlib.compress(content)
        self._save_tree()

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

    def _save_tree(self):
        objects_dir = os.path.join(self.repo_path, 'objects')
        if not os.path.exists(objects_dir):
            os.makedirs(objects_dir)
        
        dir_name = self.sha1[:2]
        file_name = self.sha1[2:]
        commit_path = os.path.join(objects_dir, dir_name)
        self.commit_file_path = os.path.join(commit_path, file_name)
        if not os.path.exists(commit_path):
            os.makedirs(commit_path)
            
        with open(self.commit_file_path, 'wb') as f:
            f.write(self.encoded_content)
        print(f"Commit SHA-1: {self.sha1}")
        
    def _get_content_file(self, file_path):
        """
        Returns the decoded content of the file
        :param str file_path: Path of the encoded Commit file 
        """
        with open(file_path, "rb") as f:
            return zlib.decompress(f.read())

def main():
    commit = Commit("example", "example/.git")
    print(commit._get_content_file(file_path=commit.commit_file_path))