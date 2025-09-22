# ---------------------------------
# Lis un objet dans `.\git`       |
# ---------------------------------

import os
import zlib
from typing import Union

from git.objects.object import Object
from git.head import get_latest_branch_content

def read(sha1:str, repo_path):
    """
    Read an object from its sha1

    Returns
    -------
    The content of the file, raises an FileExistsError if the sha1 is not valid
    """
    path = os.path.join(repo_path, ".git","objects", sha1[:2], sha1[2:])

    if not os.path.exists(path):
        raise FileNotFoundError
    
    with open(path, "rb") as f:
        content = f.read()
    
    return zlib.decompress(content).decode()

def read_object(sha1:str, repo_path:str) -> Object:
    """
    Read an object from its sha1 and returns the correspondent object

    Returns
    -------
    An object that can be a `Blog`, a `Commit` or a `Tree`
    """
    content = read(sha1, repo_path)

    content = content.split("\0")
    header, file_content = content[0], content[1]

    print(header, file_content)

def get_latest_commit(repo_path:str) -> str:
    return get_latest_branch_content(repo_path)