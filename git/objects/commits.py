import zlib
from hashlib import sha1
import time
import os

from git.objects.tree import Tree
from git.objects.object import Object
# from git.utils import get_last_commit

author = "Test Name"
email = "Test@example.fr"
message = "Test Message"

class Commit(Object):
    """Contains the current tree, the parent tree, the author, the date and the message"""

    def get_content(self):
        """
        Retourne le header et le contenu de l'objet à stocker
        
        Returns
        -------
        header:str
            Contient des informations annexes comme le nom de l'objet et sa taille
        content:str
            Le contenu de l'objet à stocker
        """
        content = self._get_content()
        header = f"commit {len(content)}".encode()

        return (header, content)

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

    def _save_file(self):
        super()._save_file()
        print(f"Commit SHA-1: {self.sha1}")

def main():
    commit = Commit("example", "example/.git")