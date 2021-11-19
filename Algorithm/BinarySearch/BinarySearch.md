### 이진 탐색 알고리즘

- 순차 탐색 : 리스트 안에 있는 특정한 데이터를 찾기 위해 앞에서부터 데이터를 하나씩 확인하는 방법 (시간복잡도가 크다.)
- 이진 탐색 : 정렬되어 있는 리스트에서 탐색 범위를 좁혀가며 데이터를 탐색하는 방법 (순차 탐색의 시간복잡도를 log 만큼 줄일 수 있다.)
n 이 엄청 큰 경우, 시간복잡도를 (log N)으로 처리해야겠다라고 생각이 들 경우 시도 해보는 알고리즘
  - 이진 탐색은 시작점, 끝점, 중간점을 이용하여 탐색 범위를 설정한다.

### 이진 탐색 동작 방법

#### [ step 1 ] 
시작점, 끝점, 중간점 설정 ( 중간점이 두개이면 소수점 이하 제거 )   

#### [ step 2 ] 
중간점의 값과 찾고자하는 값을 비교한다.

### [ step 2-0 ]
비교 후 중간점의 값이 내가 찾고자하는 값이라면 결과를 출력한다.

#### [ step 2-1 ] 
비교 후 중간점의 값이 찾고자 하는 값보다 더 크다면, 
중간점에서 오른쪽에 있는 값들은 더 볼 필요가 없다. 
(이진 탐색은 정렬되어 있는 리스트에서 데이터를 탐색하는 방법이므로 중간점 이후의 값들은 모두 찾고자하는 값보다 크기 때문이다. )

#### [ step 2-2 ] 
비교 후 중간점의 값이 찾고자하는 값보다 더 작다면,
마찬가지로 중간점 왼쪽에 있는 값들은 더 볼 필요가 없다.

#### [ step 3-1 ] 
끝점의 인덱스를 중간점의 인덱스로 옮기고 다시 [ step 2 ] 를 반복한다. ( 시작 인덱스가 끝 인덱스보다 크면 )

#### [ step 3-2 ] 
시작점의 인덱스를 중간점의 인덱스로 옮기고 다시 [ step 2 ] 를 반복한다.

### 시간복잡도
단계마다 탐색 범위를 2로 나누는 것과 동일하므로 $O(\log N)$ 이다.

### 소스코드
재귀함수를 이용
```python
def binary_search(array, start, end, target):
    """
    Args 
        array   (list)  : 이진탐색을 진행할 정렬이 되어 있는 값이 저장되어있는 리스트
        start   (int)   : 탐색을 시작할 인덱스
        end     (int)   : 탐색을 끝낼 인덱스
        target  (int)   : 찾고자하는 값
    """
    if start > end:
        return None

    # 구간 설정 ( 반으로 나눠서 이진 탐색을 진행하기 위해 첫인덱스와 끝인덱스를 더하여 반으로 나눔. )
    mid = (start + end) // 2
    
    # 찾은 경우 인덱스를 반환
    if array[mid] == target:
        return mid
    # 중간값이 target보다 작다면 중간값 + 1 부터 끝인덱스까지 재귀적으로 탐색
    elif array[mid] <= target:
        return binary_search(array, mid + 1, end, target)
    # 중간값이 target보다 크다면 첫 인덱스부터 중간값 - 1 까지 재귀적으로 탐색
    else:
        return binary_search(array, start, mid - 1, target)

```

반복문 구현
```python
def binary_search(array, start, end, target):
    while start <= end:
        mid = (start + end) // 2

        if array[mid] == target:
            return mid
        elif array[mid] < target:
            start = mid + 1
        else:
            end = mid -1
        
    return None
```

### 파이썬 이진 탐색 라이브러리

#### bisect_left(a, x) 
정렬된 순서를 유지하면서 배열 a에 x를 삽입할 가장 왼쪽 인덱스를 반환

#### bisect_right(a, x)
정렬된 순서를 유지하면서 배열 a에 x를 삽입할 가장 오른쪽 인덱스를 반환

```python
from bisect import bisect_left, bisect_right

a = [1, 2, 3, 4]
x = 4

print(bisect_left(a, x))    # 2
print(bisect_right(a, x))   # 4
```
#### 값이 특정 범위에 속하는 데이터 개수 구하기

```python
from bisect import bisect_left, bisect_right

# 값이 [left_value, right_value]인 데이터의 개수를 반환하는 함수
def count_by_range(a, left_value, right_value):
    right_index = bisect_right(a, right_value)
    left_index = bisect_left(a, left_value)
    return right_index - left_index

# 배열 선언
a = [1, 2, 3, 3, 3, 3, 4, 4, 8, 9]

# 값이 4인 데이터 개수 출력
print(count_by_range(a, 4, 4))

# 값이 [2, 5] 범위에 있는 데이터 개수 출력
print(count_by_range(a, 2, 5))
```

#### 파라메트릭 서치

이진 탐색 활용 문제
결정 문제를 ( 'YES' OR 'NO' ) 최적화 알고리즘으로 바꾸어 해결하는 기법
- 이분법 : Bisection Method $rightarrow$ 이진 탐색

어떤 함수의 값을 최대한 높이거나, 값을 최대한 낮추는 방법을 이용하여 
여러번의 결정 문제로 바꾸어서 해결하는 방법

탐색 방법을 좁혀가면서 현재 범위에서는 그 조건을 만족하는지를 체크하면서 범위를 좁혀가면서 이진 탐색을 이용하여 해결

예시 : Egg Dropping Problem -> Two Eggs Problem

 데이터의 개수가 굉장히 많거나, 데이터의 범위가 큰 탐색의 경우 이진탐색을 고려해야한다
