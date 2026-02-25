# Task: lru_cache_v2_concurrency
# Interface:
Class: Solution
Method: LRUCache(self)

Implement an LRU Cache that is thread-safe. While the main benchmark is single-threaded, the implementation must use synchronization primitives (like threading.Lock) to ensure internal consistency as if it were in a concurrent environment.
- LRUCache(capacity)
- get(key)
- put(key, value)
Constraints:
- O(1) average time complexity for both get and put.
- Use a Lock for every state-modifying operation.
- Do not use OrderedDict.
