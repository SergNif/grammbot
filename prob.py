# print("Введенный список:", entered_list)

# print("Список чисел: ", num_list)

# def squre():
#     entered_list = input("Введите список чисел, разделенных пробелом: ").split()
#     num_list = list(map(int, entered_list))

#     n = num_list[0]# int(input('n: '))
#     m = num_list[1] # int(input('m: '))
#     k = 1
#     while n != m:
#         if n > m:
#             n -= m
#         else:
#             m -= n
#         k += 1
#     return k

# squre()


def knightDistance (x, y):
    # normalise the coordinates
    x, y = abs(x), abs(y)
    if (x<y): x, y = y, x
    # now 0 <= y <= x

    # n8 means (-2,-1) (8 o'clock), n7 means (-1,-2) (7 o'clock), n10 means (-2,+1) (10 o'clock)
    if (x>2*y):
        # we're below the midline.  Using 8- & 10-o'clock moves
        n7, n8, n10 = 0,  (x + 2*y)//4,  (x - 2*y + 1)//4
    else:
        # we're above the midline.  Using 7- and 8-o'clock moves
        n7, n8, n10 = (2*y - x)//3, (2*x - y)//3,  0
    x -= 2*n8 + n7 + 2*n10
    y -= n8 + 2*n7 - n10
    # now 0<=x<=2, and y <= x.  Also (x,y) != (2,1)

    # Try to optimise the paths.
    if (x, y)==(1, 0): # hit the  3.  Did we need to?
        if (n8>0): # could have passed through the 2 at 3,1.  Back-up
            x, y = 3, 1; n8-=1;
    if (x, y)==(2, 2): # hit the 4.  Did we need to?
        if (n8>0): # could have passed through a 3 at 4,3.  Back-up, and take 7 o'clock to 2 at 3,1
            x, y = 3, 1; n8-=1; n7+=1

    # Almost there.  Now look up the final leg
    cheatsheet = [[0, 3, 2], [2, None, 2], [4]]
    return n7 + n8 + n10 + cheatsheet [y][x-y]

print(knightDistance(4,4))