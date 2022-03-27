// 자바스크립트는 synchronous(동기적)이다.
// 코드가 호이스팅이 된 이후부터 작성한 순서에 맞춰서 하나하나씩 동기적으로 실행된다.
// 호이스팅이란? var, 함수 선언들이 제일 위로 올라가는 것

// 콜백함수를 사용하는 두가지 경우 (모든 함수의 선언은 호이스팅되기때문에 제일 위로 올라간다)
// synchronous callback
function printImmediately(print) {
  print();
}

// asynchronous callback
function printWithDelay(print, timeout) {
  setTimeout(print, timeout);
}

console.log('1');
console.log('2');
console.log('3');
// 순서대로 실행된다.

// asynchonouse는 언제 코드가 실행될지 예측할 수 없는 것.

// 좋은 예로 setTimeout()이 있다. 브라우저에서 제공되는 api로 지정한 시간이 지나면 전달한 콜백함수를 호출하는 것이다.
// 콜백함수란? 전달해준 함수를 나중에 불러줘~라는 개념이다. 지금 당장 실행하진 않고 나중에 이 함수를 호출해줘~ 해서 콜백함수이다.

console.log('1'); // 동기
setTimeout(() => console.log('2'), 1000); // 비동기
console.log('3'); // 동기
printImmediately(() => console.log('hello')); // 동기
printWithDelay(() => console.log('async callback'), 2000); // 비동기

// 자바스크립트는 함수를 콜백 형태로 다른 함수의 인자로, 변수에 할당할 수도 있는 언어이다.

// 콜백 지옥의 문제점
// 1. 가독성이 떨어진다. 비지니스 로직을 한 눈에 이해하기 어렵다.
// 2. 유지 보수도 어렵다.
// -> async await
