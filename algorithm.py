1，汉诺塔(递归方式)
#递归两个特点：调用自身跟结束条件

def hanoi(n, a, b, c):
    #n个盘子
    if n > 0: #没有盘子就不需要移动了
        hanoi(n-1, a, c, b)
        print('remove from %s to %s' % (a, c))
        hanoi(n-1, b, a, c)

print(hanoi(3, 'A', "B", "C"))
-----------------------------------
remove from A to C
remove from A to B
remove from C to B
remove from A to C
remove from B to A
remove from B to C
remove from A to C
None
注意： 核心思路把问题缩小，变成移动第n和第n-1个盘子，这样理解、


2， 二分查找
def dichtomize_search(target, source_list):
    left, right = 0, len(source_list)-1
    while left <= right:
        mid = (left + right) // 2
        if source_list[mid] < target:
            left = mid + 1
        elif source_list[mid] > target:
            right = mid - 1
        else:  # source_list[mid] == target
            return mid
    else:  #没有找到对应的元素
        return None


 ---排序算法
 3， 冒泡排序
 # 列表每两个相邻的数，如果前面的比后面的大，则交换这两个数。
 # 一趟排序完成后，则无序区减少一个数，有序区增加一个数。
 # 关键点：趟、无序区范围
 def bubble_sort(source_list):
    for i in range(len(source_list)-1):  # 第i趟
        for j in range(len(source_list)-i-1):  # 指针对应的为止
            if source_list[j] > source_list[j+1]:  # 如果想要变成降序，就给成<
                source_list[j], source_list[j+1] = source_list[j+1], source_list[j]


4， 选择排序
# 一趟排序记录最小的数，放在第一个位置
# 再一趟排序记录列表无序区最小的数，放到第二个位置
# 。。。
# 算法关键点：有序区和无序区，无序区最小数的位置
def select_sort(li):
    for i in range(len(li)-1):  # 第几趟
        min_loc = i
        for j in range(i+1, len(li)):  # 每次在无序区找到最小的数
            if li[j] < li[min_loc]:
                min_loc = j
        li[i], li[min_loc] = li[min_loc], li[i]


5，插入算法
def insert_sort(li):
    for i in range(1, len(li)):
        key = li[i]
        j = i - 1  # 手里的牌的下标
        while li[j] > key and j > 0:  # 寻找插入的位置
            li[j+1] = li[j]
            j -= 1
        li[j+1] = key


6，快速排序 （时间负责度： nlogn）
def _quick_sort(li, left, right):
    def partition(li, left, right):
        tmp = li[left]
        while left < right:
            while left < right and li[right] >= tmp:  # 从右边开始找比tmp小的数
                right -= 1
            li[left] = li[right]  # 把右边的值写到左边的空位上
            while left < right and li[left] <= tmp:
                left += 1
            li[right] = li[left]
        li[left] = tmp
        return left

    if left < right:  # 至少两个元素
        mid = partition(li, left, right)
        _quick_sort(li, left, mid-1)
        _quick_sort(li, mid+1, right)

def quick_sort(li):
    _quick_sort(li, 0, len(li)-1)