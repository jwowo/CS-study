
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

```python
for dir_r, dir_c in (-1, 0), (1, 0), (0, -1), (0, 1):
    new_r, new_c = row + dir_r, col + dir_c
```

### 파이썬 배열 생성하기

1. 2차원 배열 생성하기
```python
2d_array = [[0 for _ in range(column)] for _ in range(row)] 
```

2. 3차원 리스트의 경우 호출시에

` 리스트 [ 높이인덱스 ] [ 세로인덱스 ] [ 가로인덱스 ] = 값 ` 의 형태로 호출한다.
```python 
for h in height:
    for r in row:
        for c in column:
            array[h][r][c] = 1
```

- 3차원 리스트 컴프리헨션
```python
3d_array = [[[0 for _ in range(column)] for _ in range(row)] for _ in range(depth)]
```
