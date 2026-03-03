class MinStack:

    def __init__(self):
        self.s = deque()
        self.m = deque()

    def push(self, val: int) -> None:
        self.s.append(val)
        if not self.m or val<= self.m[-1]:
            self.m.append(val)

    def pop(self) -> None:
        if self.s[-1]==self.m[-1]:
            self.m.pop()
        return self.s.pop()


    def top(self) -> int:
        return self.s[-1]

    def getMin(self) -> int:
        return self.m[-1]
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()