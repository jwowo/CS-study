# Argument Passing
Set up argument for user program in `process_exec()`

## x86-64 Calling Convention
[System V AMD64 ABI](https://en.wikipedia.org/wiki/X86_calling_conventions#System_V_AMD64_ABI)

# FAQ
- Q :  `load()` 안에서 매개변수 `const char *file_name`가 `strtok_r`에 의해 다른 인자들은 무시되고 파일 이름만 남게되는데 `filename` 이 변경되므로 deep copy를 해야할까?
A : No! 
`init.c` -> `run_actions()` -> `run_task()` -> `process_Create_initd()` 에서 
이미 caller와 유저 프로세스의 `load()`에서 race condition을 방지하기 위해서 파일 이름을 복사한 뒤에
```c
tid_t process_create_initd (const char *file_name) {
	char *fn_copy;
	tid_t tid;

	/* Make a copy of FILE_NAME.
	 * Otherwise there's a race between the caller and load(). */
	fn_copy = palloc_get_page (0);
	if (fn_copy == NULL)
		return TID_ERROR;
	strlcpy (fn_copy, file_name, PGSIZE);

	/* Create a new thread to execute FILE_NAME. */
	tid = thread_create (file_name, PRI_DEFAULT, initd, fn_copy);
	if (tid == TID_ERROR)
		palloc_free_page (fn_copy);
	return tid;
}
```
`thread_create()`에서 `initd()`의 매개변수로 전달하기 때문에 
`process_exec()` -> `load(const char *file_name)`의 매개변수로 전달된 file_name은 이미 복사본이므로 수정되어도 상관없다.
