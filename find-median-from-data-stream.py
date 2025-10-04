# Problem Title: Find Median from Data Stream
# Language: python3
# Status: Accepted
# Runtime: 208
# Memory: 40.2
# Submission URL: https://leetcode.com/submissions/detail/1790654417/

# Azure OpenAI Analysis: ### Summary
# Azure OpenAI Analysis: The code implements a data structure `MedianFinder` that can efficiently find the median of a stream of numbers. It uses two heaps:
# Azure OpenAI Analysis: - `small` as a max-heap implemented by pushing negated values into a min-heap.
# Azure OpenAI Analysis: - `large` as a standard min-heap.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: The `addNum` method adds a number to one of the heaps, then rebalances the heaps to ensure their size difference is at most 1. The `findMedian` method returns the median based on the top elements of these heaps.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Time Complexity
# Azure OpenAI Analysis: - **addNum(num)**: O(log n) due to heap insertion and popping operations.
# Azure OpenAI Analysis: - **findMedian()**: O(1), since it only peeks at the top elements of the heaps.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: Overall, for a stream of `n` elements, insertions take O(n log n), and medians can be queried in O(1).
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Space Complexity
# Azure OpenAI Analysis: - O(n), where n is the number of elements added so far. Both heaps together store all elements.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Strengths
# Azure OpenAI Analysis: - **Efficient median finding**: The two-heap approach ensures median retrieval in constant time.
# Azure OpenAI Analysis: - **Balanced heaps**: The code maintains the size invariants carefully for correct median calculation.
# Azure OpenAI Analysis: - **Proper max-heap implementation**: Uses negation to transform Python's min-heap to max-heap for the `small` heap.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Weaknesses
# Azure OpenAI Analysis: - **Unnecessary condition in `addNum`**: The first `if self.small and self.large and (-1 * self.small[0] > self.large[0])` could be replaced by a more standard approach. Normally, insertion should be done by comparing with current median or root of heaps to decide which heap to insert into, rather than always pushing to `small` and then conditionally moving elements.
# Azure OpenAI Analysis: - **Redundant rebalancing code**: The rebalancing logic is duplicated and may be simplified.
# Azure OpenAI Analysis: - **Code readability**: Negations — especially double negations — make the code slightly harder to follow.
# Azure OpenAI Analysis: - **No import statement for `heapq`**: The code snippet is missing `import heapq`.
# Azure OpenAI Analysis: - **No error handling or input validation**: Although typical for LeetCode problems, a production-ready solution might consider these.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Suggestions for Improvement
# Azure OpenAI Analysis: 1. **Add `import heapq`** to ensure the code runs standalone.
# Azure OpenAI Analysis: 2. **Insert elements more thoughtfully**: Instead of always pushing to `small`, decide based on the value of `num` relative to `small[0]` or `large[0]`. For example:
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:    ```python
# Azure OpenAI Analysis:    if not self.small or num <= -self.small[0]:
# Azure OpenAI Analysis:        heapq.heappush(self.small, -num)
# Azure OpenAI Analysis:    else:
# Azure OpenAI Analysis:        heapq.heappush(self.large, num)
# Azure OpenAI Analysis:    ```
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: 3. **Simplify rebalancing** to a single adjustment step, e.g.,
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis:    ```python
# Azure OpenAI Analysis:    # Balance heaps so that their size difference is at most 1
# Azure OpenAI Analysis:    if len(self.small) > len(self.large) + 1:
# Azure OpenAI Analysis:        val = -heapq.heappop(self.small)
# Azure OpenAI Analysis:        heapq.heappush(self.large, val)
# Azure OpenAI Analysis:    elif len(self.large) > len(self.small) + 1:
# Azure OpenAI Analysis:        val = heapq.heappop(self.large)
# Azure OpenAI Analysis:        heapq.heappush(self.small, -val)
# Azure OpenAI Analysis:    ```
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: 4. **Add comments** to clarify logic and heap roles.
# Azure OpenAI Analysis: 5. If frequent median querying is expected, this approach is suitable. Otherwise, consider alternatives (like balanced BSTs) if other operations are needed.
# Azure OpenAI Analysis: 6. **Test edge cases** such as empty data stream, very large numbers, or many duplicates.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Overall, the code is functional and efficient but can be improved for readability, clarity, and maintainability by modifying insertion logic and simplifying rebalancing.**

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