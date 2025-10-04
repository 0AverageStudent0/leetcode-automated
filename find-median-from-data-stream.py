# Problem Title: Find Median from Data Stream
# Language: python3
# Status: Accepted
# Runtime: 208
# Memory: 40.2
# Submission URL: https://leetcode.com/submissions/detail/1790654417/

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

# Azure OpenAI Analysis
'''
Here's the detailed analysis of the provided code for the "Find Median from Data Stream" problem:

---

### Summary

The code implements a data structure `MedianFinder` that supports two operations: adding a number from a stream and finding the median of all added numbers efficiently. It uses two heaps:

- `small` is a max-heap represented by a min-heap with negated values (to store the smaller half of the numbers).
- `large` is a min-heap storing the larger half of the numbers.

When a new number is added, it's initially pushed onto the `small` heap (after negation). The code then rebalances the heaps to maintain the order invariant (`max(small) <= min(large)`) and size property (heaps should not differ in size by more than one). The `findMedian` method then returns the median, which depends on the relative sizes of the two heaps.

---

### Time Complexity

- **`addNum(num)`**:  
  Each insertion involves pushing to one heap (`O(log n)`) and potentially popping and pushing between heaps once or twice (each `O(log n)`). Therefore, the overall time complexity for each addition is:  
  **O(log n)**

- **`findMedian()`**:  
  Accessing the top elements of heaps is `O(1)`, so finding the median is:  
  **O(1)**

---

### Space Complexity

- The two heaps together store all the numbers seen so far  
- Hence, space complexity is:  
  **O(n)**, where n is the number of elements inserted.

---

### Strengths

- **Efficient median finding:** Using two heaps is a classic and optimal approach for this problem, supporting median retrieval in constant time.
- **Rebalancing logic:** The code correctly balances the two heaps to keep their size difference at most one.
- **Code correctness:** Seems to correctly handle cases where one heap can have one more element than the other.

---

### Weaknesses

- **Redundant checks in `addNum`:**  
  The first conditional block checks `if self.small and self.large and (-1 * self.small[0] > self.large[0])`. This makes sense, but since `self.small` always has one element after the push and `self.large` might be empty, it can sometimes skip needing to balance. However, the size rebalancing logic can handle most cases, so this condition is slightly redundant and can be optimized.
  
- **No `import heapq`:**  
  The code snippet does not import the `heapq` module, which is necessary for using `heappush` and `heappop`. Without this, the code will throw an error.

- **Naming improvements:**  
  Variable names like `small` and `large` could be made clearer, e.g., `max_heap` and `min_heap` or `left` and `right`.

- **Potential minor inefficiency in rebalancing:**  
  This code pushes every new element directly onto `small` before adjusting. A more typical approach pushes the new element to the heap it belongs to based on comparison with the current median, reducing rebalancing operations.

- **No comments:**  
  Lack of comments makes the code less readable for those unfamiliar with this approach.

---

### Suggestions for Improvement

1. **Add the missing import:**  
   ```python
   import heapq
   ```

2. **Push into the appropriate heap directly:**  
   Modify `addNum` to decide where to push the new number first, reducing unnecessary moves. For example:

   ```python
   if not self.small or num <= -self.small[0]:
       heapq.heappush(self.small, -num)
   else:
       heapq.heappush(self.large, num)
   ```

3. **Simplify rebalancing:**  
   After pushing, just check if heaps need to be balanced by size difference and rebalance once per insertion.

4. **Add comments and clearer variable names:**  
   For example, rename `small` to `max_heap` and `large` to `min_heap` and add explanations.

5. **Add guard in `findMedian` for empty case:**  
   Though not required by the problem constraints, consider raising an error or returning a sentinel value if no numbers have been added before `findMedian` is called.

---

### Example optimized snippet for `addNum`

```python
def addNum(self, num: int) -> None:
    # Push into max_heap (small) or min_heap (large)
    if not self.small or num <= -self.small[0]:
        heapq.heappush(self.small, -num)
    else:
        heapq.heappush(self.large, num)
    
    # Balance sizes
    if len(self.small) > len(self.large) + 1:
        heapq.heappush(self.large, -heapq.heappop(self.small))
    elif len(self.large) > len(self.small) + 1:
        heapq.heappush(self.small, -heapq.heappop(self.large))
```

---

**In summary:** The original code is mostly correct and efficient for the problem, but can be improved in clarity, robustness, and small logical optimizations.
'''