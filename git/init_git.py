import os

from git.logger import Logger

# -------- Helper Functions --------

def get_current_folder_path():
    """Returns the current working directory."""
    return os.getcwd()

def is_git_repository(folder_path):
    """Checks if the given folder is a Git repository."""
    return os.path.isdir(os.path.join(folder_path, '.git'))

def create_objects_folder(git_folder_path):
    """Creates the objects folder inside the .git directory."""
    objects_path = os.path.join(git_folder_path, 'objects')
    os.makedirs(objects_path, exist_ok=True)
    return objects_path

# -------- Main Function --------

def git_init(folder_path:str = get_current_folder_path(), quiet:bool = False):
    """
    Initializes a Git repository in the specified folder if it is not already a Git repository.

    Parameters
    ----------
    folder_path (str): The path to the folder where the Git repository should be initialized.
                       Defaults to the current working directory.
    quiet (bool): If True, suppresses output messages. Defaults to False.

    To do
    -----
    --bare
    --initial-branch <name>
    --template <template_directory>
    --separate-git-dir <git dir>
    --shared[=(false|true|umask|group|all|world|everyone)]
    """
    logger = Logger(display=not quiet)

    if is_git_repository(folder_path):
        logger.print(f"The folder '{folder_path}' is already a Git repository.")
    else:
        new_folder_path = os.path.join(folder_path, '.git')
        os.makedirs(new_folder_path)
        logger.print(f"Initialized empty Git repository in '{new_folder_path}'")
    
    create_objects_folder(os.path.join(folder_path, '.git'))

def main():
    git_init("example")