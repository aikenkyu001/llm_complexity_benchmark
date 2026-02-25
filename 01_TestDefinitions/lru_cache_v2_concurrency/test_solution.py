import pytest
from solution import Solution

def test_lru_v2_basic():
    lru = Solution().LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)
    assert lru.get(2) == -1

def test_lru_v2_concurrency_logic():
    # Test if basic logic still holds with locks added
    lru = Solution().LRUCache(1)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == -1
    assert lru.get(2) == 2
