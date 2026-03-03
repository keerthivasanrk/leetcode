class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0]*n
        s = [] 
        for i in range(n):
            while s and temperatures[i]> temperatures[s[-1]]:
                index = s.pop()
                ans[index]= i - index
                
            s.append(i)
        return ans