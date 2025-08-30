import os
import zlib
from hashlib import sha1
import binascii

from typing import NamedTuple

from git.blobs.blobs import Blob

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

class Tree:
    """Represents a Git tree object."""
    def __init__(self, path:str, repo_path:str):
        self.path = path
        self.repo_path = repo_path

        entries = self.get_folder_content()
        result = list_to_bytes(entries)
        header = f'tree {len(result)}\0'.encode()

        self.sha1 = sha1(header + result).hexdigest()
        self.encoded_content = zlib.compress(header + result)
        self._save_tree()

    def get_folder_content(self):
        """
        Creates a tree object from the directory structure.
        This method reads the contents of the directory at self.path, and creates files in the .git/objects directory.
        """
        if not os.path.isdir(self.path):
            raise ValueError(f"The path {self.path} is not a valid directory.")

        entries = []
        for entry in os.listdir(self.path):
            if entry == '.git':
                continue
            entry_path = os.path.join(self.path, entry)
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
    
    def _save_tree(self):
        objects_dir = os.path.join(self.repo_path, 'objects')
        if not os.path.exists(objects_dir):
            os.makedirs(objects_dir)
        
        dir_name = self.sha1[:2]
        file_name = self.sha1[2:]
        tree_path = os.path.join(objects_dir, dir_name)
        tree_file_path = os.path.join(tree_path, file_name)
        if not os.path.exists(tree_path):
            os.makedirs(tree_path)
        
        with open(tree_file_path, 'wb') as f:
            f.write(self.encoded_content)
        print(zlib.decompress(self.encoded_content))
        print(f"Tree SHA-1: {self.sha1}")

def main():
    tree = Tree('example', 'example/.git')