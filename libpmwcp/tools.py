"""Tools needed for this library."""

from . import communicate
from .color import Style, Foreground
from io import StringIO
from typing import NoReturn
import os
import re
import sys
import traceback

USER_IS_SUDO: bool = os.geteuid() == 0


def sort_arr(arr: list) -> list:
    """Performs a dual-pivot quicksort."""
    def _partition(arr, low, high):
        if arr[low] > arr[high]:
            arr[low], arr[high] = arr[high], arr[low]
        pivot_one = arr[low]
        pivot_two = arr[high]

        i = low + 1
        lt = low + 1
        gt = high - 1

        while i <= gt:
            if arr[i] < pivot_one:
                arr[i], arr[lt] = arr[lt], arr[i]
                lt += 1
            elif arr[i] > pivot_two:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
                i -= 1
            i += 1
        
        lt -= 1
        gt += 1
        arr[low], arr[lt] = arr[lt], arr[low]
        arr[high], arr[gt] = arr[gt], arr[high]

        return lt, gt
        
    
    def _dp_qs(arr, low, high):
        if low < high:
            p, q = _partition(arr, low, high)

            _dp_qs(arr, low, p - 1)
            _dp_qs(arr, p + 1, q - 1)
            _dp_qs(arr, q + 1, high)

    
    PAST_RECURSION_LIMIT: int = sys.getrecursionlimit()

    low = 0
    high = len(arr) - 1

    if high + 1 > PAST_RECURSION_LIMIT:  # This is important
        sys.setrecursionlimit(high + 1)

    _dp_qs(arr, low, high)

    sys.setrecursionlimit(PAST_RECURSION_LIMIT)

    return arr


def exception_handler(exc_type, exc_value, exc_traceback) -> NoReturn:
    """Exception handler."""
    type_class_string = f"{exc_type}"
    type_class_match = re.match(r"<class '((\w|.)+)'>", type_class_string)

    trcbck_obj_string = f"{exc_traceback}"
    trcbck_match = re.match(r"<traceback object at (\w+)>", trcbck_obj_string)
    
    print("Exception occurred! Here are some details:")

    if type_class_match:
        exctype_str = type_class_match.group(1)
    else:
        exctype_str = "<match_didnt_return>"
    print(f"\t- Exception type: {exctype_str}")
    print(f"\t- Exception value: {exc_value}")
    if trcbck_match:
        trcbck_obj_is_at = trcbck_match.group(1)
    else:
        trcbck_obj_is_at = "<match_didnt_return>"
    print(f"\t- Traceback object is at {trcbck_obj_is_at}")
    print("\t- Exception that would be printed out:")

    with StringIO() as tb_buffer:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=tb_buffer)
        tb_buffer.seek(0)
        intended_tb: str = "\n".join(["\t\t- " + line for line in tb_buffer.getvalue().strip().split("\n")])
        print(intended_tb)
        
    print("If you have not modified the source code, please report a bug.")
    communicate.id_list_clear()
    exit(1)


def confirm(to_ask: str, switch_colors: bool = False) -> bool:
    """Return a boolean if the user confirmed."""

    while True:
        if not switch_colors:
            answer: str = input(
                f"{Style.BOLD}{Foreground.WHITE}{to_ask} " +
                f"[{Foreground.GREEN}y{Foreground.MAGENTA}/{Foreground.RED}n{Foreground.WHITE}]"
                + f"{Foreground.RESET}{Style.RESET} ")
        else:
            answer: str = input(
                f"{Style.BOLD}{Foreground.WHITE}{to_ask} " +
                f"[{Foreground.RED}y{Foreground.MAGENTA}/{Foreground.GREEN}n{Foreground.WHITE}]"
                + f"{Foreground.RESET}{Style.RESET} ")

        if answer.lower() in ["y", "yes", ""]:
            return True
        elif answer.lower() in ["n", "no"]:
            return False
        else:
            print(
                f"{Style.BOLD}{Foreground.BLUE}I didn't recognize that. Please try again.{Style.RESET}{Foreground.RESET}"
            )
