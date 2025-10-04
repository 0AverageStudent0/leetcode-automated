# Problem Title: String to Integer (atoi)
# Language: python3
# Status: Accepted
# Runtime: 5
# Memory: 17.8
# Submission URL: https://leetcode.com/submissions/detail/1790839196/

class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        if not s:
            return 0
        
        INT_MAX = 2**31 -1
        INT_MIN = -2**31
        sign = 1
        idx = 0
        if s[0] == "+":
            idx += 1
        elif s[0] == "-":
            sign = -1
            idx += 1
        
        def helper (i, parsed) -> int:
            if i >= len(s) or not s[i].isdigit():
                return parsed * sign
            digit = int(s[i])
            parsed = parsed*10 + digit
            if parsed*sign < INT_MIN:
                return INT_MIN
            elif parsed*sign > INT_MAX:
                return INT_MAX
            return helper(i+1,parsed)
        return helper(idx, 0)


# Azure OpenAI Analysis
'''
### Summary of the code
This Python solution implements the "String to Integer (atoi)" problem using:
- Initial stripping of leading whitespace.
- Handling optional sign characters `+` or `-`.
- Recursive parsing of the digit characters to build the integer value.
- Clamping the result to the 32-bit signed integer range ([−2³¹,  2³¹−1]).
- Returns 0 if the string is empty or doesn't contain valid digits after optional sign.

### Time complexity
- Each character in the string is processed at most once in the recursive helper function.
- Let n = length of the input string.
- Time complexity is **O(n)**.

### Space complexity
- Recursive calls depth depends on the number of digits processed. In the worst case, this could be O(n).
- So space complexity due to recursion stack is **O(n)**.
- Other than recursion, constant additional space is used.

### Strengths
- Correctly implements all steps required by the problem:
  - Handling whitespace.
  - Handling sign.
  - Clamping to integer bounds.
- Uses recursion in an elegant and clean way to parse and accumulate the digits.
- Code is clear and easy to follow.

### Weaknesses
- Recursive approach causes O(n) call stack space, which can be a problem for very long numeric strings (stack overflow risk).
- Parsing digits one-by-one using recursion can be less efficient than iteration.
- No explicit handling of non-digit characters after the initial digit sequence (though it works by stopping parsing).
- `lstrip()` creates a new string, which is fine but could be avoided by moving index instead.
- Multiplying by `sign` multiple times in each recursion call is slightly inefficient.

### Suggestions for improvement
- Convert the recursion to an iterative approach to reduce space complexity from O(n) to O(1).
- Use a simple loop to parse the digits, stop when a non-digit is encountered.
- Avoid repeated multiplication by `sign` in each recursion; multiply once at the end.
- Instead of `lstrip()`, consider advancing an index to skip whitespace to avoid creating a copy.
- Add boundary checks using intermediate checks before multiplication/addition to prevent integer overflow during parsing.
- Add comments or docstring for better readability.

---

### Example iterative approach for improvement

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31
        
        i, n = 0, len(s)
        # Skip leading whitespace
        while i < n and s[i] == ' ':
            i += 1
        
        if i == n:
            return 0
        
        # Check sign
        sign = 1
        if s[i] == '+':
            i += 1
        elif s[i] == '-':
            sign = -1
            i += 1
        
        result = 0
        while i < n and s[i].isdigit():
            digit = int(s[i])
            # Check for overflow
            if result > (INT_MAX - digit) // 10:
                return INT_MAX if sign == 1 else INT_MIN
            result = result * 10 + digit
            i += 1
        
        return sign * result
```
This approach is O(n) time and O(1) space and more robust for long inputs.
'''