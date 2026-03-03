class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        s = []
        maps = {}

        for i in nums2:
            while s and i>s[-1]:
                small = s.pop()
                maps[small] = i

            s.append(i)
        while s :
            maps[s.pop()] = -1

        return [maps[i]for i in nums1]