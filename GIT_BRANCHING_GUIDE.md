# Git Branching Guide

This guide explains how to create and manage branches in Git, covering essential commands and providing practical examples for each.

## Table of Contents
- [Understanding Git Branches](#understanding-git-branches)
- [git branch - Branch Management](#git-branch---branch-management)
- [git checkout - Switching Branches](#git-checkout---switching-branches)
- [git merge - Merging Branches](#git-merge---merging-branches)
- [git rebase - Rewriting History](#git-rebase---rewriting-history)
- [Best Practices](#best-practices)

## Understanding Git Branches

A branch in Git represents an independent line of development. The default branch in Git is typically called `main` (or `master` in older repositories). Branches allow you to work on new features, bug fixes, or experiments without affecting the main codebase.

## git branch - Branch Management

The `git branch` command is used to create, list, rename, and delete branches.

### List Branches

**List all local branches:**
```bash
git branch
```

**Example output:**
```
  feature/user-auth
* main
  bugfix/login-error
```
The asterisk (*) indicates the current branch.

**List all branches (local and remote):**
```bash
git branch -a
```

**Example output:**
```
  feature/user-auth
* main
  remotes/origin/main
  remotes/origin/feature/user-auth
  remotes/origin/develop
```

**List remote branches only:**
```bash
git branch -r
```

### Create a New Branch

**Create a new branch:**
```bash
git branch feature/new-feature
```

This creates a new branch called `feature/new-feature` but doesn't switch to it.

**Create a branch from a specific commit:**
```bash
git branch feature/hotfix abc123
```

This creates a branch from commit `abc123`.

### Delete a Branch

**Delete a local branch (safe delete - only if merged):**
```bash
git branch -d feature/old-feature
```

**Force delete a local branch (even if not merged):**
```bash
git branch -D feature/abandoned-feature
```

**Example:**
```bash
# Create a test branch
git branch test/experimental

# Delete it safely
git branch -d test/experimental
# Output: error: The branch 'test/experimental' is not fully merged.

# Force delete it
git branch -D test/experimental
# Output: Deleted branch test/experimental (was abc123).
```

**Delete a remote branch:**
```bash
git push origin --delete feature/old-feature
```

### Rename a Branch

**Rename the current branch:**
```bash
git branch -m new-branch-name
```

**Rename a different branch:**
```bash
git branch -m old-branch-name new-branch-name
```

**Example:**
```bash
# Rename current branch
git branch -m feature/user-authentication

# Rename a specific branch
git branch -m feature/old-name feature/new-name
```

## git checkout - Switching Branches

The `git checkout` command switches between branches and can also create new branches.

### Switch to an Existing Branch

**Switch to a branch:**
```bash
git checkout feature/user-auth
```

**Example:**
```bash
# You're on main branch
git checkout develop
# Output: Switched to branch 'develop'

# Check current branch
git branch
# Output:
#   main
# * develop
```

### Create and Switch to a New Branch

**Create a new branch and switch to it:**
```bash
git checkout -b feature/new-feature
```

This is equivalent to:
```bash
git branch feature/new-feature
git checkout feature/new-feature
```

**Example:**
```bash
# Create and switch to new feature branch
git checkout -b feature/payment-integration
# Output: Switched to a new branch 'feature/payment-integration'

# Make some changes
echo "payment code" > payment.js
git add payment.js
git commit -m "Add payment integration"
```

**Create a branch from a specific commit:**
```bash
git checkout -b bugfix/critical-fix abc123
```

**Create a branch from a remote branch:**
```bash
git checkout -b feature/local-copy origin/feature/remote-branch
```

### Modern Alternative: git switch

Git 2.23+ introduced `git switch` as a clearer alternative to `git checkout` for branch operations:

```bash
# Switch to existing branch
git switch develop

# Create and switch to new branch
git switch -c feature/new-feature

# Switch to previous branch
git switch -
```

## git merge - Merging Branches

The `git merge` command integrates changes from one branch into another. It creates a new "merge commit" that combines the histories.

### Basic Merge

**Merge a branch into the current branch:**
```bash
git checkout main
git merge feature/user-auth
```

**Example:**
```bash
# Switch to the branch you want to merge INTO
git checkout main

# Merge the feature branch
git merge feature/user-auth
# Output: Updating abc123..def456
#         Fast-forward
#          auth.js | 45 +++++++++++++++++++++++++++++++++++++++++++++
#          1 file changed, 45 insertions(+)
```

### Fast-Forward Merge

When the target branch hasn't diverged from the source branch, Git performs a "fast-forward" merge (simply moves the pointer forward).

**Example:**
```bash
# Initial state: main is at commit A, feature is at commit C
# main:    A
# feature: A -> B -> C

git checkout main
git merge feature/user-auth
# Result: main now points to C (fast-forward)
# main:    A -> B -> C
# feature: A -> B -> C
```

### No Fast-Forward Merge

Force creation of a merge commit even when fast-forward is possible:

```bash
git merge --no-ff feature/user-auth
```

**Example:**
```bash
git checkout main
git merge --no-ff feature/user-auth
# Output: Merge made by the 'recursive' strategy.
#          auth.js | 45 +++++++++++++++++++++++++++++++++++++++++++++
#          1 file changed, 45 insertions(+)

# This creates a merge commit even if fast-forward was possible
```

### Resolving Merge Conflicts

When Git can't automatically merge changes, you'll encounter a merge conflict.

**Example:**
```bash
git checkout main
git merge feature/conflicting-branch
# Output: Auto-merging config.js
#         CONFLICT (content): Merge conflict in config.js
#         Automatic merge failed; fix conflicts and then commit the result.

# View conflicted files
git status
# Output: On branch main
#         You have unmerged paths.
#         
#         Unmerged paths:
#           (use "git add <file>..." to mark resolution)
#                 both modified:   config.js

# Open config.js and look for conflict markers:
# <<<<<<< HEAD
# const API_URL = "https://api.example.com";
# =======
# const API_URL = "https://api.newdomain.com";
# >>>>>>> feature/conflicting-branch

# Edit the file to resolve conflicts, then:
git add config.js
git commit -m "Merge feature/conflicting-branch and resolve conflicts"
```

### Abort a Merge

If you want to cancel a merge in progress:

```bash
git merge --abort
```

## git rebase - Rewriting History

The `git rebase` command moves or combines a sequence of commits to a new base commit. Unlike merge, it creates a linear history.

### Basic Rebase

**Rebase current branch onto another branch:**
```bash
git checkout feature/user-auth
git rebase main
```

**Example:**
```bash
# Initial state:
# main:    A -> B -> C
# feature: A -> D -> E

git checkout feature/user-auth
git rebase main

# Result:
# main:    A -> B -> C
# feature: A -> B -> C -> D' -> E'
# (D and E are replayed on top of C, creating D' and E')
```

### Interactive Rebase

Interactive rebase allows you to edit, reorder, squash, or drop commits:

```bash
git rebase -i HEAD~3
```

**Example:**
```bash
# Rebase the last 3 commits interactively
git rebase -i HEAD~3

# This opens an editor with:
# pick abc123 Add user authentication
# pick def456 Fix typo in auth
# pick ghi789 Update auth tests

# You can change 'pick' to:
# - squash (s): combine commit with previous one
# - reword (r): change commit message
# - edit (e): pause to amend the commit
# - drop (d): remove the commit

# Example: squash the typo fix into the main commit
pick abc123 Add user authentication
squash def456 Fix typo in auth
pick ghi789 Update auth tests

# Save and close the editor
# Git will combine the first two commits
```

### Rebase onto a Specific Branch

**Rebase feature branch onto main:**
```bash
git rebase main feature/user-auth
```

This is equivalent to:
```bash
git checkout feature/user-auth
git rebase main
```

### Resolving Rebase Conflicts

Similar to merge conflicts, but resolved one commit at a time:

**Example:**
```bash
git checkout feature/user-auth
git rebase main
# Output: CONFLICT (content): Merge conflict in auth.js
#         error: could not apply abc123... Add user authentication

# Fix conflicts in auth.js, then:
git add auth.js
git rebase --continue

# If you want to skip this commit:
git rebase --skip

# If you want to abort the rebase:
git rebase --abort
```

### Rebase vs Merge

**When to use rebase:**
- Before pushing to keep history clean and linear
- When working on a feature branch that you want to update with latest main
- To clean up local commit history before sharing

**When to use merge:**
- When integrating completed features into main branch
- When working on public/shared branches
- When you want to preserve the complete history of how branches evolved

**Example workflow combining both:**
```bash
# Update your feature branch with latest main (rebase)
git checkout feature/user-auth
git fetch origin
git rebase origin/main

# After feature is complete, merge into main (merge)
git checkout main
git merge --no-ff feature/user-auth
git push origin main
```

## Best Practices

### Branch Naming Conventions

Use descriptive names with prefixes:
```bash
feature/user-authentication
bugfix/login-error
hotfix/security-patch
release/v1.2.0
```

### Common Workflow

**1. Create a feature branch:**
```bash
git checkout main
git pull origin main
git checkout -b feature/new-feature
```

**2. Work on your feature:**
```bash
# Make changes
git add .
git commit -m "Implement new feature"
```

**3. Keep your branch updated:**
```bash
git fetch origin
git rebase origin/main
```

**4. Push your branch:**
```bash
git push origin feature/new-feature
```

**5. Create a pull request (via GitHub/GitLab/etc.)**

**6. After PR is approved, merge:**
```bash
git checkout main
git pull origin main
git merge --no-ff feature/new-feature
git push origin main
```

**7. Clean up:**
```bash
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### Quick Reference

```bash
# List branches
git branch                    # local branches
git branch -a                 # all branches
git branch -r                 # remote branches

# Create branch
git branch branch-name        # create only
git checkout -b branch-name   # create and switch

# Switch branches
git checkout branch-name      # switch to branch
git switch branch-name        # modern alternative

# Delete branch
git branch -d branch-name     # safe delete
git branch -D branch-name     # force delete
git push origin --delete name # delete remote

# Merge
git merge branch-name         # merge into current
git merge --no-ff branch-name # force merge commit
git merge --abort             # cancel merge

# Rebase
git rebase branch-name        # rebase onto branch
git rebase -i HEAD~n          # interactive rebase
git rebase --continue         # continue after conflict
git rebase --abort            # cancel rebase
```

## Additional Resources

- [Git Official Documentation](https://git-scm.com/doc)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)

---

This guide covers the essential commands for branch management in Git. Practice these commands in a test repository to become comfortable with branching workflows.
