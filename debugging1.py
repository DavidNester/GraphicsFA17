# exception handling
#-----------------------------------------------------------

denominator = int (input ("enter a denominator value "))

try:
    formula = 10/denominator
	
    print ("the result is ",formula)

except ZeroDivisionError:
    print ("dividing by zero is not allowed")

else:
    print ("no error here")

finally:
    print ("this code is always run")

#-----------------------------------------------------------

try:
    x = input ("enter a number between 1 and 10 ")

    if x<1 or x>10:
        raise Exception

    print ("you entered a good number")

except:
    print ("your number is outside the range")
    
#-----------------------------------------------------------

