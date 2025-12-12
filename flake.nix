{
  description = "Development flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
  };

  outputs =
    { nixpkgs, ... }:
    let
      x86 = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages."${x86}";
      lib = nixpkgs.lib;
      lintPkgs = with pkgs; [
        black
        beautysh
        mdformat
        deadnix
        nixfmt-rfc-style
      ];
    in
    {
      checks."${x86}" = {
        lint = pkgs.stdenv.mkDerivation {
          name = "lint";
          src = ./.;

          dontBuild = true;
          doCheck = true;

          buildInputs = lintPkgs;

          checkPhase = ''
            ${lib.getExe pkgs.treefmt} --ci
          '';

          installPhase = ''
            mkdir "$out"
          '';
        };
      };

      devShells."${x86}".default = pkgs.mkShellNoCC {
        packages = [
          (pkgs.python3.withPackages (python-pkgs: [
            python-pkgs.pygithub
          ]))
        ] ++ lintPkgs;

        shellHook = ''
          git config --local core.hooksPath .githooks/
          git config --local pull.rebase true
        '';

        # Environment Variables
        GH_TOKEN = "xxx";
        GH_USER = "xxx";
        GOGS_TOKEN = "xxx";
        GOGS_URL = "https://git.xxx/api/v1";
        GOGS_USER_ID = "xxx";
      };
    };
}
