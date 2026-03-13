class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        c = 0
        maxi = 0
        v = {'a', 'e', 'i', 'o','u'}
        for i in range (len(s)):
            if s[i] in v:
                c+=1
            if i>=k and s[i-k]in v:
                c-=1
            maxi = max(maxi,c)
        return maxi



        
            
