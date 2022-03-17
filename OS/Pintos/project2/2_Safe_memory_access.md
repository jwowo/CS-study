# TASK 2 : Implement Safe Memory Access

두가지 방법
- Verify every user pointer before dereferencing(simpler)
  - Is it in the user's address space, i.e. below PHYS_BASE?
    - is_user_vaddr() in threads/vaddr.h
  - Is it mapped or unmapped?
    - page_dir_get_page() in userprog/pagedir.c
  - These checks apply to buffes as well!
- Modify page fault handler in userprog/exception.c (우리가 해야할 방법)
  - Only check that a user pointer/buffer is below PHYS_BASE
  - Invalid pointers will trigger a page fault, which can be handled correctly
  - accessing user memory

# TASK 3 : System Call Infrastructure
- Implement syscall_handler() in syscall.c
- What does this involve?
  - Read syscall number at stack pointer
    - SP is accessible as "esp" member of the struct `intr_frame *f` passed to syscall_handler
  - Read some number of arguments above the stack pointer, depending on the syscall
  - Dispatch to the desired function
    - First implement dummy skeletons only.
  - Return the value to the user in `f->eax`

# TASK 4 : System Calls
- Syscall numbers are defined in lib/syscall-nr.h
  - You will not implement all the calls.
- Don't get confused by the "user" side of system calls, in lib/user/syscall.c
- Many of the syscalls involve file system functionality
  - Use the mentioned pintos file system
  - Use coarse synchronization to ensure that any file system code is a rcritical section
  - Syscalls take "file descriptors" as arguements, but the Pintos file system uses `struct file *s`
    - You mst design a proper mapping scheme
- Reading from keyboard and writing to the console are special cases with special file descriptors
  - "write" syscall with fd = STDOUT_FILENO
    - Use putbuf(....) or putchar(....) in lib/kernel/consol.c
  - "read" syscall with fd = STDIN_FILENO
    - Use input_getc(....) in devices/input.h
      

 