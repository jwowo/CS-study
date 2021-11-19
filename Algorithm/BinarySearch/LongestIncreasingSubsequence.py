# import sys

# n = int(sys.stdin.readline().strip())
# a = list(map(int, sys.stdin.readline().split()))

"""
문제 접근 방법
이분 탐색 문제 리스트에서 이 문제를 보게됐다. 
맨 처음 문제를 봤을때는 어느 부분에 이분 탐색을 적용해야하는지 진짜 감이 안잡혔다.

이진 탐색을 하기 위해서는 전제조건이 정렬이 되어있는 리스트인데,
입력받은 수열 A의 순서를 변경하면
문제에서 찾고자하는 가장 긴 증가하는 부분 수열을 확인 할 수 없기 때문에 이 방법은 패스



입력 받은 수열 A의 각 요소에
"""

n = 6
arr = [ 10, 20, 10, 30, 20, 50 ]

dp = [1 for _ in range(n)]

for i in range(n):
    for j in range(i):
        if arr[j]
