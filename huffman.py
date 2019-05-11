from tree import TreeNode
import bisect
import math
import re
import bm

def huffman_initial_count(message_count, digits):
    """
    Return the number of messages that must be grouped in the first layer for
    Huffman Code generation.
    """

    if message_count <= 0:
        raise ValueError("cannot create Huffman tree with <= 0 messages!")
    if digits <= 1:
        raise ValueError("must have at least two digits for Huffman tree!")

    if message_count == 1:
        return 1

    return 2 + (message_count - 2) % (digits - 1)

def combine_and_replace(nodes, n):
    """
    Combine n nodes from the front of the low-to-high list into one whose key is
    the sum of the merged nodes. The new node's data is set to None, then
    inserted into its proper place in the list.

    Note: The sum of keys made here is the smallest such combination.

    In the contradictory style of Huffman, if any set of nodes were chosen
    except for the first n, then changing a node not in the first n to one that
    is from the first n would reduce the sum of their keys. Thus the smallest
    sum is made from the first n nodes.

    :nodes: A list of TreeNodes.
    :n: Integer < len(nodes).
    :returns: Low-to-high list that combines the last n nodes into one.
    """
    group = nodes[:n]
    combined = TreeNode(sum(node.key for node in group), None, group)
    nodes = nodes[n:]
    bisect.insort(nodes, combined)

    return nodes

def huffman_nary_tree(probabilities, digits):
    """Return a Huffman tree using the given number of digits.

    This `digits`-ary tree is always possible to create. See ./notes.md.

    :probabilities: List of tuples (symbol, probability) where probability is
                    any floating point and symbol is any object.
    :digits: Integral number of digits to use in the Huffman encoding. Must be
             at least two.
    :returns: TreeNode that is the root of the Huffman tree.
    """
    if digits <= 1:
        raise ValueError("must have at least 2 digits!")

    if len(probabilities) == 0:
        raise ValueError("cannot create a tree with no messages!")

    if len(probabilities) == 1:
        symbol, freq = probabilities[0]
        if freq != 1:
            print("The probabilities sum to {} (!= 1)...".format(freq))
        if math.isclose(probabilities[0].key, 1.0):
            print("(but they are close)")

        return TreeNode(freq, symbol)

    # TreeNode does rich comparison on key value (probability), so we can
    # pass this right to sorted().
    probabilities = [TreeNode(freq, symbol) for (symbol, freq) in probabilities]
    probabilities = sorted(probabilities)

    # Grab the required first set of messages.
    initial_count = huffman_initial_count(len(probabilities), digits)
    probabilities = combine_and_replace(probabilities, initial_count)

    # If everything is coded correctly, this loop is guaranteed to terminate
    # due to the initial number of messages merged.
    while len(probabilities) != 1:
        # Have to grab `digits` nodes from now on to meet an optimum code requirement.
        probabilities = combine_and_replace(probabilities, digits)

    if probabilities[0].key != 1:
        print("The probabilities sum to {} (!= 1)...".format(probabilities[0].key))
        if math.isclose(probabilities[0].key, 1.0):
            print("(but they are close)")

    return probabilities.pop()

def indicies_to_code(path, digits, tagged):
    """Convert the path into a string.

     We join the indices directly, from most to least significant, keeping
     leading zeroes.
     Examples:
       [1, 2, 3] -> "123"
       [7, 2, 10] -> "72a"
       [0, 2, 1] ->  "021"
    """
    combination = ""
    for index in path:
        if index < 0:
            raise ValueError("cannot accept negative path indices (what went wrong?)")
        if index >= digits:
            raise ValueError("cannot have an index greater than the number of digits!")

        combination += baseN(index, digits, tagged)

    return combination

def huffman_nary_dict(probabilities, digits, tagged):
    """Return a dictionary that decodes messages from the nary Huffman tree.

    This gives a method of _decoding_, but not _encoding_. For that, an inverse
    dictionary will need to be created. See inverse_dict().

    :probabilities: List of tuples (symbol, probability)
    :digits: Integral number of digits to use in the Huffman encoding. Must be
             at least two.
    :returns:  A dictionary of {code: message} keys, where "code" is a string
               of asscii chars that represent the value of the bytes
    """
    def visit(node, path, decoding_dict, tagged):
        # The goal here is to visit each node, passing the path taken to get there
        # as well. When we reach a leaf, then we know that we're at a message, so
        # we can turn the path into digits (in an arbitrary but consistent way) and
        # add it to the dict.
        # Here, the "path" is the list of indices for children that we have to
        # access to get to the needed node. In binary, paths would be lists of
        # 0s and 1s.
        # We modify the passed in dictionary, so no returning is needed.
        # See: https://stackoverflow.com/questions/986006.
        if len(node.children) == 0:
            code = indicies_to_code(path, digits, tagged)
            decoding_dict[code] = node.data
        else:
            for k, child in enumerate(node.children):
                path.append(k)
                visit(child, path, decoding_dict, tagged)
                path.pop()

    root = huffman_nary_tree(probabilities, digits)
    decoding_dict = dict()
    visit(root, [], decoding_dict, tagged)

    return decoding_dict

def inverse_dict(original):
    """Return a dictionary that is the inverse of the original. i.e. switch the key, value pair

    :original: Dictionary.
    :returns: Inverse dictionary of `original`.
    """
    ret = dict()

    for key, value in original.items():
        ret[value] = key

    return ret

# http://stackoverflow.com/a/2267428
def baseN(n,b, tagged):

    if n == 0:
        return chr(0)
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    list =  digits[::-1]
    text_code = ''

    if tagged == True:
        text_code += chr(2**7 + list[0])
    else:
        text_code += chr(list[0])


    for num in list[1:]:
        text_code += chr(num)
    return text_code


def ascii_encode(string):
    """Return the 8-bit ascii representation of `string` as a string.

    :string: String.
    :returns: String.
    """
    def pad(num):
        binary = baseN(num, 2, False)
        padding = 8 - len(binary)
        return "0"*padding + binary
    return "".join(pad(ord(c)) for c in string)

class HuffmanCode(object):

    """Encode and decode messages with a constructed Huffman code."""

    def __init__(self, probabilities, digits, tagged = False):
        """Create the Huffman dictionaries needed for encoding and decoding.

        :probabilities: List of (message, frequency) tuples.
        :digits: Number of digits to use in the Huffman encoding.
        :tagged: True for tagged huffman tree
        """
        self.probabilities = probabilities
        self.huffman = huffman_nary_dict(probabilities, digits, tagged)
        self.inv_huffman = inverse_dict(self.huffman)
        self.indices_mapping = {}
        #print(self.inv_huffman)

    def encode(self, messages, word = False):
        """Encode each item in `messages` with the stored Huffman code.

        Raises a KeyError if there is a message in `messages` that is not in
        the inverse Huffman dictionary.

        :messages: List of messages to be encoded.
        :word: True if word-based, False if char-based(default)
        :returns: String of digits that represents Huffman encoding.
        """
        if word == True:
            messages = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(messages)

        text_code = ""

        for i in range(len(messages)):
            self.indices_mapping[len(text_code)] = i
            text_code += self.inv_huffman[messages[i]]

        #return "".join(self.inv_huffman[message] for message in messages)
        return text_code

    def decode(self, string):
        """Decode the given string with the stored Huffman dictionary.

        :string: String encoded with the stored inverse Huffman dictionary.
        :returns: String.
        """

        decode = ""
        length = len(string)
        index, count = 0, 0
        while (count<=length):
            if string[index:count] in self.huffman:
                code = string[index:count]
                decode += self.huffman[code]
                index = count

            count += 1

        return decode

    def search(self, compressed, pattern):
        """
        :compressed: the compressed String
        :pattern: the matching pattern form the original text
        :return: the index of the starting position for the last occurrence
        """
        pattern = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(pattern)
        try:
            encoded_pattern = "".join(self.inv_huffman[p] for p in pattern)
        except KeyError:
            print("word not in vocabulary")
            return None
        p = bm.boyer_moore_match(compressed, encoded_pattern)
        if p ==-1:
            return p
        return self.indices_mapping[p]

    def shift_or_search(self, compressed, pattern):
        pattern = re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(pattern)
        mark_dict = {}
        mark = '0'+'1'*len(pattern)
        for i, p in enumerate(pattern):
            encoded_p = self.inv_huffman[p]
            if encoded_p in mark_dict:
                m = mark_dict[encoded_p]
                new_m = m[:i] + '0'
                if i < len(pattern) :
                    new_m = m[:i] + '0'+m[i+1:]
                mark_dict[encoded_p] = new_m
            else:
                new_m = mark[:i] + '0'
                if i < len(pattern) :
                    new_m = mark[:i] + '0'+mark[i+1:]
                mark_dict[encoded_p] = new_m
        self.shift_or_match(compressed, mark_dict, len(pattern))

    def shift_or_match(self, compressed, mark_dict, plen):
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

        r = '1'+'1'*plen
        default_mark = '0' + '1'*plen
        length = len(compressed)
        index, count = 0, 0
        token_count = 0
        while (count<=length):
            if compressed[index:count] in self.huffman:
                token_count += 1
                code = compressed[index:count]

                r = shift_right(r)
                mark = default_mark
                if code in mark_dict:
                    mark = mark_dict[code]
                result = bitwise_or(r, mark)
                r = result
                if result[-1] == '0':
                    return token_count-plen, token_count
                index = count


            count += 1
        return None, None



if __name__ == "__main__":
    from freq import str_freq
    with open("test.txt") as f:
        in_str = f.read()

    freqs = str_freq(in_str)
    probabilities = list(freqs.items())

    #root = huffman_nary_tree(probabilities, 2)
    huffman = HuffmanCode(probabilities, 2)
    #alt_root = huffman_nary_tree(probabilities, 128)
    alt_huffman = HuffmanCode(probabilities, 128, True)

    #print(alt_huffman.encode(in_str))
    print()
    print(huffman.encode(in_str))
    print()
    print(huffman.decode(huffman.encode(in_str)))
    print()
    #print(ascii_encode(in_str))
    print()
    #print(alt_huffman.decode(alt_huffman.encode(in_str)))
