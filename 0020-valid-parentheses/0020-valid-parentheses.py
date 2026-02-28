class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {
            ')': '(',
            ']': '[',
            '}': '{'
        }

        for char in s:
            if char in mapping:
                if not stack or stack[-1]!=mapping[char]:
                    return False
                else:
                    stack.pop()
            else:
                stack.append(char)
        return not stack
            