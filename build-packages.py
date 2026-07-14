import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
from typing import Self
from dataclasses import dataclass
from pathlib import Path
from itertools import chain
from datetime import datetime

ARCH_MAP = {
    "AMD64": "x86_64",
    "x64": "x86_64",
    "x86_64": "x86_64",
    "i386": "x86",
    "i686": "x86",
    "aarch64": "aarch64",
    "ARM64": "aarch64",
    "arm64": "aarch64",
}

@dataclass(frozen=True)
class DEFAULTS:
    VERSION = "0.1.0"
    LICENSE = "MIT"
    AUTHOR = "GitHub Actions"
    ARCHITECTURE = ARCH_MAP.get(platform.machine(), platform.machine()) # ie: x86_64 or "native"
    FORMAT = "rpm"

class PackageScripts:
    before_install: str | None
    after_install: str | None

    before_remove: str | None
    after_remove: str | None

class PrebuiltBinaries:
    _paths: dict[str, list[str]] = {}

    def add(self, fmt: str, path: str) -> None:
        if fmt in self._paths:
            self._paths[fmt].append(path)
        else:
            items = [path]
            self._paths[fmt] = items

    def get(self, fmt: str) -> list[str] | None:
        if fmt in self._paths:
            return self._paths[fmt]
        return None

class PackageMetadata:
    name: str
    version: str = DEFAULTS.VERSION
    cpu: list[str] = [ DEFAULTS.ARCHITECTURE ]
    fmts: list[str] = [ DEFAULTS.FORMAT ]
    description: str = ""
    license: str = DEFAULTS.LICENSE
    author: str = DEFAULTS.AUTHOR
    vendor: str = DEFAULTS.AUTHOR
    iteration: int = 1

    dependencies: list[str] | None
    provides: list[str] | None
    replaces: list[str] | None

    tags: list[str] | None = []
    scripts: PackageScripts = PackageScripts()
    binaries: PrebuiltBinaries = PrebuiltBinaries()

    files: list[str] | None = None
    
    def __init__(self):
        pass

    @staticmethod
    def load(package_dir: Path) -> Self | None:
        full_path = package_dir / "package.json"
        if not full_path.exists():
            return None
    
        print(f"> Loading metadata for {package_dir.name}")

        metadata = PackageMetadata()
        metadata.name = package_dir.name
        metadata.description=f"RPM package for {package_dir.name}"

        with full_path.open() as file:
            data = json.load(file)

        def as_list(value):
            if value is None:
                return []

            if isinstance(value, str):
                return [value]

            if isinstance(value, list):
                return [str(x) for x in value]
            
            return []
        
        def as_dict(value):
            if value is None:
                return {}
            if isinstance(value, dict):
                return value
            return {}

        metadata.name = data.get("name", metadata.name)
        metadata.cpu = as_list(data.get("cpu", metadata.cpu))
        metadata.fmts = as_list(data.get("os", metadata.fmts))
        metadata.version = data.get("version", metadata.version)
        metadata.description = data.get("description", metadata.description)
        metadata.license = data.get("license", metadata.license)
        metadata.author = data.get("author", metadata.author)
        metadata.vendor = data.get("vendor", metadata.author)
        metadata.tags = as_list(data.get("keywords", metadata.tags))

        metadata.scripts.before_install = data.get("scripts", {}).get("before-install", None)
        metadata.scripts.after_install = data.get("scripts", {}).get("after-install", None)
        metadata.scripts.before_remove = data.get("scripts", {}).get("before-remove", None)
        metadata.scripts.after_remove = data.get("scripts", {}).get("after-remove", None)

        bins = as_dict(data.get("bin", {}))
        for key, value in bins:
            if not isinstance(key, str):
                continue
            metadata.binaries.add(key, as_list(value))

        metadata.dependencies = list(data.get("dependencies", {}).keys())
        metadata.provides = as_list(data.get("provides"))
        metadata.replaces = as_list(data.get("replaces"))

        return metadata
    

class FPMBuilder:
    _kind: str
    _args: list[list[str]]

    def __init__(self, type: str):
        self._kind = type
        self._args = [
            ["fpm"],
            ["-s", "dir"],
            ["-t", type]
        ]

    def output(self, output_path: Path) -> None:
        self.add_option("-p", str(output_path))

    def source(self, source_path: Path) -> None:
        self.add_option("-C", str(source_path))

    def add_arg(self, arg: str) -> None:
        self._args.append([arg])
    
    def add_option(self, arg: str, value: str | Path | int) -> None:
        self._args.append([arg, str(value)])

    def add_dependencies(self, dependencies: list[str] | None) -> None:
        if dependencies:
            for dependency in dependencies:
                self.add_option("-d", dependency)

    def add_provides(self, provides: list[str] | None) -> None:
        if provides:
            for capibility in provides:
                self.add_option("--provides", capibility)

    def add_replaces(self, replaces: list[str] | None) -> None:
        if replaces:
            for capibility in replaces:
                self.add_option("--replaces", capibility)

    def build(self) -> bool:
        try:
            args = list(chain.from_iterable(self._args))
            print(f"> Building {self._kind} package: " + shlex.join(args))
            subprocess.run(args, check=True)
            return True
        except:
            print("> ERROR: Failed to build RPM package")
            return False


class PackageBuilder:

    def _fmt_license(self, license: str, author: str) -> str:
        year = datetime.now().year
        lower = license.lower()
        if lower == "mit":
            return f"""Copyright {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the “Software”), to deal in the Software without 
restriction, including without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom 
the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE."""
        # TODO allow for more license templates to be here to be auto-generated
        return license

    def _generate_files(self, pkg: PackageMetadata, package_dir: Path) -> None:
        # Shell script based generation
        shell_script_path = package_dir / "build.sh"
        if shell_script_path.exists():
            print(f"> Running build.sh script")
            try:
                if os.name != "nt":
                    subprocess.run(["chmod", "+x", str(shell_script_path)], check=True)

                shell = "bash" if shutil.which("bash") else "sh"
                subprocess.run([shell, "build.sh"], cwd=package_dir, check=True)
            except:
                print(f"> An error occurred executing build.sh")

        python_script_path = package_dir / "build.py"
        if python_script_path.exists():
            print(f"> Running build.py script")
            try:
                subprocess.run([sys.executable, "build.py"], cwd=package_dir, check=True)
            except:
                print(f"> An error occurred executing build.py")

        files_dir = package_dir / "files"
        if not files_dir.is_dir():
            return
        
        # Generate a license file if it needs to be generated
        license_dir = files_dir / "usr" / "share" / "licenses" / pkg.name
        license_file0 = package_dir / "LICENSE"
        license_file1 = package_dir / "LICENSE.md"
        license_file2 = package_dir / "LICENSE.txt"
        make_license = True if (pkg.license or license_file0.exists() or license_file1.exists() or license_file2.exists()) and not license_dir.exists() else False
        if make_license:
            license_dir.mkdir(exist_ok=True, parents=True)
            if license_file1.exists():
                shutil.copy(license_file1, license_dir)
            elif license_file0.exists():
                shutil.copy(license_file0, license_dir)
            elif license_file2.exists():
                shutil.copy(license_file2, license_dir)
            else:
                with open(license_dir / "LICENSE.txt", 'w') as file:
                    file.write(self._fmt_license(pkg.license, pkg.author))

    def build(self, package_dir: Path, output_dir: Path) -> PackageMetadata | None:
        # Load package metadata
        metadata: PackageMetadata | None = PackageMetadata.load(package_dir)
        if metadata == None:
            print(f"> SKIPPED: No package metadata")
            return None
        
        # Run build script(s) if they exists
        self._generate_files(metadata, package_dir)
        files_dir = package_dir / "files"

        # Build package for each architecture supported
        built_cps = []
        built_files = []
        
        for arch in metadata.cpu:
            built_any = False
            built_all = True
            for fmt in metadata.fmts:
                # Compile the files_dir into a package
                if files_dir.is_dir():
                    # Ensure the format folder exists
                    output_dir_package = output_dir / fmt   # IE output/rpm or output/deb
                    output_dir_package.mkdir(exist_ok=True)
                    output_filename = f"{metadata.name}-{metadata.version}-{str(metadata.iteration)}.{arch}.{fmt}"
                    output_path = output_dir_package / output_filename

                    # Configure FPM arguments
                    builder = FPMBuilder(fmt)
                    builder.source(files_dir)
                    builder.output(output_path)
                    builder.add_option("-n", metadata.name)
                    builder.add_option("-v", metadata.version)
                    builder.add_option("-a", arch)
                    builder.add_option("--iteration", metadata.iteration)
                    builder.add_option("--rpm-os", "linux")
                    builder.add_option("--prefix", "/")
                    builder.add_option("--description", metadata.description)
                    builder.add_option("--license", metadata.license)
                    builder.add_option("--maintainer", metadata.author)
                    builder.add_option("--vendor", metadata.vendor)

                    if (metadata.scripts.before_install):
                        builder.add_option("--before-install", metadata.scripts.before_install)
                    if (metadata.scripts.after_install):
                        builder.add_option("--after-install", metadata.scripts.after_install)
                    if (metadata.scripts.before_remove):
                        builder.add_option("--before-remove", metadata.scripts.before_remove)
                    if (metadata.scripts.after_remove):
                        builder.add_option("--after-remove", metadata.scripts.after_remove)

                    builder.add_dependencies(metadata.dependencies)
                    builder.add_provides(metadata.provides)
                    builder.add_replaces(metadata.replaces)

                    builder.add_arg(".")

                    # Build the package
                    didBuild = builder.build()
                    built_all &= didBuild
                    if didBuild:
                        built_any = True
                        built_files.append(f"{fmt}/{output_filename}")

            if built_any:
                built_cps.append(arch)

        # Check for any prebuilt binaries for each supported format
        for fmt in metadata.fmts:
            output_dir_package = output_dir / fmt 

            binaries: list[str] = metadata.binaries.get(fmt)
            if binaries == None:
                continue

            for path in binaries:
                file_path = package_dir / path
                if not file_path.exists():
                    continue
                shutil.copy(file_path, output_dir_package)
                built_files.append(f"{fmt}/{file_path.name}")

        metadata.cpu = built_cps                # overwrite the supported architectures with those that actually built successfully
        metadata.files = built_files            # record a list of all the generated files for the packages.json index to know about

        if len(built_files) <= 0:
            print(f"> SKIPPED: No packages generated")
            return None
        else:
            return metadata

    def build_all(self, root_dir: Path, output_dir: Path) -> None:  
        root_dir.mkdir(exist_ok=True, parents=True)
        output_dir.mkdir(exist_ok=True, parents=True)

        packages = root_dir.iterdir()
        index = []

        for package_dir in packages:
            if not package_dir.is_dir():
                continue
        
            print(f"Entering package: {package_dir.name}")
            metadata = self.build(package_dir, output_dir)
            if not metadata:
                continue

            index.append(vars(metadata))

        with open("packages.json", 'w') as file:
            file.write(json.dumps({ "packages": index }, indent=2))

if __name__ == "__main__":
    builder = PackageBuilder()
    builder.build_all(Path("pkgs"), Path("output"))