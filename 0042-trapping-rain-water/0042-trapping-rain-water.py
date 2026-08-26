class Solution(object):
    def trap(self, height):
        L=0
        R=len(height)-1
        leftmax=height[L]
        rightmax=height[R]
        total_water=0
        
        while L<R:
            if leftmax<rightmax:
                
                L += 1
                leftmax = max(leftmax, height[L])
                total_water+=leftmax - height[L]
            else:
                
                R -= 1
                rightmax = max(rightmax, height[R])
                total_water+=rightmax -height[R]
        return total_water
            
        """
        :type height: List[int]
        :rtype: int
        """
        