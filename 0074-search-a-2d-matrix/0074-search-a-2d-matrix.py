class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        m,n = len(matrix),len(matrix[0])
        l,r = 0 , (m*n)-1

        while l<=r:
            mid = (l+r)//2
            mv = matrix[mid//n][mid%n]
            if target == mv:
                return True
            elif mv<target:
                l=mid+1
            else:
                r= mid-1
        return False