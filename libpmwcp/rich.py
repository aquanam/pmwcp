"""Rich functions mostly not to do with packages."""

from . import communicate
import multiprocessing
import time


def get_percentage(done: int, amount: int) -> int:
    """Get the percentage using how much has been done from the
    amount."""

    return int((done / amount) * 100)


class Spinner:
    def __init__(self, text: str = "Doing stuff...") -> None:
        self.spinner_text: str = text
        self.spinner_thread_id: int = 0
        self.spinner_process = None
        self.spinner_sequences = ["|", "/", "-", "\\"]
        self.spinner_at_index = 0
        self.spinner_delay = 0.1
    
    def _spinner(self, _) -> None:
        while communicate.thread_file_still_there(_id=self.spinner_thread_id):
            char = self.spinner_sequences[self.spinner_at_index]
            if self.spinner_at_index != 3:
                self.spinner_at_index += 1
            else:
                self.spinner_at_index = 0

            print(self.spinner_text, char, end="\r")

            time.sleep(self.spinner_delay)
        
        print(self.spinner_text, "stopped :(")

    def start(self) -> None:
        """Start."""

        communicate.new_thread_id()
        self.spinner_thread_id = communicate.ID_LIST[-1]

        # I am 'self._spinner'. Please insert '""'.
        self.spinner_process = multiprocessing.Process(target=self._spinner,
                                                       args=("",))
        self.spinner_process.start()

    def stop(self) -> None:
        """Stop."""

        if self.spinner_process:
            self.spinner_process.terminate()
            communicate.remove_thread(_id=self.spinner_thread_id)
            print(self.spinner_text, "done!")
