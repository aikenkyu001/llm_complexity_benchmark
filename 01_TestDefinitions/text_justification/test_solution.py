import pytest
from solution import Solution

def test_text_justification_basic():
    solution = Solution()
    words = ["This", "is", "an", "example", "of", "text", "justification."]
    maxWidth = 16
    expected = [
       "This    is    an",
       "example  of text",
       "justification.  "
    ]
    assert solution.fullJustify(words, maxWidth) == expected

def test_text_justification_complex():
    solution = Solution()
    words = ["What","must","be","acknowledgment","shall","be"]
    maxWidth = 16
    expected = [
      "What   must   be",
      "acknowledgment  ",
      "shall be        "
    ]
    assert solution.fullJustify(words, maxWidth) == expected
