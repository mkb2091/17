# 17
17 is a programming language that uses stack based memory and compiles to python(hopefully more in the future)

## To run
    python3 17.py <file>.17
    python3 output

It has two stores of data: mem and stack
Mem is a dynamic array which can be stored to and loaded from
Stack is a stack on which most operations are performed

A program is a loop which execute block of code at address stored in mem[0], if it doesn't exist the program exits.

Commands are seperated by whitespace.

Commands:
Base 17 number: Pushes it to the stack.

\+ : Adds top two numbers on stack.

\- : Takes top number away from second to top.

\* : Multiplies top two numbers on stack.

\/ : Divides second from top by top.

\@ : Stores numbers second from top at mem[top]

\# : Loads number at mem[top]

\: : Duplicates top number on stack

\=\= : If top two numbers are equal pushes 1, else 0

\! : If top > 0 pushes 1, else 0

\> : If second from top > top

\< : If second from top < top

\% : Second from top mod top

\$ : Prints chr(top)

\$\$ : Prints number form of top
