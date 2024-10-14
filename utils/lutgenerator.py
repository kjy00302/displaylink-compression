#!/usr/bin/python3
# BFS based LUT generator
import decomptable_util
import struct
import csv
import os
import sys


table = []

if len(sys.argv) < 2:
    print(f'{sys.argv[0]} decomptable(.csv | .bin)')
    exit()

if sys.argv[1].endswith('.csv'):
    with open(sys.argv[1], newline='') as f:
        table = decomptable_util.from_csv(csv.reader(f))
else:
    with open(sys.argv[1], 'rb') as f:
        table = decomptable_util.unpack(f.read())


def lookup(bool_, idx, acc):
    color, _, _, nextidx = table[idx][bool_ == '1']
    acc += color
    acc &= 0xffff
    if nextidx == 0:
        return (True, 0, acc)
    return (False, nextidx, acc)


def finder(startpoint):
    findings = {}
    works = [('0', startpoint, 0), ('1', startpoint, 0)]
    nextworks = []  # NOTE: queue is slow

    while True:
        for work in works:
            is_end, nextidx, acc = lookup(work[0][0], work[1], work[2])
            if is_end:
                # later findings are more expensive then now
                if not findings.get(acc):
                    findings[acc] = work[0]
            else:
                nextworks.append(('0' + work[0], nextidx, acc))
                nextworks.append(('1' + work[0], nextidx, acc))
        works.clear()
        if nextworks:
            works.extend(nextworks)
            nextworks.clear()
        else:
            break
    return findings


findings_8 = finder(0)
findings_16 = finder(8)

os.makedirs('lut', exist_ok=True)

with open('lut/8_lut_bits.bin', 'wb') as f_bit, \
        open('lut/8_lut_bits_len.bin', 'wb') as f_len:
    for i in range(0x100):
        bitlen = len(findings_8[i])
        bits = int(findings_8[i], 2)
        f_bit.write(bits.to_bytes(2, 'little'))
        f_len.write(bitlen.to_bytes(1, 'little'))

with open('lut/16_lut_bits.bin', 'wb') as f_bit, \
        open('lut/16_lut_bits_len.bin', 'wb') as f_len:
    for i in range(0x1_0000):
        bitlen = len(findings_16[i])
        bits = int(findings_16[i], 2)
        f_bit.write(bits.to_bytes(4, 'little'))
        f_len.write(bitlen.to_bytes(1, 'little'))

# libtubecable compatable table
with open('lut/tubecable_huffman.bin', 'wb') as f:
    for i in range(0x1_0000):
        i = (i + 0x8000) & 0xffff
        bitlen = len(findings_16[i])
        bits = int(findings_16[i], 2)
        f.write(struct.pack('>BI', bitlen, bits))
