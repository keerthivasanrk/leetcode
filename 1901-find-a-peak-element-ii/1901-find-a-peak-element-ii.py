class Solution:
    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:
        mi,n = len(mat), len(mat[0])
        l,h = 0,n-1
        while l<=h:
            m = (l+h)//2
            mr = 0
            for r in range(mi):
                if mat[r][m]>mat[mr][m]:
                    mr = r
            lv = mat[mr][m-1] if m-1>=0 else -1
            rv = mat[mr][m+1] if m+1<n else -1
            cr = mat[mr][m]

            if cr>lv and cr>rv :
                return [mr,m]
            elif cr<lv:
                h = m-1
            else:
                l = m+1
        return []