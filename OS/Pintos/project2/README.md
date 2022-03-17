# User Programs

## Introduction
현재의 핀토스는 유저 프로그램과 관련된 기본 코드들을 제공하고 있다. 하지만 I/O 또는 상호작용은 불가능하다.
이번 프로젝트 목표는 사용자 프로그램들이 system call을 통해서 OS와 상호작용하도록 코드를 작성하는 것이다.
이 과제를 위해 userprog 디렉토리에서 주로 작업하게 되지만 거의 모든 다른 코드들도 사용한다.
**완성된 Porject 1 위에서 Project 2를 진행해야 한다.** Project 1의 코드가 Project 2의 코드에 영향을 끼치지는 않지만 test case 통과를 위해 Project 1의 테스트도 통과해야한다. 

## Background
[synchronization](https://casys-kaist.github.io/pintos-kaist/appendix/synchronization.html) 과 [virtual address](https://casys-kaist.github.io/pintos-kaist/appendix/virtual_address.html) 를 공부하길 바란다.

## Source Files
`userprog` 폴더 내 파일 설명
- `process.c`, `process.h`
ELF(Executable and Linkable Format) 바이너리 파일을 load 하고 프로세스를 시작한다.
  - ELF 파일이란?
   유닉스 계열 운영체제(리눅스 등)에서 사용되는 실행 파일이다. 표준 바이너리 파일 형식으로 (파일명.o 인 오브젝트 파일 형식) 링커를 거쳐서 나온다. 
  이러한 실행 파일을 통해 프로그램이 사용하는 다양한 정보(API 등)와 어느 메모리 주소에 로딩되는지를 확인할 수 있다. (파일이 실행되기 위한 모든 정보를 알 수 있다)
  윈도우의 경우 PE 파일이다.
- `syscall.c`, `syscall.h`
사용자 프로세스가 일부 커널 기능에 접근하고자 할 때 system call을 호출한다. 스켈레톤 코드에는 메세지를 출력하고 사용자 프로세스를 종료한다. Project 2에서 system call을 수행하기 위해 필요한 코드를 추가해야 한다.
- `syscall-entry.S`
system call handler를 구축하는 어셈블리 코드이다. 현재는 이해하지 않아도 된다.
- `exception.c`, `exception.h`
사용자 프로세스가 권한이 필요한 작업 또는 금지된 작업을 수행하면 커널에 `exception` 또는 `fault` 로 트랩된다. 위 파일들은 exception을 처리(handle)한다. 현재는 모든 예외에 대해 간단한 메세지를 출력하고 프로세스를 종료한다. Project에서는 `page_fault()`를 주로 수정해야한다.
- `gdt.c`, `gdt.h`
x86-64는 분할된 아키텍처이다. GDT(Global Descriptor Table)은 사용중인 세그먼트를 설명하는 테이블이다. 이 파일은 GDT를 설정한다. 이 파일은 수정하면 안된다. GDT가 어떻게 동작하는지 궁금하다면 이 파일을 읽어라.
- `tss.c`,`tss.h`
TSS(Task-State Segment) 는 x86 아키텍처의 task switching에 사용 되었다. 그러나 x86-64에서는 태스크 전환이 사용되지 않는다. 그렇지만 TSS는 Ring switching에서 스택 포인터를 찾기 위해 사용된다. 사용자 프로세스가 인터럽트 핸들러에 들어갈 때 하드웨어는 커널의 스택 포인터를 찾기 위해 tss를 참조한다. 이 파일을 수정할 필요 없다. TSS가 어떻게 동작하는지 궁금하다면 이 파일을 읽어라.

## Using the File System
사용자 프로그램이 파일 시스템에서 로드되고 구현해야하는 많은 system call이 파일 시스템과 관련이 있기 때문에 파일 시스템 코드가 어떻게 동작하는지에 대한 인터페이스를 알아야 한다. 
이 프로젝트의 초점은 파일 시스템이 아니라 사용자 프로세스이므로 기본 파일 시스템 코드를 제공한다. 
`include/filesys.h` 및 `include/file.h` 를 통해 파일 시스템 사용 방법과 많은 제한 사항을 파악해야 한다. (파일 시스템 코드를 수정할 필요는 없다. 파일 시스템의 루틴을 파악하면 프로젝트 4를 수행하는데 수월할 것 이다.)
- 현재 구현된 파일 시스템의 limitation
  - 내부 동기화가 없다. 동시에 같은 파일에 액세스하면 서로 간섭한다. 동기화를 사용하여 한 번에 하나의 프로세스만 파일 시스템의 코드를 실행하고 있는지 확인해야 한다. 
  - 파일이 생성될 때 파일의 크기가 고정된다. 생성할 수 있는 파일의 수도 제한된다.
  - 파일의 데이터는 단일 익스텐트로 할당된다. 단일 파일의 데이터가 디스크의 섹터 범위를 차지해야 한다. 따라서 시간이 지남에 따라 파일 시스템이 사용되기 때문에 외부 조각화는 심각한 문제가 될 수 있다. **(다시 이해할 것)**
  - 하위 디렉토리는 없다.
  - 파일의 이름은 14 characters로 제한된다.
  - 작업 도중 시스템 충돌로 인해 디스크가 손상될 수 있는데 파일 시스템 복구 도구는 없다.
- 중요한 기능 
`filesys_remove()`
  - 파일이 제거되었지만 열려있는 경우, 해당 블럭은 할당 해제되지 않으며 마지막으로 열려 있는 파일이 닫히기 전까지 다른 쓰레드에 의해 액세스할 수 있다. 더 자세한 내용은 [FAQ](https://casys-kaist.github.io/pintos-kaist/project2/FAQ.html)를 확인할 것

---

Project 1에서는 테스트 프로그램이 kernel 이미지에 있었지만 Project 2는 핀토스 가상 머신에 사용자 공간에서 실행되는 테스트 프로그램을 넣어야 한다. 우리의 편의를 위해 테스트 스크립트 (i.e. `make check`) 에서 이 작업을 자동으로 처리한다. `make check` 수정을 통해 개별 테스트를 수행할 수 있다.

- 핀토스 가상 머신에 파일을 넣기
  1. `pintos-mkdisk`프로그램을 통해 가상 디스크 생성
  2. `userprog/build` 디렉터리에서 `pintos-mkdist filesys.dsk 2` 실행하여 `filesys.dsk` 라는 이름의 2MB 핀토스 파일 시스템 파티션을 생성
  3. `pintos --fs-disk filesys.disk -- 커널 명령` 을 통해 디스크 지정
  4. 








# 블로그 참조
프로젝트 2의 목표 **PintOS가 user program을 실행하도록**
- Argument Passing
- User memory access
- System calls
- Process Termination Message
- Deny Write on Executables
- 


# TO DO
- [ ] Background (synchronization, virtual memory) 공부
- [ ] `filesys.h` 와 `file.h` 공부하여 파일 시스템 동작 과정과 제한 사항 파악

# My Keyword
- POSIX
  - https://www.quobyte.com/storage-explained/posix-filesystem





