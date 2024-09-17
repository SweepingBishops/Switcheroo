#!/usr/bin/env python

def find_largest_prod_palindrome(n):
    start = 10**(n-1)
    end = 10**(n)
    pals = list()
    for i in range(end,start,-1):
        for j in range(end, start,-1):
            check_palindome(i,j, pals)
    print(max(pals))
        
def check_palindome(i,j, pals):
    num = i*j
    word = str(num)
    if word == word[::-1]:
        #print(f"{num}={i}*{j}")
        pals.append(num)
        

find_largest_prod_palindrome(3)
