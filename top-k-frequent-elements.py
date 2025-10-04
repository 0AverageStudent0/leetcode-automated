# Problem Title: Top K Frequent Elements
# Language: python3
# Status: Accepted
# Runtime: 7
# Memory: 21.2
# Submission URL: https://leetcode.com/submissions/detail/1790654230/

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = defaultdict(int)
        for num in nums:
            count[num] += 1
        heap = []
        for num,cnt in count.items():
            heapq.heappush(heap,[-1 * cnt, num])
        res = []
        while len(res) < k:
            cnt,num = heapq.heappop(heap)
            res.append(num)
        return res