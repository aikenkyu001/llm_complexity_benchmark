# Task: Autocomplete System
# Interface:
Class: Solution
Method: initAutocomplete(self, sentences: List[str], times: List[int]) -> None
Method: query(self, prefix: str) -> List[str]

Design an autocomplete system that returns the top 3 historical sentences that start with the same prefix.
The system is initialized with a list of sentences and their respective search counts (times).
- `initAutocomplete(sentences, times)`: Initializes the system.
- `query(prefix)`: Returns the top 3 hot sentences starting with the prefix. If multiple sentences have the same frequency, return them in lexicographical order.

# Implementation Hint:
Use a Trie to store sentences. Each node in the Trie can store the historical sentences and their frequencies passing through that node.
For the `query` method, navigate to the node representing the prefix and retrieve the top results.

Constraints:
- Sentences contain only lowercase English letters and spaces.
- Up to 100 historical sentences.
