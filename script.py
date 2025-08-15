import os
import sys
import random
import requests
from typing import List
from github import Github
from github import Auth
from github.Repository import Repository


def get_env_var(name: str) -> str:
    result = os.environ.get(name)
    if result == None:
        sys.exit("Environment variable %s is not defined, exiting script!" % name)
    return result


def get_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value != None and value.isdigit():
        return int(value)
    else:
        return default


def get_list(name: str, default: List[str]) -> List[str]:
    value = os.environ.get(name)
    if value == None:
        return default
    return value.split(";")


def get_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value != None:
        return value in value in ["true", "1", "yes"]
    else:
        return default


def get_github_repos(gh_access_token: str, owner: str) -> List[Repository]:
    auth = Auth.Token(gh_access_token)
    g = Github(auth=auth)

    matching_repos = []
    for repo in g.get_user().get_repos(visibility="all"):
        if repo.owner.login == owner:
            matching_repos.append(repo)

    g.close()

    return matching_repos


def get_gogs_repos(gogs_token: str, gogs_url: str) -> List[str]:
    headers = {"Authorization": "token " + gogs_token, "Accept": "application/json"}

    response = requests.get(gogs_url + "/user/repos", headers=headers)
    response.raise_for_status()

    repo_names = [repo["name"] for repo in response.json()]
    return repo_names


def create_gogs_repo(
    gogs_token: str,
    gogs_url: str,
    gogs_user_id: int,
    gh_user: str,
    gh_access_token: str,
    repo: Repository,
):
    headers = {
        "Authorization": "token " + gogs_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "clone_addr": repo.clone_url,
        "repo_name": repo.name,
        "uid": gogs_user_id,
        "mirror": True,
        "private": True,
        "description": repo.description,
        "auth_username": gh_user,
        "auth_password": gh_access_token,
    }
    response = requests.post(gogs_url + "/repos/migrate", headers=headers, json=payload)
    response.raise_for_status()


def remove_forks(repositories: List[Repository]) -> List[Repository]:
    for repo in repositories:
        if repo.fork is True:
            repositories.remove(repo)
    return repositories


def main():
    GH_USER = get_env_var("GH_USER")
    GH_ACCESS_TOKEN = get_env_var("GH_TOKEN")
    MIRROR_FORKS = get_bool("MIRROR_FORKS", False)
    GOGS_URL = get_env_var("GOGS_URL")
    GOGS_ACCESS_TOKEN = get_env_var("GOGS_TOKEN")
    GOGS_USER_ID = int(get_env_var("GOGS_USER_ID"))

    repositories = get_github_repos(GH_ACCESS_TOKEN, GH_USER)

    print("Found {:d} repositories on GitHub".format(len(repositories)))

    if MIRROR_FORKS:
        repositories = remove_forks(all_repositories)

    gogs_repositories = get_gogs_repos(GOGS_ACCESS_TOKEN, GOGS_URL)

    for repo in repositories:
        print("Checking {:s}...".format(repo.name))
        if repo.name not in gogs_repositories and repo.get_stats_contributors() != None:
            print("Create new mirror for {:s}".format(repo.name))
            create_gogs_repo(
                GOGS_ACCESS_TOKEN,
                GOGS_URL,
                GOGS_USER_ID,
                GH_USER,
                GH_ACCESS_TOKEN,
                repo,
            )
            print("Successfully created new mirror for {:s}".format(repo.name))
        else:
            print("{:s} does already exist or is empty".format(repo.name))


if __name__ == "__main__":
    main()
