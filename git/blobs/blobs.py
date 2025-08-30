import os
from hashlib import sha1
import zlib

def is_child(path, repo_path):
    """Check if 'path' is a child of 'repo_path'."""
    abs_path = os.path.abspath(path)
    abs_repo_path = os.path.abspath(repo_path)

    return abs_path.startswith(abs_repo_path)

class Blob:
    def __init__(self, file_path: str, repo_path:str):
        self.file_path = file_path

        if not is_child(file_path, repo_path):
            self.init_file(repo_path)
        else: 
            self.intit_blob(repo_path)
    
    def init_file(self, repo_path: str):
        """Initialize a blob from a file path"""
        self.content = self._read_file()
        self.size = len(self.content)
        
        self.sha1, self.encoded_content = self._encode_blob()
        print(f"Blob SHA-1: {self.sha1}", f"Encoded Content: {self.encoded_content}", sep="\n")

        self._save_blob(repo_path)

    def intit_blob(self, repo_path: str):
        """Initialize a blob from an existing blob file path"""
        self.content = self._read_file()
        self.content = zlib.decompress(self.content)
        self.content = self.content.decode()
        try:
            self.content = self.content.split('\0', 1)[1]
        except Exception as e:
            print("Error decoding blob content:", e)
            return
        
        print(self.content)

    def _read_file(self) -> bytes:
        with open(self.file_path, 'rb') as f:
            return f.read()
    
    def _encode_blob(self) -> tuple[str, bytes]:
        header = f'blob {self.size}\0'.encode()
        blob_content = header + self.content
        
        sha1_hash = sha1(blob_content).hexdigest()
        encoded_content = zlib.compress(blob_content)
        return sha1_hash, encoded_content
    
    def _save_blob(self, repo_path: str):
        objects_dir = os.path.join(repo_path, 'objects')
        if not os.path.exists(objects_dir):
            os.makedirs(objects_dir)
        
        dir_name = self.sha1[:2]
        file_name = self.sha1[2:]
        dir_path = os.path.join(objects_dir, dir_name)
        
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        blob_path = os.path.join(objects_dir, dir_name)
        blob_file_path = os.path.join(blob_path, file_name)
        with open(blob_file_path, 'wb') as f:
            f.write(self.encoded_content)

blob = Blob('.git/objects/fc/e4387400f4bee19265a966929a2e68a390da31', '.git')