#!/usr/bin/python3
# Decompress table utility
import struct
import csv
import sys


def pack(data):
    return b''.join((struct.pack(
        '>HBBBHBB',
        row[0][0], row[0][1], 0x60 * row[0][2] | row[0][3] >> 4,
        (row[0][3] & 0xf) << 4 | (row[1][3] & 0xf),
        row[1][0], row[1][1], 0x60 * row[1][2] | row[1][3] >> 4,
    ) for row in data))


def unpack(data):
    return [(
        # rgb565, pixelcount?, unknown, next row number
        (h_a, b1_a, bool(b2_a & 0x60), (b2_a & 0x1f) << 4 | b_ab >> 4),
        (h_b, b1_b, bool(b2_b & 0x60), (b2_b & 0x1f) << 4 | b_ab & 0xf)
    ) for h_a, b1_a, b2_a, b_ab, h_b, b1_b, b2_b in
        struct.iter_unpack('>HBBBHBB', data)]


def from_csv(reader):
    return [(
        (int(color_a, 16), int(count_a), bool_a == 'True', int(next_a)),
        (int(color_b, 16), int(count_b), bool_a == 'True', int(next_b))
    ) for color_a, count_a, bool_a, next_a,
        color_b, count_b, bool_b, next_b in reader]


def to_csv(data, writer):
    # writer.writerow("ffff bool ff 1ff ffff bool ff 1ff".split())
    for row in data:
        writer.writerow((
            f"{row[0][0]:04x}", row[0][1], row[0][2], row[0][3],
            f"{row[1][0]:04x}", row[1][1], row[1][2], row[1][3],
        ))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'{sys.argv[0]} decomptable(.csv | .bin)')
        exit()
    fname = sys.argv[1]
    if fname.endswith('.csv'):
        # pack
        with open(fname, newline='') as f:
            with open(fname.removesuffix('.csv')+'.new', 'wb') as g:
                g.write(pack(from_csv(csv.reader(f))))
    else:
        # unpack
        with open(fname, 'rb') as f:
            with open(f'{fname}.csv', 'w', newline='') as g:
                to_csv(unpack(f.read()), csv.writer(g))
