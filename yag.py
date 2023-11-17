import signal
from sys import argv
import time
import re
import pyttsx3  # type: ignore
from typing import Iterator

from expressions import EXPRESSIONS, SPLITTER


class yag:
    def __init__(self, log_file: str):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[1].id)
        self.log_file = log_file

    def run(self):
        self.output("Welcome to Yet Another Gina.\n")

        signal.signal(signal.SIGINT, self.signal_handler)

        with open(self.log_file, "r") as file:
            for line in file:
                pass
            for line in self.follow(file):
                if _line := self.process_new_line(line):
                    self.output(_line)

    def signal_handler(self, signal, frame):
        self.output("Goodby")
        exit(0)

    def output(self, line: str):
        print(line, end="")
        self.engine.say(line)
        self.engine.runAndWait()

    def follow(self, file, sleep_sec=0.1) -> Iterator[str]:
        """Yield each line from a file as they are written.
        `sleep_sec` is the time to sleep after empty reads."""
        line = ""
        while True:
            if tmp := file.readline():
                line += tmp
                if line.endswith("\n"):
                    yield line
                    line = ""
            elif sleep_sec:
                time.sleep(sleep_sec)

    def process_new_line(self, line: str) -> str | None:
        """Process a new line of text."""
        for expression in EXPRESSIONS:
            if re.search(expression, line):
                return line.split(SPLITTER)[1]
        return None


def main():
    if len(argv) != 2:
        print("Usage: yag.py <log_file>")
        exit(1)
    yag(argv[1]).run()


if __name__ == "__main__":
    main()
