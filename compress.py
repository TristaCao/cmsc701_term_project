import os, re, array,argparse, time, sys
import huffman
import freq
import random
import matplotlib.pyplot as plt

binary, plain, tagged, length = [], [], [], []
binaryR, plainR, taggedR = [], [], []
length = [35,69,105,140,177,212,246,281,315,348]

for i in range(0,10):
    path="testdata/testdata"+ str(i)
    with open(path) as f:
        in_str = f.read()


    freq_dict = freq.str_freq(in_str)
    freqs = list(freq_dict.items())
    original_len = len(in_str)
    ascii_encoding = huffman.ascii_encode(in_str)

    start = time.time()
    binary_huffman = huffman.HuffmanCode(freqs, 2)
    binary_encoding = binary_huffman.encode(in_str, True)
    end = time.time()
    binary.append(end-start)
    binaryR.append(len(binary_encoding)/8/original_len)

    freq_dict = freq.str_freq(in_str, True)
    freqs = list(freq_dict.items())

    start = time.time()
    plain_huffman = huffman.HuffmanCode(freqs, 256)
    plain_encoding = plain_huffman.encode(in_str, True)
    end = time.time()
    plain.append(end-start)
    plainR.append(len(plain_encoding)/original_len)


    start = time.time()
    tagged_huffman = huffman.HuffmanCode(freqs, 128, True)
    tagged_encoding = tagged_huffman.encode(in_str, True)
    end = time.time()

    tagged.append(end-start)
    taggedR.append(len(tagged_encoding)/original_len)

plt.figure(1)
plt.subplot(221)
plt.plot(length, binary, 'r--', label = 'binary')
plt.plot(length, plain, 'b--', label = 'plain')
plt.plot(length, tagged, 'g--', label = 'tagged')
plt.title("compression time")
plt.legend(('Binary', 'Plain', 'Tagged'),
           loc='upper left')


#plt.axis([0, 6, 0, 20])
plt.subplot(222)
plt.plot(length, binaryR, 'r--', label = 'binary')
plt.plot(length, plainR, 'b--', label = 'plain')
plt.plot(length, taggedR, 'g--', label = 'tagged')
plt.title("compression rate (compressed text/original text)")
plt.xlabel('file size (KB)')
plt.legend(('Binary', 'Plain', 'Tagged'),
           loc='upper left')
plt.show()
