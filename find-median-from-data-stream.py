# Problem Title: Find Median from Data Stream
# Language: python3
# Status: Accepted
# Runtime: 208
# Memory: 40.2
# Submission URL: https://leetcode.com/submissions/detail/1790654417/

# Azure OpenAI Analysis: **Summary:**  
# Azure OpenAI Analysis: This Python solution implements a `MedianFinder` class that maintains a running median from a stream of numbers using two heaps: a max-heap (`small`) for the smaller half of numbers and a min-heap (`large`) for the larger half. The approach balances these two heaps to efficiently provide the median in O(1) time after O(log n) insertion time.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Strengths:**  
# Azure OpenAI Analysis: 1. **Efficient Approach:** The use of two heaps (a max heap via negation in Python, and a min heap) is a classic and optimal way to find the median in a data stream.
# Azure OpenAI Analysis: 2. **Balancing Heaps:** The code correctly balances the heaps so that their sizes differ by at most one, which ensures correct median retrieval.
# Azure OpenAI Analysis: 3. **Correct Median Calculation:** The median is correctly calculated depending on the relative sizes of the heaps.
# Azure OpenAI Analysis: 4. **Readable:** Code is fairly straightforward and easy to understand for those familiar with the two heap method.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Weaknesses:**  
# Azure OpenAI Analysis: 1. **Missing `import heapq`:** The code does not import the `heapq` module, which will cause a `NameError` on usage.
# Azure OpenAI Analysis: 2. **Redundant heap condition check:** In `addNum()`, the first `if` condition checks `if self.small and self.large and ...`. The check for `self.small` is redundant because `small` always receives the new element first before any balancing.
# Azure OpenAI Analysis: 3. **Heap balancing could be streamlined:** The heap balancing code can be slightly simplified by focusing on balance rather than separate conditions; currently code repeats popping and pushing operations.
# Azure OpenAI Analysis: 4. **No edge case handling or input validation:** There’s no explicit input validation (although generally not required on LeetCode).
# Azure OpenAI Analysis: 5. **Code comments and docstrings:** There are no comments or explanations inside methods, which could help readability.
# Azure OpenAI Analysis: 6. **Class attribute naming:** Variable names `small` and `large` are somewhat non-standard; commonly `max_heap` and `min_heap` could be clearer.
# Azure OpenAI Analysis: 7. **Minor inconsistency:** When pushing negated values into `small`, negation is applied twice (`-1 *`), which is fine but can be replaced with `-num` for cleaner code.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Suggestions for Improvement:**  
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: - Add `import heapq` at the top.  
# Azure OpenAI Analysis: - Replace `-1 * num` with `-num` for readability.  
# Azure OpenAI Analysis: - Simplify the heap balancing logic, for example:
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:   ```python
# Azure OpenAI Analysis:   def addNum(self, num: int) -> None:
# Azure OpenAI Analysis:       heapq.heappush(self.small, -num)
# Azure OpenAI Analysis:       # Ensure the max element of small is <= min element of large
# Azure OpenAI Analysis:       if self.large and (-self.small[0] > self.large[0]):
# Azure OpenAI Analysis:           val = -heapq.heappop(self.small)
# Azure OpenAI Analysis:           heapq.heappush(self.large, val)
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:       # Balance sizes
# Azure OpenAI Analysis:       if len(self.small) > len(self.large) + 1:
# Azure OpenAI Analysis:           val = -heapq.heappop(self.small)
# Azure OpenAI Analysis:           heapq.heappush(self.large, val)
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:       elif len(self.large) > len(self.small) + 1:
# Azure OpenAI Analysis:           val = heapq.heappop(self.large)
# Azure OpenAI Analysis:           heapq.heappush(self.small, -val)
# Azure OpenAI Analysis:   ```
# Azure OpenAI Analysis:   
# Azure OpenAI Analysis: - Add a couple of docstrings and comments explaining key steps.  
# Azure OpenAI Analysis: - Rename `small` and `large` to `max_heap` and `min_heap` (optional but helps clarity).  
# Azure OpenAI Analysis: - Consider adding type hints at the class attribute level for readability (Python 3.6+).  
# Azure OpenAI Analysis: - Add minimal unit tests or example usage in comments for demonstration.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Example of slightly improved code snippet:**
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ```python
# Azure OpenAI Analysis: import heapq
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: class MedianFinder:
# Azure OpenAI Analysis:     def __init__(self):
# Azure OpenAI Analysis:         # max_heap stores the smaller half (negated values)
# Azure OpenAI Analysis:         self.max_heap = []
# Azure OpenAI Analysis:         # min_heap stores the larger half
# Azure OpenAI Analysis:         self.min_heap = []
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:     def addNum(self, num: int) -> None:
# Azure OpenAI Analysis:         heapq.heappush(self.max_heap, -num)
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:         # Ensure every number in max_heap <= min_heap
# Azure OpenAI Analysis:         if self.min_heap and (-self.max_heap[0] > self.min_heap[0]):
# Azure OpenAI Analysis:             val = -heapq.heappop(self.max_heap)
# Azure OpenAI Analysis:             heapq.heappush(self.min_heap, val)
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:         # Balance the heaps sizes
# Azure OpenAI Analysis:         if len(self.max_heap) > len(self.min_heap) + 1:
# Azure OpenAI Analysis:             val = -heapq.heappop(self.max_heap)
# Azure OpenAI Analysis:             heapq.heappush(self.min_heap, val)
# Azure OpenAI Analysis:         elif len(self.min_heap) > len(self.max_heap) + 1:
# Azure OpenAI Analysis:             val = heapq.heappop(self.min_heap)
# Azure OpenAI Analysis:             heapq.heappush(self.max_heap, -val)
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:     def findMedian(self) -> float:
# Azure OpenAI Analysis:         if len(self.max_heap) > len(self.min_heap):
# Azure OpenAI Analysis:             return float(-self.max_heap[0])
# Azure OpenAI Analysis:         elif len(self.min_heap) > len(self.max_heap):
# Azure OpenAI Analysis:             return float(self.min_heap[0])
# Azure OpenAI Analysis:         else:
# Azure OpenAI Analysis:             return (-self.max_heap[0] + self.min_heap[0]) / 2
# Azure OpenAI Analysis: ```
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: Overall, the solution correctly implements the median finder with the standard two heap method but can be polished for readability, robustness, and completeness.

class MedianFinder:

    def __init__(self):
        self.small = []
        self.large = []
    def addNum(self, num: int) -> None:
        heapq.heappush(self.small,-1 * num)

        if self.small and self.large and (-1 * self.small[0] > self.large[0]):
            val = -1 * heapq.heappop(self.small)
            heapq.heappush(self.large,val)
        
        if len(self.small) > len(self.large) + 1:
            val = -1 * heapq.heappop(self.small)
            heapq.heappush(self.large,val)
        
        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -1 * val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -1 * self.small[0]
        
        if len(self.large) > len(self.small):
            return self.large[0]
        
        else:
            val = (-1 * self.small[0]) + self.large[0]
            return val/2

# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()