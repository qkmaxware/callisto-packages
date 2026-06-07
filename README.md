<div align="center">
    <img src="wwwroot/favicon.svg" width=96>
</div>
<hr>

# System Packages for Callisto OS
This repository serves as an automated rpm package repository for the Fedora based Callisto OS image.

## Structure
- .github/
  - workflows/
    - publish.yml         -- Publish all Packages to github pages
- pkgs/
  - &lt;package-name&gt;/ -- Subdirectories for each package.
    - files/              -- Files that are apart of the package (acts like root/ on installation system)
    - build.sh            -- Script to build each package. May generate the files/ automatically or modify it before packaging
    - metadata.conf       -- Environment file with package specific metadata (author, name, desc, dependencies, etc)
- wwwroot/                -- Website for package browsing

## Packages
### callisto-backgrounds
Astrophotography images taken by me to be used as computer wallpapers and background for Callisto OS

### callisto-icons
Iconography for Callisto OS. Applications launcher icon, OS release icon, etc. 

### reset-home
Simple console app for resetting your home directory to the configuration in /etc/skel in case of new defaults being applied down the line. Additional files are ignore but conflicting files will be replaced with those from /etc/skel.

### webapp-manager
A small python gui app to create and manage web-applications as if they were native applications. It does so by creating .desktop files that open the configured website in one of your installed browsers and attempts to configure that browser to run in an applications mode, removing all browser toolbars etc, though this is not always possible or easy. 