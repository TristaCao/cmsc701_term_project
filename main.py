import os, re, array,argparse, time, sys
import huffman
import freq
import random

def show_match(text, huffman, encoding, pattern):
    p = huffman.search(encoding, pattern)
    if (p == None or p == -1) :
        print("No matching found!!")
        return

    text = re.findall(r"[\w']+|[.,!?;]", text)

    for i in range(len(pattern)):
        if pattern[i]!= text[p+i]:
            print("the matching found is INCORRECT!!!")
            return
    print("correct matching at %s th word!"%p)

def shift_or_show_match(text, huffman, encoding, pattern):
    startp, endp = huffman.shift_or_search(encoding, pattern)
    if startp == None or endp == None:
        print("No matching found!!")
        return


    text = re.findall(r"[\w']+|[.,!?;]", text)

    for i in range(len(pattern)):
        if pattern[i]!= text[startp+i]:
            print("the matching found is INCORRECT!!!")
            return
    print("correct matching at %s th word!"%startp)


parser = argparse.ArgumentParser()
#parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
parser.add_argument("-f", "--infile", default = "", help="pass infile to compress")
parser.add_argument( "-p", "--pattern", help="pass pattern to search")
parser.add_argument("-s", "--type", default = "bm", help="choose searching method", choices=["bm", "tso","pso"])


args = parser.parse_args()

if not args.infile == "":
    with open(args.infile) as f:
        in_str = f.read()

    start = time.time()
    freq_dict = freq.str_freq(in_str, True)
    freqs = list(freq_dict.items())

    text = re.findall(r"[\w']+|[.,!?;]", in_str)
    pattern = re.findall(r"[\w']+|[.,!?;]", args.pattern)


    if type == "tso":
        # Tagged Shift-Or
        tagged_huffman = huffman.HuffmanCode(freqs, 128, True)
        tagged_encoding = tagged_huffman.encode(in_str, True)
        shift_or_show_match(in_str,tagged_huffman, tagged_encoding, pattern)
    elif type == "pso":
        # Shift-Or Plain Huffman
        plain_huffman = huffman.HuffmanCode(freqs, 256)
        plain_encoding = plain_huffman.encode(in_str, True)
        shift_or_show_match(in_str,plain_huffman, plain_encoding, pattern)
    else:
        # Boyer Moore
        tagged_huffman = huffman.HuffmanCode(freqs, 128, True)
        tagged_encoding = tagged_huffman.encode(in_str, True)
        show_match(in_str,tagged_huffman, tagged_encoding, pattern)
    end = time.time()
    print("pattern searched in %s second"%(end-start))

else:
    for i in range(0,10):
        path="testdata/testdata"+ str(i)
        with open(path) as f:
            in_str = f.read()


        freq_dict = freq.str_freq(in_str, True)
        freqs = list(freq_dict.items())
        tagged_huffman = huffman.HuffmanCode(freqs, 128, True)
        tagged_encoding = tagged_huffman.encode(in_str, True)
        text = re.findall(r"[\w']+|[.,!?;]", in_str)


        start = time.time()
        for r in range(0,len(text)-10,int((len(text)-10)/10)):

            pattern = text[r:r+10]

            show_match(in_str,tagged_huffman, tagged_encoding, pattern)
        end = time.time()
        print(str(i)+"k=1 BM search time:", end - start)

        start = time.time()
        for r in range(0,len(text)-10,int((len(text)-10)/10)):
            pattern = text[r:r+10]
            shift_or_show_match(in_str,tagged_huffman, tagged_encoding, pattern)
        end = time.time()
        print(str(i)+"k=1 TAGGED Shift-Or search time:", end - start)

        """PLAIN huffman shift-or"""
        plain_huffman = huffman.HuffmanCode(freqs, 256)
        plain_encoding = plain_huffman.encode(in_str, True)
        start = time.time()

        for r in range(0,len(text)-10,int((len(text)-10)/10)):
            pattern = text[r:r+10]
            shift_or_show_match(in_str,plain_huffman, plain_encoding, pattern)
        end = time.time()
        print(str(i)+"k=1 PLAIN Shift-Or search time:", end - start)
