### 지금까지 뭐한거야? (User stack에 넣은거)
thread.c 파일 안에 
```c
tid_t thread_create (const char *name, int priority, thread_func *function, void *aux) {}
```
를 보면

```c
t->tf.rip = (uintptr_t) kernel_thread;
t->tf.R.rdi = (uint64_t) function;
t->tf.R.rsi = (uint64_t) aux;
```
rip(다음 명령이 실행될 주소)에 kernel_thread()의 주소를 넣어서 매개 변수로 받은 function을 실행한다.
그리고 첫번째 인자인 rdi에는 실행할 함수(function)을 두번째 인자인 rsi에는 인자(aux)를 넣어준다.
따라서 thread_create()을 통해 생성된 쓰레드가 실행되면 인자로 넘어온 function()이 실행된다.


- thread 구조체에 exit_status 멤버 변수 추가
```c
thread/thread.h

struct thread {
	int exit_status;	 /* to give child exit_status to parent */
```

