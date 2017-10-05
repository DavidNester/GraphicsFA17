dim = 10#dimensions of box
#initialize board with zeroes
board = [[0 for i in range(dim)] for j in range(dim)]
board[0][0] = 1 #start location defaults to 0
#calculate by adding above and left to each spot (try/catch for edges for IndexOutOfBoundsException)
for i in range(0,dim):
    for j in range(0,dim):
        try:
            above = board[i-1][j]
        except:
            above = 0
        try:
            left = board[i][j-1]
        except:
            left = 0
        board[i][j] += above + left

#displaying notes and board
print
for i in range(0,dim):
    s = '|'
    for j in range(0,dim):
        if i == 5 and j == 5:
            s += '*' + str(board[i][j]) + '*' + '|'
        elif len(str(board[i][j])) == 1:
            s += '  ' + str(board[i][j]) + '  ' + '|'
        elif len(str(board[i][j])) == 2:
            s += ' ' + str(board[i][j]) + '  ' + '|'
        elif len(str(board[i][j])) == 3:
            s += ' ' + str(board[i][j]) + ' ' + '|'
        elif len(str(board[i][j])) == 4:
            s += str(board[i][j]) + ' ' + '|'
        elif len(str(board[i][j])) == 5:
            s += str(board[i][j]) + '|'
    print s
    print '-' * len(s)

print 'The number of paths to any box is the sum of the number of paths to the box above it and left of it'
print 'The solution to the 6x6 box problem is signified by *'
print 'The number of paths to box (n,m) can also be calculated as (n+m)! / (n! m!)'
print 'Must mean that: (n+m)! / (n!m!) =  (n-1+m)! / ((n-1)! m!) + (n+m-1)! / (n! (m-1)!)'
print 'I have not calculated this out but it looks like it has to be true'
