class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m = len(matrix)
        n = len(matrix[0])
        zr = [False]*m
        zc = [False]*n
        for r in range(m):
            for c in range(n):
                if matrix[r][c]==0:
                    zr[r]=True
                    zc[c]=True
        for r in range(m):
            for c in range(n):
                if zr[r] or zc[c] == True:
                    matrix[r][c]=0