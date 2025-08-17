# GitHub to Gogs Mirror

![quality workflow](https://github.com/MasterEvarior/gh-to-gogs-mirror/actions/workflows/quality.yaml/badge.svg) ![release workflow](https://github.com/MasterEvarior/gh-to-gogs-mirror/actions/workflows/publish.yaml/badge.svg)

A small utility script, which setups mirror repository on my [Gogs](https://gogs.io/) instance for each of my [GitHub](https://github.com/) repositories.

## Build

To build the container yourself, simply clone the repository and then build the container with the provided docker file. You can the run it as described in the section below.

```shell
docker build --tag gtgm .
```

Alternatively you can install the necessary dependencies with `pip` and the run the script:

```shell
pip install --no-cache-dir -r requirements.txt
python script.py
```

## Run

The easiest way is to use the provided container. Do not forget to add the necessary environment variables.

```shell
docker run -d \
  -e GH_TOKEN='ghp_o123asd31a' \
  -e GH_USER='JohnGit' \
  -e GOGS_TOKEN='ah19np12123' \
  -e GOGS_URL='https://git.my-url/api/v1' \
  -e GOGS_USER_ID='78' \
  ghcr.io/masterevarior/gh-to-gogs-mirror:latest
```

### Environment Variables

| Name         | Description                                          | Default | Example                     | Mandatory  |
|--------------|------------------------------------------------------|---------|-----------------------------|------------|
| GH_TOKEN     | API Token for GitHub                                 |         | `ghp_o123asd31a`            | ✅         |
| GH_USER      | Your GitHub username                                 |         | JohnGit                     | ✅         |
| GOGS_TOKEN   | API Token for Gogs                                   |         | `ah19np12123`               | ✅         |
| GOGS_URL     | URL to your Gogs instance                            |         | `https://git.my-url/api/v1` | ✅         |
| GOGS_USER_ID | Id of our Gogs user                                  |         | 78                          | ✅         |
| MIRROR_FORKS | Wether or not you want to mirror forks you have made | False   | False                       | ❌         |

## Development

### Linting

All linters are run with the treefmt command. Note that the command does not install the required formatters.

```shell
treefmt
```

### Git Hooks

There are some hooks for formatting and the like. To use those, execute the following command:

```shell
git config --local core.hooksPath .githooks/
```

### Nix

If you are using [NixOS or the Nix package manager](https://nixos.org/), there is a dev shell available for your convenience. This will install Go, everything needed for formatting, set the Git hooks and some default environment variables. Start it with this command:

```shell
nix develop
```

If you happen to use [nix-direnv](https://github.com/nix-community/nix-direnv), this is also supported.

## Improvements, issues and more

Pull requests, improvements and issues are always welcome.
