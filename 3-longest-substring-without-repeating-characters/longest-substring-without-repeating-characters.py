class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start_ptr = 0
        end_ptr = 0
        max_len = 0

        str_len = len(s)

        while (end_ptr < str_len):
            candidate = s[end_ptr]

            while (candidate in s[start_ptr:end_ptr]):
                start_ptr += 1

            end_ptr += 1
            max_len = max(max_len, end_ptr - start_ptr)

        return max_len

        