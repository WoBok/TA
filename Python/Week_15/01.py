# import sys

# print(sys.argv)
# print(sys.argv[1] + sys.argv[3])
# print(int(sys.argv[2]) + int(sys.argv[4]))

# # Cmd: py D:\TA\Python\Week_15\01.py a 1 b 2
# # LogPython: ab
# #LogPython: 3

# ---------------------------------------------------

import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--a', type=int)  # 任意个“-”都会被忽略，最终只留下“-”后的参数名
# parser.add_argument('--b', type=int)
# args = parser.parse_args()
# print(f"{args.a}, {args.b}")

# # Cmd: py D:\TA\Python\Week_15\01.py --b 3 --a 4
# # LogPython: 4, 3

# ---------------------------------------------------

# # --a, --b更类似于关键字参数，a, b更类似于位置参数
# parser = argparse.ArgumentParser()
# parser.add_argument('a', type=int)
# parser.add_argument('b', type=int)
# args = parser.parse_args()
# print(f"{args.a}, {args.b}")

# # Cmd: py D:\TA\Python\Week_15\01.py 3 4
# # LogPython: 3, 4

# ---------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('--mul', action='store_true')
parser.add_argument('--div', action='store_true')
parser.add_argument('a', type=int)
parser.add_argument('b', type=int)
args = parser.parse_args()
if args.mul:
    print(args.a * args.b)
elif args.div:
    print(args.a / args.b)
else:
    print(args.a + args.b)

# Cmd: py D:\TA\Python\Week_15\01.py --div 3 4
# LogPython: 0.75
# Cmd: py D:\TA\Python\Week_15\01.py --mul 3 4
# LogPython: 12
# Cmd: py D:\TA\Python\Week_15\01.py  3 4
# LogPython: 7
# Cmd: py D:\TA\Python\Week_15\01.py --div --mul 3 4 # 应该是由于--mul的判断更先于--div，所以优先执行--mul
# LogPython: 12
# Cmd: py D:\TA\Python\Week_15\01.py --mul --div 3 4
# LogPython: 12
