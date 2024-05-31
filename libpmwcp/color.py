"""ANSI color codes for coloring/styling terminal output."""

from dataclasses import dataclass


@dataclass
class Style:
    """ANSI color codes for styling terminal output."""
    RESET: str = "\033[0m"
    BOLD: str = "\033[1m"
    DIM: str = "\033[2m"
    UNDERLINE: str = "\033[4m"
    INVERT: str = "\033[7m"
    STRIKETHROUGH: str = "\033[9m"


@dataclass
class Foreground:
    """ANSI color codes for coloring the foreground of the terminal output."""
    BLACK: str = "\033[30m"
    RED: str = "\033[31m"
    GREEN: str = "\033[32m"
    YELLOW: str = "\033[33m"
    BLUE: str = "\033[34m"
    MAGENTA: str = "\033[35m"
    CYAN: str = "\033[36m"
    WHITE: str = "\033[37m"
    RESET: str = "\033[39m"


@dataclass
class Background:
    """ANSI color codes for coloring the background of the terminal output."""
    BLACK: str = "\033[40m"
    RED: str = "\033[41m"
    GREEN: str = "\033[42m"
    YELLOW: str = "\033[43m"
    BLUE: str = "\033[44m"
    MAGENTA: str = "\033[45m"
    CYAN: str = "\033[46m"
    WHITE: str = "\033[47m"
    RESET: str = "\033[49m"
