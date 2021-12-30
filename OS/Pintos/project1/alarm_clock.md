# Alarm clock

## 과제 목표
Alarm 이란 호출한 프로세스를 정해진 시간 후에 다시 시작하는 커널 내부 함수이다. 
현재 Pintos에서는 알람 기능이 Busy waiting을 이용하여 구현되어 있다.
본 과제에서는 알람 기능을 sleep/wake up 방식으로 구현하는 것이 목표이다.

### Busy waiting
- Thread가 CPU를 점유하면서 대기하고 있는 상태
- CPU 자원이 낭비되고, 소모 전력이 불필요하게 낭비될 수 있다.

### 수정해야할 주요 파일
- thread/thread.*
- device/timer.*

### 수정 및 추가 함수
```c
void timer_sleep (int64_t ticks)
void thread_sleep (int64_t ticks)
void thread_awake (int64_t ticks)
void update_next_tick_to_awake (int64_t ticks)
int64_t get_next_tick_to_awake (int64_t ticks)
```

### Busy waiting
현재는 `timer_sleep()` 에서 `thread_yield()`를 통해 CPU를 양도한다. 주어진 tick 경과 후 timer interrupt를 통해 ready_list에 삽입된다.

### sleep/wake up 기반의 alarm clock 구현
timer_sleep()을 호출하면 호출한 thread를 sleep queue에 삽입한다.

## Alarm clock 구현 전 코드 기초

#### Thread 구조체
```c
struct thread {
	/* Owned by thread.c. */
	tid_t tid;                          /* Thread identifier. */
	enum thread_status status;          /* Thread state. */
	char name[16];                      /* Name (for debugging purposes). */
	int priority;                       /* Priority. */

	/* Shared between thread.c and synch.c. */
	struct list_elem elem;   
```
주요 특징으로는 thread_status는 열거형으로 `THREAD_RUNNING`, `THREAD_READY`, `THREAD_BLOCKED`, `THREAD_DYING` 의 4가지 상태가 있다.
thread의 우선순위는 0 ~ 63으로 숫자가 클수록 우선순위가 높다. (default : 31)

```c
struct list_elem {
	struct list_elem *prev;     /* Previous list element. */
	struct list_elem *next;     /* Next list element. */
};
```
ready list 혹은 sleep list등에서 이전 thread의 element와 다음 thread의 element를 연결한다.

```c
struct list {
	struct list_elem head;      /* List head. */
	struct list_elem tail;      /* List tail. */
};
```
`list_elem`은 `list` 구조체에 의해 `head`와 `tail` 사이에 이중 연결 리스트로 연결된다.

```c
#define list_entry(LIST_ELEM, STRUCT, MEMBER)           \
	((STRUCT *) ((uint8_t *) &(LIST_ELEM)->next     \
		- offsetof (STRUCT, MEMBER.next)))
```
list_entry는 구조체 멤버변수의 주소를 알고 있을 때 멤버변수의 주소를 이용하여 구조체 변수의 주소를 알 수 있다.

#### 리스트와 관련된 helper functions

### 솔루션
- sleep queue의 도입
  - sleep된 thread를 저장하는 자료구조
  - timer_sleep()을 호출한 thread를 저장
- 수정
  - loop 기반 wait() -> sleep/wake up 으로 변경
  - timer_sleep() 호출시 thread를 ready_list에서 제거, sleep queue에 추가
  - wake up 수행
    - timer interrupt 발생시 tick 체크
    - 시간이 다 된 thread는 sleep queue에서 삭제하고 ready_list에 추가

### 구현 

[x] thread descripter 필드 추가
  - thread 구조체에 해당 thread가 일어나야 할 tick을 저장할 필드 (wake_up_tick)
```c
threads/thread.h 

struct thread {
	/* Owned by thread.c. */
	tid_t tid;                          /* Thread identifier. */
	enum thread_status status;          /* Thread state. */
	char name[16];                      /* Name (for debugging purposes). */
	int priority;                       /* Priority. */

	/* Shared between thread.c and synch.c. */
	struct list_elem elem;              /* List element. */

	/* ---------- PROJECT 1 ----------
	
	int64_t wake_up_tick;   /* 스레드가 일어날 시간 */

        /* ------------------------------ */

```

[x] 전역 변수 추가
- `sleep queue` 자료구조 추가
```c
threads/thread.h

static struct list sleep_list;
```

- `next_tick_to_awake` 전역 변수 추가
  - sleep_list에서 대기중인 thread들의 wakeup_tick 값 중 최소값을 저장
```c
threads/thread.h

int64_t get_next_tick_to_awake(void);
```

[x] `thread_init()` 함수 수정
- main() 함수에서 호출되는 thread 관련 초기화 함수
- sleep queue 자료구조 초기화 코드 추가
```c
void
thread_init (void) {
	ASSERT (intr_get_level () == INTR_OFF);

	/* Reload the temporal gdt for the kernel
	 * This gdt does not include the user context.
	 * The kernel will rebuild the gdt with user context, in gdt_init (). */
	struct desc_ptr gdt_ds = {
		.size = sizeof (gdt) - 1,
		.address = (uint64_t) gdt
	};
	lgdt (&gdt_ds);

	/* Init the globla thread context */
	lock_init (&tid_lock);
	list_init (&ready_list);
	list_init (&destruction_req);

	/* ---------- project 1 ----------------
	sleep list init for blocked thread */
	list_init (&sleep_list);

	/* sleep list에서 가장 먼저 깨울 쓰레드의 시간을 저장을 위한 변수
        thread가 sleep 할때마다 비교 후 작은 값으로 갱신 */
	next_tick_to_awake = INT64_MAX;
	
	/* ----------------------------------- */
```


[x] `timer_sleep()` 함수 수정
- 기존의 busy waiting을 유발하는 코드 삭제 (thread가 자는 시간동안 CPU는 while문을 반복하며 cpu의 제어권을 넘기)
- sleep queue를 이용하여 함수 수정
  - 구현하게 될 함수인 thread_sleep()함수 사용
```c
void
timer_sleep (int64_t ticks) {
	int64_t start = timer_ticks ();

	ASSERT (intr_get_level () == INTR_ON);

	/* ----------- busy wait ---------- */
	// while (timer_elapsed (start) < ticks)
	// 	thread_yield ();
        /* --------------------------------*/

	/* ---------- project 1 ---------- */
	
        thread_sleep(start+ticks);
       
        /* ------------------------------- */

}
```

[x] `thread_sleep()` 함수 구현
- 재워야할 thread를 sleep queue에 삽입하고 blocked 상태로 만들어 대기
- 해당 과정중에는 인터럽트를 받아들이지 않는다
- next_tick_to_awake보다 현재 thread를 재울 시간이 더 작다면 업데이트 한다
- devices/timer.c : timer_sleep()함수에 의해 호출된다
```c
void 
thread_sleep(int64_t ticks){
	struct thread *curr;
	enum intr_level old_level;

	ASSERT (!intr_context ());//?
	old_level = intr_disable ();
	curr = thread_current ();

	ASSERT(curr != idle_thread)
	
	if (next_tick_to_awake > ticks){
		next_tick_to_awake = ticks;
	} 

	curr->wake_up_tick = ticks;
	list_push_back (&sleep_list, &curr->elem);	
	thread_block();
	intr_set_level (old_level);
}
```

[x] `timer_interrupt()` 함수 수정
- 매 tick마다 timer 인터럽트 시 호출되는 함수
- sleep queue에서 깨어날 thread가 있는지 확인 (get_next_tick_to_awake())
  - sleep queue에서 가장 빨리 깨어날 thread의 tick값 확인 (next)
  - 있다면 sleep queue를 순회하며 thread 깨움 (thread_awake())
    - 구현하게 될 함수인 thread_awake() 함수 사용
```c
static void
timer_interrupt (struct intr_frame *args UNUSED) {
	ticks++;
	thread_tick ();

	/*--------- PROJECT 1 --------- */
	int64_t next;
	next = get_next_tick_to_awake();
	
	if (next <= ticks) {
		thread_awake(ticks);
	}
	/* ---------------------------- */
}
```

[x] `thread_awake()` 함수 구현
- wakeup_tick 값이 인자로 받은 ticks 보다 크거나 같은 thread 깨움
- 현재 대기중인 thread들의 wakeup_tick 변수 중 가장 작은 값을 next_tick_to_awake 전역 변수에 저장
```c
threads/thread.c

void thread_awake(int64_t ticks){
	next_tick_to_awake = INT64_MAX;
	enum intr_level old_level;
	struct list_elem *e;

	ASSERT (intr_context ());

	for (e = list_begin (&sleep_list); e != list_end (&sleep_list);) {
		struct thread* t = list_entry(e, struct thread, elem);

		if (t->wake_up_tick <= ticks) {
			e = list_remove(e);
			thread_unblock(t);
			if (preempt_by_priority()){
				intr_yield_on_return();
			}
		}
		else {
			if (t->wake_up_tick<next_tick_to_awake){
				next_tick_to_awake = t->wake_up_tick;
			}
			e = list_next(e);
		}
	}
}
```

[x] `get_next_tick_to_awake()` 함수 추가
- thread.c 이외의 파일 (device/timer.c 등)에서도 next_tick_to_awake 변수를 참조하는데 용이하게 하기 위해 추가 
```c
threads/thread.c

int64_t get_next_tick_to_awake(void) {
	return next_tick_to_awake;
}
```



### Q & A
#### Q1. 
`void thread_yield(void)` 함수(thread.c:298) 안에서 `do_schedule` 함수를 호출하기 전에 `intr_disable` 함수를 통해 `maskable interrupts`를 끄는 걸 확인했다.  
`do_schedule` 함수의 설명을 봐도 `At entry, interrupts must be off` 라고 기술하고 있다. 
이와 유사한 방식으로 잠시 interrupts를 끄는 경우가 소스코드의 여러 군데서 확인되는데 
interrupts를 안 끌 경우 어떤 문제가 있을지 궁금하다. 
`casys-kaist.github.io`에 `Synchronization` 부록의 `Disabling interrupts` 안에서 다음과 같이 기술하고 있지만 구체적으로 어떤 문제가 있을지 궁금하다. 
`:The main reason to disable interrupts is to synchronize kernel threads with external interrupt handlers, which cannot sleep and thus cannot use most other forms of synchronization.`
#### A1
interrupt를 disable하는 것은 cpu의 제어권을 interrupt가 다시 enable될 때 까지 넘겨주지 않겠다는 의미와 흡사하다. 
이러한 interrupt는 scheduling에 중요한 timer interrupt나 입출력 장치에 의해 발생하는 I/O interrupt등이 포함될 수 있다.
interrupt disable을 남발하는 행위는 OS 자체의 response time을 증가시키는 등의 이유로 좋지 않은 디자인으로 평가받는다. 
이에 일반적으로 interrupt disable 대신 semaphore나 lock과 같은 synchronization primitive를 주로 사용하지만, project 1에서 다루는 do_schedule 함수 등 scheduling에 직접적으로 연관된 함수들이나, lock/semaphore를 사용할 수 없을 때 (예를들면 lock/semaphore를 구현해야 할 때)는 interrupt disable로써 synchronization을 확보한다.

- `interrupt disable/enable`과 이에 관련된 `assert`가 전부 없을때 발생할 수 있는 `bug case` 중 하나
  1. 현재 thread가 `thread_yield` 함수를 통해 다른 thread에게 cpu 제어권을 넘기려고 시도한다.
  2. 이 thread는 `ready_list`에 삽입되어 다음 `scheduling`을 대기합니다. 이때 `ready_list`에 thread를 삽입하기 위한 함수 `list_push_back`  은 여러 `instruction`으로 구성되어 있다. 
  (https://github.com/casys-kaist/pintos-kaist/blob/ee7443d7ae850c7cb704db6e8213c5cb67cacd0b/threads/thread.c#L306)
  3. `timer interrupt`가 발생한다.
  4. `scheduling`을 위해 `intr_handler` -> `timer_interrupt` -> `thread_tick` 함수가 호출되고, scheduler가 현재 thread가 `yield`가 필요하다고 판단하여 `intr_yield_on_return` 함수를 통해 `interrupt handler` 종료와 함께 `thread를 yield`하려 시도한다.
  5. `thread_yield` 가 다시한번 호출되고, 여기서부터 많은 문제가 발생할 수 있다. 
  우선 현재 thread가 `ready_list`에 두번 삽입되어 `logical bug`를 일으킬 수도 있고, 최악에는 thread가 `ready_list`에 완전히 삽입되지 않은상태에서 (즉 list의 fd/bk가 완전히 연결되어있지 않은상태에서) 다시 `ready_list`에 접근하여 `invalid memory access`에 의한 `kernel panic`등이 발생할 수 있다.

`lock/semaphore`와 같은 `synch primitive`들은 thread/thread 간의 `race condition`을 방지하기 위해서 사용될 수 있으나, 위에 예시로 든 것과 같이 `thread/interrupt handler` 간의 `race condition`은 방지할 수 없다. 이러한 경우에는 `interrupt disable`을 사용하여 `synchronization`을 확보할 수 밖에 없다.

- 정리
  - Disable interrupts를 직접적으로 사용해야만 하는 경우에 관하여
  1. 우선 Response time을 낮추기 때문에 interrupts를 아예 꺼버리는 방법은 가능한 피해야 한다. 따라서 thread와 thread 사이의 race condition 방지를 위해서는 보통 semaphore나 lock 등과 같은 synch primitives를 사용해야 합다.
  2. 참고로 synch primitives의 내부 구현을 보면 사실 interrupts를 disable 해주는 작업이 들어갑니다. interrupts를 직접적으로 끄는 게 아니라 semaphore나 lock이라는 기법으로 감싸서 interrupts를 간접적으로 끄는 방법을 사용하는 이유는 다음과 같다. interrupts를 끄는 작업은 매우 low-level 작업이어서 안전장치가 없기 때문이다. 예를 들어, 코드 어딘가에서 interrupts를 껐다가 실수로 다시 키는 걸 깜빡하면 response time이 크게 증가하는데, 컴파일 에러 혹은 런타임 에러가 발생하는 게 아니라서 수많은 코드 중 어디에서 interrupts가 꺼졌는지 코드를 다 뒤져보지 않는 이상 알 수 있는 방법이 없다. synch primitives의 경우 interrupts를 변동해줬다가 다시 최초 상태로 돌아가게 하는 것을 보장하기 때문에 보다 안전하다.
  3. 그런데, thread(특히 kernel thread)와 외부 하드웨어 모듈에 의해 발생하는 external interrupt handler 간의 race condition 방지에는 synch primitives를 사용할 수 없다. 왜냐하면 synch primitives의 경우 한 thread를 sleep(혹은 block)하게 함으로써 다른 thread와 race condition 들어가는 것을 방지하는데, external interrupt handler의 경우 interrupt가 발생하면 무조건 작동돼야 하기 때문에 sleep/block 상태에 들어가는 것이 불가능하기 때문이다. 따라서 interrupt 자체를 꺼놔서 external interrupt handler가 절대 동작이 될 수 없게 함으로써 synchronization을 달성해야 한다.

#### Q2 
Project 1 의 스케줄러는 `라운드 로빈`으로 구현되어 있고 이를 우선 순위를 고려하여 스케줄링 하어야 한다.
따라서 `ready list`에 thread가 새로 추가되면 현재 ready_list에서 우선 순위가 가장 큰 thread와 현재 CPU를 점유 중인 thread(running) 를 비교하여 우선 순위가 더 높은 thread가 cpu를 점유하도록 코드를 작성중에 있다.
1. thread_unblock() 은 ready_list에 쓰레드를 추가하는 함수라고 생각하여
thread_unblock() 내에서 현재 RUNNING 상태인 쓰레드와 ready_list에서 우선 순위가 가장 큰 쓰레드의 우선 순위를 비교하여 thread_yield() 를 통해 cpu의 제어권을 우선 순위가 더 높은 thread에게 주고자 했다.
이후 테스트를 진행해보니 에러가 나고 디버깅 중에 thread_unblock() 함수 주석에
This function does not preempt the running thread.  This can be important: 이라고 적혀 있는
것을 확인했다. thread_unblock() 함수 내에서 현재 RUNNING 인 쓰레드를 선점하면 안되는 이유가 궁금하다.
2. Project 1 Alarm clock 구현에서  timer_interrupt() 를 통해 현재 tick에서 깨워야 할 thread가 존재한다면 thread_awake() 를 통해 ready_list에 해당 쓰레드를 추가하도록 코드 구현을 했습니다.
이 후 우선순위 스케줄링 과제 구현 중에서  thread_awake() 과정 중에 ready_list에 thread가 추가되면
위와 비슷하게 현재 RUNNING 상태인 쓰레드의 우선순위와 ready_list에서 우선 순위가 가장 큰 쓰레드를
비교하여 우선 순위가 더 높은 쓰레드에게 CPU의 제어권을 넘겨 줘야한다고 생각한다.
이 후 팀원들과 상의해보니 thread_awake() 는 timer_interrupt 과정 중이므로 인터럽트 진행 중에는
RUNNING 상태인 쓰레드가 바뀌면 안될 것 같다는 의견이 나왔다.
thread_awake() 는 인터럽트 과정 중이므로 ready_list에 쓰레드가 추가되어도 우선 순위에 따라 CPU에 제어권을 넘기면 안되는 것이 맞는지 궁금하다.

#### A2
1. thread_unblock 함수는 THREAD_BLOCKED state의 thread를 THREAD_READY state로 변경해 주기 위한 함수로, preemption을 수행하지 않습니다.
 THREAD_RUNNING state의 current thread가 THREAD_READY state의 thread에 의해 preempt 되기 위해서는 current thread가 thread_yield 함수를 호출하거나, timer interrupt 시 scheduler에 의해 intr_yield_on_return 등의 함수로 preemption이 발생해야 합니다.
2. timer interrupt 과정중에 running thread의 변경은 intr_yield_on_return 함수의 호출에 의해 interrupt handler의 종료와 함께 current thread가 cpu를 yield하며 수행되어야 합니다. 해당 함수의 구현과 interrupt handler의 구현 (https://github.com/casys-kaist/pintos-kaist/blob/c38de3056d626442ad4b78a08c55acbd885547b1/threads/interrupt.c#L332) 을 참고하세요.

#### Q3
`thread_unblock()`의 설명에서 `if the caller had disabled interrupts itself,
   it may expect that it can atomically unblock a thread and
   update other data` 부분이 이해되지 않는다 추가 설명 부탁드린다.

#### A3
만약 caller가 thread_unblock 을 호출하기 전에 interrupt를 disable하였다면, 해당 함수의 인자로 전달된 thread의 unblocking과 다른 data의 update를 atomic하게 수행할 수 있다는 뜻이다.

#### Q4
실제 OS(unix 기반)에서 main_thread, peer_thread 관계와 핀토스 OS에서 main_thread, idle_thread, 이외의 thread 관계가 조금 다르다고 생각되어
핀토스 전체 코드에서 process를 생성하는 로직과 thread가 생성되는 로직을 살펴보니
실제 OS 에서 process-thread 관계와 핀토스에서 그것  역시 다르다고 생각되어 혼동이 오는데
실제로 차이가 있는 것인지, 있다면 어떤 차이점이 있는지 질문드립니다.

#### A4
Process란 하나의 virtual address space(프로젝트 3에서 다루게 됩니다)를 가지는 실행 단위를 의미하며, thread는 하나의 process에 속해 있는 더 세부적인 실행 단위를 의미합니다. 실제 OS에서는 하나의 process 안에 여러 개의 thread가 존재할 수 있으며, 이 thread들은 같은 virtual address space를 공유합니다. 핀토스에서도 이런 기본적인 컨셉은 동일하지만, 구현을 단순화하기 위해 하나의 process에 하나의 thread만 있을 수 있도록 구성되어 있습니다. 아마 이런 차이 때문에 혼동이 있을 수 있을 것이라 생각합니다.

#### Q5
그렇다면 user_program의 process.h 에서 process_create_initd() 함수를 보면 함수 선언에서 pid 가 아니라 tid_t로 함수 반환값의 자료형이 선언 되어있습니다. 또한 내부에서 thread_create()를 통해 ‘프로세스‘가 아닌 ‘쓰레드‘를 생성합니다.
process_fork() 역시 마찬가지로 확인됩니다.
그렇다면 핀토스 os에 한해서 프로세스 = 쓰레드 라고 생각해도 되는 건가요?
연관지어, 이번 과제에서 여러개의 thread가 생성되는데 말씀하신 것처럼 ‘하나의 프로세스당 하나의 쓰레드만 존재’할 수 있다면 프로젝트 1에서 각 리스트들에 있는 여러개의 쓰레드들 마다 각각 구별되는 하나의 프로세스가 존재하고, 쓰레드마다 별도의 virtual address space를 가지게 되는건지 궁금합니다.

또한 기존의 쓰레드 구조는 main_thread에서 peer_thread를 생성하고, peer_thread의 실행이 끝나면 main_thread로 cpu 제어를 돌려준다고 알고 있는데 이 역할을 pintos 에서는 idle_thread가 하는 것처럼 코드상에서 해석됩니다.
그렇기 때문에 idle_thread = main_thread라고 임의적으로 가정하고 과정을 이해하였는데 thread_initial에서 별도로 main이라는 이름의 thread를 initial_thread로 생성합니다. 
정리하면, main_thread가 별도로 있음에도 기존 os 컨셉에서의 main_thread 역할을 일부 수행하는 idle_thread가 존재하는데 이 thread를 기존 개념과 연관지어 main_thread로 봐야할지, peer_thread로 봐야할지 아니면 pintos에 한정된 특수한 구조인지 명확한 판단이 서지 않아 추가적으로 질문드립니다.

#### A5
1.
(1) 우선 한 가지를 짚고 넘어가자면, 프로젝트 1에서는 프로세스의 개념이 등장하지 않습니다! 프로세스 개념은 프로젝트 2부터 등장해서, 위에서 말씀드린 내용은 다음 프로젝트부터 해당되는 내용이라고 생각해주시면 좋겠습니다. (위 답변에서 이 부분을 언급하지 않아 혼동이 있었던 것 같습니다...!)
(2) 프로젝트 1에서는 virtual address space도 구현되어있지 않으며, 따라서 모든 쓰레드가 같은 address space를 공유합니다.
(3) 핀토스 os에 한해서는 프로세스 = 쓰레드라고 생각하셔도 무방할 듯 합니다. 실제로 thread.h의 struct thread를 보시면 pml4(특정 프로세스의 virtual address 정보를 담고 있는 테이블입니다) 등, 쓰레드보단 프로세스가 가지고 있어야 할 내용을 쓰레드 struct가 가지고 있는 것을 확인할 수 있습니다.

2.
(1) idle_thread는 ready list가 비어 있을 때 (즉 당장 실행할 수 있는 쓰레드가 없을 때) 임시로 실행되는 쓰레드로, 계속 scheduling을 시도하면서 실행할 수 있는 쓰레드가 생길 때까지 기다리는 역할을 합니다. 즉 main thread의 역할을 하는 쓰레드는 아니며, peer thread도 아닌 특수한 thread라고 이해해주세요. 다만 이런 구조가 핀토스에 한정된 것은 아니고, 몇몇 실제 운영체제에도 idle thread가 등장한다고 합니다.
(2) 또한 main thread에서 peer thread를 생성했을 때, 명시적으로 wait을 하지 않는 이상 두 쓰레드는 동시에 실행될 수 있습니다. (즉 main thread가 항상 peer thread가 완료될 때까지 기다리지는 않습니다)

#### Q6
Priority-scheduling에서 cond_wait 함수 관련 질문 드립니다. 구현을 위해 참고하고 있는 자료에서 cond_wait을 수정할 때 priority의 순서를 지키면서 thread를 waiters에 넣으라는 가이드를 보았습니다.
우선 기존의 cond_wait 함수를 보면 list_push_back(&cond->waiter, &waiter.elem) 와 같이 우선순위를 무시하고 queue의 뒤에 삽입해주고 있습니다(https://github.com/casys-kaist/pintos-kaist/blob/master/threads/synch.c#L285). 만약 우선순위를 적용하게 된다면 list_insert_ordered 함수 같은 것을 사용하게 될 것입니다. 그런데 문제는, 우선순위를 확인하기 위해서는 thread의 priority 정보가 필요한데, sema_down 함수가 작동하기 전까지는 waiter.semaphore의 waiters에 현재 running 중인 thread의 정보가 들어가지 않는다는 점입니다. thread의 정보가 없는 상태에서 어떻게 list_insert_ordered가 작동할 수 있도록 구현할 수 있는지 궁금합니다.
보다 근본적으로, 어짜피 cond_signal 에서 sorting을 할건데 굳이 cond_wait에서 우선순위를 지켜가며 O(n) 시간 복잡도를 소모하는 방식을 사용할 이유가 무엇인지 의문입니다.
매번 감사드립니다!

#### A6
해당 자료가 pintos-kaist에서 공식으로 제공하는 자료는 아니라서, 저희도 제대로 본 적이 없기 때문에 자료에서의 구현 방식에 대해 정확한 말씀을 드리긴 어렵습니다. 다만 말씀하신 대로 cond_signal에서 어차피 sorting을 한다면, 굳이 cond_wait에서까지 중복으로 sorting할 필요는 없어 보입니다.


### + 가상 메모리 참고 블로그
https://gamedevlog.tistory.com/85