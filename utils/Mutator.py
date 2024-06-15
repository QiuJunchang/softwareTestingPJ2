import math
import random
import struct
from typing import Any


def insert_random_character(s: str) -> str:
    """
    向 s 中下标为 pos 的位置插入一个随机 byte
    pos 为随机生成，范围为 [0, len(s)]
    插入的 byte 为随机生成，范围为 [32, 127]
    """
    pos = random.randint(0, len(s))
    random_byte = chr(random.randint(32, 127))
    return s[:pos] + random_byte + s[pos:]


def flip_random_bits(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 bitflip 与 random havoc 实现相邻 N 位翻转（N = 1, 2, 4），其中 N 为随机生成
    从 s 中随机挑选一个 bit，将其与其后面 N - 1 位翻转（翻转即 0 -> 1; 1 -> 0）
    注意：不要越界
    """
    bytes_list = bytearray(s, 'utf-8')
    bit_length = len(bytes_list) * 8

    if bit_length == 0:
        return s  # 如果输入字符串为空，直接返回

    N = random.choice([1, 2, 4])

    if bit_length < N:
        N = bit_length  # 调整 N 以避免越界

    pos = random.randint(0, bit_length - N)
    
    for i in range(N):
        byte_index = (pos + i) // 8
        bit_index = (pos + i) % 8
        bytes_list[byte_index] ^= 1 << bit_index
    
    return bytes_list.decode('utf-8', errors='ignore')


def arithmetic_random_bytes(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 arithmetic inc/dec 与 random havoc 实现相邻 N 字节随机增减（N = 1, 2, 4），其中 N 为随机生成
    字节随机增减：
        1. 取其中一个 byte，将其转换为数字 num1；
        2. 将 num1 加上一个 [-35, 35] 的随机数，得到 num2；
        3. 用 num2 所表示的 byte 替换该 byte
    从 s 中随机挑选一个 byte，将其与其后面 N - 1 个 bytes 进行字节随机增减
    注意：不要越界；如果出现单个字节在添加随机数之后，可以通过取模操作使该字节落在 [0, 255] 之间
    """
    bytes_list = bytearray(s, 'utf-8')
    
    if len(bytes_list) == 0:
        return s  # 如果输入字符串为空，直接返回

    N = random.choice([1, 2, 4])
    
    if len(bytes_list) <= N:
        N = len(bytes_list)

    pos = random.randint(0, len(bytes_list) - N)

    for i in range(N):
        num1 = bytes_list[pos + i]
        num2 = (num1 + random.randint(-35, 35)) % 256
        bytes_list[pos + i] = num2

    return bytes_list.decode('utf-8', errors='ignore')


def interesting_random_bytes(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 interesting values 与 random havoc 实现相邻 N 字节随机替换为 interesting_value（N = 1, 2, 4），其中 N 为随机生成
    interesting_value 替换：
        1. 构建分别针对于 1, 2, 4 bytes 的 interesting_value 数组；
        2. 随机挑选 s 中相邻连续的 1, 2, 4 bytes，将其替换为相应 interesting_value 数组中的随机元素；
    注意：不要越界
    """
    interesting_values_1 = [0, 1, 255]
    interesting_values_2 = [0, 1, 32767, 65535]
    interesting_values_4 = [0, 1, 2147483647, 4294967295]
    
    bytes_list = bytearray(s, 'utf-8')
    
    if len(bytes_list) == 0:
        return s  # 如果输入字符串为空，直接返回原字符串

    N = random.choice([1, 2, 4])
    
    if len(bytes_list) < N:
        N = len(bytes_list)

    pos = random.randint(0, len(bytes_list) - N)

    if N == 1:
        value = random.choice(interesting_values_1)
        struct.pack_into('B', bytes_list, pos, value)
    elif N == 2:
        value = random.choice(interesting_values_2)
        struct.pack_into('H', bytes_list, pos, value)
    elif N == 4:
        value = random.choice(interesting_values_4)
        struct.pack_into('I', bytes_list, pos, value)
    
    return bytes_list.decode('utf-8', errors='ignore')


def havoc_random_insert(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 random havoc 实现随机插入
    随机选取一个位置，插入一段的内容，其中 75% 的概率是插入原文中的任意一段随机长度的内容，25% 的概率是插入一段随机长度的 bytes
    """
    pos = random.randint(0, len(s))
    if random.random() < 0.75:
        if len(s) == 0:
            return s  # 如果输入字符串为空，直接返回
        start = random.randint(0, len(s) - 1)
        end = random.randint(start, len(s))
        return s[:pos] + s[start:end] + s[pos:]
    else:
        random_bytes = ''.join(chr(random.randint(32, 127)) for _ in range(random.randint(1, 10)))
        return s[:pos] + random_bytes + s[pos:]


def havoc_random_replace(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 random havoc 实现随机替换
    随机选取一个位置，替换随后一段随机长度的内容，其中 75% 的概率是替换为原文中的任意一段随机长度的内容，25% 的概率是替换为一段随机长度的 bytes
    """
    if len(s) == 0:
        return s  # 如果输入字符串为空，直接返回

    start = random.randint(0, len(s) - 1)
    end = random.randint(start, len(s))
    
    if random.random() < 0.75:
        if len(s) == 0:
            return s  # 再次检查空字符串
        replacement_start = random.randint(0, len(s) - 1)
        replacement_end = random.randint(replacement_start, len(s))
        replacement = s[replacement_start:replacement_end]
    else:
        replacement = ''.join(chr(random.randint(32, 127)) for _ in range(end - start))
    
    return s[:start] + replacement + s[end:]


class Mutator:

    def __init__(self) -> None:
        """Constructor"""
        self.mutators = [
            insert_random_character,
            flip_random_bits,
            arithmetic_random_bytes,
            interesting_random_bytes,
            havoc_random_insert,
            havoc_random_replace
        ]

    def mutate(self, inp: Any) -> Any:
        mutator = random.choice(self.mutators)
        return mutator(inp)
