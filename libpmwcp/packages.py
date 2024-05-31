from .unders import get_under_file
from .color import Style, Foreground

WHOLE_UNDER_FILE: str = get_under_file("_whole")
INSTALLED_PACKAGES_PATH: str = "/var/lib/pmwcp/installed_packages"


def installed_packages() -> list[str]:
    """Return a list of packages that are installed."""

    with open(INSTALLED_PACKAGES_PATH, 'r') as file:
        packages_installed: list[str] = [
            line.rstrip('\n') for line in file.readlines()
        ]

    return packages_installed


def add_package(package: str) -> None:
    """Add package to the installed package list."""

    print(
        f"{Style.BOLD}{Foreground.GREEN}>>>{Style.RESET}{Foreground.RESET} Adding package '{Foreground.BLUE}{package}{Foreground.RESET}' to the installed package list..."
    )

    if package in installed_packages():
        print(
            f"{Style.BOLD}{Foreground.MAGENTA}>>>{Style.RESET}{Foreground.RESET} '{Foreground.BLUE}{package}{Foreground.RESET}' is already in the list; don't need to add package."
        )

        return
    
    try:
        with open(INSTALLED_PACKAGES_PATH, "a") as file:
            file.write(f"{package}\n")
    except PermissionError as e:
        print(
            f"{Style.BOLD}{Foreground.RED}>>>{Style.RESET}{Foreground.RESET} Couldn't add package: PermissionError: {e}"
        )
        exit(1)
