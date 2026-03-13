class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0: return False
        # print(numToArrayRev(x))

        return x == arrayToNum(numToArrayRev(x))

def numToArray(x: int) -> list:
    if x < 10:
        return [x]
    else:
        return numToArray(x // 10) + [x % 10]

def numToArrayRev(x: int) -> list:
    if x < 10:
        return [x]
    else:
        return [x % 10] + numToArrayRev(x // 10)

def arrayToNum(x_ls: list):
    mult = 1
    acc = 0

    for i in x_ls[::-1]:
        acc += (i * mult)
        mult *= 10

    return acc

        