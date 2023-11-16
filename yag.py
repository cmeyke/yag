from sys import argv
import time
import re
import pyttsx3  # type: ignore
from typing import Iterator


def main(log_file: str):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    output("Welcome to Yet Another Gina.\n", engine)

    with open(log_file, "r") as file:
        for line in file:
            pass
        for line in follow(file):
            if _line := process_new_line(line):
                output(_line, engine)


def follow(file, sleep_sec=0.1) -> Iterator[str]:
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


EXPRESSIONS = [
    "(tells you)(?!((, 'That'll be)|(.*Master)))",
    "You feel yourself starting to appear",
    "You appear",
    "Your skin stops tingling",
]


def process_new_line(line: str) -> str | None:
    """Process a new line of text."""
    for expression in EXPRESSIONS:
        if re.search(expression, line):
            return line.split("] ")[1]
    return None


def output(line: str, engine):
    """Output a line of text on the console and via text-to-speech."""
    print(line, end="")
    engine.say(line)
    engine.runAndWait()


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: yag.py <log_file>")
        exit(1)
    main(argv[1])
