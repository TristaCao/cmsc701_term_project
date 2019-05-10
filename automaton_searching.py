import huffmancoding 
import heapq
import contextlib, sys
python3 = sys.version_info.major >= 3


# Returns a frequency table based on the bytes in the given file.
# Also contains an extra entry for symbol 256, whose frequency is set to 0.
def get_frequencies(filepath):
    freqs = huffmancoding.FrequencyTable([0] * 257)
    with open(filepath, "rb") as input:
        while True:
            b = input.read(1)
            if len(b) == 0:
                break
            b = b[0] if python3 else ord(b)
            freqs.increment(b)
    return freqs


def write_code_len_table(bitout, canoncode):
    for i in range(canoncode.get_symbol_limit()):
        val = canoncode.get_code_length(i)
        # For this file format, we only support codes up to 255 bits long
        if val >= 256:
            raise ValueError("The code for a symbol is too long")
        
        # Write value as 8 bits in big endian
        for j in reversed(range(8)):
            bitout.write((val >> j) & 1)



def compress(code, inp):
    result = ''
    enc = huffmancoding.HuffmanEncoder()
    enc.codetree = code
    for b in inp:
        result += enc.write(ord(b))
    result += enc.write(256)  # EOF
    return result


def decompress(code, text):
    dec = huffmancoding.HuffmanDecoder(text)
    dec.codetree = code
    result = ''
    while True:
        symbol = dec.read()
        if symbol == 256:  # EOF symbol
            break
        b= chr(symbol)
        result += b
    return result
        

def mark_dic(pattern, code, freqs):
    mark_dic = ['0'*len(pattern)]*len(freqs)
    for i,byte in enumerate(pattern):
        try:
            mark = '0' *len(pattern)
            mark = mark[:i]+'1'+mark[i+1:]                
            compress(code, byte)
            old = mark_dic[ord(byte)]
            new =  str(int(old) + int(mark))
            new = '0'*(len(pattern)-len(new)) + new
            mark_dic[ord(byte)] = new
        except ValueError as e:  # as e syntax added in ~python2.5
            if str(e) != "No code for given symbol":
                raise
            else:
                return None
    for i, mark in enumerate(mark_dic):
        m = ''
        for b in mark:
            m += '1' if b=='0' else '0'
        mark_dic[i] = '0'+m
    return mark_dic

def bitwise_or(str1, str2):
    assert len(str1) == len(str2)
    result = ''
    for i in range(len(str1)):
        if str1[i] == '1' or str2[i] == '1':
            result += '1'
        else:
            result += '0'
    return result

def shift_right(str1):
    #shift right and pad first bit as 0
    result = '0'
    for i in range(len(str1)-1):
        result += str1[i]
    return result

def shift_or_search(text, pmarks, plen):
    r = '1'+'1'*plen
    for i,char in enumerate(text):
        r = shift_right(r)
        mark = pmarks[ord(char)]
        result = bitwise_or(r, mark)
        r = result
        if result[-1] == '0':
            i += 1
            return i-plen, i
    return None, None

def main(args):
    inputfile = "test_text.txt"
    patternf = "test_pattern.txt"
    freqs = get_frequencies(inputfile)
    freqs.increment(256)  # EOF symbol gets a frequency of 1
    code = freqs.build_code_tree()
    canoncode = huffmancoding.CanonicalCode(tree=code, symbollimit=freqs.get_symbol_limit())
    # Replace code tree with canonical one. For each symbol,
    # the code value may change but the code length stays the same.
    code = canoncode.to_code_tree()
    input_text = "Donald John Trump is the 45th and current president of the United States. Before entering politics, he was a businessman and television personality. Trump was born and raised in the New York City borough of Queens and received an economics degree from the Wharton School."
    encoded_text = compress(code,input_text)
    
    
    # encoded_text and code are supposed to be provided
    # we make them here
    # Now starts the searching
    pattern = "New York City"
    decoded_text = decompress(code, encoded_text)
    pmarks = mark_dic(pattern, code, freqs.frequencies)
    start, end = shift_or_search(decoded_text, pmarks, len(pattern))
    print(decoded_text[start:end])
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
    
    
    
    

