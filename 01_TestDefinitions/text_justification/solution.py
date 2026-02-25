class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        def justify_line(words: List[str], total_length: int, is_last_line: bool) -> str:
            if len(words) == 1 or is_last_line:
                # Left-justify the line
                return ' '.join(words).ljust(maxWidth)
            
            num_spaces = maxWidth - total_length
            gaps = len(words) - 1
            spaces_per_gap, extra_spaces = divmod(num_spaces, gaps)
            
            justified_line = []
            for i in range(len(words)):
                justified_line.append(words[i])
                if i < gaps:
                    justified_line.append(' ' * (spaces_per_gap + (1 if i < extra_spaces else 0)))
            
            return ''.join(justified_line)
        
        result = []
        current_line = []
        current_length = 0
        
        for word in words:
            # Check if adding the next word exceeds maxWidth
            if current_length + len(word) + len(current_line) > maxWidth:
                # Justify the current line and add it to the result
                result.append(justify_line(current_line, current_length, False))
                # Reset for the new line
                current_line = []
                current_length = 0
            
            # Add the word to the current line
            current_line.append(word)
            current_length += len(word)
        
        # Justify and add the last line
        if current_line:
            result.append(justify_line(current_line, current_length, True))
        
        return result