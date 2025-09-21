from git.objects.read import read
from git.init_git import main as init_git
from git.objects.commits import main as commit_main
from git.objects.tree import main as tree_main

if __name__ == "__main__":
    init_git()
    # tree_main()
    sha1 = commit_main()
    print(read(sha1, "example"))