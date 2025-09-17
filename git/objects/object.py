import os
from hashlib import sha1
import zlib

from typing import Optional

def is_child(path, repo_path):
    """Check if 'path' is a child of 'repo_path'."""
    abs_path = os.path.abspath(path)
    abs_repo_path = os.path.abspath(repo_path)

    return abs_path.startswith(abs_repo_path)

def get_object_path(sha1, repo_path):
    """Retourne le chemin du fichier à enregistrer"""
    objects_dir = os.path.join(repo_path, 'objects')
    if not os.path.exists(objects_dir):
        os.makedirs(objects_dir)

    dir_name = sha1[:2]
    file_name = sha1[2:]
    dir_path = os.join(objects_dir, dir_name)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    object_file_path = os.path.join(dir_path, file_name)
    with open(object_file_path, "wb") as f:
        f.write()
    
    return object_file_path

class Object:
    def __init__(self, file_path:str, repo_path:str):
        self.file_path = file_path
        self.repo_path = repo_path

        if is_child(file_path, repo_path):
            self.init_file()
        else:
            self.init_object()
    
    def init_file(self):
        """Crée un objet dans `.\git`"""
        # Obtenir le contenu à stocker
        self.header, self.object_content = self.get_content()
        self.content = f"{self.header}\0{self.object_content}".encode()

        self.sha1 = sha1(self.content).hexdigest()
        self.encoded_content = zlib.compress(self.content)

        self._save_file()

    def init_object(self):
        """Lis un objet git et stocke ses informations"""
        # Trouver le chemin du fichier
        self.encoded_content = self._read_file()
        self.content = zlib.decompress(self.encoded_content).decode()
        try:
            els = self.content.split("\0", 1)
            self.content = els[1]
            self.header = els[0]
        except Exception as e:
            print("Error decoding blob content:", e)
            return

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
        raise NotImplementedError(f"`get_content` n'est pas implémenté dans {type(self)}")

    def _read_file(self, file_path:Optional[str] = None):
        if file_path is None:
            file_path = self.file_path

        with open(file_path, 'rb') as f:
            return f.read()
    
    def _save_file(self):
        self.git_object_path = get_object_path(self.sha1, self.repo_path)

        with open(self.git_object_path, "wb") as f:
            f.write(self.encoded_content)