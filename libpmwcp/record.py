"""Record packages."""

from .color import Style, Foreground
from .unders import get_under_file, packages_in_under


def record_to_favorites(package: str = 'system-apps/pmwcp') -> None:
    """Record a package to favorites.
    Requires admin privileges."""

    print(
        f"{Style.BOLD}{Foreground.GREEN}>>>{Style.RESET}{Foreground.RESET} Recording '{Foreground.BLUE}{package}{Foreground.RESET}' to favourites..."
    )

    try:
        if package not in packages_in_under('_favorites'):
            with open(get_under_file('_favorites'), 'a') as file:
                file.write(f"{package}\n")
        else:
            print(
                f"{Style.BOLD}{Foreground.MAGENTA}>>>{Style.RESET}{Foreground.RESET} '{Foreground.BLUE}{package}{Foreground.RESET}' is already in favorites; don't need to record."
            )
    except PermissionError as e:
        print(
            f"{Style.BOLD}{Foreground.RED}>>>{Style.RESET}{Foreground.RESET} Couldn't record: PermissionError: {e}"
        )
        exit(1)
