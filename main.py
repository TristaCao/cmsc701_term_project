import os, re, array,argparse, time, sys
import huffman
import freq
import random

def show_match(text, huffman, encoding, pattern):
    p = huffman.search(encoding, pattern)
    if (p == None or p == -1) :
        print("No matching found!!")
        return

    #pattern = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(pattern)
    #text = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(text)
    #pattern = re.findall(r"[\w']+|[.,!?;]", pattern)
    text = re.findall(r"[\w']+|[.,!?;]", text)

    for i in range(len(pattern)):
        if pattern[i]!= text[p+i]:
            print("the matching found is INCORRECT!!!")
            return
    #print("correct matching!!!!!!!!")

def shift_or_show_match(text, huffman, encoding, pattern):
    startp, endp = huffman.shift_or_search(encoding, pattern)
    if startp == None or endp == None:
        print("No matching found!!")
        return

    #pattern = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(pattern)
    #text = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(text)
    #pattern = re.findall(r"[\w']+|[.,!?;]", pattern)
    text = re.findall(r"[\w']+|[.,!?;]", text)

    for i in range(len(pattern)):
        if pattern[i]!= text[startp+i]:
            print("the matching found is INCORRECT!!!")
            return
    #print("correct matching!!!!!!!!")


parser = argparse.ArgumentParser()
#parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
parser.add_argument("-f", "--infile", default = "", help="pass infile to huff-compress/decompress for compression/decompression")
args = parser.parse_args()

if not args.infile == "":
    with open(args.infile) as f:
        in_str = f.read()

    freq_dict = freq.str_freq(in_str)
    freqs = list(freq_dict.items())
    original_len = len(in_str)
    ascii_encoding = huffman.ascii_encode(in_str) # 8-bit ascii encoding.


    """
    binary huffman:
    for binary huffman, we compare the compressed binary string to the ascii string that
    directly translated from the original text.

    """
    start = time.time()
    binary_huffman = huffman.HuffmanCode(freqs, 2)
    binary_encoding = binary_huffman.encode(in_str)
    end = time.time()
    print("binary huffman: ")
    print("\tcompress time: ", end - start)
    print("\tcompressed rate:", len(binary_encoding)/len(ascii_encoding))
    print()


    freq_dict = freq.str_freq(in_str, True)
    freqs = list(freq_dict.items())


    """
    plain huffman:
    here we compare the compressed string that formed by the byte-oriented coding of
    each words, to the original text.

    """
    start = time.time()
    plain_huffman = huffman.HuffmanCode(freqs, 256)
    plain_encoding = plain_huffman.encode(in_str, True)
    end = time.time()
    print("plain huffman: ")
    print("\tcompress time: ", end - start)
    print("\tcompressed rate:", len(plain_encoding)/original_len)
    print()


    """
    tagged huffman:
    here we compare the compressed string that formed by the byte-oriented coding of
    each words, to the original text.
    this way we can search using a regular searching algorithm

    """
    start = time.time()
    tagged_huffman = huffman.HuffmanCode(freqs, 128, True)
    tagged_encoding = tagged_huffman.encode(in_str, True)
    end = time.time()
    print("tagged huffman: ")
    print("\tcompress time: ", end - start)
    print("\tcompressed rate:", len(tagged_encoding)/original_len)
    print()


for i in range(0,10):
    path="testdata/testdata"+ str(i)
    with open(path) as f:
        in_str = f.read()


    freq_dict = freq.str_freq(in_str, True)
    freqs = list(freq_dict.items())
    tagged_huffman = huffman.HuffmanCode(freqs, 128, True)
    tagged_encoding = tagged_huffman.encode(in_str, True)
    #text = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(in_str)
    text = re.findall(r"[\w']+|[.,!?;]", in_str)


    start = time.time()
    for r in range(0,len(text)-10,int((len(text)-10)/10)):
        #pattern = "".join(text[r:r+10])
        #print(pattern)
        pattern = text[r:r+10]

        show_match(in_str,tagged_huffman, tagged_encoding, pattern)
    end = time.time()
    print(str(i)+"k=1 BM search time:", end - start)

    start = time.time()
    for r in range(0,len(text)-10,int((len(text)-10)/10)):
        #pattern = "".join(text[r:r+10])
        pattern = text[r:r+10]
        shift_or_show_match(in_str,tagged_huffman, tagged_encoding, pattern)
    end = time.time()
    print(str(i)+"k=1 TAGGED Shift-Or search time:", end - start)

    """PLAIN huffman shift-or"""
    plain_huffman = huffman.HuffmanCode(freqs, 256)
    plain_encoding = plain_huffman.encode(in_str, True)
    start = time.time()

    for r in range(0,len(text)-10,int((len(text)-10)/10)):
        #pattern = "".join(text[r:r+10])
        pattern = text[r:r+10]
        shift_or_show_match(in_str,plain_huffman, plain_encoding, pattern)
    end = time.time()
    print(str(i)+"k=1 PLAIN Shift-Or search time:", end - start)
