# debugging with the debugger
#-----------------------------------------------------------

def funcA(first_val, second_val):
        # divide by 4 changed to divide by 0
	result = (first_val*2) - (second_val/4)
	return result

def functionB(first_val=23, last_val=72):
        # set breakpoint here
	response = funcA(first_val, last_val)
	result = response * first_val/7
	return result


functionB(33, 88)
##functionB()

