from git.init_git import main as init_git
from git.commits.commits import main as commit_main
from git.trees.tree import main as tree_main

if __name__ == "__main__":
    init_git()
    # tree_main()
    commit_main()