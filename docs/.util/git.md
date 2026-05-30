# Git Command Reference

## Branches
- `git branch` - list local branches
- `git branch -a` - list all local and remote branches
- `git branch -d <branch>` - delete local branch
- `git branch -D <branch>` - force delete local branch
- `git push origin --delete <branch>` - delete remote branch
- `git branch --move <old-name> <new-name>` - rename branch locally

## Commits and History
- `git commit --amend` - amend last commit
- `git reset --soft HEAD~1` - undo last commit but keep changes staged
- `git reset --mixed HEAD~1` - undo last commit and keep changes unstaged
- `git reset --hard HEAD~1` - undo last commit and discard changes
- `git log` - show commit history
- `git log --oneline --graph --decorate --all` - readable history graph
- `git log -p` - show patch for each commit
- `git log --stat` - show changed files and summary
- `git show <commit>` - show a single commit

## Merge and Rebase
- `git merge <branch>` - merge branch into current
- `git merge --no-ff <branch>` - merge with merge commit
- `git rebase <branch>` - rebase current branch onto another branch
- `git rebase --continue` - continue after resolving conflicts
- `git rebase --abort` - abort rebase and return to previous state
- `git rebase --skip` - skip current patch during rebase

## Push and Pull
- `git push` - push current branch to remote
- `git push origin <branch>` - push specific branch to origin
- `git push --tags` - push all tags to remote
- `git pull` - fetch + merge remote changes
- `git pull --rebase` - fetch and rebase
- `git fetch --all` - fetch all remotes

## Tags and Releases
- `git tag -a v1.0.0 -m "Release v1.0.0"` - create annotated tag
- `git tag` - list tags
- `git push origin v1.0.0` - push tag to remote
- `git push origin --tags` - push all tags
- `git tag -d v1.0.0` - delete local tag
- `git push origin :refs/tags/v1.0.0` - delete remote tag

## Inspection and Configuration
- `git status` - show working tree status
- `git diff` - show unstaged changes
- `git diff --staged` - show staged changes
- `git diff <branch>..<branch>` - compare two branches
- `git remote -v` - show remote names and URLs
- `git remote show origin` - show remote details
- `git config user.name` - show Git user name
- `git config user.email` - show Git user email
- `git config --list` - show all Git configuration

## Logs with Arguments
- `git log --author="Name"` - filter commits by author
- `git log --since="2 weeks ago" --until="today"` - filter by time range
- `git log --grep="fix"` - search commit messages
- `git log --follow -- <file>` - history for a single file
- `git log --pretty=format:"%h %ad | %s%d [%an]" --graph --date=short` - custom formatted log

## Useful Shortcuts
- `git checkout <branch>` - switch branch
- `git switch <branch>` - switch branch (modern alternative)
- `git switch -c <branch>` - create and switch to new branch
- `git stash` - stash local changes
- `git stash pop` - apply and remove stash
- `git stash list` - list stashes
- `git stash drop` - remove a stash
- `git clean -fd` - remove untracked files and directories
