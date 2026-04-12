class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key = lambda x:x[0])
        m = []
        for i in intervals:
            if not m or m[-1][1] <i[0]:
                m.append(i)
            else:
                m[-1][1] = max(m[-1][1],i[1])
        return m
