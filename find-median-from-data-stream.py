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
Here is the detailed analysis of the given solution:

---

### Summary
The code implements a data structure `MedianFinder` to efficiently find the median of a stream of integers. It uses two heaps (priority queues):

- `small`: a max heap (implemented by pushing negative values) to store the smaller half of the numbers.
- `large`: a min heap to store the larger half of the numbers.

The `addNum` method inserts a new number into one of the heaps and maintains the size property such that the heaps differ in size by at most 1. The `findMedian` method then returns the median based on the root elements of the two heaps.

---

### Time Complexity
- `addNum`: Each insertion involves pushing to a heap and possibly popping/pushing to maintain balance. Each heap operation (push/pop) is O(log n), where n is the number of elements processed so far. So each call is O(log n).
- `findMedian`: This just accesses the top elements of the heaps and does O(1) work.

Overall:
- `addNum`: O(log n)
- `findMedian`: O(1)

---

### Space Complexity
The two heaps together will store all `n` elements added, so space is O(n).

---

### Strengths
- Uses a well-known and efficient approach using two heaps to maintain running median.
- Balances heaps properly to ensure size difference is at most 1.
- `findMedian` returns result in O(1) time.
- Uses the Python `heapq` module appropriately for min heaps and negation trick for max heap.

---

### Weaknesses
- The code in `addNum` is slightly redundant in heap balancing:
  - The conditional that compares `(-1 * self.small[0] > self.large[0])` and moves an element from small to large is potentially redundant given the balancing steps that follow.
- Could use comments for clarity in difficult parts (e.g., why values are negated).
- The code does balanced checking in three separate if statements, but it may be more efficient or readable to combine balancing logic.
- Lack of input validation (e.g., what if `self.large` is empty at certain points).
- Minor clarity issue: pushing negative values can be confusing without comments.

---

### Suggestions for Improvement
1. **Add comments** explaining the negation trick and balancing logic to improve readability.
2. **Combine balancing conditions** into one place after insertion for clarity and efficiency.
3. **Clarify or simplify the balancing logic** to avoid redundant checks.
4. Import `heapq` explicitly in the code snippet for completeness.
5. Optionally, add type hints to the class attributes and methods for better clarity and static checking.
6. Add edge case handling or assertions to ensure `findMedian` is only called after at least one number is added.

---

### Example Improved Code Snippet (partial)

```python
import heapq

class MedianFinder:

    def __init__(self):
        # Max heap (store negative values) for smaller half
        self.small = []
        # Min heap for larger half
        self.large = []
        
    def addNum(self, num: int) -> None:
        # Add to max heap (remember negation)
        heapq.heappush(self.small, -num)

        # Ensure every number in small <= every number in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance sizes: the heaps can differ at most by 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
        
    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2
```

---

### Summary

| Criteria            | Analysis                         |
|---------------------|---------------------------------|
| **Time Complexity**  | `addNum`: O(log n), `findMedian`: O(1) |
| **Space Complexity** | O(n) (to store all numbers)     |
| **Strengths**        | Efficient median-finding approach with heaps, simple to understand  |
| **Weaknesses**       | Minor redundancy and lack of comments, some logic can be clearer    |
| **Suggestions**      | Add comments, simplify balancing, handle edge cases, import statements |

---

Overall, the code is a solid and standard solution for the problem but can be improved for clarity and minor efficiency improvements.
'''