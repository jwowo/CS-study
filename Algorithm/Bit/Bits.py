from random import randint

def nth_bit_on(n):
    return (1 << n)

"""
print(bin(nth_bit_on(0)))
print(nth_bit_on(0))

print(bin(nth_bit_on(1)))
print(nth_bit_on(1))

print(bin(nth_bit_on(2)))
print(nth_bit_on(2))

print(bin(nth_bit_on(3)))
print(nth_bit_on(3))

print(bin(nth_bit_on(4)))
print(nth_bit_on(4))
"""

def get_nth_bit(n, nth):
    return 1 if n & (1 << nth) else 0

def get_nth_bit_no(n, nth):
    return n & (1 << nth)

"""
print('10진수 100을 2진수로 변환한 값:', bin(100))
print(get_nth_bit(100, 2))
print(get_nth_bit_no(100, 2))
"""

def get_trailing_bits(n, count):
    return n & ((1 << count) - 1)

N = randint(1, 2 ** 32)
last_4_bits = get_trailing_bits(N, 4)

"""
print('N은', N, ', 2진수로는', bin(N), '입니다.')
print('이때 N의 마지막 4개의 비트는', '{:04b}'.format(last_4_bits), '입니다.')
print(last_4_bits)

print(9 & (1 << 1) - 1)
print(9 & (1 << 2) - 1)
print(9 & (1 << 3) - 1)
print(9 & (1 << 4) - 1)
"""

### 정수의 2의 지수승 여부 확인하기

def is_exp_binary(n):
    return n & (n - 1) == 0

print(1, is_exp_binary(2 ** 0))
print(2, is_exp_binary(2 ** 1))
print(4, is_exp_binary(2 ** 2))
print(1024, is_exp_binary(2 ** 10))

print(3, is_exp_binary(3))
print(15, is_exp_binary(15))
print(101, is_exp_binary(101))
print(1000, is_exp_binary(1000))