import pytest
from solution import Solution

def test_context_secret():
    sol = Solution()
    # The actual text doesn't matter as much as the LLM's understanding of the NL spec
    assert sol.findSecret("Some long text... secret word is: SIGMA") == "SIGMA"
