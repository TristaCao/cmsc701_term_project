# -*- coding: utf-8 -*-
import os, re, array, pickle, argparse, time, sys,random


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
        #print('build the symbol model: ', end1 - start1)
        start2 = time.time()
        self.__compress()
        end2 = time.time()
        #print('encode the symbol model: ', end2 - start2)
        self.code_text=self.buildcodetext()

    def __to_dic(self):
        """
        Build a dictionary to store words and their frequency.
        :return: a string of input txt file, and a word-frequency dictionary
        """
        with open(self.text_path, encoding='utf-8') as f:
            text = f.read()
        if self.level == 'word':
            text=re.sub('\n', '', text)
            text=re.sub(r'[^a-zA-Z\s]', '', text)
            text = text.strip().split()#re.compile(r'[^a-zA-Z]|[a-zA-Z]+').findall(text) #!! modified
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

    def buildcodetext(self):
        code_text={}
        for key in self.text_code:
            code_text[self.text_code[key]]=key
        
        return code_text

    def getText(self):
        return self.text

    def getCompressedText(self,mytext):
        tokens=mytext
        compresed=""
        for t in tokens:
            compresed+=self.text_code[t]
        return compresed

    def traverseToLeaf(self,code):
        curr=code
        processedcode=""
        for i in range(1,len(curr)):
            if(curr[0:i] in self.code_text):
                return curr[0:i],curr[i:]
        
        return "",""
    def traverseToLeaf2(self,code):
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
                regex="^*"+regex[1:]
            else:
                regex="^"+regex
            regex=re.sub("\*","[a-zA-Z0-9]*",regex)
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
            if(currcode==""):
                break
            currmask=masks[currcode]
            D=self.shiftAND(int(currmask,2),D)
            if(D==targetD):
                startpos=pos-len(tokens)+1
                endpos=pos
                return startpos,endpos
                #print("FOUND: startpos:",startpos, self.text[startpos:endpos+1])
                break
            pos+=1
        return -1,-1

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
            if(Ds[num_error]>=targetD):
                startpos=pos-len(tokens)+1
                endpos=pos
                return startpos,endpos
                #print("FOUND: startpos:",startpos, self.text[startpos:endpos+1])
                break
            pos+=1
        return -1,-1

            



    def plain_search(self,query):
        start = time.time()
        tokens=query.split()
        #start2 = time.time()
        #print(("split token",start2-start))
        masks=self.computemask(tokens)
        #start3 = time.time()
        #print(("compute mask token",start3-start2))
        return self.search(tokens,masks)
        #start4 = time.time()
        #print(("search token",start4-start3))

    def regex_search(self,query):
        tokens=query.split()
        masks=self.computemaskRegex(tokens)
        return self.search(tokens,masks)

    def approx_search(self,query,num_error):
        tokens=query.split()
        masks=self.computemask(tokens)
        return self.search_allow_error(tokens,masks,num_error)


def experiment(type,k=0):
    for i in range(0,10):
        fn="testdata/testdata"+str(i)
        compress = HuffmanCompress("word",fn)
        text=compress.getText();
        start = time.time()
        for r in range(0,len(text)-10,int((len(text)-10)/10)):
            #r=random.randint(0,len(text)-10)
            query=" ".join(text[r:r+10])
            if(type=="plain"):
                compress.plain_search(query)
            if(type=="approx"):
                compress.approx_search(query,k)
            if(type=="regex"):
                compress.regex_search(query)
        end = time.time()
        print("FileName:",fn)
        print("Time elapsed for "+type+" search:",end - start)


if __name__ == '__main__':
    ##Run python huff-compress.py -s word mydata.txt
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-s", help="specify character- or word-based Huffman encoding", choices=["char", "word"])
    #parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
    #args = parser.parse_args()
    #start = time.time()
    #compress = HuffmanCompress(args.s, args.infile)
    #end = time.time()
    #print("compress time: ", end - start)


    #Runing experiment
    #experiment("plain")
    #experiment("approx",1)
    #experiment("approx",2)
    #experiment("regex")
    
    #individual runs
    filename="mydata.txt" #specify your file name here
    compress = HuffmanCompress("word",filename)
    text=compress.getText();



    #Plain search 
    startpos,endpos=compress.plain_search("there is some")
    print("%s at position %d %d"%(text[startpos:endpos+1],startpos,endpos))

    #Approx search k=1
    startpos,endpos=compress.approx_search("there is teee",1)
    print("%s at position %d %d"%(text[startpos:endpos+1],startpos,endpos))

    #Approx search k=2
    startpos,endpos=compress.approx_search("there is teee",2)
    print("%s at position %d %d"%(text[startpos:endpos+1],startpos,endpos))

    #regex
    ## * matches any number of token between [a-zA-Z0-9], Eg t* == t and  any number of token following t
    ## . can replace any token
    startpos,endpos=compress.regex_search("there are *a*")
    print("%s at position %d %d"%(text[startpos:endpos+1],startpos,endpos))
    startpos,endpos=compress.regex_search("there are *x*")
    print("%s at position %d %d"%(text[startpos:endpos+1],startpos,endpos))
    startpos,endpos=compress.regex_search("there is s.me")
    print("%s at position %d %d"%(text[startpos:endpos+1],startpos,endpos))
    startpos,endpos=compress.regex_search("two *r[ef]es there")
    print("%s at position %d %d"%(text[startpos:endpos+1],startpos,endpos))
