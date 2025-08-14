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


def get_github_repos(g: Github, owner: str) -> List[Repository]:
    matching_repos = []
    for repo in g.get_user().get_repos():
        if repo.owner.login == owner:
            matching_repos.append(repo)
    return matching_repos


def get_gogs_repos(gogs_token: str, gogs_url: str) -> List[str]:
    headers = {"Authorization": "token " + gogs_token, "Accept": "application/json"}

    response = requests.get(gogs_url + "/user/repos", headers=headers)
    response.raise_for_status()

    print("Test")
    print(response)
    print(response.json())

    return repo_names


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

    auth = Auth.Token(GH_ACCESS_TOKEN)
    g = Github(auth=auth)

    repositories = get_github_repos(g, GH_USER)

    if MIRROR_FORKS:
        repositories = remove_forks(all_repositories)

    gogs_repositories = get_gogs_repos(GOGS_ACCESS_TOKEN, GOGS_URL)
    print(gogs_repositories)

    # for repo in repositories:
    #     # print(repo.full_name)
    #     print(repo.clone_url)
    #     print(repo.fork)

    g.close()


if __name__ == "__main__":
    main()
