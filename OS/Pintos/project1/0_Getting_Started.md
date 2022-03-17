### Source Tree Overview
- `threads/` : 기본 커널을 위한 소스 코드 (프로젝트 1에서 수정)
- `userprog/` : user program loader를 위한 소스 코드 (프로젝트 2에서 수정)
- `vm/` : 거의 비어있는 폴더 (프로젝트 3에서 가상 메모리 구현)
- `filesys/` : 기본 파일 시스템을 위한 소스 코드 (사용하긴 하지만 프로젝트 4에서만 수정)
- `lib/` : 표준 C 라이브러리의 일부 구현. 이 디렉토리에 있는 소스 코드들은 Pintos 커널과 그 아래에서 돌아가는 user program(프로젝트 2)에서 컴파일 된다. 조금의 수정이 필요하다.
- `include/lib/kernel/` : Pintos 커널에 포함되는 C 라이브러리. 이 디렉토리에 구현된 자료형은 우리가 작성해야 할 커널 코드에 사용 가능하다. (bitmaps, double linked list, hash tables) 커널에서 이 디렉토리의 헤더는 `#include <...>` 표기를 통해 포함할 수 있다.
- `include/lib/user/` : user programs에 포함되는 C 라이브러리. user programs에서 이 디렉토리의 헤더는 `#include <...>` 표기를 통해 포함할 수 있다.
- `tests/` : 프로젝트 2 user programs에서 사용될 기초 예제
- `include/` : 헤더 소스 파일 (*.h)

### Building Pintos
첫 프로젝트를 하기 위해 소스 코드를 빌드한다. 
1. `cd threads` : 프로젝트 1과 관련된 threads 파일로 이동
2. `make` : make 명령을 실행하면 threads 디렉토리 안에 `build` 디렉토리가 생성되어 Makefile과 몇 개의 하위 폴더들이 생성된다. 그럼 커널 내부를 빌드하면 된다!

#### 빌드 후 생성되는 관심있게 볼 파일
- `Makefile` : `pintos/src/Makefile.build`의 복사본, 어떻게 커널을 빌드해야 하는지 설명
- `kernel.o` : 전체 커널의 실행 파일. 각각의 커널 소스 코드들로 부터 모든 linking object files을 컴파일하여 생성되는 파일. 디버그 정보를 포함하고 있으므로, [GDB](https://casys-kaist.github.io/pintos-kaist/appendix/debugging_tools.html#GDB) 실행 또는 [backtrace](https://casys-kaist.github.io/pintos-kaist/appendix/debugging_tools.html#Backtraces) 할 수 있다.
- `kernel.bin` : 커널의 메모리 이미지. 핀토스 커널을 실행하기 위해 가상메모리에 적재되는 실제 바이트. 그냥 `kernel.o`에서 디버깅 정보를 제거하여 커널의 사이즈를 줄인 파일이다.
- `loader.bin` : 커널 로더를 위한 메모리 이미지. 작은 단위의 어셈블리 코드로 작성되어 있고 디스크에서 커널을 읽어서 메모리에 적재하고 시작한다. 정확이 PC BIOS에 의해 정해진 512 바이트 크기이다. 빌드의 하위 디렉토리에는 컴파일러에서 생성된 실행 파일(object) (.o)와 종속 파일(dependency) (.d)가 포함되어 있다. 종속 파일은 어떤 소스 코드 또는 헤더가 변경되었을 때, 어느 파일을 재컴파일해야하는지 알려준다

### 프로세스와 쓰레드
- .exe 는 프로그램, 그 프로그램이 실행되어 돌아가고 있는 상태 : 프로세스
- 

### 시스템 콜
- 시스템 콜은 운영체제에서 사용할 수 있는 서비스에 대한 인터페이스를 제공한다.
- 프로그램은 유저모드와 커널모드로 실행될 수 있다.
- 유저모드는 메모리에 직접 접근할 수 없다.
- 커널모드로 실행된 프로그램은 메모리, 하드웨어와 그 밖의 리소스에 접근 가능하다. 메모리에 직접 접근 가능하기 때문에 특권 모드라고도 한다.

### 동기식 입출력 (synchronous I/O)
- I/O 요청 후 입출력 작업이 완료된 후에 야 제어가 사용자 프로그램에 넘어감
- 구현 방법 1
  - I/O가 끝날 때까지 CPU를 낭비시킴
  - 매시점 하나의 I/O만 일어날 수 있음
- 구현 방법 2
  - I/O가 완료될 때까지 해당 프로그램에게서 CPU를 빼앗음
  - I/O 처리를 기다리는 줄에 그 프로그램을 줄 세움
  - 다른 프로그램에게 CPU를 줌

### 비동기식 입출력 (asynchronous I/O)
- I/O가 시작된 후 입출력 작업이 끝나기를 기다리지 않고 제어가 사용자 프로그램에 즉시 넘어감

두 경우 모두 I/O의 완료는 인터럽트로 알려줌

