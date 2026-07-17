class Solution(object):
    def groupAnagrams(self, strs):
        d={}
        for s in strs:
            k="".join(sorted(s))
            if k not in d:
                d[k]=[]
            d[k].append(s)
        return list(d.values())
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        