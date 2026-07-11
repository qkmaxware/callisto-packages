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

class PackageScripts:
    before_install: str | None
    after_install: str | None

    before_remove: str | None
    after_remove: str | None

class PackageMetadata:
    name: str
    version: str = DEFAULTS.VERSION
    cpu: list[str] = [ DEFAULTS.ARCHITECTURE ]
    description: str = ""
    license: str = DEFAULTS.LICENSE
    author: str = DEFAULTS.AUTHOR

    dependencies: list[str] | None
    provides: list[str] | None
    replaces: list[str] | None

    tags: list[str] | None = []
    scripts: PackageScripts = PackageScripts()
    
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

        metadata.name = data.get("name", metadata.name)
        metadata.cpu = as_list(data.get("cpu", metadata.cpu))
        metadata.version = data.get("version", metadata.version)
        metadata.description = data.get("description", metadata.description)
        metadata.license = data.get("license", metadata.license)
        metadata.author = data.get("author", metadata.author)
        metadata.tags = as_list(data.get("keywords", metadata.tags))

        metadata.scripts.before_install = data.get("scripts", {}).get("before-install", None)
        metadata.scripts.after_install = data.get("scripts", {}).get("after-install", None)
        metadata.scripts.before_remove = data.get("scripts", {}).get("before-remove", None)
        metadata.scripts.after_remove = data.get("scripts", {}).get("after-remove", None)

        metadata.dependencies = list(data.get("dependencies", {}).keys())
        metadata.provides = as_list(data.get("provides"))
        metadata.replaces = as_list(data.get("replaces"))

        return metadata
    

class FPMBuilder:
    _args: list[list[str]]

    def __init__(self, type: str):
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
            print("> Building RPM package: " + shlex.join(args))
            subprocess.run(args, check=True)
            return True
        except:
            print("> ERROR: Failed to build RPM package")
            return False


class PackageBuilder:

    def _generate_files(self, package_dir: Path) -> None:
        # Shell script based generation
        shell_script_path = package_dir / "build.sh"
        if shell_script_path.exists():
            print(f"> Running build.sh script")
            if os.name != "nt":
                subprocess.run(["chmod", "+x", str(shell_script_path)], check=True)

            shell = "bash" if shutil.which("bash") else "sh"
            subprocess.run([shell, str(shell_script_path)], cwd=package_dir, check=True)

        python_script_path = package_dir / "build.py"
        if python_script_path.exists():
            print(f"> Running build.py script")
            subprocess.run([sys.executable, "build.py"], cwd=package_dir, check=True)

    def build(self, package_dir: Path, output_dir: Path) -> PackageMetadata | None:
        # Load package metadata
        metadata: PackageMetadata | None = PackageMetadata.load(package_dir)
        if metadata == None:
            print(f"> SKIPPED: No package metadata")
            return None
        
        # Run build script(s) if they exists
        self._generate_files(package_dir)

        # Check for files
        files_dir = package_dir / "files"
        if not files_dir.is_dir():
            print(f"> SKIPPED: No files to package")
            return None
        
        output_path = output_dir / f"{metadata.name}-{metadata.version}.rpm"

        # Build package for each architecture supported
        built_cps = []
        for arch in metadata.cpu:
            # Configure FPM arguments
            builder = FPMBuilder("rpm")
            builder.source(files_dir)
            builder.output(output_path)
            builder.add_option("-n", metadata.name)
            builder.add_option("-v", metadata.version)
            builder.add_option("-a", arch)
            builder.add_option("--iteration", 1)
            builder.add_option("--rpm-os", "linux")
            builder.add_option("--prefix", "/")
            builder.add_option("--description", metadata.description)
            builder.add_option("--license", metadata.license)
            builder.add_option("--maintainer", metadata.author)
            builder.add_option("--vendor", metadata.author)

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
            if didBuild:
                built_cps.append(arch)

        metadata.cpu = built_cps # overwrite the supported architectures with those that actually built successfully
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

        if not any(output_dir.glob("*.rpm")):
            raise SystemExit("No RPM packages were created")

if __name__ == "__main__":
    builder = PackageBuilder()
    builder.build_all(Path("pkgs"), Path("output/rpm"))