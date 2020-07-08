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

