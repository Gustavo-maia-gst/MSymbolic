# MSymbolic
Pure python code capable of reading, evaluating and deriving functions of arbitrary complexity.

## How it works?
Let's consider a relatively complex function, such as tanh(x), which we can define as:

![image](https://github.com/user-attachments/assets/7803e2a1-7a70-4262-bf63-4052abd98167)

- we can write the tanh function as: (1 - e^(-2*x)) / (1 + e^(-2*x)), and pass it to the program! which will translate the text into a expression tree that can be evaluated

(The process of translating the text into an expression tree is complex and will be avoided in this discussion, as I am not an expert in lexical analysis)

### The expression tree
- The tree works in a very simplified way, everything is a function! Is the number 1 a function? Yes, it is, and this is the fundamental concept, as everything is a function, a sum, or whatever operation, between two nodes will also be a function!!!
- At each leaf node there is a constant function, such as f(x) = 1, or a variable function, f(x) = x for all of them, the other nodes are just compositions of these two functions
- In addition to the leaf nodes, there are also some special functions, such as sine, cosine, exponential and logarithm, these functions are defined in the form: g(f(x)), to maintain the function-oriented design of the tree.
- Having defined everything, we just need to add operations, and voila, we have a 100% functional tree! (the operators defined are binary operators).
- The layout of the tree for tanh(x) will look something like this:

![image](https://github.com/user-attachments/assets/4e39accb-4136-4d3c-bad4-f2ce2cab9da1)

- Here is the output of the program for this function, as expected for tanh, with some precision problems:

![image](https://github.com/user-attachments/assets/30be260c-3aef-492a-b9fd-ac7627715546)

- You've probably noticed that the entire exponential subtree will be calculated TWICE! Yes... There's plenty of room for optimization (maybe put functions and parameters in a cache? Feel free to do a pull request!), but performance wasn't my goal with this repository.
- Finally, it was a really fun problem to solve. If you love math as much as I do, I encourage you to try solving this problem yourself, and if you want, send me an email with the solution, maybe we can learn something new.
