# DisplayLink DL-1x0 compression technology analysis

**This document is README.ko.md file translated with Google Translator.**

This document describes the compression method used by the first generation DisplayLink devices to transmit compressed data.

## How the compression works

The compression method uses a type of Huffman encoding as analyzed by the Tubecable developer, but it does not designate a code for every value. Instead, it has an accumulator that stores value. As the tree is traversed based on the input, the value assigned to the node is added to the accumulator, and if the next row is 0, it is considered the end and the value stored in the accumulator so far is used.

![Decompression flows](./img/dlcomp.svg)

## Structure of the decompression table

A node of the decompression table consists of a total of 9 bytes. It consists of the following fields:

![Compression table row](./img/comprow.svg)

A node can be further decomposed into two elements.

|Element|Color|UnkByte|UnkBool|NextNode|
| :--- | :--- | :--- | :--- | :--- |
|A|ShortA|Byte1A|bool(Byte2A & 0x60)|(Byte2A & 0x1f) << 4 | ByteAB >> 4|
|B|ShortB|Byte1B|bool(Byte2B & 0x60)|(Byte2B & 0x1f) << 4 | ByteAB & 0x0f|

The fields in each element have the following roles:

 - Color: The color to add to the color accumulator.
 - UnkByte: Not yet figured out.
 - UnkBool: Not yet figured out.
 - NextNode: The number of the node to move to.

## Example: How the bitstream `111000` is interpreted as `0xF800`

![decompression figure](./img/decoding.svg)

## Utilities

### decomptable_util.py

A Python module for manipulating the decompression table transmitted to the device.

    ./decomptable_util.py decomptable.bin

### generate_graph.py

Prints the graph (in DOT language format) of the decompression table to standard output.

    ./generate_graph.py decomptable.bin > graph.dot

Example: Generated [graph](./img/tubecable_huffman.svg) of [decompression table from Tubecable](https://github.com/floe/tubecable/blob/db650b417c1d9ffd9b0e5d93ac167176f337f177/tubecable.c#L325)

### lutgenerator.py

Generates compressed color values ​​that are transmitted to the device.

    ./lutgenerator.py decomptable.bin
