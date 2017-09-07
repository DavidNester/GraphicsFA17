# Super-3 Numbers

import string

i = int(input('Please enter the upper bound: '))

for n in range(i):
    x = 3*n**3
    string_x = str(x)
    if (string_x.find("333") != -1):
        print (n, x)

# End of program

