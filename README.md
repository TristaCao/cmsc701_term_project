# cmsc701_term_project
For EXACT Searching for a single word or a phrase using Boyer Moore or Shift-OR Algorithm with our experiment data, simply do 

`python main.py`. 
For generating the test and see the cpmpression time and rate for three HUffman variant, do 

`python compress.py`

If you want to apply to new dataset `FILENAME` with customized pattern string `PATTERN`, run

`Python main.py -f FILENAME PATTERN -s CHOICE`
you can choose the searching method as Boyer-Moore(use CHOICE as "bm" or leave it since it's the default), Shift-Or on Plain Huffman("pso") 
or Shift-Or on Tagged Huffman("tso"), for example if you want to search the phrase `no such roses` in `shortext.txt` using Boyer-Moore, simply run:

`Python main.py -f shortext.txt "no such roses"` or `Python main.py -f shortext.txt "no such roses -s bm"`

For Approximate matching and Regex search, please visit the `huff-compress-approxsearch.py` file.
To run the experiments, please enter the following code in the main method:
--Approximation Search with k erros: `experiment("approx",1)`
--Search with Regex (please see description in code for range of possible query):  `experiment("regex")`

To perform search in arbitary of of your choice, please modify the `filename`  at `line 350`, there are examples of running various search in the main method.



