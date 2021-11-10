## Sorting Algorithm

Sorting Algorithm은 크게 Comparisions 방식과 Non-Comparisions 방식으로 나눌 수 있다.

### Comparisions Sorting Algorithm

`Bubble Sort`, `Selection Sort`, `Insertion Sort`, `Shell Sort`, `Merge Sort`, `Heap Sort`, `Quick Sort`를 소개한다.

### Bubble Sort

Bubble Sort란 인접한 두 원소를 비교하여 조건에 맞지 않으면 두 원소의 위치를 변경하면서 정렬하는 알고리즘이다.

n개의 원소를 가지고 있는 배열을 오름차순 정렬을 구현한다고 가정했을때, 뒤에서 부터 앞으로 정렬하는 구조를 가지고 있다. 즉 맨 뒷자리에 제일 큰 값을 보내고, 그 앞자리에는 두번째로 큰 값을 보낸다.

이를 n-1번 반복하여 정렬을 완료한다.

| 시간 복잡도 | 공간 복잡도 |
| :---------: | :---------- |
|   O(N^2)    | O(N)        |

## Quick Sort

Sorting는 정렬 알고리즘 중에서 빠르다고 해서 quick 이라는 이름이 붙여졌다.

Quick Sort란 분할 정복( Divide and Conquer ) 기법과 재귀 알고리즘을 이용한 정렬 알고리즘이다.

Quick Sort는 Pivot이라는 임의의 기준값을 설정하여

python 내장 함수로 제공하는 sort() 함수도 Merge Sort와 Quick Sort의 기법을 채택하여 빠르게 정렬되도록 작성되었다고 한다.

**( 주말에 알아보자 ! )**