## 완전 탐색( Brute Force )

문제를 해결하기 위해서 확인해야하는 모든 경우를 전부 탐색하는 방법
컴퓨터의 빠른 계산 능력을 이용하여 가능한 경우의 수를 일일이 나열하면서 답을 찾는 방법 ('무식하게 푼다')

완전 탐색은 함수 정의 잘하는 것이 중요하다.

그 중에서도 백 트래킹(Back-Tracking)을 통해야 하는 상황 해결하기
* 모든 코테 문제에서 기본적으로 접근해봐야한다. 많은 연습 필요!
정답은 무조건 구할 수 있다. 관건은 시간복잡도 통과이다.

### 고려해야하는 것
1. 해결하고자 하는 문제의 가능한 경우의 수를 대략적으로 계산한다.
2. 가능한 모든 방법을 다 고려한다.
3. 실제 답을 구할 수 있는지 적용한다

### 2번의 모든 방법
1. **Brute Force 기법** - 반복 / 조건문을 활용해 테스트
- 모든 경우의 수를 비교해가며 풀 수도 있지만 아래 2~5 방법을 이용해서 풀 수도 있다.
2. **순열(Permutation)** - n 개의 원소 중 r 개의 원소를 중복 허용 없이 나열하는 방법
3. **재귀 호출**
4. **비트마스크** - 2진수 표현 기법을 활용하는 방법
5. **BFS**, **DFS**를 활용하는 방법

### 완전 탐색 종류

1. N 개 중에서 1) 중복을 허용해서, M 개를 A) 순서 있게 나열하기
- [N과 M (3)](https://www.acmicpc.net/problem/15651)
2. N 개 중에서 1) 중복을 허용해서, M 개를 B) 고르기
- [N과 M (4)](https://www.acmicpc.net/problem/15652)
3. N 개 중에서 1) 중복없이, M 개를 A) 순서 있게 나열하기
- [N과 M (1)](https://www.acmicpc.net/problem/15649)
4. N 개 중에서 1) 중복없이, M 개를 B) 고르기
- [N과 M (2)](https://www.acmicpc.net/problem/15650)

| 중복 고려 | 순서 고려 |   시간 복잡도     |   공간 복잡도     |
|:---------:|:---------:|:-----------------:|:-----------------|
|   O   |   O   |   $O$ ( $ N^M $ )                                                                         |   $O(M)$  |
|   X   |   O   |   $O$ ( $\begin{matrix} N \\ M\end{matrix}$ $P$ ) = $O$ ( $ {N! \over (N - M)! } $ )      |   $O(M)$  |
|   O   |   X   |   $O$ ( $N^M$ ) 보다 작음                                                                 |   $O(M)$  |
|   X   |   X   |   $O$ ( $\begin{matrix} N \\ M\end{matrix}$ $P$ ) = $O$ ( $ {N! \over M! (N - M)! } $ )   |   $O(M)$  | 
