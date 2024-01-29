import random
s = "Please submit value of k squared!"
print("65 120 ", end='')
for x in s:
    print(random.randrange(65, 90), random.randrange(97, 122), random.randrange(65, 90), str(
        ord(x)), random.randrange(65, 90), random.randrange(97, 122), sep=' ', end=' ')
