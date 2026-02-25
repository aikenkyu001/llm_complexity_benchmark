# solution.py
from typing import List, Optional, Dict, Set, Any
import threading

class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache_v2_concurrency:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.lock = threading.Lock()

    def get(self, key: int) -> int:
        with self.lock:
            if key not in self.cache:
                return -1
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value

    def put(self, key: int, value: int) -> None:
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                node.value = value
                self._remove(node)
                self._add(node)
            else:
                if len(self.cache) == self.capacity:
                    node_to_remove = self.tail.prev
                    self._remove(node_to_remove)
                    del self.cache[node_to_remove.key]
                new_node = Node(key, value)
                self.cache[key] = new_node
                self._add(new_node)

    def _remove(self, node: Node) -> None:
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def _add(self, node: Node) -> None:
        prev = self.head
        next = self.head.next
        prev.next = node
        node.prev = prev
        node.next = next
        next.prev = node

# The Solution class must remain the primary interface for the tests
class Solution:
    def LRUCache_v2_concurrency(self, capacity: int) -> LRUCache_v2_concurrency:
        return LRUCache_v2_concurrency(capacity)