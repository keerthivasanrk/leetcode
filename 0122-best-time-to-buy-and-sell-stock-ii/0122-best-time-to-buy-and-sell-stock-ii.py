class Solution(object):
    def maxProfit(self, prices):
        profit=0
        for i in range(1,len(prices)):
            if prices[i]>prices[i-1]:
                profit+=prices[i]-prices[i-1]
            else:
                continue
        return profit
        """
        :type prices: List[int]
        :rtype: int
        """
        