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

### Summary of the code

The solution maintains two heaps:
- `small`: a max-heap simulated using Python's `heapq` by pushing negative values (to store the smaller half of the numbers)
- `large`: a min-heap storing the larger half of the numbers

When a new number is added via `addNum`:
1. It is pushed onto the `small` heap (as a negative value).
2. The code ensures the max of the smaller half is not greater than the min of the larger half by swapping elements between heaps if necessary.
3. It balances the heaps so that their sizes differ by at most 1.

When `findMedian` is called:
- If one heap is larger, the median is the root element of that heap.
- If they are equal in size, the median is the average of the two root elements.

This approach allows efficient retrieval of median numbers from a data stream.

---

### Time complexity

- `addNum(num)`:
  - Each insertion into a heap is O(log n).
  - There can be up to 2 heap operations per call (push followed by potential pop/push to maintain balance).
  - **Overall time complexity:** O(log n) per insertion.

- `findMedian()`:
  - Access to the root of the heaps is O(1).
  - **Overall time complexity:** O(1).

---

### Space complexity

- Two heaps store all the numbers added so far.
- **Overall space complexity:** O(n), where n is the number of elements added.

---

### Strengths

- Efficient median retrieval in O(1) time.
- Balanced data structure keeps insertion in O(log n).
- Uses heaps effectively to maintain two halves of the data.
- Correct handling of max-heap in Python using negative values.

---

### Weaknesses

- The code pushes every new number directly to `small` first, which might be a little unintuitive. Usually, you decide which heap to push to first based on the new number to reduce rebalancing.
- The conditional checks could be combined or clarified to avoid redundant comparisons.
- Lack of inline comments or docstrings reduces readability.
- Minor inefficiencies in heap balancing:
  - The third if condition can be simplified with an `elif` since only one of these length conditions will hold true after insertion.
- No explicit import statement for `heapq`. While it's known that this is needed, adding the import increases clarity for standalone code.

---

### Suggestions for improvement

1. **Add `import heapq`:** Make the code runnable independently.
2. **Reconsider insertion logic:** 
   - Insert the number into `large` or `small` based on comparison with existing root elements to reduce swaps.
   - For example, push into `small` if the new number is less or equal to the max of `small`; otherwise `large`.
3. **Simplify balancing logic:**
   - Use `elif` for checking heap sizes since only one condition can be true after an insertion.
4. **Add comments and docstrings:** Improve readability.
5. **Improve variable naming:** For example, rename `small` to `max_heap` and `large` to `min_heap` for clarity.
6. **Edge case handling:** Though currently valid, explicitly handle the case when heaps are empty in `findMedian`.

---

### Revised snippet illustrating insertion logic improvement (pseudo):

```python
def addNum(self, num: int) -> None:
    if not self.small or num <= -self.small[0]:
        heapq.heappush(self.small, -num)
    else:
        heapq.heappush(self.large, num)
    
    # Balance the heaps
    if len(self.small) > len(self.large) + 1:
        heapq.heappush(self.large, -heapq.heappop(self.small))
    elif len(self.large) > len(self.small) + 1:
        heapq.heappush(self.small, -heapq.heappop(self.large))
```

---

### Overall

The solution is correct and efficient but can be improved in readability, insertion logic clarity, and code comments. The chosen approach is the standard optimal one for the problem.

---

Let me know if you want a fully cleaned-up and commented version!
'''