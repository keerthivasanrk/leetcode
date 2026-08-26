class Solution(object):
    def trap(self, height):
        lmax=rmax=total=0
        l,r=0,len(height)-1
        while l<r:
            if height[l]<=height[r]:
                if lmax>height[l]:
                    total+=lmax-height[l]
                else:
                    lmax=height[l]
                l+=1
            else:
                if rmax>height[r]:
                    total+=rmax-height[r]
                else:
                    rmax=height[r]
                r-=1
        return total
        """
        :type height: List[int]
        :rtype: int
        """
        