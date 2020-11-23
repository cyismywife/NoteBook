1, __slots__

正常情况下，当我们定义了一个class，创建了一个class的实例后，我们可以给该实例绑定任何属性和方法，这就是动态语言的灵活性。
先定义class：
class Student:
    pass

然后实例化对象，尝试给实例绑定一个属性：
s = Student()
s.name = 'CaiYe' # 动态给实例绑定一个属性
print(s.name)  # 输出 ‘CaiYe’

还可以尝试给实例绑定一个方法：
from types import MethodType
s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
s.set_age(23)  # 调用实例方法
print(s.age) # 输出： 23

但是，给一个实例绑定的方法，对另一个实例是不起作用的：
s2 = Student()
s2.set_age(18) # 报错：AttributeError: 'Student' object has no attribute 'set_age'

为了给所有实例都绑定方法，可以给class绑定方法：
def set_score(self, score):
    self.score = score

Student.set_score = MethodType(set_score, Student)
给class绑定方法后，所有实例均可调用：
s.set_score = 18
print(s.set_score) # 输出：18
s2.set_score = 19
print(s2.set_score) # 输出： 19
------------------------------------------------------------------------------------
使用__slots__
但是，如果我们想要限制class的属性怎么办？比如，只允许对Student实例添加name和age属性。

为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class能添加的属性：

class Student:
    __slots__ = ('name', 'age')
    pass

s = Student()
s.name = 'Cai'
s.age = 18
s.score = 98 # 报错： AttributeError: 'Student' object has no attribute 'score'

由于'score'没有被放到__slots__中，所以不能绑定score属性，试图绑定score将得到AttributeError的错误。

使用__slots__要注意，__slots__定义的属性仅对当前类起作用，对继承的子类是不起作用的：
class MyStudent(Student):
    pass

my = MyStudent()
s.score = 99 # 不会报错

除非在子类中也定义__slots__，这样，子类允许定义的属性就是自身的__slots__加上父类的__slots__。
---------------------------------------------------------------------------------------------------

总结

当一个类需要创建大量实例时，可以使用__slots__来减少内存消耗。如果对访问属性的速度有要求，也可以酌情使用。另外可以利用slots的特性来限制实例的属性。
而用在普通类身上时，使用__slots__后会丧失动态添加属性和弱引用的功能，进而引起其他错误，所以在一般情况下不要使用它。



2， setdefault  与  defaultdict

words = ['apple', 'bat', 'bar', 'artom', 'book']
现在需要把上面你的列表转换成如下字典格式：
{'a': ['apple', 'artom'], 'b': ['bat', 'bar', 'book']}

(1)
def func(value):
    mydict = {}
    for i in value:
        first_word = i[0]
        if first_word not in mydict:
            mydict[first_word] = [i]
        else:
            mydict[first_word].append(i)
    return mydict
(2)
def func(value):
    mydict = {}
    for i in value:
        first_word = i[0]
        mydict.setdefault(first_word, []).append(i)
    return mydict
(3)
def func(value):
    mydict = defaultdict(list)
    for i in value:
        mydict[i[0]].append(i)
    return mydict


3, 交集合集并集，啦啦啦......


a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7, 8}

(1)连集
a.union(b)
a | b

(2)交集
a.intersection(b)
a & b

(3)


(4) a是不是b的父集合
a = {1, 2 ,3 ,4, 5}
b = {1, 2}
a.issuperset(b) # True

(5) b是不是a的子集
a = {1, 2 ,3 ,4, 5}
b = {1, 2}
b.issubset(a) #True



4， __getitem__  特殊方法（或称魔法方法）
··················································

import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])
class FrenchDeck:
    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suits = 'spades diamons clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):    # 实现这个特殊方法之后，类就支持切片、迭代等操作， in操作也同时支持
        return self._cards[item]
·································································
maozhu = FrenchDeck()
print(maozhu._cards)
print(len(maozhu))
print(maozhu[-1])    # 切片
print(choice(maozhu))

for i in maozhu:    #  迭代
    print(i)

if Card(rank='6', suit='diamons') in maozhu:   # in操作
    print(True)
else:
    print(False)



4， 模拟数值类型 

from math import hypot

class Vactor:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):   # ‘字符串表示形式’
        return 'Vactor(%r, %r)' % (self.x, self.y)

    def __abs__(self):   # 返回模
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):  # 实现两个Vactor对象相加
        x = self.x + other.x
        y = self.y + other.y
        return Vactor(x, y)

    def __mul__(self, other): 
        return Vactor(self.x * other, self.y * other)
·································································
    aa = Vactor(3, 4)
    print(abs(aa))   # 输出：5.0
    print(aa * 3)  # 输出 Vactor(9, 12)



5， __repr__ 和 __str__ 的区别
class PrintTest:

    def __repr__(self):
        return 'This is repr'

    def __str__(self):
        return  'This is str now'

if __name__ == '__main__':
    zy = PrintTest()
    print(zy)   #  优先调用__str__ 


 两者的区别在于，后者是在str()函数被使用，或者用在print函数打印一个对象的时候才被调用的，并且它返回的字符串对终端用户更友好。

如果只想实现这两个特殊方法中的一个，__repr__ 是更好的选择，
因为如果一个对象没有__str__函数，而Python有需要调用它的时候，解释器会用__repr__作为代替。



6，  布尔类型 （bool） （True 或 False）

bool(x) 的背后其实是调用x.__bool__()的结果，如果不允许__bool__方法，那么bool(x)会尝试调用x.__len__().
若返货0， 则bool会返回False，否则返回True。


