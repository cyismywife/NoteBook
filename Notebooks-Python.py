# 1，
# reduce() 函数会对参数序列中的元素进行累积, 语法：reduce(function, iterable[, initializer])
# 函数将一个数据集合（链表，元组等）中的所有数据进行下列操作：用传给 reduce 中的函数 function（有两个参数）先对集合中的第 1、2 个元素进行操作，得到的结果再与第三个数据用 function 函数运算，最后得到一个结果。
# 示例： 使用reduce函数和一个匿名函数计算阶乘
from functools import reduce
def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))

# operator 模块为多个算术运算符提供了对应的函数
# 示例： 使用 reduce 和 operator.mul 函数计算阶乘， 效果与上面的相同
from functools import reduce
from operator import mul
def shenz(n):
    return reduce(mul, range(1, n+1))

# mul函数源码
def mul(a, b):
    "Same as a * b."
    return a * b



2，
from operator import itemgetter
# itemgetter 根据元祖的某个字段元祖列表排序
# 示例
from operator import itemgetter

# 现在列表中的元素是元祖，换乘列表也是可以的，即列表中的元素还是列表
metro_data = [('Tokyo', 'JP', 36.933, (35.689722, 139.691667)), 
	('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)), 
	('Mexico City', 'MX', 20.142, (19.433333, -99.133333)), 
	('New York-Newark', 'US', 20.104, (40.808611, -74.020386)), 
	('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))]

for city in stored(metro_data, key=itemgetter(1)):
	print(city)

# 输出
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
('New York-Newark', 'US', 20.104, (40.808611, -74.020386))



3,  生成一个随机长度的字符串
class RandomStr:
    """Generate a random length string"""

    @classmethod
    def getstr(cls):
        import random
        temp_list = []
        list_letter = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        for _ in range(1, random.randint(2, 11)):
            temp_list.append(random.choice(list_letter))
        return ''.join(temp_list)

    def getlist(self, nums):
        """Generate a list of random strings"""
        return [RandomStr.getstr() for _ in range(nums)]



4,  filter函数
def caiye(n):
    return len(n) > 5  # 返回的是True 或 Flase

mylist = ['dxnufuhlu', 'xdcx', 'zjswnqb', 'abzqwjato', 'xbwezlyzln', 'fulqnkr', 'ixa', 'sqmp']
endlist = list(filter(caiye, mylist)) # 如果不用list的话，返回的是一个filter对象
print(endlist)
# 输出
# ['dxnufuhlu', 'zjswnqb', 'abzqwjato', 'xbwezlyzln', 'fulqnkr']



5,  函数参数
def tag(name: str, *args, cls:'int > 0'=80, **kwargs):
    print('name: {}'.format(name))
    print('args: {}'.format([i for i in args]))
    print('cls: {}'.format(cls))
    print('kwargs: {}'.format([i for i, _ in kwargs.items()]))


aa = dict(a=1, b=2, c=3)
tag('caiye', 'maozhu', 'duoduo', 'tarlor', **aa, cls='mylovecaiye')

# 输出
# name: caiye
# args: ['maozhu', 'duoduo', 'tarlor']
# cls: mylovecaiye
# kwargs: ['a', 'b', 'c']


# 定义函数时 若想指定仅限关键字参数，要把它们放到前面有 * 的参数后面。如果不 想支持数量不定的定位参数，但是想支持仅限关键字参数，在签名中放 一个 *
def f(a, *, b):
    print(a, b)

# f(1, 2)  # 报错
f(1, b=2)  # 输出: 1, 2



6，hasattr() 函数用于判断对象是否包含对应的属性。
# 语法： hasattr(object, name) ，   object对象， name字符串类型，属性名
class LineItem:
    def __init__(self, product, quantity, price):
        """
        :param product: 产品类型
        :param quantity: 数量
        :param price: 价格
        """
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


maozhu = LineItem('banana', 23, 2.6)
print(hasattr(maozhu, 'price')) # 输出 True



7， 抽象基类
# 由于python 没有抽象类、接口的概念，所以要实现这种功能 得使用 ABC这个模块
# @abstractmethod：抽象方法，含abstractmethod方法的类不能实例化，继承了含abstractmethod方法的子类必须复写所有abstractmethod装饰的方法，未被装饰的可以不重写
from abc import ABC, abstractmethod

class Promotion(ABC):
    @abstractmethod
    def discount(self):
        """"""


class FidelityPromo(Promotion):
    """为积分为1000或以上的顾客提供5%的折扣"""
    def discount(self, order):
        print('I am here')
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


if __name__ == '__main__':
    caiye = Promotion() # 抽象基类不能被实例化
# 此处报错：TypeError: Can't instantiate abstract class Promotion with abstract methods discount

-----------------------------------------------------------------------------------------------
class Promotion(ABC):
    @abstractmethod
    def discount(self):
        """"""


class FidelityPromo(Promotion):
    """为积分为1000或以上的顾客提供5%的折扣"""
    def discount(self, order):  # 重写继承Promotion类中被abstractmethod装饰的类
        print('I am here')
        # return order.total() * .05 if order.customer.fidelity >= 1000 else 0


if __name__ == '__main__':
    caiye = FidelityPromo()
    caiye.discount('dd')


# 8，
# 闭包
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return averager


avg = make_averager()
print(avg(10))
print(avg(11))
print(avg(12))

print(avg.__code__.co_varnames)  # 局部变量  输出:('new_value', 'total')
print('-' * 20)
print(avg.__code__.co_freevars)  # 函数定义体中的自由变量  输出: ('series',)


9， python装饰器中functools.wraps的作用详解
# 直接上代码看效果:

# 定义一个最简单的装饰器

　　def user_login_data(f):
　　　　def wrapper(*args, **kwargs):
　　　　　　return f(*args, **kwargs)

　　　　return wrapper

# 用装饰器装饰以下两个函数
　　
　　@user_login_data
　　def num1():
　　　　print("aaa")


　　@user_login_data
　　def num2():
　　　　print("bbbb")

　　if __name__ == '__main__':
　　　　print(num1.__name__)
　　　　print(num2.__name__)



# 　以上代码的输出结果为:
# 　　　　wrapper
# 　　　　wrapper
# 由此函数使用装饰器时,函数的函数名即 __name__已经被装饰器改变.
# 一般定义装饰器的话可以不用考虑这点,但是如果多个函数被两个装饰器装饰时就报错,因为两个函数名一样,第二个函数再去装饰的话就报错.
# 解决方案就是引入  functools.wraps  ,以上代码的解决如下: 

　　　　
　　　　def user_login_data(f):
　　　　@functools.wraps(f)
　　　　　　def wrapper(*args, **kwargs):
　　　　　　　　return f(*args, **kwargs)

　　　　　　return wrapper


# 增加@functools.wraps(f), 可以保持当前装饰器去装饰的函数的 __name__ 的值不变
# 以上输出结果就是: 
# 　　　　num1
# 　　　　num2


# 10,
# 计算每一步的平均值
def make_averager():
    series = []   # 此处是series 是列表

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return averager



# 换另一种更好的实现方法，只存储目前的总值和元素个数，然后使用这两 个数计算均值
def make_caiye():
    count = 0
    total = 0

    def averager(new_value):
        count += 0
        total += new_value
        return total / count

    return averager

# 这样写是有问题的
# 运行会报错：UnboundLocalError: local variable 'count' referenced before assignment

# 原因是： 当count是数字或任何不可变类型时， count += 1 语句的作用其实与 count = count + 1 一样
#  因此，我们在averager的定义体重为count赋值了， 这会把count变成局部变量. total变量也受这个问题影响

# 而在函数make_averager函数没有这个问题，是因为我们没有给series赋值，我们只是调用了series.append，
#  并把它传给sum和len， 也就是说，我们利用了列表是可变的对象这一事实

# 但对数字，字符串， 元祖等不可变类型来说， 只能读取，不能更新。
# 如果尝试重新绑定，例如count = count + 1， 其实会隐式创建局部变量count，
# 这样，count就不是自由变量了，因此不会保持在闭包中

# 为了解决这个问题， Python3中引入了nonlocal申明。 它的作用是把变量标记成自由变量，即使在函数中为变量赋予了新值了，
# 也会变成自由变量，如果nonloacal声明的变量赋予新值，闭包中保存的绑定会更新

def make_caiye():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 0
        total += new_value
        return total / count

    return averager



11，type-object-class的 关系


#type-->int-->1
#type-->class-->obj(对象)
a=1      
b="abc"
print(type(1))   # <class 'int'>
print(type(int))  # <class 'type'>
print(type(b))    #  <class 'str'>
print(type(str))  #  <class 'type'>


class Student:
    pass

class MyStudent(Student):
	pass

stu = Student()  
print(type(stu))   #  <class '__main__.Student'> 。 说明stu 是Student类的一个实例
print(type(Student))  # <class 'type'> 。 说明Student类 也是type类的一个实例



# object是最顶层基类
# type也是一个类，同时type也是一个对象
print(int.__bases__) # (<class 'object'>,)
print(str.__bases__)   # (<class 'object'>,)
print(MyStudent.__bases__)  #  (<class '__main__.Student'>,)  说明MyStudent 继承自Student类
print(Student.__bases__)   #   (<class 'object'>,)   而 Student类则继承自 object 
print(type.__bases__)     #  (<class 'object'>,)   说明type类的基类也是object
print(object.__bases__)   # ()  #  正好说明object 是最顶层的
print(type(object))   #   <class 'type'>


12, __new__

# 在object类中存在一个静态的__new__(cls, *args, **kwargs)方法，该方法需要传递一个参数cls，cls表示需要实例化的类，此参数在实例化时由Python解释器自动提供，
# __new__方法必须有返回值，且返回的是被实例化的实例，只有在该实例返回后才会调用__init__来进行初始化，初始化所用的实例就是__new__返回的结果，也就可以认为是self，我们来看下面的例子：
class Nums:
    def __init__(self):
        print('this is init')
        
    # def __new__(cls, *args, **kwargs):
    #     print('this is new')
    #     return object.__new__(cls)

    def __new__(cls):
    	print('this is new')
    	return super().__new__(cls)
    
num = Nums()  #  实例化

# this is new
# this is init


#  可以看到，在实例化时候，先执行__new__再执行__init__，而且python会自动传入我们希望实例化的类，这里我们显示的调用了object的__new__，
#  也可以调用其他的父类的__new__，那么如果我们定义了__new__，但是并没有返回一个本身实例，会发生什么事呢？例子如下：
class Nums:
    def __init__(self):
        print('this is init')
        
    def __new__(cls, *args, **kwargs):
        print('this is new')
        return 'caiye'
    
num = Nums()  #  实例化

# this is new


# 可以看到本身的__init__函数并未被调用，而是调用了str的__init__，可能这样并不直观，那么换一个实例返回，如下：
class Obj:
    def __init__(self):
        print('this is ojb init')

class Nums:
    def __init__(self):
        print('this is init')
        
    def __new__(cls, *args, **kwargs):
        print('this is Nums new')
        obj = Obj()
        return obj
    
num = Nums()  #  实例化

# this is new
# this is ojb init

# 这个就比较明显了，另一个实例的__init__被调用了。


13, python中的cls到底指的是什么，与self有什么区别?
#  @staticmethod和@classmethod


# 一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。

# 而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。

# 这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。

class A(object):
    a = 'a'

    @staticmethod
    def foo1(name):
        print('hello', name)
    def foo2(self, name):
        print('hello', name)
    @classmethod
    def foo3(cls, name):
        print('hello', name)


#  首先定义一个类A，类A中有三个函数，foo1为静态函数，用@staticmethod装饰器装饰，这种方法与类有某种关系但不需要使用到实例或者类来参与。
#  如下两种方法都可以正常输出，也就是说既可以作为类的方法使用，也可以作为类的实例的方法使用。
a = A()
a.foo1('caiye')  # hello caiye
A.foo1('caiye')  # hello caiye

#  foo2为正常的函数，是类的实例的函数，只能通过a调用。
a.foo2('duoduo')  # hello duoduo
A.foo2('duoduo')  # TypeError: foo2() missing 1 required positional argument: 'name'

# foo3为类函数，cls作为第一个参数用来表示类本身. 在类方法中用到，类方法是只与类本身有关而与实例无关的方法。如下两种方法都可以正常输出。
a.foo3('maozhu')  # hello maozhu
A.foo3('maozhu')  # hello maozhu


# 但是通过例子发现staticmethod与classmethod的使用方法和输出结果相同，再看看这两种方法的区别。
既然@staticmethod和@classmethod都可以直接类名.方法名()来调用，那他们有什么区别呢
从它们的使用上来看,
@staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
@classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。
而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码。


也就是说在classmethod中可以调用类中定义的其他方法、类的属性，但staticmethod只能通过A.a调用类的属性，但无法通过在该函数内部调用A.foo2()。修改上面的代码加以说明：
class A(object):

a = 'a'
@staticmethod
def foo1(name):
    print('hello', name)
    print(A.a) # 正常
    print(A.foo2('mamq')) # 报错: unbound method foo2() must be called with A instance as first argument (got str instance instead)

def foo2(self, name):
    print('hello', name)

@classmethod
def foo3(cls, name):
    print('hello', name)
    print(A.a)
    print(cls().foo2(name))



14， 自省： 是通过一定的查询到对象的内部结构
自省是获取对象的能力，反射是操纵对象的能力，python中使用getattr()和setattr()实现反射，而其他的则是自省

type()，判断对象类型
dir()， 带参数时获得该对象的所有属性和方法；不带参数时，返回当前范围内的变量、方法和定义的类型列表
isinstance()，判断对象是否是已知类型
hasattr()，判断对象是否包含对应属性
getattr()，获取对象属性
setattr()， 设置对象属性


In [1]: class Myobject(object):
   ...:     def __init__(self):
   ...:         self.x = 9
   ...:     def power(self):
   ...:         return self.x * self.x
   ...:

In [2]: obj = Myobject()

In [3]: obj.power()
Out[3]: 81

In [4]: hasattr(obj, 'x') # 有属性x么？
Out[4]: True

In [5]: hasattr(obj, 'y') # 有属性y么？
Out[5]: False

In [6]: setattr(obj, 'y') # 设置属性必须有三个参数，少了值
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-6-3b0a0f22117d> in <module>()
----> 1 setattr(obj, 'y')

TypeError: setattr expected 3 arguments, got 2

In [7]: setattr(obj, 'y', 100) # 设置属性y的值为100

In [8]: hasattr(obj, 'y') # 有属性y么？
Out[8]: True

In [9]: getattr(obj, 'y') # 获取属性y！
Out[9]: 100

In [10]: obj.y # 获取属性y
Out[10]: 100

In [11]: obj.x # 获取属性x
Out[11]: 9



15， super函数的使用

一， 简单使用
在类的继承中，如果重定义某个方法，该方法会覆盖父类的同名方法，但有时，我们希望能同时实现父类的功能，
这时，我们就需要调用父类的方法了，可通过使用 super 来实现，比如：
class Animal:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print('Hello, I am %s.' % self.name)

class Dog(Animal):
    def greet(self):
        super(Dog, self).greet()  # Python3 可使用 super().greet()
        print('WangWang...')

 在上面，Animal 是父类，Dog 是子类，我们在 Dog 类重定义了 greet 方法，为了能同时实现父类的功能，我们又调用了父类的方法，看下面的使用：
dog = Dog('dog')
dog.greet()
--------------------
Hello, I am dog.
WangWang...


super 的一个最常见用法可以说是在子类中调用父类的初始化方法了，比如：
class Base:
    def __init__(self, a, b):
        if a > 10:
            self.a = a
        else:
            raise ValueError('caiye wrong')
        self.b = b + 1

class A(Base):
    def __init__(self, a, b, c):
        super(A, self).__init__(a, b)  # Python3 中可使用 super().__init__(a, b)
        self.c = c

a = A(12, 12, 3)
print(a.b)  # 13

二， 深入使用
看了上面的使用，你可能会觉得 super 的使用很简单，无非就是获取了父类，并调用父类的方法。
其实，在上面的情况下，super 获得的类刚好是父类，但在其他情况就不一定了，super 其实和父类没有实质性的关联。

让我们看一个稍微复杂的例子，涉及到多重继承，代码如下：
class Base:
    def __init__(self):
        print('enter Base')
        print('leave Base')
        
class A(Base):
    def __init__(self):
        print('enter A')
        super(A, self).__init__()
        print('leave A')

class B(Base):
    def __init__(self):
        print('enter B')
        super(B, self).__init__()
        print('leave B')

class C(B, A):
    def __init__(self):
        print('enter C')
        super(C, self).__init__()
        print('leave C')

其中，Base 是父类，A, B 继承自 Base, C 继承自 A, B，它们的继承关系如下：
    Base
   / \
  /	  \
 A     B
 \    /
  \  /
    C

 如果你认为 super 代表『调用父类的方法』，那你很可能会疑惑为什么 enter A 的下一句不是 enter Base 而是 enter B。
 原因是，super 和父类没有实质性的关联，现在让我们搞清 super 是怎么运作的。

 三， MRO列表
 事实上，对于你定义的每一个类，Python 会计算出一个方法解析顺序（Method Resolution Order, MRO）列表，它代表了类继承的顺序，我们可以使用下面的方式获得某个类的 MRO 列表：
 print(C.__mro__)
 输出：  (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class '__main__.Base'>, <class 'object'>)

 那这个 MRO 列表的顺序是怎么定的呢，它是通过一个 C3 线性化算法来实现的，这里我们就不去深究这个算法了，感兴趣的读者可以自己去了解一下，
 总的来说，一个类的 MRO 列表就是合并所有父类的 MRO 列表，并遵循以下三条原则：

子类永远在父类前面
如果有多个父类，会根据它们在列表中的顺序被检查
如果对下一个类存在两个合法的选择，选择第一个父类

四， super原理

super 的工作原理如下：
def super(cls, inst):
    mro = inst.__class__.mro()
    return mro[mro.index(cls) + 1]

其中，cls 代表类，inst 代表实例，上面的代码做了两件事：

获取 inst 的 MRO 列表
查找 cls 在当前 MRO 列表中的 index, 并返回它的下一个类，即 mro[index + 1]
当你使用 super(cls, inst) 时，Python 会在 inst 的 MRO 列表上搜索 cls 的下一个类。

现在，让我们回到前面的例子。

首先看类 C 的 __init__ 方法：
super(C, self).__init__()
这里的 self 是当前 C 的实例，self.__class__.mro() 结果是：
(<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class '__main__.Base'>, <class 'object'>)

可以看到，C 的下一个类是 A，于是，跳到了 A 的 __init__，这时会打印出 enter A，并执行下面一行代码：
super(A, self).__init__()
注意，这里的 self 也是当前 C 的实例，MRO 列表跟上面是一样的，搜索 A 在 MRO 中的下一个类，发现是 B，于是，跳到了 B 的 __init__，这时会打印出 enter B，而不是 enter Base。

整个过程还是比较清晰的，关键是要理解 super 的工作方式，而不是想当然地认为 super 调用了父类的方法。

五，小结

事实上，super 和父类没有实质性的关联。
super(cls, inst) 获得的是 cls 在 inst 的 MRO 列表中的下一个类。



16， mixin

一，概念
Mixin 即 Mix-in，常被译为“混入”，是一种编程模式，在 Python 等面向对象语言中，通常它是实现了某种功能单元的类，用于被其他子类继承，将功能组合到子类中。

利用 Python 的多重继承，子类可以继承不同功能的 Mixin 类，按需动态组合使用。

当多个类都实现了同一种功能时，这时应该考虑将该功能抽离成 Mixin 类。

举个例子
定义一个简单的类：

class Person:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
我们可以通过调用实例属性的方式来访问：

p = Person("小陈", "男", 18)
print(p.name)  # "小陈"

然后我们定义一个 Mixin 类：

class MappingMixin:
    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        return self.__dict__.set(key, value)
这个类可以让子类拥有像 dict 一样调用属性的功能

我们将这个 Mixin 加入到 Person 类中：

class Person(MappingMixin):
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

现在 Person 拥有另一种调用属性方式了：

p = Person("小陈", "男", 18)
print(p['name'])  # "小陈"
print(p['age'])  # 18
再定义一个 Mixin 类，这个类实现了 __repr__ 方法，能自动将属性与值拼接成字符串：

class ReprMixin:
    def __repr__(self):
        s = self.__class__.__name__ + '('
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                s += '{}={}, '.format(k, v)
        s = s.rstrip(', ') + ')'  # 将最后一个逗号和空格换成括号
        return s
利用 Python 的特性，一个类可以继承多个父类：

class Person(MappingMixin, ReprMixin):
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
这样这个子类混入了两种功能：

p = Person("小陈", "男", 18)
print(p['name'])  # "小陈"
print(p)  # Person(name=小陈, gender=男, age=18)


二， 总结
Mixin 实质上是利用语言特性，可以把它看作一种特殊的多重继承，所以它并不是 Python 独享，只要支持多重继承或者类似特性的都可以使用，比如 Ruby 中 include 语法，Vue 等前端领域也有 Mixin 的概念。

但 Mixin 终归不属于语言的语法，为了代码的可读性和可维护性，定义和使用 Mixin 类应该遵循几个原则：

Mixin 实现的功能需要是通用的，并且是单一的，比如上例中两个 Mixin 类都适用于大部分子类，每个 Mixin 只实现一种功能，可按需继承。
Mixin 只用于拓展子类的功能，不能影响子类的主要功能，子类也不能依赖 Mixin。比如上例中 Person 继承不同的 Mixin 只是增加了一些功能，并不影响自身的主要功能。如果是依赖关系，则是真正的基类，不应该用 Mixin 命名。
Mixin 类自身不能进行实例化，仅用于被子类继承。


17， 上下文管理器协议

一， 要自己实现这样一个上下文管理，要先知道上下文管理协议。

简单点说，就是在一个类里，实现了__enter__和__exit__的方法，这个类的实例就是一个上下文管理器。
实例：
class Resource():
    def __enter__(self):
        print('===connect to resource===')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('===close resource connection===')
        
    def operate(self):
        print('===in operation===')
        
with Resource() as res:
    res.operate()
我们执行一下，通过日志的打印顺序。可以知道其执行过程。
输出：
===connect to resource===
===in operation===
===close resource connection===


为什么要使用上下文管理器？

在我看来，这和 Python 崇尚的优雅风格有关。
可以以一种更加优雅的方式，操作（创建/获取/释放）资源，如文件操作、数据库连接；
可以以一种更加优雅的方式，处理异常；

仍然是以上面的代码为例，我们将1/0 这个一定会抛出异常的代码写在 operate 里
class Resource():
    def __enter__(self):
        print('===connect to resource===')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('===close resource connection===')
        return True

    def operate(self):
        1/0

with Resource() as res:
    res.operate()

运行一下，惊奇地发现，居然不会报错。

这就是上下文管理协议的一个强大之处，异常可以在__exit__ 进行捕获并由你自己决定如何处理，是抛出呢还是在这里就解决了。
在__exit__ 里返回 True（没有return 就默认为 return False），就相当于告诉 Python解释器，这个异常我们已经捕获了，不需要再往外抛了。

在 写__exit__ 函数时，需要注意的事，它必须要有这三个参数：

exc_type：异常类型
exc_val：异常值
exc_tb：异常的错误栈信息
当主逻辑代码没有报异常时，这三个参数将都为None。

二， 理解并使用 contextlib

在上面的例子中，我们只是为了构建一个上下文管理器，却写了一个类。如果只是要实现一个简单的功能，写一个类未免有点过于繁杂。这时候，我们就想，如果只写一个函数就可以实现上下文管理器就好了。

这个点Python早就想到了。它给我们提供了一个装饰器，你只要按照它的代码协议来实现函数内容，就可以将这个函数对象变成一个上下文管理器。

我们按照 contextlib 的协议来自己实现一个打开文件（with open）的上下文管理器。
import contextlib

@contextlib.contextmanager
def open_func(file_name):
    # __enter__方法
    print('open file:', file_name, 'in __enter__')
    file_handler = open(file_name, 'r')
	
    # 【重点】：yield
    yield file_handler

    # __exit__方法
    print('close file:', file_name, 'in __exit__')
    file_handler.close()
    return

with open_func('/Users/MING/mytest.txt') as file_in:
    for line in file_in:
        print(line)

在被装饰函数里，必须是一个生成器（带有yield），而yield之前的代码，就相当于__enter__里的内容。yield 之后的代码，就相当于__exit__ 里的内容。

上面这段代码只能实现上下文管理器的第一个目的（管理资源），并不能实现第二个目的（处理异常）。

如果要处理异常，可以改成下面这个样子。
import contextlib

@contextlib.contextmanager
def open_func(file_name):
    # __enter__方法
    print('open file:', file_name, 'in __enter__')
    file_handler = open(file_name, 'r')

    try:
        yield file_handler
    except Exception as exc:
        # deal with exception
        print('the exception was thrown')
    finally:
        print('close file:', file_name, 'in __exit__')
        file_handler.close()

        return

with open_func('/Users/MING/mytest.txt') as file_in:
    for line in file_in:
        1/0
        print(line)


18,  序列类型

分类，
按照存放的数据类型来分类：
容器序列：list, tuple, deque
扁平序列：str， bytes, bytearray, array.array

按照可变：
可变序列： list, deque, bytearray, array
不可变：tuple, str, bytes



19, 自定义可切片的序列
class Group:
    # 自定义序列
    def __init__(self, group_name, company_name, staffs):
        self.group_name = group_name
        self.company_name = company_name
        self.staffs = staffs

    def __reversed__(self):  # 反转序列, reversed(group)的时候就会调用该方法
        print('start reverse')
        self.staffs.reverse()

    def __getitem__(self, item):
        import numbers
        cls = type(self)
        if isinstance(item, slice):  # slice 切片对象
            return cls(group_name=self.group_name, company_name=self.company_name,
                       staffs=self.staffs[item])
        elif isinstance(item, numbers.Integral):
            return cls(group_name=self.group_name, company_name=self.company_name,
                       staffs=[self.staffs[item]])

    def __len__(self):
        return len(self.staffs)

    def __iter__(self):   # 返回一个迭代器， for i in group:
        return iter(self.staffs)

    def __contains__(self, item):  # 处理if _ in _, 例如:if 'maozhu' in group:
        if item in self.staffs:
            return True
        else:
            return False


20，
import bisect
# 用来处理已排序的序列(可变的)，用来维持已排序的序列， 升序
# 二分查找

inter_list = []
bisect.insort(inter_list, 3)
bisect.insort(inter_list, 5)
bisect.insort(inter_list, 6)
bisect.insort(inter_list, 2)
bisect.insort(inter_list, 1)
print(inter_list)  # [1, 2, 3, 5, 6]



21，
enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中

以下是 enumerate() 方法的语法:
enumerate(sequence, [start=0])

参数
sequence -- 一个序列、迭代器或其他支持迭代对象。
start -- 下标起始位置。
返回值
返回 enumerate(枚举) 对象。

以下展示了使用 enumerate() 方法的实例：

>>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']

>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]

>>> list(enumerate(seasons, start=1))       # 下标从 1 开始
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]


普通的 for 循环
>>>i = 0
>>> seq = ['one', 'two', 'three']
>>> for element in seq:
...     print i, seq[i]
...     i +=1
... 
0 one
1 two
2 three
for 循环使用 enumerate
>>>seq = ['one', 'two', 'three']
>>> for i, element in enumerate(seq):
...     print i, element
... 
0 one
1 two
2 three


20, property  动态属性

# @property的应用，其功能1是可定义只读属性，也就是真正意义上的私有属性(属性前双下划线的私有属性也是可以访问的）

class Person(object):
    def __init__(self, name, age=18):
        self.name = name
        self.__age = 18  

    @property
    def age(self):
        return self.__age
        
xm = Person('xiaoming')  #定义一个人名小明
print(xm._Person__age) #  输出18
print(xm.age)	#结果为18
xm.age = -4	#报错无法给年龄赋值
print(xm.age)

@property真正强大的是可以限制属性的定义。往往我们定义类，希望其中的属性必须符合实际，
但因为在__init__里定义的属性可以随意的修改，导致很难实现。
如我想实现Person类，规定每个人(即创建的实例)的年龄必须大于18岁，
正常实现的话，则必须将属性age设为只读属性，然后通过方法来赋值，代码如下：
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.__age = 18

    @property
    def age(self):
        return self.__age

    def set_age(self, age):  # 定义函数来给self.__age赋值
        if age < 18:
            print('年龄必须大于18岁')
            return
        self.__age = age
        return self.__age

对于上面的代码，不是谁都可以记住方法名，所以可以简化成如下：
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.__age = 18

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if age < 18:
            print('年龄必须大于18岁')
            return
        self.__age = age
        return self.__age

xm = Person('xiaoming', 20)
print(xm.age)
print('----------')
xm.age = 10  # 可以像修改属性一样修改

结果和上图一致。两段代码变化的内容：将set_age修改为age，并且在上方加入装饰器@age.setter。
这就是@property定义可访问属性的语法，即仍旧以属性名为方法名，并在方法名上增加@属性.setter就行了。

下面来说下@property的实现原理
在开头也说了，@property是个描述符，它其实也是一个类，代码如下：
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.__age = 18

    def get_age(self): #恢复用方法名来获取以及定义
        return self.__age

    def set_age(self, age): 
        if age < 18:
            print('年龄必须大于18岁')
            return
        self.__age = age
        return self.__age

    age = property(get_age, set_age)  #增加property类

上述代码的运行结果和前面一致，将@property装饰的属性方法再次修改回定义方法名，
然后再类的最下方，定义：属性=property(get,set,del)，这个格式是固定的。。。


class property(object):
	def __init__(self, fget=None, fset=None, fdel=None, doc=None):
		“”“
        Property attribute.
        
          fget
            function to be used for getting an attribute value
          fset
            function to be used for setting an attribute value
          fdel
            function to be used for del'ing an attribute
		class C(object):
            @property
            def x(self):
                "I am the 'x' property."
                return self._x
            @x.setter
            def x(self, value):
                self._x = value
            @x.deleter
            def x(self):
                del self._x
  		”“”
 		pass	
     def __set__(self, *args, **kwargs): # real signature unknown
       """ Set an attribute of instance to value. """
       	pass
     def __get__(self, *args, **kwargs): # real signature unknown
	    """ Return an attribute of instance, which is of type owner. """
	    pass
     def __delete__(self, *args, **kwargs): # real signature unknown
        """ Delete an attribute of instance. """
        pass

介绍下python的描述符，定义：如果一个类里定义了__set__、__get __ 、__delete __三个方法之一，
同时给另一个类的属性赋值为实例，那么该类可以称之为描述符。因为描述符的使用目前就python，所以了解下就行了


21, Python中获取属性:getattr、__get__、__getattr__和__getattribute__

一， getattr

getattr (object, name[, default])是Python的内置函数之一，它的作用是获取对象的属性。
object 对象
name 属性名
default 当属性不存在时，返回的默认值
实例：
>>> class Foo:
...     def __init__(self, x):
...         self.x = x
...
>>> f = Foo(10)
>>> getattr(f, 'x')
10
>>> f.x
10
>>> getattr(f, 'y', 'bar')
'bar'
>>> hasattr(f, 10)
True

二， _ __getattr _ __

object. __getattr__(self, name)是一个对象方法，如果找不到对象的属性时会调用这个方法。

这个方法应该返回属性值或者抛出AttributeError异常。


>>> class Frob:
...     def __init__(self, bamf):
...         self.bamf = bamf
...     def __getattr__(self, name):
...         return 'Frob does not have `{}` attribute.'.format(str(name))
...
>>> f = Frob("bamf")
>>> f.bar
'Frob does not have `bar` attribute.'
>>> f.bamf
'bamf'

三， ____ getattribute __ __

当访问 某个对象的属性时，会无条件的调用这个方法。这个方法只适用于新式类。
新式类就是集成自object或者type的类。

如果类还同时定义了__getattr__()方法，则不会调用__getattr__()方法，除非在__getattribute__()方法中显示调用__getattr__()或者抛出了AttributeError。

该方法应该返回属性值或者抛出AttributeError异常。

为了避免在方法中出现无限递归的情况，应该总是使用基类的方法来获取属性：（以下两种方式都可行）
        return super().__getattribute__(item)
        return object.__getattribute__(self, item)


22， 属性描述符
import numbers


class IntField:
    # 数据描述符
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("int value need")
        if value < 0:
            raise ValueError("positive value need")
        self.value = value

    def __delete__(self, instance):
        pass

# class NonDataIntField:
#     # 非数据属性描述符
#     def __get__(self, instance, owner):
#         return self.value

class User:
    age = IntField()
    # age = NonDataIntField()


if __name__ == "__main__":
    user = User()
    user.age = 30　　# 调用age对象的__set__
    print(user.age)　　# 调用age对象的__get__



23， 元祖拆包

先看一个简单的例子：

student1 = ("David", 90)
stuName, stuScore = student1;
print('Name: %s, Score: %s' %(stuName, stuScore))
其中第二行代码就是一个简单的元组拆包，它将一个学生对象按照Name, Score拆分，并赋值给stuName, stuScore这两个变量，
这种简单的元组拆包叫做平行赋值
还可以用*将一个可迭代对象拆分成函数的参数：

t = [88,20]
print(*t)
print(divmod(*t))
产生的结果是：
88 20
(4, 8)

除此之外，可以用*来处理剩下的元素：

a,b,*rest = range(10)
print(a,b,rest)
这时a = 0; b = 1; rest = [2,3,4,5,6,7,8,9]

a,*rest,b = range(10)
print(a,rest,b)
这时a = 0; rest = [1,2,3,4,5,6,7,8]; b = 9

a, b, *rest = range(3)
print(a,b,rest)
这时a = 0; b = 1; rest = [2]

a, b, *rest = range(2)
print(a,b,rest)
这时a = 0; b = 1; rest = []
但是不用*来表示剩余元素时，编译过程就会报错：

a, b, rest = range(10)
print(a,b,rest)

Traceback (most recent call last):
  File "D:/PythonWorkSpace/FluentPython/c2/c2-7.py", line 21, in <module>
    a, b, rest = range(10)
ValueError: too many values to unpack (expected 3)
总结一下，元组拆包可以应用到任何可迭代的对象上，
唯一的硬性要求是，被拆包的对象的元素数量必须和接受这些元素的元组的空档数一致，除非用*来表示忽略多余的元素。



24， socket 模仿http请求

import socket
from urllib.parse import urlparse


def ciaye(url):
    # 通过socket请求html
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'

    # 建立socket链接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 80))

    # 发送请求
    client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path, host).encode('utf8'))

    data = b''
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break
    print(data.decode('utf8'))
    client.close()


if __name__ == '__main__':
    ciaye('http://www.baidu.com')


25，socket 仿造聊天软件

服务端
import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8000))
server.listen()
# sock, addr = server.accept()

def handle_sock(sock, addr):
    while True:
        data = sock.recv(2048)
        if data == 'bye':
            break
        print(data.decode('utf8'))
        re_data = input('--》')
        sock.send(re_data.encode('utf8'))
    sock.close()


# 获取从客户端发送的数据
# 一次获取1k的数据
while True:
    sock, addr = server.accept()

    # 用线程去处理新接收的链接(用户)
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()


    # data = sock.recv(2048)
    # print(data.decode('utf8'))
    # re_data = input('--》')
    # sock.send(re_data.encode('utf8'))
    # server.close()
    # sock.close()


客户端
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))
while True:
    # client.send('caiye i love you'.encode('utf8'))
    re_data = input('--->')
    client.send(re_data.encode('utf8'))
    if re_data == 'bye':
        break
    data = client.recv(2048)
    print(data.decode('utf8'))
client.close()




