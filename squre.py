# def squre():
#     higth = int(input("Введите высоту: "))
#     up_list = input("Введите список чисел, разделенных пробелом: ").split()
#     up_num_list = list(map(int, up_list))
#     down_list = input("Введите список чисел, разделенных пробелом: ").split()
#     down_num_list = list(map(int, down_list))

#     hg = 0

#     for i,ll in enumerate(up_list):
#         print(f'{i=}')
#         print(f' {up_num_list[i]=} - {down_num_list[i]=} ')
#         jk =  (up_num_list[i] - down_num_list[i])
#         hg = hg + jk
#         if hg < 0:
#             hg = 0
#             print(hg) 
#         print(f'{hg=}') 
#         if hg >= higth:
#             return i
#     if hg < higth:
#         return -1


# print(squre())
# def squre():
#     up_list = input("Введите список чисел, разделенных пробелом: ").split()
#     up = list(map(int, up_list))

#     if (up[0] > up[1]) and (up[2] <= ((up[0] - up[1])//2)):
#         return 'YES'
#     else:
#         return 'NO'

# print(squre())

n,m = map(int, input().split())
F = [[0] * (m+1) for i in range(n+1)]
F[1][1] = 1
for i in range(2, n+1):
    for j in range(2, m+1):
        F[i][j] = F[i + 1][j +2] - F[i+2][j+1]
print(F[n][m])