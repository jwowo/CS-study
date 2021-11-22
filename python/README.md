
### lambda
(https://dojang.io/mod/page/view.php?id=2360)

### sort


### join


### map



### 이차원 배열에서의 방향성(상, 하, 좌, 우)을 줄 때 자주 사용되는 루틴

```python
dx = [ 0, 1, 0, -1 ]
dy = [ 1, 0, -1, 0 ]

for i in range(4):
    nx = x + dx[i]
    ny = y + dy[j]
```

### 파이썬 배열 생성하기

1. 2차원 배열 생성하기
```python
2d_array = [[0 for _ in range(column)] for _ in range(row)] 
```

2. 3차원 배열 생성하기
```python
3d_array = [[[0 for _ in range(column)] for _ in range(row)] for _ in range(level)]
```
- 2 ~ 3 중 반복문을 선언함에 따라 `range`의 파라미터는 열(column) -> 행(row) -> 층(level) 의 순서로 선언된다.

