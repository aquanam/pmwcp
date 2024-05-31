"""pmwcp instances."""
from . import color
from . import communicate
from . import sync
from . import tools
from argparse import Namespace
from typing import NoReturn


def _pfmake_main() -> int:
    print("Pfmake")

    return 0


def _main(args: Namespace) -> int:
    if not tools.USER_IS_SUDO:
        print(f"{color.Style.BOLD}{color.Foreground.RED}You must run this as administrator!" +
              color.Style.RESET)
              
        # Just in case that the user ran a thread and ID'd it through
        # communicate.new_thread_id()
        communicate.id_list_clear()
        return 1

    if args.sync is not None:
        repos_to_sync: list[str] = args.sync

        print(color.Style.BOLD, end="")

        # TODO: Kind of applies to the last todo
        if "pmwcp" in repos_to_sync and len(repos_to_sync) == 1:
            print("~~ Note: 'pmwcp' is the default if you pass in no repositories.")
        
        if len(repos_to_sync) == 0:
            # TODO: When we are able to sync more repos, append the recently
            #       synced ones.
            repos_to_sync.append('pmwcp')

        return_code: int = 0
        repo_use_count: int = 0
        already_talked_about: list[str] = []

        for repo in repos_to_sync:
            if repo not in already_talked_about:
                repo_use_count = repos_to_sync.count(repo)

                if repo_use_count > 1:
                    print(f"~~ Repository '{repo}' has been repeated {repo_use_count} times.")
                    print(f"   It will be synced {repo_use_count} times, as you've requested.")

                    already_talked_about.append(repo)

        print(color.Style.RESET, end="")

        for repo in repos_to_sync:
            return_code = sync.sync_repo(repo)
            if return_code != 0:
                communicate.id_list_clear()
                return return_code

    communicate.id_list_clear()
    return 0


def new_pfmake_instance() -> NoReturn:
    """Create a new pfmake instance."""
    exit(_pfmake_main())


def new_pmwcp_instance(args: Namespace) -> NoReturn:
    """Create a new pmwcp instance."""
    exit(_main(args))
