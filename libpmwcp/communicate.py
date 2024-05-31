"""Communicate with threads."""

import os
import re

CURRENT_ID: int = 0
ID_LIST: list[int] = []
ID_GAPS_TO_FILL: list[int] = []


def new_thread_id(name: str = "No Name", max: int = 1000) -> None:
    """Create a new thread ID."""
    global ID_LIST, CURRENT_ID, ID_GAPS_TO_FILL

    if len(ID_LIST) == max:
        raise RuntimeError("Maximum ID limit has reached")

    if len(ID_GAPS_TO_FILL) == 0:
        new_id = CURRENT_ID + 1
        CURRENT_ID = new_id
    else:
        new_id = ID_GAPS_TO_FILL[0]
        CURRENT_ID = new_id
        ID_GAPS_TO_FILL.pop(0)

    ID_LIST.append(CURRENT_ID)
    open(f'/var/log/pmwcp/threads/private_thread-{new_id}.running.log', 'x')

    with open(f'/var/log/pmwcp/threads/private_thread-{new_id}.running.log', 'w') as file:
        file.write("This is a private file which should not be editted and definitely not\n" +
                   "to be deleted. This will be deleted after the thread is finished, so do\n" +
                   "not worry!" +
                   "------------------------------------------------------------------------" +
                   f"id={new_id}" +
                   f"name={name}")


def get_id_from_name(name: str = "No Name") -> list[int]:
    """Get (a list of) IDs from a thread name."""

    THREAD_FILE_LISTS: list[str] = []

    for _id in ID_LIST:
        THREAD_FILE_LISTS.append(f"/var/log/pmwcp/threads/private_thread-{_id}.running.log")

    FOUND_IDS: list[int] = []

    for thrd_file in THREAD_FILE_LISTS:
        with open(thrd_file, "r") as file:
            this_thrd_contents: str = file.read()

        this_name_match = re.match(r"name=(.*)", this_thrd_contents)
        if this_name_match:
            this_thrd_name: str = this_name_match.group(1)
            if this_thrd_name != name:
                continue
        else:
            raise RuntimeError("Couldn't get thread name")

        this_id_match = re.match(r"id=(.*)", this_thrd_contents)
        if this_id_match:
            this_thrd_id: int = int(this_id_match.group(1))
            FOUND_IDS.append(this_thrd_id)
        else:
            raise RuntimeError("Couldn't get thread ID")

    return FOUND_IDS


def get_name_from_id(_id: int = 0) -> str:
    """Get a name from an ID."""

    with open(f"/var/log/pmwcp/threads/private_thread-{_id}.running.log", "r") as file:
        thrd_contents: str = file.read()

    name_match = re.match(r"name=(.*)", thrd_contents)
    if name_match:
        thrd_name: str = name_match.group(1)
    else:
        raise RuntimeError("Couldn't get thread name")

    return thrd_name


def remove_thread(_id: int = 0) -> None:
    """Remove the thread with it's ID."""

    global ID_LIST, ID_GAPS_TO_FILL

    if _id in ID_LIST:
        os.remove(f'/var/log/pmwcp/threads/private_thread-{_id}.running.log')
    else:
        raise ValueError(f"Thread ID {_id} isn't on the available ID list")
        
    ID_LIST.remove(_id)
    ID_GAPS_TO_FILL.append(_id)


def id_list_clear() -> None:
    """Clear the (current) ID list. (Do this if you know what you're
    doing, and make sure the threads are stopped!)"""

    global ID_LIST, ID_GAPS_TO_FILL
    
    for _id in ID_LIST:
        os.remove(f'/var/log/pmwcp/threads/private_thread-{_id}.running.log')

    ID_LIST = []
    ID_GAPS_TO_FILL = []


def thread_file_still_there(_id: int = 0) -> bool:
    """Return a boolean if a thread file still exists."""

    return os.path.exists(f'/var/log/pmwcp/threads/private_thread-{_id}.running.log')
