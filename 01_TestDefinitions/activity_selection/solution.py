# solution.py
from typing import List, Tuple

class Solution:
    def maxActivities(self, activities: List[Tuple[int, int]]) -> int:
        """
        Select the maximum number of non-overlapping activities that can be performed by a single person.

        :param activities: A list of tuples where each tuple represents an activity with a start and end time.
        :return: The maximum number of activities that can be selected.
        """
        if not activities:
            return 0

        # Sort activities based on their finish times
        activities.sort(key=lambda x: x[1])

        # Initialize the count of activities and the end time of the last selected activity
        max_count = 1
        end_time = activities[0][1]

        # Iterate through the sorted activities
        for start, finish in activities[1:]:
            if start >= end_time:
                max_count += 1
                end_time = finish

        return max_count