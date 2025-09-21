# ---------------------------------
# Lis un objet dans `.\git`       |
# ---------------------------------

import os
import zlib

def read(sha1:str, repo_path):
    """
    Read an object from its sha1

    Returns
    -------
    The content of the file, raises an FileExistsError if the sha1 is not valid
    """
    path = os.path.join(repo_path, ".git","objects", sha1[:2], sha1[2:])

    if not os.path.exists(path):
        raise FileExistsError
    
    with open(path, "rb") as f:
        content = f.read()
    
    return zlib.decompress(content).decode()