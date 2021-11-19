### C89 표준
- 1989년에 ANSI(American National Standards Institue)에 의해 채택된 첫번째 C표준
  - 그래서 ANSI C라고도 부름
- 30년이 지났지만 아직도 대부분의 컴파일러가 지원하는 표준

### C89 표준 (2)
- 오늘날 대부분의 C코드도 이 버전
  - 많은 임베디드 시스템은 여전히 C89만 지원
  - 특화된 소형 하드웨어는 그것을 직접 제어하는 전용 운영체제를 지원함
  - 즉, 윈도우 및 리눅스처럼 발전된 기능을 갖춘 범용 운영체제를 지원 안함
  - 그 하드웨어 + 운영체제 용으로 컴파일이 가능하면서도 하드웨어에 직접 접근할 수 있는 컴파일러를 제작해야 한다면 C89 표준이 가장 간단

```c
#include <stdio.h>

int main(void)
{
    print('Hello World~!');
}
```

### #include 
- 다른 파일에 구현된 함수나 변수를 사용할 수 있게 해줌
- #include 는 전처리기 지시문 중 하나
- 전처리기(preprocessor)란?
  - 컴파일을 하기 전에 텍스트를 '복붙'해주는 일을 함

> '#' 은 전처기리이다

### #include <>
- <> 안에 단어(예: stdio.h)는 실제 디스크 상에 존재하는 파일 이름
- 이 파일 찾아서 포함해줘
  - 전처리기가 컴파일하기 전에 include를 찾고 
  - 그 파일을 열어서 복사한 뒤 
  - #include <stdio.h> 자리에 내용을 교체한다.
  - 결국 교체된 내용까지 같이 컴파일 된다.
  
> C에서 컴파일하는 과정, 어떤 라이브러리를 가져오는 과정, #include 하는 과정은 모두 텍스트 파일을 열어서 복붙해오는 과정이다.  

### #include 사용법
```c
#include <stdio.h> /* 컴파일 O */ 
#include 'stdio.h' /* 컴파일 오류 */
#include "stdio.h" /* 컴파일 O 그러나 일단 사용하지 말 것! */
```

### <stdio.h>
- C 표준 라이브러리( C Standard Libray, libc ) 중 일부

### C 표준 라이브러리란?
- 다음에 필요한 매크로, 자료형(data type), 함수 등을 모아 놓은 것
  - 문자열 처리
  - 수학 계산
  - 입출력 처리
  - 메모리 관리

### <stdio.h> 의 역할
- libc에서 표준 입출력 (Standard Input and Output) 을 담당
- 스트림 입출력에 관련된 함수들을 포함
- stdio 라이브러리에 있는 함수의 몇 가지 예:
  - printf()
  - scanf()
  - fopen()
  - fclose()

### main(void) 함수








