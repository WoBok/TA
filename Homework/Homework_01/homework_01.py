str = "ABCDEF"
print(str[::-1])

#----------------------------------------------------

#str[start:stop:step]
#其中start表示开始索引，stop表示停止索引，step表示步长，默认值均为None
#step为正时读取方向为正（从左至右），step为负时读取方向为负（从右至左），step默认方向为正
#当step为正时，当前索引<stop时则进行读取，当step为负时，当前索引>stop时则进行读取
#start省略时，可理解为从“起点”开始，stop省略时可理解为至“终点”结束，“起点”与“终点”由step方向决定

#与此同理
reversedStr =""
for i in range(len(str)-1,-1,-1):
    reversedStr+=str[i]
print(reversedStr)

#https://www.cnblogs.com/malinqing/p/11272485.html
#https://blog.csdn.net/qq_34769162/article/details/107711331