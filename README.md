# cmsc701_term_project
For Searching using Boyer Moore or Shift-OR Algorithm with our experiment data, simply do `python main.py`. 

If you want to apply to new dataset with customized pattern, comment out `line 130` - `line 172` and uncomment `line 106` - `line 128` in `main.py`. Change the path file name in `line 106` and search pattern in `line 119` as you want. Then you can choose to run Boyer Moore algorithm with `line 122`, Shift-Or algorithm with tagged Huffman with `line 124`, or Shift-Or Algorithm with `line 126-128`.

For Approximate matching and Regex search, please visit the `huff-compress-approxsearch.py` file.
To run the experiments, please enter the following code in the main method:
--Approximation Search with k erros: `experiment("approx",1)`
--Search with Regex (please see description in code for range of possible query):  `experiment("regex")`

To perform search in arbitary of of your choice, please modify the `filename`  at `line 350`, there are examples of running various search in the main method.



