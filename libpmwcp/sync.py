from . import color
from .rich import Spinner
from .tools import sort_arr
from typing import Any
import json
import re
import requests

CACHED_MIRROR_LINKS: dict | None = None


def _compact_get(url: str) -> requests.Response | int:
    response: requests.Response = requests.get(
        url=url
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        return response.status_code

    return response


def sync_repo(repo: str) -> int:
    """Sync a repository."""
    global CACHED_MIRROR_LINKS

    print(f"{color.Style.BOLD}{color.Foreground.GREEN}* {color.Style.RESET}" +
          f"Syncing repository '{color.Foreground.BLUE}{repo}{color.Foreground.RESET}'...")
    
    if CACHED_MIRROR_LINKS is not None:
        print(">>> Using cached mirror links")
        mirror_links = CACHED_MIRROR_LINKS
    else:
        spinner = Spinner(">>> Getting mirror links...")
        spinner.start()

        res = _compact_get("https://aquanam.github.io/pmwcp-mirror/mirrors/mirror_links.jsonc")

        if type(res) is int:
            spinner.stop()
            print(f"Error: Returned status code: {res}")
            return 1

        # Note:
        #     Since this is a jsonc file, we need to subtract
        #     the comments from it so json.loads doesn't return
        #     any errors.
        mirror_links_content: str = re.sub(
            r'//.*',
            '',
            res.text  # pyright: ignore[reportAttributeAccessIssue]
        )
        mirror_links: Any = json.loads(mirror_links_content)
        CACHED_MIRROR_LINKS = mirror_links

        spinner.stop()

    if repo in mirror_links.get('mirrors'):
        print(f">>> Mirror is {color.Foreground.GREEN}valid" +
              f"{color.Foreground.RESET}!")
    else:
        print(f">>> Mirror is {color.Foreground.RED}not valid" +
              f"{color.Foreground.RESET}!")
        print(f"{color.Style.BOLD}Not syncing this mirror, since it is not valid." +
              color.Style.RESET)
            
        return 0

    this_mirror_link: str = mirror_links.get('mirrors').get(repo)
    if this_mirror_link == '.':
        this_mirror_link = "https://aquanam.github.io/pmwcp-mirror/"

    print(f">>> Syncing from link '{color.Foreground.MAGENTA}" +
          f"{this_mirror_link}{color.Foreground.RESET}'")

    spinner = Spinner(">>> Getting timestamp list...")
    spinner.start()

    this_timestamp_link: str = f"{this_mirror_link}this/timestamps/all.json"
    res = _compact_get(this_timestamp_link)
    if type(res) is int:
            spinner.stop()
            print(f"Error: Returned status code: {res}")
            return 1

    all_timestamps: Any = json.loads(res.text)  # pyright: ignore[reportAttributeAccessIssue]
    timestamps: list = all_timestamps.get("timestamps")

    dates: list[int] = []
    for this_timestamp in timestamps:
        dates.append(int(this_timestamp[10:15]))

    sorted_dates = sort_arr(dates)
    chosen_timestamp = f"timestamp-{sorted_dates[-1]}.tstmp.zip"  # The biggest element will always be last

    spinner.stop()

    print(f">>> Chosen timestamp: {color.Foreground.MAGENTA}{chosen_timestamp}{color.Foreground.RESET}")

    return 0
