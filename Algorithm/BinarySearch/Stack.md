## Stack

스택과 큐는 컴퓨터 공학에서 가장 기본이 되는 자료구조
메모리 안의 데이터들을 효율적으로 다루기 위해 만들어진 데이터 참조 방식

LIFO (Last In First Out)
한 쪽 끝에서만 데이터를 넣거나 뺄 수 있는 선형구조
제일 마지막에 들어온 데이터가 제일 빨리 나가는 형식

주요 기능
push
pop

ctrl + z 를 이용하여 우리가 한 작업을 되돌리는 것이 stack의 예

## Queue

FIFO (First In First)
양 쪽 끝에서만 데이터를 넣거나 뺄 수 있는 선형구조
제일 처음에 들어온 데이터가 제일 빨리 나가는 방식

은행의 대기표, 카페 

컴퓨터에서 Queue의 사용
: 프로세스 스케쥴링, 대부분의 입출력 (파일 입출력), 프린터 대기열, 네트워크 패킷 처리, 게임 대기열

주요 기능
first 와 next를 이용
Enqueue
Dequeue

Queue의 다른 형식
Circular Queue(환형 큐)
Priority Queue(우선 순위 큐) : 먼저 들어와도 우선순위가 있다.