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
- 프로그램의 진입점
- C코드를 빌드해서 나오느 실행파일 (.exe 또는 .out)을 실행하면 main(void) 함수가 자동적으로 실행됨
- 반환형
  - 0: 프로그램에 문제가 없었다는 뜻
- void
  - 다른 언어와 달리 void를 생략한다고 매개변수가 없다는 뜻이 아님
  - c에는 함수 선언과 함수 정의가 있음 (나중에 봄)
    - 함수 선언에서 void를 생략하면 매개변수를 받는다는 의미
      - 단, 아직 매개변수의 갯수와 자료형을 모를뿐
    - 함수, 정의에서 void를 생략하면 매개변수가 없다는 뜻
  - 따라서, 언제나 void를 넣는 습관을 기르자

```c
int sum(void) /* 함수 선언 : 매개변수가 없음 */
int sum()     /* 함수 선언 : 매개변수가 있는데, 아직 뭔지 모름 */

int sum(void) /* 함수 정의 : 매개변수가 없음 */
{
  /* 코드 생략 */
}

int sum()   /* 함수 정의 : 매개변수가 없음 */
{
  /* 코드 생략 */
}

```

### main() 함수와 커맨드 라인 인자
- c에도 같은 코드가 있음
- 포인터를 제대로 배운 뒤 자세히 공부 예정

예
```c
int main(int argc, char** argv)
{
  return 0
}
```

### prinf() 함수
- 화면에 데이터를 출력할 때 사용하는 함수
- printf의 뜻은 `print formatted (서식에 맞게 출력하다)
- 줄 바꿈 -> `\n`
  - \n : 새 줄(new line)을 의미하는 이스케이프 문자(escape character)
- string.Forma(), 혹은 answkduf qhrks($"{}")를 이용
- c는 그런거 없음
  - `%s` 라는 서식 문자(format specifier)가 문자열이 들어갈 위치를 알려줌
    - string이어서 %s
  - `%d` 정수가 들어가 들어갈 위치를 알려줌
    - decimal(10진수)여서 %d

### 주석 (comment)
- ` /* */ ` 만 지원 (최소한 C89 에선)
- 주석이 한 줄이든 여러 줄이든 다 `/* */` 만
- 다른 언어에선 여러줄에는 `/* */`를 한 줄에는 `//`를 쓰는게 일반적
- c는 그런거 없음

### C는 절차적 언어이다
- C로 작성한 코드는 데이터보다 프로세스에 중점이 맞춰져 있음
- 추상적인 개념이 없음
- class 없음
- 모두 전역(global) 함수, 기본적으로 어디에서나 호출 가능
- 변수
  - 함수 밖에 선언 되어있으면, 전역(global) 변수
  - 함수 안에 선언 되어있으면, 지역(local) 변수

### 자료형, unsigned와 signed
- 기본 자료형 : char, short, int, long, float, double, long double

### unsigned 와 signed
- 예 : unsigned 라는 단어를 자료형 이름 앞에 넣어줘야 함
- '부호 있음'을 명확하게 보여주기 위해서 signed를 붙일 수 있음
- unsigned/signed를 생략하면 '부호있음'이 기본
  - 예외 : char

### char
```c
char ch_a = 'a';
char_b = char_a +  1; /* b */
char ch_c = 99;       /* c */

```
- 최소 8비트인 정수형
- 표준은 8비트 이상이라고만 정의함(...)
  - 따라서 컴파일러 제멋대로 1백만 비트도 가능

### char가 몇 비트인지 찾는 방법
- <limit.h> 헤더를 인클루드한 뒤, `CHAR_BIT`를 보면 몇 비트인지 알 수 있음
- 참고로 C표준은 기본 자료형의 정확한 바이트 수를 강요 안함
  - 각 컴파일러마다 알아서 하라고 함
- 더 나아가 1바티으를 CHAR_BIT만큼이라고 말함

### char와 ASCII 문자
- 정수형
- `char`는 ASCII 문자를 표현하기에 충분
  - 아스키(ASCII)는 0 ~ 127인 숫자
- 덧셈 가능

### char와 signed/unsigned
- 정수형이니 signed와 unsigned가 있음
- c 표준은 그런거 정하지 않음
- 컴파일러 구현에 따라 정해짐(...)
  - clang windows에서는? signed

### char의 기본 부호가 지정 안 된 이유는?
- 아스키의 범위를 0-127이므로 부호 여부는 상관이 없음
- 단 8비트 정수형으로 쓰로고 할 때는 반드시 char 앞에 signed, unsigned를 넣어주는게 좋음
- 안 그러면 포팅해도 문제없는 정수 범위는 0-127 사이뿐
  - `0000 0000(2)` ~ `0111 1111(2)`

### char의 부호여부를 판단하는 방법
- <limit.h> 헤더 파일에서 CHAR_MIN을 보면 부호 식별자가 없는 char가 signed인지 unsigned인지 알 수 있음

### char로 표현 가능한 숫자의 범위(표준)
| unsigned char | char | signed char |
|:-------------:|:----:|:-----------:|
| 0 ~ 255     | 0 ~ 127 | -127 ~ 127 |

- 왜 signed char는 -128이 아니라 -127인가요?
- 1의 보수('예~~~~~전의 기계는 1의 보수 쓸지도 ) 
- 그래도 '안전한' 포팅을 위해서는 -128이 아니라 -127

### char로 표현 가능한 숫자의 범위(보통)
- 표준은 표준일 뿐이고
- 실제 보통(데스트톱 개발할 때) 안전하게 생각해도 되는 것
  1. 크기 : 8비트
  2. 부호(unsigned/signed)를 생략할 경우 : signed
  `char signed_char = -1
  3. 범위
     - 부호 없는 경우(unsigned) : 0 ~ 255
     - 부호 있는 경우(signed) : -128 ~ 127


### short
- 최소 16비트이고 char의 크기 이상인 정수형
- 포팅 문제 없는 값의 범위
  - signed short : 0 ~ 65525
  - unsigned shor : -32767 ~ 32767
- 기본 정수형(int)보다 짧음
- 메모리를 적게 쓰기 위해 사용
- 그러나 `int` 대신 `short`를 사용할 경우 성능이 느려질 수도 있다.
- 표준에 상관없이 보통 안전하게 생각해도 되는 것
  1. 크기 : 16 비트
  2. 범위 
     - 부호 없는 경우(unsigned) : 0 ~ 255
     - 부호 있는 경우(signed) : -128 ~ 127

### int
- 표준에 따르면 최소 16비트 그리고 `short` 크기 이상인 정수형
- int는 기본 정수! 그냥 '정수(integer)'라는 의미
- 따라서, CPU에게 앞뒤 생략하고 '정수 처리해!' 라고 하면 CPU가 딱 아는 크기여야 함
- 그게 무엇의 크기일까?
  - CPU의 산술논리장치(ALU, Arithmetic Logic Unit)가 사용하는 기본 데이터
  - 이 데이터를 워드(word)라 하고, 그 크기를 워드 크기라고 함
  - 워드 크기는 레지스터 크기랑 일치 (레지스터는 나중에 배움)
- 즉, CPU에 따라 다름
- 예전에는 16비트 CPU가 흔했음 -> 그래서 표준에는 최소 16비트라고 적혀 있음

### int와 64비트 플랫폼
- 그 뒤에 32비트 컴퓨터가 나오면서 `int`의 크기는 32비트가 됨
- 그러나 이제 64비트 컴퓨터인데? 그래도 32비트로 머묾(...)
  - 원칙적으로 말하면 c 표준을 어긴 것
  - 그러나 64비트로 올리면 32비트 정수를 어떻게 표현하지? (...)
  - 너무 오랜동안 32비트를 `int`의 크기로 사용(다른 언어들도 마찬가지!)
  - 32비트에서 64비트로 바꾼다고 성능이 무조건 빨라지지도 않음
  (이유 : 캐시 메모리 등)
  - `int`를 64비트로 올리면 `short`은...? 32비트가 되야 하나..?

### int로 표현 가능한 숫자의 범위
- 포팅에 안전한 범위 : `short`와 같음
- 표준에 상관없이 보통 안전하게 생각해도 되는 것
  1. 크기 : 16 비트
  2. 범위 
      - 부호 없는 경우(unsigned) : 0 ~ 4,294,967,295
      - 부호 있는 경우(signed) : -2,147,483,648 ~ 2,147,483,647

### int의 리터럴
- 리터럴(literal)
  - 'u'혹은 'U' : 부호 없는(unsigned) 수를 표현하는 접미사
    - 부호 있는 수의 최댓값보다 큰 값을 unsigned int에 대입할 경우
    'u' 혹은 'U'를 붙여야 함
    - 안붙이면 경고(warining) 발생

### long
- `int`가 16비트일 때 그것보다 2배 큰 자료형이 필요했음
- 따라서, `long`은 최소 32비트이고 `int` 이상의 크기(...)
  - 다른 언어에서는 `long`이 보통 64비트
- 그럼 최소 64비트인 정수형은?
  - C89에는 없다.
- 포팅에 안전한 범위 : -2,147,483,647 ~ 2,147,483,647
- 표준에 상관없이 보통 안전하게 생각해도 되는 것
  - `int`와 같음

### long의 리터럴
- 'l' 혹은 'L' : long을 의미하는 접미사
- 'u' 혹은 'U' : 부호 없는(unsigned) 수를 표현하는 접미사
- 두 접미사를 같이 쓸 수 있음 : unsigned long이라는 의미가 됨
`214783645UL`, `214783645LU`, `214783645lu`, `214783645ul`


### float
- 표준에 따르면 C의 `float`은 
  - IEEE 754일 수도 아닐 수도 있음
  - 컴파일러 구현에 따라 다름
  - 크기는 `char`이상이기만 하면 됨
- `unsigned` 형 없음
- 표준에 상관없이 보통 안전하게 생각해도 되는 것
  - 크기 : 32비트
  - 범위 : IEEE 754 Single과 동일
- 관련 헤더 파일 : float.h

### float의 리터럴
- 리터럴 
  - `f`혹은 `F` : float을 의미하는 접미사

### double 
- 표준애 따르면 CP가 계산에 사용하는 기본 데이터 크기
  - 크기는 `float` 이상이면 됨
  - `float`은 그저 `double`보다 빠르게 연산하기 위해 만든 작은 부동소수점(...)
- 역시 컴파일러 구현따라 다름
  - IEEE 754 Double이라는 보장이 없음
- `unsigned` 없음
- 표준에 상관없이 보통 안전하게 생각해도 되는 것
  - 크기 : 64비트
  - 범위 : IEEE 754 Double과 동일
- 관련 헤더 파일 : float.h

### long double
- `double`보다 정밀도가 높음
- `double`이상의 크기면 됨
- 다른 부동소수점들과 마찬가지로 `unsigned`형 없음
- 관련 헤더 파일 : float.h

### 여기서 얻을 수 있는 교훈
- 데스크톱에서는 다른 언어와 비슷하게 사용 가능
  - 예외 : `long`(32비트)
- 소형 기기를 다룰 때는?
  - 매뉴얼에서 자료형 크기 확인 후 사용할 것
- 여기저기서 사용할 코드라면?
  - 포팅이 보장되는 범위의 값으로만 사용할 것
  - `float / double`은 플랫폼 사이에 값이 정확히 일치하지 않을 수 있음

#### 서식 문자는 자료형을 어떤 형태로 출력해야 하는지 알려줌

### bool 형
- C89에 없음
- C99에서 (좀 이상한 형태로) 새로 들어옴
- 그러나 대부분의 C 프로그래머들은 `bool`을 사용하지 않음

### bool 형을 안 쓰는 이유
- 정수로 대신 쓸 수 있음
- 0이면 false, 0 이 아니면 true
- 하드웨어ㅔ서도 실제 `bool`이 없음
  - 0 이냐 아니냐만 있음
- 따라서 `while`문의 조건으로 숫자를 사용가능함(...)
  ```c
  int counter = 5;
  
  while (counter--) {  /* 나쁜 조건식 */
    printf("%d\n", counter);
  } 
  ```

### 코딩 표준 : 참, 거짓을 반환해야 할 때는?
- c에서 참이나 거짓을 반환해야 하는 함수의 경우 보통 이렇게 함
  - 거짓일 때는 0을 반환
  - 참일 때는 1을 반환

### 열거형(enum)
- 열거형 

### 변수 선언 위치
- 변수 선언은 반드시 블럭의 시작에서만 해야함
- 코드 중간에 사용하는 변수는 블록 시작에서 선안만 하고 뒤에 대입

### 연산자
- C에는 연산자 우선순위가 있어서 여러 연산자가 같이 사용되면 우선순위에 의해 연산된다.
- 연산자마다 동일한 순위의 연산자가 있을 때 연산자 결합 법칙에 의해 실행된다.

### sizeof()
- 피연산자의 크기를 바이트로 변환해주는 연산자
- 함수가 아니다. 연산자이다
- sizeof()는 컴파일 중에 평가된다
  - 실행 중이 아니라 컴파일 도중에 크기를 찾음
  - 컴파일 할때 모르는 크기는 찾아줄 수 없음
  - `char`형을 넣으면 반드시 1이 반환된다
  - 이 연산자가 반환하는 값은 부호 없는 정수형의 상수로 `size_t` 형이다

### size_t
- 부호 없는 정수형이나 실제 데이터형은 아님
- _t는 typedef를 했다는 힌트
  - typedef는 다른 자료형에 별칭을 붙이는 것
  - 플랫폼에 따라 다른 자료형을 쓰기 위해서 size_t를 typedef 한 것

### size_t의 크기
- C89 표준은 size_t의 크기를 딱히 명시하지 않음
- 단 배열을 만들면 그 배열의 바이트 크기를 얻을 수 있다고 명시함
  - size_t는 최소 그 정도는 담을 수 있는 크기
  - 배열의 크기가 얼마나 커질 수 있냐...
- 보통은 unsigned int를 사용

### size_t 의 용도
- 어떤 것의 크기를 나타내기 위해 사용
- 반복문이나 배열에 접근할 떄 사용
  - 반복문의 카운터 변수에 음수가 필요 없을 때


### . 연산자
- c에는 클래스가 없으므로 함수 호출에 쓸 수 없음
- 단 구조체와 공용체는 있으니 그들의 멤버변수에 접근할 때 사용

### -> 연산자
- 2개의 연산자 '.'와 '*'를 합친 것
- 이 또한 구조체와 공용체의 멤버변수에 접근할 때 사용

### 조건 연산자
- 삼항 연산자
```c
int min = num1 < num2 ? num1: num2
```






