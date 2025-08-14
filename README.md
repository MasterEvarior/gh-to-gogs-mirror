# Plex Pinned Collection Randomizer

![quality workflow](https://github.com/MasterEvarior/plex-pinned-collection-randomizer/actions/workflows/quality.yaml/badge.svg) ![release workflow](https://github.com/MasterEvarior/plex-pinned-collection-randomizer/actions/workflows/publish.yaml/badge.svg)

A small utility script, which randomises the pinned collections on my [Plex server](http://plex.tv). I run this in conjunction with [Kometa](https://kometa.wiki/en/latest/).

If you want something more capable or with a GUI, you may want to use these alternatives instead:

- [ColleXions ](https://github.com/jl94x4/ColleXions/tree/main)
- [DynamiX](https://github.com/TheImaginear/dynamiX)

## Build

To build the container yourself, simply clone the repository and then build the container with the provided docker file. You can the run it as described in the section below.

```shell
docker build --tag ppcr .
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
  -e PPCR_BASE_URL='http://192.168.1.1:32400' \
  -e PPCR_TOKEN='xxxx' \
  ghcr.io/masterevarior/plex-pinned-collection-randomizer:latest
```

### Environment Variables

| Name             | Description                                                | Default                                                                                 | Example             | Mandatory  |
|------------------|------------------------------------------------------------|-----------------------------------------------------------------------------------------|---------------------|------------|
| PPCR_BASE_URL    | URL to your Plex server |                                  | `http://192.168.1.1:32400`   | ✅         |
| PPCR_TOKEN       | Token for your Plex server |                               | `xxxxxxx`                    | ✅         |
| PPCR_AMOUNT      | Amount of collections that should be pinned at random      | `5`             | `12`       | ❌         |
| PPCR_MIN_AMOUNT_IN_COLLECTION | Amount of movies/shows a collection does need to include to be considered for pinning | `0`             | `3`       | ❌         |
| PPCR_ALWAYS_PIN  | A list of strings, seperated by `;`. If these strings are found inside of a collection name, it will always be pinned|       (empty)       | `Popular;Christmas Things`       | ❌         |
| PPCR_ALLOW_DUPLICATES | If set to false, no collections with the same name will be pinned. | `True` | `False` | ❌ |
| PPCR_INCLUDED_LIBRARY_TYPES | A list of strings, seperated by `;`. Only libraries with this type of media will be considered, valid are `movie` and `show`.   | `movie;show` | `movie` | ❌ |

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
