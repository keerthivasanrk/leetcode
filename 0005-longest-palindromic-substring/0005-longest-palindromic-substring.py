class Solution(object):
    def longestPalindrome(self, s):
        longest=""
        for i in range(len(s)):
            l,r=i,i
            while l>=0 and r<len(s) and s[l]==s[r]:
                if (r-l+1) > len(longest):
                    longest=s[l:r+1]
                l-=1
                r+=1
            
            l,r=i,i+1
            while l>=0 and r<len(s) and s[l]==s[r]:
                if (r-l+1) > len(longest):
                    longest=s[l:r+1]
                l-=1
                r+=1
        return longest
                                    
        """
        :type s: str
        :rtype: str
        """
        