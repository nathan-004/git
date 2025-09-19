import os
from hashlib import sha1
import zlib

from git.objects.object import Object

class Blob(Object):

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
        file_content = self._read_file()
        header = f"blob {len(file_content)}"
        
        return (header,file_content)