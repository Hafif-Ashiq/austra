{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.python39Packages.pip
    pkgs.python39Packages.virtualenv
    pkgs.postgresql_15
    pkgs.chromium
    pkgs.chromedriver
    pkgs.nodejs-18_x
    pkgs.yarn
  ];
} 