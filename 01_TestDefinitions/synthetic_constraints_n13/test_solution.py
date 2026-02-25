import pytest
from solution import Solution

def test_constraints_pass():
    sol = Solution()
    # A large value like 100000 should satisfy simple 'greater than' and 'not equal' rules
    # We use a value that is likely to be a multiple of small primes too
    assert sol.isValid(720720) == True 

def test_constraints_fail():
    sol = Solution()
    assert sol.isValid(-1) == False
