"""Tools for working with unders."""

from .color import Style, Foreground
from .tools import confirm


def is_valid_under(under: str) -> bool:
    """Check if a string is a valid under.
    Here is a list of valid unders:
        _whole
        _beta
        _proprietary
        _favorites"""

    return under in ["_whole", "_beta", "_proprietary", "_favorites"]


def get_under_file(under: str) -> str:
    """Get the under file path."""

    if not is_valid_under(under):
        raise ValueError(f"{under} is not a valid under")

    return f"/var/lib/pmwcp/unders/{under[1:]}"


def packages_in_under(under: str) -> list[str]:
    """Return a list of packages in an under.
    Requires admin privileges."""

    if not is_valid_under(under):
        raise ValueError(f"{under} is not a valid under")

    with open(get_under_file(under), 'r') as file:
        packages: list[str] = [line.rstrip('\n') for line in file.readlines()]

    return packages


def clear_under(under: str) -> None:
    """Clear all the packages from an under.
    NOT recommended! This function will ask you if you are sure.
    Requires admin privileges."""

    if not is_valid_under(under):
        raise ValueError(f"{under} is not a valid under")

    if under == '_whole':
        print(f"{Style.BOLD}{Foreground.BLUE}>>>{Style.RESET}{Foreground.RESET} You may need to resync the repository to restore the _whole under!")

    print(f"{Style.BOLD}{Foreground.RED}>>>{Foreground.RESET} Are you sure you want to clear this under?{Style.RESET}")
    if confirm("Clear under?", switch_colors=True):
        try:
            with open(get_under_file(under), 'w') as _:
                pass
            
            print(f"{Style.BOLD}{Foreground.GREEN}>>>{Style.RESET}{Foreground.RESET} Under cleared.")
        except PermissionError as e:
            print(
                f"{Style.BOLD}{Foreground.RED}>>>{Style.RESET}{Foreground.RESET} Couldn't clear under: PermissionError: {e}"
            )
            exit(1)
