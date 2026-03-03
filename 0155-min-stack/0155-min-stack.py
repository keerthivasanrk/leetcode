class MinStack:

    def __init__(self):
        self.s = deque()

    def push(self, val: int) -> None:
        self.s.append(val)

    def pop(self) -> None:
        return self.s.pop()

    def top(self) -> int:
        return self.s[-1]

    def getMin(self) -> int:
        min = self.s[0]
        for i in self.s:
            if i<min:
                min = i
        return min
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()