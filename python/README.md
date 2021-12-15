
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

### python is 와 == 
#### is 
- identity 연산자
- reference comparison ( 참조 비교 )

#### == 
- 비교 연산자
- value comparison ( 값 비교 )

```python 
>>> no1_1 = 1
>>> no1_2 = 1
>>> str1_1 = 'hello'
>>> str1_2 = 'hello'
>>> no1_1 == no1_2
True
>>> no1_1 is no1_2
True
>>> str1_1 == str1_2
True
>>> str1_1 is str1_2
True
```
위의 예시에서는 변수가 달라도 값이 같으면 `is` 와 `==` 모두 `True` 이다.

값을 아래와 같이 다르게 하면
```python 
>>> no2_1 = 1234
>>> no2_1 = 1234
>>> str2_1 = 'hello world, nice to meet you. What are you doing'
>>> str2_2 = 'hello world, nice to meet you. What are you doing'
>>> no2_1 == no2_2
True
>>> no2_1 is no2_2
False
>>> str2_1 == str2_2
True
>>> str2_1 is str2_2
False
```
값이 같으니 `==` 는 `True`이지만 `is` 는 `False`가 나왔다.
`==` 는 값이 같으면 `True`를 반환, 다르면 `False`를 반환한다.
반면에 `is` 는 주소값이 같으면 `True`를 반환, 다르면 `False`를 반환한다.

### and 와 &

#### and
- 논리 연산자
- True, False 연산
- python docs의 `and` 연산자 설명
> The expression x and y first evaluates x; if x is false, its value is returned; otherwise, y is evaluated and the resulting value is returned.
  - 즉, x and y 가 있을 때, x가 False면 x를 반환, x가 True면 y를 반환한다
#### &
- 비교 연산자
- bitwise 연산자

### or 과 | 
- or 
  - 논리 연산자
  - True, False 연산
  - python docs의 `and` 연산자 설명
    > The expression x and y first evaluates x; if x if true, its value is returned; otherwise, y is evaluated and the resuling value is returned.
- |
  - 비교 연산자
  - bitwise 연산자

  ### not 과 ~ 
- not 
  - 논리 연산자
  - True, False 연산
- ~
  - 비교 연산자
  - bitwise 연산자
  
