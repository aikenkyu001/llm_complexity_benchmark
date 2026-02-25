# solution.py
from typing import Dict, Optional
import threading

class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, Node] = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.lock = threading.Lock()

    def _remove(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                self._remove(node)
                self._add_to_head(node)
                return node.value
            else:
                return -1

    def put(self, key: int, value: int) -> None:
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                self._remove(node)
            new_node = Node(key, value)
            self._add_to_head(new_node)
            self.cache[key] = new_node
            if len(self.cache) > self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

class Solution:
    def LRUCache(self, capacity: int) -> LRUCache:
        return LRUCache(capacity)