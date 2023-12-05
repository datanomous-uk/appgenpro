import os
from git import Repo
from git.exc import GitCommandError
from github import Github, GithubException


def push_to_github(
    local_folder_path: str,
    github_token: str,
    repository_name: str
):

    # Check if the repository already exists on GitHub
    g = Github(github_token)
    user = g.get_user()
    repo = None



    try:
        repo = user.get_repo(repository_name)
        repo.delete()  # This deletes the repository
        print(f"Repository '{repository_name}' existed and was deleted.")
    except GithubException as e:
        if e.status == 404:  # Repository does not exist
            print(f"Repository '{repository_name}' does not exist.")
        else:
            raise  # Re-raises the exception for any other errors

    # Create the repository again
    repo = user.create_repo(repository_name)
    repo_url = repo.clone_url
    print(f"Repository '{repository_name}' created at {repo_url}")


    if os.path.exists(local_folder_path):
        Repo.init(local_folder_path)

        try:
            # Add all files to the Git repository
            repo = Repo(local_folder_path)
            repo.git.add('--all')

            # Commit changes
            repo.git.commit('-m', 'aipreneurosBot made changes.')

            # Set the remote URL for the GitHub repository
            repo.create_remote('origin', repo_url)
        
        except GitCommandError as e:
            # Push changes to GitHub
            repo.git.push('--set-upstream', 'origin', 'main')
            print(f"Changes pushed to '{repository_name}' on GitHub.")
            return repo_url
    return None
