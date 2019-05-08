import os, re, array,argparse, time, sys
import huffman
import freq

def show_match(text, huffman, encoding, pattern):
    p = huffman.search(encoding, pattern)
    if (p == None or p == -1) :
        print("No matching found!!")
        return

    pattern = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(pattern)
    text = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(text)

    for i in range(len(pattern)):
        if pattern[i]!= text[p+i]:
            print("the matching found is INCORRECT!!!")
            return
    print("correct matching!!!!!!!!")


parser = argparse.ArgumentParser()
parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
args = parser.parse_args()


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
pattern = 'she walk'
show_match(in_str,tagged_huffman, tagged_encoding, pattern)
