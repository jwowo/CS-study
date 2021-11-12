# 떡볶이 떡 만들기 

# 절단기의 높이가 높아질수록 손님이 가져가는 떡의 길이는 짧아진다.
# 절단기의 높이를 이진탐색을 통해 바꿔가면서 
# 남아있는 떡의 길이와 손님이 요청한 떡의 길이의 대소비교를 통해 절단기의 높이를 조절한다.
# 

import sys

def recursion(elements, target, start, end):
    middle = ( start + end ) // 2
    # print(f'middle : {middle}')
    sum = 0

    for element in elements:
        if element > middle:
            sum += (element - middle)

    # print(f'sum : {sum}')

    if sum > target:
        recursion(elements, target, middle+1, end)
    elif sum == target:
        print(middle)
    else:
        recursion(elements, target, start, middle-1) 
"""
n = 떡의 개수
m = 요청한 떡의 길이 
"""
n, m = map(int, sys.stdin.readline().split())
elements = list(map(int, sys.stdin.readline().split()))


max_height = max(elements)
# print(f'max height : {max_height}')

recursion(elements, m, 0, max_height)
