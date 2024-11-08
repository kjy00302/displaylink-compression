# DisplayLink DL-1x0의 압축 기술 분석

이 문서는 1세대 DisplayLink 장치가 압축된 데이터를 전송하는 데 사용하는 압축 방식을 서술한다.

## 압축의 동작 방식

압축 방식은 Tubecable 개발자의 분석대로 일종의 Huffman 부호화를 사용하나, 모든 값에 대해 코드를 지정한 것은 아니다. 그 대신 값을 저장하는 누산기를 두었다. 입력에 따라 트리를 순회하면서 노드에 지정된 값을 누산기에 더하고, 다음 행이 0인 경우를 끝으로 간주해 지금까지 누산기에 저장된 값을 사용하게 된다.

![Decompression flows](./img/dlcomp.svg)

## 압축 테이블의 구조

압축 테이블의 한 노드는 총 9바이트로 구성된다. 이는 다음과 같은 필드로 구성된다.

![Compression table row](./img/comprow.svg)

한 노드는 다시 2개의 요소로 분해가 가능하다.

|요소|색상|바이트|부울|다음 노드|
| :--- | :--- | :--- | :--- | :--- |
|A|ShortA|Byte1A|bool(Byte2A & 0x60)|(Byte2A & 0x1f) << 4 | ByteAB >> 4|
|B|ShortB|Byte1B|bool(Byte2B & 0x60)|(Byte2B & 0x1f) << 4 | ByteAB & 0x0f|

각 요소의 필드는 다음과 같은 역할을 한다.

 - 색상: 색상 누산기에 더할 색상.
 - 바이트: 아직 파악되지 않음.
 - 부울: 아직 파악되지 않음.
 - 다음 노드: 이동할 노드의 번호.

## 예시: 비트스트림 `111000`이 `0xF800`으로 해석되는 과정

![decompression figure](./img/decoding.svg)

## 유틸리티들

### decomptable_util.py

장치에 전송되는 압축 테이블을 조작하기 위한 파이썬 모듈이다.

    ./decomptable_util.py decomptable.bin

### generate_graph.py

압축 테이블의 그래프 (DOT 언어 형태)를 표준 출력으로 출력한다.

    ./generate_graph.py decomptable.bin > graph.dot

예: [Tubecable의 압축 테이블](https://github.com/floe/tubecable/blob/db650b417c1d9ffd9b0e5d93ac167176f337f177/tubecable.c#L325)로 생성된 [그래프](./img/tubecable_huffman.svg)

### lutgenerator.py

장치에 전송되는 압축된 색상 값을 생성한다.

    ./lutgenerator.py decomptable.bin
