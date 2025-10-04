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
Here is the analysis of the provided solution for the "Find Median from Data Stream" problem:

---

### Summary
The given solution uses two heaps to efficiently maintain the median of a stream of numbers:
- `small` is a max-heap (implemented using a min heap by pushing negative values).
- `large` is a min-heap.

The idea:
- The `small` heap stores the smaller half of the numbers.
- The `large` heap stores the larger half of the numbers.
- The heaps are balanced such that their size difference is at most 1.
- The median is derived either from the root of one of the heaps (if odd length) or the average of both roots (if even length).

---

### Time Complexity
- `addNum()`:
  - `heapq.heappush` and `heapq.heappop` operations take O(log n) time,
  - Since each `addNum` involves a constant number of heap operations,
  - Overall: **O(log n)** per insertion.
  
- `findMedian()`:
  - The median is retrieved by accessing the top elements of the heaps, which is O(1),
  - Overall: **O(1)** for each median query.

---

### Space Complexity
- The space used by the two heaps is proportional to the number of elements inserted,
- Hence, total space complexity is **O(n)** for storing all elements in the two heaps.

---

### Strengths
- Uses the well-known two-heap approach that balances time and space efficiency.
- Efficient median retrieval with O(1) time complexity.
- Balances heaps correctly after each insertion maintaining invariants needed to find the median.
- Implements a max-heap using negatives in Python’s min-heap cleanly.

---

### Weaknesses
- The balancing condition `if self.small and self.large and (-1 * self.small[0] > self.large[0])` ensures order but does not guarantee rebalancing at all times which might be unnecessary or could be simplified.
- The rebalancing code occurs twice with similar logic but could be made more concise.
- Pushing negative values can sometimes be confusing for readability.
- There is some redundancy in heap size balancing steps which might cause inefficiencies or confusion.
- The comments and code formatting can be improved for clarity.
- `heapq` is used but not imported in the provided snippet; it is assumed to be imported outside the given code.

---

### Suggestions for Improvement
1. **Code clarity and readability**:
   - Add import statement for `heapq` explicitly.
   - Add comments explaining the purpose of each step, especially the balancing logic.
   - Avoid repeating similar balancing code by combining the logic into one rebalance function.

2. **Simplify balancing logic**:
   - After pushing into `small`, always push the largest element from `small` to `large` if it violates the order of max in `small` and min in `large`.
   - Then rebalance by sizes in a clean loop or simple if-else.

3. **Use clearer variable names**:
   - Instead of `small` and `large`, names like `max_heap` and `min_heap` could be more descriptive.

---

### Example improved balancing approach (conceptual):

```python
def addNum(self, num: int) -> None:
    heapq.heappush(self.small, -num)
    # Move the largest from small to large to maintain order
    if self.small and self.large and (-self.small[0] > self.large[0]):
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    
    # Rebalance sizes
    if len(self.small) > len(self.large) + 1:
        heapq.heappush(self.large, -heapq.heappop(self.small))
    elif len(self.large) > len(self.small) + 1:
        heapq.heappush(self.small, -heapq.heappop(self.large))
```

Alternatively, simplify to the well-known pattern:
- Push new number to `small`.
- Pop max from `small` and push to `large`.
- If sizes get unbalanced, move elements accordingly.

---

**In summary, this solution is sound and efficient but could benefit from cleaner, more readable balancing logic and added comments.**

---

Feel free to ask if you want me to rewrite the code following these improvements!
'''