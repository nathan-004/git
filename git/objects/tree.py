import os
import zlib
from hashlib import sha1
import binascii

from typing import NamedTuple

from git.objects.blobs import Blob
from git.objects.object import Object

class Entry(NamedTuple):
    mode:str
    type:str
    sha1:str
    name:str

def list_to_bytes(entries:list[Entry]) -> bytes:
    """Convert a list of Entry objects to bytes suitable for a Git tree object."""
    result = b''
    for entry in entries:
        entry_line = f"{entry.mode} {entry.name}\0".encode() + binascii.unhexlify(entry.sha1)
        result += entry_line
    return result

class Tree(Object):
    """Represents a Git tree object."""

    def get_content(self) -> tuple[str, str]:
        """
        Retourne le header et le contenu de l'objet à stocker
        
        Returns
        -------
        header:str
            Contient des informations annexes comme le nom de l'objet et sa taille
        content:str
            Le contenu de l'objet à stocker
        """
        entries = self.get_folder_content()
        result = list_to_bytes(entries)
        return (f'tree {len(result)}\0'.encode(), result)

    def get_folder_content(self):
        """
        Creates a tree object from the directory structure.
        This method reads the contents of the directory at self.path, and creates files in the .git/objects directory.
        """
        if not os.path.isdir(self.file_path):
            raise ValueError(f"The path {self.file_path} is not a valid directory.")

        entries = []
        for entry in os.listdir(self.file_path):
            if entry == '.git':
                continue
            entry_path = os.path.join(self.file_path, entry)
            if os.path.isfile(entry_path):
                blob = Blob(entry_path, self.repo_path)
                entries.append(Entry(mode='100644', type='blob', sha1=blob.sha1, name=entry))
            elif os.path.isdir(entry_path):
                # Recursively create trees for subdirectories
                sub_tree = Tree(entry_path, self.repo_path)
                entries.append(Entry(mode='40000', type='tree', sha1=sub_tree.sha1, name=entry))
            else:
                print(f"Skipping unsupported file type: {entry_path}")
        
        return entries
    
    def _save_file(self):
        super()._save_file()
        print(f"Tree SHA-1: {self.sha1} - Path: {self.file_path}")

def main():
    tree = Tree('example', 'example/.git')