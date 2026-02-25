class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Implement regular expression matching with support for '.' and '*'.
        
        :param s: Input string to match.
        :param p: Pattern string containing '.', '*', and lowercase English letters.
        :return: True if the input string matches the pattern, otherwise False.
        """
        # Create a DP table where dp[i][j] is True if s[:i] matches p[:j]
        dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
        
        # Base case: empty string matches empty pattern
        dp[0][0] = True
        
        # Handle patterns like a*, a*b*, a*b*c* etc.
        for j in range(2, len(p) + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]
        
        # Fill the DP table
        for i in range(1, len(s) + 1):
            for j in range(1, len(p) + 1):
                if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                elif p[j - 1] == '*':
                    # '*' can match zero or more of the preceding element
                    dp[i][j] = dp[i][j - 2]  # Match zero elements
                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                        dp[i][j] |= dp[i - 1][j]  # Match one or more elements
        
        return dp[len(s)][len(p)]