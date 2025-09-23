from git.objects.read import read
from git.init_git import main as init_git
from git.objects.commits import main as commit_main
from git.objects.tree import main as tree_main
from git.objects.branches import main as branch_main

if __name__ == "__main__":
    init_git()
    # tree_main()
    branch_main()
    print(read("bbd158bcdbd5ba611cdd48b898f77a652cad603d", "example"))