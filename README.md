<div align="center">
    <img src="wwwroot/favicon.svg" width=96>
</div>
<hr>

# System Packages for Callisto OS
This repository serves as an automated rpm package repository for the Fedora based Callisto OS image.

- [System Packages for Callisto OS](#system-packages-for-callisto-os)
  - [Git Repository Structure](#git-repository-structure)
    - [Package.json Format](#packagejson-format)
    - [Build System](#build-system)
  - [System Packages](#system-packages)
    - [callisto-backgrounds](#callisto-backgrounds)
    - [callisto-logos](#callisto-logos)
    - [callisto-theme](#callisto-theme)
    - [reset-home](#reset-home)
    - [webapp-manager](#webapp-manager)


## Git Repository Structure
| Folder/File | Description |
|-------------|-------------|
| **.github/**    | GitHub configuration directory |
| &emsp;**workflows/** | GitHub automated ci/cd pipeline definitions |
| &emsp;&emsp;publish.yml | Pipeline to publish all Packages to github pages |
| **flatpaks/** | Reserved for flatpack apps |
| **pkgs/**     | All native rpm/deb packages |
| &emsp;**&lt;package-name&gt;/** | Package directory, subdirectories for each package |
| &emsp;&emsp;files/ | Files that are apart of the package (acts like root/ on installation system) |
| &emsp;&emsp;build.sh (optional) | Shell script used to generate or modify the contents of the files/ directory automatically |
| &emsp;&emsp;build.py (optional) | Python script used to generate or modify the contents of the files/ directory automatically |
| &emsp;&emsp;package.json | Package information file whose format is borrowed from NodeJS package files with specific metadata (author, name, desc, dependencies, etc) |
| **wwwroot/** | Website for package browsing |
| build-packages.py | Python script for facilitating the building of the native packages |

### Package.json Format
The `package.json` file within each package borrows heavily from the package.json file used by JavaScript NodeJS projects though the fields have been repurposed for different uses and a few new fields have been added. To see how these fields are actually used by the build system see the [Build System](#build-system) section. An example of such a package.json can be seen detailed below.
```json
{
    "name": "my-package",
    "author": "my-name",
    "vendor": "my-company",
    "version": "1.0.0",
    "license": "MIT",
    "description": "A description of this package",
    "cpu": [ 
      "noarch",
      "x86_64",
      "aarch64" 
    ],
    "os": [
      "rpm",
      "deb",
      "pacman",
      "apk"
    ],
    "scripts": {
      "before-install": "path/to/script",
      "after-install": "path/to/script",
      "before-remove": "path/to/script",
      "after-remove": "path/to/script"
    },
    "dependencies": {
      "some-dependency": "^1.0.0"
    },
    "provides": [
      "capability-one", 
      "capability-two"
    ],
    "replaces": []
}
```

### Build System
[FPM](https://fpm.readthedocs.io/en/latest/cli-reference.html) is used as the build system for native packages. As such, the package.json fields map to specific arguments in the FPM command.

| Package.json Field | FPM Argument | Description |
|--------------------|--------------|-------------|
| name | -n NAME | Package name, if missing defaults to folder name |
| author | -m MAINTAINER | Author/package maintainer |
| vendor | --vendor VENDOR | Package vendor (defaults to the author if not provided) |
| version | -v VERSION | Package version |
| license | --license LICENSE | Package license name |
| description | --description DESCRIPTION | Package short description |
| cpu | -a ARCHITECTURE | CPU architecture the package works on: noarch, x86_64, aarch64, all, native etc. |
| os | -t OUTPUT_TYPE | Supported OS package managers: deb, rpm, solaris, pacman, apk etc. |
| scripts | --before-install, --after-install, --before-remove, --after-remove FILE | Path to a script to run when installing or uninstalling the package | 
| dependencies | -d DEPENDENCY | List of package dependencies, versions are ignored |
| provides | --provides PROVIDES | Capabilities provided by this package |
| replaces | --replaces REPLACES | Packages replaced by this package |

## System Packages
### callisto-backgrounds
Astrophotography images taken by me to be used as computer wallpapers and background for Callisto OS

### callisto-logos
Iconography for Callisto OS. Applications launcher icon, OS release icon, etc. 

### callisto-theme
A package and set of config files to define the look and feel of the OS. 

### reset-home
Simple console app for resetting your home directory to the configuration in /etc/skel in case of new defaults being applied down the line. Additional files are ignore but conflicting files will be replaced with those from /etc/skel.

### webapp-manager
A small python gui app to create and manage web-applications as if they were native applications. It does so by creating .desktop files that open the configured website in one of your installed browsers and attempts to configure that browser to run in an applications mode, removing all browser toolbars etc, though this is not always possible or easy. 