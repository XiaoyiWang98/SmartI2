import pyautogui
import math

width, height = pyautogui.size()

r = 250  # 圆的半径
# 圆心
o_x = width / 2
o_y = height / 2

pi = 3.1415926

for i in range(10):
    pyautogui.moveRel(0, 100, duration=0.25)
    pyautogui.moveRel(-100, 0, duration=0.25)
    pyautogui.moveRel(0, -100, duration=0.25)