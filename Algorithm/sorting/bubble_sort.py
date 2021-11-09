import sys

def bubble_sort(arr):
    n = len(arr)

    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]


arr = [1, 4, 3, 5, 2]

bubble_sort(arr)

print(arr)

# 문제 출처 : 백준 2750 수 정렬하기
# (https://www.acmicpc.net/problem/2750)
