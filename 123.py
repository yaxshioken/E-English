import math

from config.settings import SIMPLE_JWT


class Solution:
    def categorizeBox(self, length: int, width: int, height: int, mass: int) -> str:

        vol = length * width * height
        r = False
        s=False

        if  vol <= math.pow(10, 9):
            r=True
        if mass >= 100:
            s = True
        if s:
            return "Heavy"
        if r and width>=math.pow(10,4) and height>=math.pow(10,4) and length>=math.pow(10,4) :
            return "Bulky"
        if r and s:
            return "Both"
        if not r and not r:
            return "Neither"
        if r and not s:
            return "Bulky"
        if not r and s:
            return "Heavy"
length=200
width=50
height=800
mass=50
vol = mass * width * height
print(Solution().categorizeBox(length=200,
width=50,
height=800,
mass=50),vol)
# print(math .pow(10, 4) <= vol and vol <= math.pow(10, 9))
is_correct = "w".lower() == "w".lower()
if __name__ == '__main__':
    print(is_correct)