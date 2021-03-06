### 다이나믹 프로그래밍

- 다이나믹 프로그래밍은 메모리를 적절히 사용하여 수행 시간 효율성을 비약적으로 향상시키는 방법이다
- 이미 계산된 결과(작은 문제)는 별도의 메모리 영역에 저장하여 다시 계산하지 않도록 한다.
- 다이나믹 프로그래밍의 구현은 일반적으로 두 가지 방식( Top-down, Botton-up )으로 구성된다.
- 동적 계획법이라고도 부른다.
- 일반적인 프로그래밍 분야에서의 동적(Dynamic)이란 어떤 의미를 가질까요?
  - 자료구조에서 동적 할당(dynamic Allocation)은 '프로그램이 실행되는 도중에 실행에 피요한 메모리를 할당하는 기법을 의미한다.
  - 반면에 다이나믹 프로그래밍에서 '다이나믹'은 별다른 의미 없이 사용된 단어이다.

### 동적 프로그래밍의 조건
1. 최적 부분 구조 (Optimal Substructure)
   - 큰 문제를 작은 문제로 나눌 수 있으며 작은 문제의 답을 모아서 큰 문제를 해결할 수 있다.
2. 중복되는 부분 문제 (Overlapping Subproblem)
   - 동일한 작은 문제를 반복적으로 해결해야 한다.

### 대표적인 예 - 피보나치 수열

1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89

- **점화식**이란 인접한 항들 사이의 관계식을 의미한다.
- 피보나치 수열을 점화식으로 표현하면 다음과 같다.
  - $a_n = a_{n-1} + a_{n-2}, a_1 = 1, a_2 = 1$

### 피보나치 수열의 시간 복잡도 분석
- 단순 재귀 함수로 피보나치 수열을 해결하면 지수 시간 복잡도를 가지게 된다.
- f(2)가 여러번 호출 되는 것을 알 수 있다. (중복되는 부분 문제)
- $O(2^N)$
- 빅오 표기법을 기준으로 f(30)을 계산하기 위해 약 10억가량의 연산을 수행해야 한다.
- 그렇다면 f(100)을 계산하기 위해 얼마나 많은 연산을 수행해야 할까?

### 피보나치 수열의 효율적인 해법 : 다이나믹 프로그래밍
- 다이나믹 플그래밍의 사용 조건을 만족하는지 확인
  1. 최적 부분 구조 : 큰 문제를 작은 문제로 나눌 수 있다.
  2. 중복되는 부분 문제 : 동일한 작은 문제를 반복적으로 해결할 수 있다.
- 피보나치 수열은 다이나믹 프로그래밍의 사용 조건을 만족한다.

### 메모이제이션 (Memoization) - 하향식
- 메모이제이션은 다이나믹 프로그래밍을 구현하는 방법 중 하나
- 한 번 계한한 결과를 메모리 공간에 메모하는 기법
  - 같은 문제를 다시 호출하면 메모했던 결과를 그대로 가져온다.
  - 별도의 배열에 값을 기록해 놓는다는 점에서 캐싱(Caching)이라고도 한다.

### 탑다운(메모이제이션, 재귀) vs 바텀업(반복문)
- 다이나믹 프로그래밍의 전형적인 형태는 바텀업 방식이다.
  - 결과 저장용 리스트는 DP 테이블이라고 부른다.
- 엄밀히 말하면 메모이제이션은 이전에 계산된 결과를 일시적으로 기록해 놓는 넓은 개념을 의미
  - 메모이제이션은 다이나믹 프로그래밍에 국한된 개념은 아니다.
  - 한 번 계산된 결과를 담아 놓기만 하고 다이나믹 프로그래밍을 위해 활용하지 않을 수 도 있다.

### 피보나치 수열: 탑다운 다이나믹 프로그래밍 코드
- 탑 다운
```python
# 한 번 계산된 결과를 메모이제이션하기 위한 리스트 초기화
d = [0] * 100

# 피보나치 함수를 재귀함수로 구현(탑다운)
def fibo(x):
    # 종료 조건 (1 혹은 2일 때 1을 반환)
    if x == 1 or x == 2:
        return 1
    # 이미 계산한 적 있는 문제라면 그대로 반환
    if d[x] != 0:
        return d[x]
    # 아직 계산하지 않은 문제라면 점화식에 따라서 피보나치 결과 반환
    d[x] = fibo(x - 1) + fibo(x - 2)
    return d[x]

print(fibo(99))
```

#### 메모이제이션을 이용하는 경우 피보나치 수열 함수의 시간 복잡도는 O(N)이다.

- 바텀업
```python
# 앞서 계산된 결과를 저장하기 위한 DP 테이블 초기화
d = [0] * 100

# 첫 번째 피보나치 수와 두 번째 피보나치 수는 1
d[1] = 1
d[2] = 1
n = 99

# 피보나치 함수(Fibonacci Function) 반복문으로 구현(바텀업)
for i in range(3, n + 1):
    d[i] = d[i-1] + d[i - 2]
print(d[n])
```

### 다이나믹 프로그래밍 vs 분할 정복
- 둘 다 최적 부분 구조를 가질 때 사용할 수 있다
  - 큰 문제를 작은 문제로 나눌 수 있으며 작은 문제의 답을 모아서 큰 문제를 해결할 수 있는 상황
- 다이나믹 프로그래밍과 분할정복의 차이점은 **부분 문제의 중복**이다.
  - 다이나믹 프로그래밍 문제에서는 각 부분 문제들이 서로 영향을 미치며 부분 문제가 중복된다.
  - 분할 정복 문제에서는 동일한 부분 문제가 반복적으로 계산되지 않는다.

- 분할 정복의 대표적인 예신인 퀵 정렬을 보자
  - 한 번 기준 원소(Pivot)가 자리를 변경해서 자리를 잡으면 그 기준 원소는 바뀌지 않는다.
  - 분할 이후에 해당 피벗을 다시 처리하는 부분 문제는 호출하지 않는다.

### 다이나믹 프로그래밍 문제에 접근하는 방법
- 주어진 문제가 다이나믹 프로그래밍 유형임을 파악하는 것이 중요
- 가장 먼저 그리디, 구현, 완전 탐색 등의 아이디어로 문제를 해결할 수 있는지 검토
  - 다른 알고리즘으로 풀이 방법이 떠오르지 않으면 다이나믹 프로그램밍을 고려
- 재귀 함수로 비효율적인 완전 탐색 프로그램을 작성한 뒤에 (탑다운, 메모이제이션) 작은 문제에서 구한 답이 큰 문제에서 그대로 사용될 수 있으면, 코드를 개선하는 방법을 사용할 수 있다.
- 일반적인 코딩 테스트 수준에서는 기본 유형의 다이나믹 프로그래밍(점화식) 문제가 출제되는 경우가 많다. 