# -*- coding: utf-8 -*-
import os, re, array, pickle, argparse, time, sys


class Node(object):
    def __init__(self, char=None, value=None):
        self.char = char
        self.value = value
        self.left = None
        self.right = None


def binary_search(target, arr):
    """
    Binary search method for a sorted list of Node class objects.
    :param target: a Node object
    :param arr: a sorted list of Node objects
    :return: the index that target should insert into arr
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid].value < target.value:
            left = mid + 1
        elif arr[mid].value > target.value:
            right = mid - 1
        else:
            return mid
    return -1


class HuffmanCompress(object):
    def __init__(self, level, text_path):
        start1 = time.time()
        self.text_path, self.level = text_path, level
        self.text, self.text_fre = self.__to_dic()
        self.root, self.text_code = self.__to_tree()
        end1 = time.time()
        print('build the symbol model: ', end1 - start1)
        start2 = time.time()
        self.__compress()
        end2 = time.time()
        print('encode the symbol model: ', end2 - start2)

    def __to_dic(self):
        """
        Build a dictionary to store words and their frequency.
        :return: a string of input txt file, and a word-frequency dictionary
        """
        with open(self.text_path, encoding='utf-8') as f:
            text = f.read()
        if self.level == 'word':
            text=re.sub(r'([^\s\w]|_)+', '', text)
            text = text.strip().split(" ")#re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(text) #!! modified
            # Get words and punctuations. Another method: text = [i for i in re.split(r'(\W)', text) if i != '']
        text_fre = {}
        for i in range(len(text)):
            word = text[i]
            text_fre[word] = text_fre[word] + 1 if word in text_fre.keys() else 1
        return text, text_fre

    def __to_tree(self):
        """
        Build huffman tree.
        :return: root of the huffman tree, and a empty dictionary to store word-code pairs later.
        """
        nodes_list = [Node(char, self.text_fre[char]) for char in self.text_fre.keys()]
        nodes_list.sort(key=lambda node: node.value)
        while len(nodes_list) > 1:
            parent_node = Node(None, nodes_list[0].value + nodes_list[1].value)
            parent_node.left = nodes_list.pop(0)
            parent_node.right = nodes_list.pop(0)
            index = binary_search(parent_node, nodes_list)
            nodes_list.insert(index, parent_node)
        root = nodes_list[0]
        text_code = {}
        return root, text_code

    def __traverse(self, node, binary_code=''):
        """
        Traverse the huffman tree by recursion to give each word a code.
        :param node: a Node class object, initial value = root
        :param binary_code: the code of current node, initial value = ''
        """
        code_list = binary_code
        if node.char:
            self.text_code[node.char] = code_list
        else:
            self.__traverse(node.left, code_list+'0')
            self.__traverse(node.right, code_list+'1')

    def __padding(self):
        """
        Convert input txt file into a long string text_code, and add '0' at the end to ensure its length is a multiple of 8.
        :return: string, number of padding '0's
        """
        self.__traverse(self.root)
        text_code = ''.join([self.text_code[char] for char in self.text])
        if len(text_code) % 8 != 0:
            padding = (8 - (len(text_code) % 8))
            text_code += '0' * padding
        else:
            padding = 0
        return text_code, padding

    def __to_binary(self):
        """
        Build a binary array to store the code of input txt file.
        :return: binary array, number of padding '0's
        """
        text_code, padding = self.__padding()
        string = ''
        compress_text = array.array('B')
        for i in text_code:
            string += i
            if len(string) == 8:
                compress_text.append(int(string, 2))
                string = ''
        return compress_text, padding

    def __compress(self):
        """
        Compress input txt file.
        """
        compress_text, padding = self.__to_binary()
        compress_text.tofile(open(os.path.splitext(self.text_path)[0] + '.bin', "wb"))
        self.text_code['padding_length'] = padding
        pickle.dump(self.text_code, open(os.path.splitext(self.text_path)[0] + '-symbol-model.pkl', "wb"))


    ###### my code starts here, __to_dic function above is modified###

    def getCompressedText(self,mytext):
        tokens=mytext
        compresed=""
        for t in tokens:
            compresed+=self.text_code[t]
        return compresed

    def traverseToLeaf(self,code):
        curr=code
        currnode=self.root
        processedcode=""
        for i in range(0,len(curr)):
            if(currnode.left==None and currnode.right==None):
                break
            currbit=curr[0]
            processedcode+=currbit
            curr=curr[1:]
            if(currbit=='0'):
                currnode=currnode.left
            else:
                currnode=currnode.right
        #print(processedcode,curr)
        return processedcode,curr;



    def shiftANDApprox(self,currmask,Ds):
        Ds[0]=(Ds[0]<<1)|1
        oldD=Ds[0]
        Ds[0]=Ds[0]&currmask
        for i in range(1,len(Ds)):
            tmp=(Ds[i]<<1|1)
            Ds[i]=oldD|(tmp&currmask)
            oldD=tmp
        return Ds

    def shiftAND(self,currmask,D):
        D=(D<<1)|1
        D=D&currmask

        return D;

    #for testing
    def inorder(self,node,code):
        if(node!=None):
            self.inorder(node.left,code+"0")
            if(node.left==None and node.right==None):
                print(node.value,code)
            self.inorder(node.right,code+"1")

    def computemask(self,tokens):
        masks={}
        for key in self.text_code:
            val=self.text_code[key]
            for token in tokens:
                if(val not in masks):
                    masks[val]=""

                if(token==key):
                    masks[val]="1"+masks[val]
                else:
                    masks[val]="0"+masks[val]
        return masks

    def computemaskRegex(self,tokens):
        masks={}
        regextokens=[]
        for token in tokens:
            regex=token
            if(token[-1]!="*"):
                regex=regex+"$"

            if(token[0]=="*"):
                regex="^[a-zA-Z0-9]*"+regex[1:]
            else:
                regex="^"+regex
            regextokens.append(regex)
        for key in self.text_code:
            val=self.text_code[key]
            for regex in regextokens:
                if(val not in masks):
                    masks[val]=""
                if(len(re.findall(regex, key))>=1):
                    masks[val]="1"+masks[val]
                else:
                    masks[val]="0"+masks[val]
        return masks

    def search(self,tokens,masks):
        searchtextcompressed=self.getCompressedText(self.text)
        remaincode=searchtextcompressed
        pos=0
        D=0
        targetD=2**(len(tokens)-1) # Eg if query of length 4, target D looks like 1000 (b) = 8 (d)

        while(len(remaincode)>0):
            currcode,remaincode=self.traverseToLeaf(remaincode)
            currmask=masks[currcode]
            D=self.shiftAND(int(currmask,2),D)
            if(D==targetD):
                startpos=pos-len(tokens)+1
                endpos=pos
                print("FOUND: startpos:",startpos, self.text[startpos:endpos+1])
                break
            pos+=1

    def search_allow_error(self,tokens,masks,num_error):
        Ds=[0]*(num_error+1)
        searchtextcompressed=self.getCompressedText(self.text)
        remaincode=searchtextcompressed
        pos=0
        targetD=2**(len(tokens)-1) 
        while(len(remaincode)>0):
            currcode,remaincode=self.traverseToLeaf(remaincode)
            currmask=masks[currcode]
            Ds=self.shiftANDApprox(int(currmask,2),Ds)
            print(Ds,Ds[num_error],targetD)
            if(Ds[num_error]>targetD):
                startpos=pos-len(tokens)+1
                endpos=pos
                print("FOUND: startpos:",startpos, self.text[startpos:endpos+1])
                break
            pos+=1
            



    def plain_search(self,query):
        tokens=query.split()
        masks=self.computemask(tokens)
        self.search(tokens,masks)

    def regex_search(self,query):
        tokens=query.split()
        masks=self.computemaskRegex(tokens)
        self.search(tokens,masks)

    def approx_search(self,query,num_error):
        tokens=query.split()
        masks=self.computemask(tokens)
        self.search_allow_error(tokens,masks,num_error)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="specify character- or word-based Huffman encoding", choices=["char", "word"])
    parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
    args = parser.parse_args()
    start = time.time()
    compress = HuffmanCompress(args.s, args.infile)
    #print(compress.getCompressedText())
    end = time.time()
    print("compress time: ", end - start)
    ##Run python huff-compress.py -s word mydata.txt
    compress.plain_search("there is")
    compress.regex_search("two *r[ef]es there")
    compress.approx_search("two ok there is",2) #allow 2 substitution