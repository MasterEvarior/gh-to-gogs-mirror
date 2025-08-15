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
    in
    {
      devShells."${x86}".default = pkgs.mkShellNoCC {
        packages = with pkgs; [
          # Python
          (pkgs.python3.withPackages (python-pkgs: [
            python-pkgs.pygithub
          ]))

          # Formatters
          black
          beautysh
          mdformat
          deadnix
          nixfmt-rfc-style
        ];

        shellHook = ''
          git config --local core.hooksPath .githooks/
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
