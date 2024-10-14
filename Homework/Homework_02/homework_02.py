"""
思路：
1. 取出年份作为key，书籍名称作为value
2. 将年份存入列表并排序
3. 根据排序好的年份取出对应的书籍名称
4. 根据已排序的书籍名称从字典library中取出书籍信息
"""


#排序算法-------------------------------------------------------------------------------------
"""因对稳定性未作要求，故选用速度更快的快速排序"""

#根据选定的枢轴对列表进行划分
def partition(l, low, hight):
    pivot = l[low] #将子表的第一个元素作为枢轴元素
    while low < hight: #若low==hight则表示已找到枢轴位置
        while l[hight] >= pivot and low < hight: #若高位元素大于等于枢轴元素则hight--，否则跳出循环，将hight索引处的元素移动至low索引处
            hight -= 1
        l[low] = l[hight]
        while l[low] <= pivot and low < hight: #若低位元素小于等于枢轴元素则low++，否则跳出循环，将low索引处的元素移动至hight索引处
            low += 1
        l[hight] = l[low]
    l[low] = pivot #将枢轴元素放到最终的枢轴位置
    return low #返回枢轴位置

#快速排序
def quickSort(l, low, hight):
    if (low < hight):#递归跳出条件
        splitIndex = partition(l, low, hight)#将列表划分为左右两个子表
        quickSort(l, low, splitIndex - 1)#对左子表继续划分
        quickSort(l, splitIndex + 1, hight)#对右子表继续划分
#-----------------------------------------------------------------------------------------

#简化快速排序的使用
def sort(l):
    quickSort(l, 0, len(l) - 1)

library = {
    "1984": {"author": "George Orwell", "year": 1949, "genre": "Dystopian"},
    "To Kill a Mockingbird": {"author": "Harper Lee", "year": 1960, "genre": "Southern Gothic"},
    "The Great Gatsby": {"author": "F. Scott Fitzgerald", "year": 1925, "genre": "Tragedy"},
    "Moby Dick": {"author": "Herman Melville", "year": 1851, "genre": "Adventure"},
    "War and Peace": {"author": "Leo Tolstoy", "year": 1869, "genre": "Historical Fiction"},
    "Pride and Prejudice": {"author": "Jane Austen", "year": 1813, "genre": "Romance"},
    "Brave New World": {"author": "Aldous Huxley", "year": 1932, "genre": "Science Fiction"},
    "The Catcher in the Rye": {"author": "J.D. Salinger", "year": 1951, "genre": "Realist Fiction"},
    "The Lord of the Rings": {"author": "J.R.R. Tolkien", "year": 1954, "genre": "Fantasy"},
    "The Hobbit": {"author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy"},
    "The Odyssey": {"author": "Homer", "year": -800, "genre": "Epic Poetry"},
    "Crime and Punishment": {"author": "Fyodor Dostoevsky", "year": 1866, "genre": "Psychological Fiction"},
    "The Brothers Karamazov": {"author": "Fyodor Dostoevsky", "year": 1880, "genre": "Philosophical Fiction"},
    "Jane Eyre": {"author": "Charlotte Brontë", "year": 1847, "genre": "Gothic Fiction"},
    "The Divine Comedy": {"author": "Dante Alighieri", "year": 1320, "genre": "Epic Poetry"},
    "Don Quixote": {"author": "Miguel de Cervantes", "year": 1605, "genre": "Satire"},
    "Ulysses": {"author": "James Joyce", "year": 1922, "genre": "Modernist Fiction"},
    "Frankenstein": {"author": "Mary Shelley", "year": 1818, "genre": "Gothic Fiction"},
    "The Iliad": {"author": "Homer", "year": -762, "genre": "Epic Poetry"},
    "Madame Bovary": {"author": "Gustave Flaubert", "year": 1856, "genre": "Realism"}
}

#遍历library获取书籍年份作为键，书籍名称作为值存入字典libraryYearTitles中
libraryYearTitles = {}
for title, value in library.items():
    libraryYearTitles[value['year']] = title

#将书籍的年份存入列表libraryYears中
libraryYears = list(libraryYearTitles.keys())

#对书籍的年份进行排序
sort(libraryYears)
#亦可使用python内置函数sort()对列表进行排序
#libraryYears.sort()

"""
1. 遍历列表libraryYears中的年份
2. 根据年份从字典libraryYearTitles中取出书籍名称（此时的书籍名称便是排序后的书籍名称）
3. 使用刚取出的书籍名称从library中取出相关书籍信息并存入字典sortedlibrary中
"""
sortedlibrary = {}
for year in libraryYears:
    title = libraryYearTitles[year]
    sortedlibrary[title] = library[title]
print(sortedlibrary)