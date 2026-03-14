class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        num_len = len(nums)

        for left in range(len(nums) - 2):
            mid = left + 1
            right = num_len - 1
            exhaust = False

            if left > 0 and nums[left] == nums[left - 1]:
                continue

            while mid < right:
                t_sum = nums[left] + nums[mid] + nums[right]
                if t_sum == 0:
                    result.append([nums[left], nums[mid], nums[right]])
                    while mid < right and nums[mid] == nums[mid + 1]:
                        mid += 1
                    while mid < right and nums[right] == nums[right - 1]:
                        right -= 1
                    mid += 1
                    right -= 1

                elif t_sum > 0:
                    right -= 1

                else:
                    mid += 1

        return result

                
        