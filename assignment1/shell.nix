{ pkgs ? import (fetchTarball {
  name = "nixpkgs-master-16-02-2022";
  url = "https://github.com/nixos/nixpkgs/archive/5e0670ee9117d180e3220cd367ac67b440474349.tar.gz";
  sha256 = "169q4x3a7z64j5lqmwfn1f50wcbhbx2p5zkm4j27v0aa2734dkdx";
}) {} }:

let
  extensions = (with pkgs.vscode-extensions; [
      ms-vsliveshare.vsliveshare
      bbenoist.nix
    ] ++ [{
      name = "python";
      publisher = "ms-python";
      version = "2021.12.1559732655";
      sha256 = "hXTVZ7gbu234zyAg0ZrZPUo6oULB98apxe79U2yQHD4=";
    } {
      name = "vscode-terminal-capture";
      publisher = "devwright";
      version = "0.0.1";
      sha256 = "sha256-jjmAIIvuQ2DlBddPuJA35NDpVsDRKcwnfb7S3dXM7dw=";
    }]);

  vscode-with-extensions = pkgs.vscode-with-extensions.override {
    vscodeExtensions = extensions;
  };

  pythonPackages = pkgs.python39Packages;

in pkgs.mkShell rec {
    name = "parallel-computing-dev";

    packages = [
      pythonPackages.jupyter
      pythonPackages.pandas
      pythonPackages.python
      pythonPackages.matplotlib
      pythonPackages.gprof2dot
      pkgs.valgrind
      pkgs.automake
      pkgs.gperftools
      pkgs.graphviz
      pkgs.gv
    ];

    phases = [];

    src = ./.;
}
