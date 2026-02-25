import pytest
from solution import Solution

def test_lru_basic():
    lru = Solution().LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)    # evicts key 2
    assert lru.get(2) == -1
    lru.put(4, 4)    # evicts key 1
    assert lru.get(1) == -1
    assert lru.get(3) == 3
    assert lru.get(4) == 4

def test_lru_update():
    lru = Solution().LRUCache(1)
    lru.put(2, 1)
    assert lru.get(2) == 1
    lru.put(2, 2)
    assert lru.get(2) == 2
    lru.put(3, 3)    # evicts key 2
    assert lru.get(2) == -1

def test_lru_complex_sequence():
    lru = Solution().LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.get(1)       # key 1 becomes most recent
    lru.put(3, 3)    # evicts key 2
    assert lru.get(2) == -1
    assert lru.get(3) == 3
