import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Yields all real numbers found in the text.
    Numbers are assumed to be separated by spaces.
    """
    pattern = r"\b\d+\.\d+\b"

    for match in re.findall(pattern, text):
        yield float(match)
 