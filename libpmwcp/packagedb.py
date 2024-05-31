"""Package database."""


class PackageDatabase:
    """Package database class."""

    def __init__(self) -> None:
        """Initialize the package database."""

        # TODO: When available, put the all the packages and its
        #       version in the database here
        self.db: dict[str, list[dict]] = {
            "system-apps/pmwcp": [{'versions': ["1.0.0", "9999"]},
                                  {"current_version": "9999"},
                                  {"depends": []}]
        }

        # TODO: When available, put the installed packages in here
        self.installed_packages: list[str] = [
            "system-apps/pmwcp"
        ]

    def __str__(self) -> str:
        return f"PackageDatabase[Database: {self.db} | Installed packages: {self.installed_packages}]"

    def __repr__(self) -> str:
        return f"self=Self@PackageDatabase PackageDatabase.db={self.db} PackageDatabase.installed_packages={self.installed_packages}"

    def is_package_installed(self, package: str) -> bool:
        """Return a boolean if a package is installed."""

        return package in self.installed_packages

    def return_package_info(self, package: str) -> list[dict]:
        """Return the info for a package."""

        if package not in self.db:
            raise ValueError(f"{package} is not in the database")
        
        return self.db.get(package)  # pyright: ignore

    def package_dependencies(self, package: str) -> list:
        """Return a list of dependencies for a package."""

        package_info: list[dict] = self.return_package_info(package)
        dependencies_dict: dict = package_info[2]
        
        return dependencies_dict.get('depends')  # pyright: ignore

    def using_version(self, package: str) -> str:
        """Get what the version the user is using for a package."""
        
        if not self.is_package_installed(package):
            raise ValueError(f"{package} is not installed")

        package_info: list[dict] = self.return_package_info(package)
        current_version: str = package_info[1].get('current_version')  # pyright: ignore

        return current_version

    def versions_for_package(self, package: str) -> list[str]:
        """Return a list of versions for a package."""

        package_info: list[dict] = self.return_package_info(package)
        all_versions_for_package: dict = package_info[0]

        return [f"{package}={version}" for version in all_versions_for_package.get('versions')]  # pyright: ignore
