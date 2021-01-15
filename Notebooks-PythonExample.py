from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools


class Vector:
    typecode = 'd'

    def __init__(self, componments):
        self._componments = array(self.typecode, componments)

    def __iter__(self):
        return iter(self._componments)

    def __repr__(self):
        components = reprlib.repr(self._componments)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._componments)
               )

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._componments)

    def __getitem__(self, item):
        cls = type(self)
        if isinstance(item, slice):
            return cls(self._componments[item])
        elif isinstance(item, numbers.Integral):
            return self._componments[item]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    shortcut_names = 'xyzt'

    def __getattr__(self, item):
        cls = type(self)
        if len(item) == 1:
            pos = cls.shortcut_names.find(item)
            if 0 <= pos < len(self._componments):
                return self._componments[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, item))

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self)],
                                     self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


import abc
import random

class Tombola(abc.ABC):  # 自己定义的抽象基类要继承abc.ABC

    @abc.abstractmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""

    @abc.abstractmethod
    def pick(self):
        """随机删除元素，然后将其返回。
        如果实例为空，这个方法应该跑出‘LookError’"""

    def loaded(self):   # 抽象基类可以包含具体方法
        """如果至少有一个元素，返回'True', 否则返回'False'"""
        return bool(self.inspect())  # 抽象基类中的具体方法只能依赖抽象基类定义的接口（即只能使用 抽象基类中的其他具体方法、抽象方法或特性）

    def inspect(self):
        """返回一个有序元祖，由当前元素构成"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))


class BingoCage(Tombola):

    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, iterable):
        self._items.extend(iterable)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self, *args, **kwargs):
        self.pick()


class LotteryBlower(Tombola):

    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotterBlower')
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))

#虚拟子类是将其他的不是从抽象基类派生的类”注册“到抽象基类，让Python解释器将该类作为抽象基类的子类使用，因此称为虚拟子类，这样第三方类不需要直接继承自抽象基类。注册的虚拟子类不论是否实现抽象基类中的抽象内容，Python都认为它是抽象基类的子类，调用 issubclass(子类，抽象基类),isinstance (子类对象，抽象基类)都会返回True。
#这种通过注册增加虚拟子类是抽象基类动态性的体现，也是符合Python风格的方式。它允许我们动态地，清晰地改变类的属别关系。当一个类继承自抽象基类时，该类必须完成抽象基类定义的语义；当一个类注册为虚拟子类时，这种限制则不再有约束力，可以由程序开发人员自己约束自己，因此提供了更好的灵活性与扩展性（当然也带来了一些意外的问题）。这种能力在框架程序使用第三方插件时，采用虚拟子类即可以明晰接口，只要第三方插件能够提供框架程序要求的接口，不管其类型是什么，都可以使用抽象基类去调用相关能力，又不会影响框架程序去兼容外部接口的内部实现。从某种程度上讲，虚拟子类这种模式，是在继承这种模式下的一种多态实现
@Tombola.register
class TomboList(list):  # 虚拟子类（）

    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))


class DoppelDict(dict):
    """继承内置类型（dict）"""
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)
#dd = DoppelDict(one=1) 输出{'one': 1}， 继承自 dict 的 __init__ 方法显然忽略了我们覆盖的 __setitem__ 方法：'one' 的值没有重复
#dd['two'] = 2  输出{'one': 1, 'two': [2, 2]}，[] 运算符会调用我们覆盖的 __setitem__ 方法，按预期那样工 作：'two' 对应的是两个重复的值，即 [2, 2]。
#dd.update(three=3) 输出{'one': 1, 'two': [2, 2], 'three': 3}， 继承自 dict 的 update 方法也不使用我们覆盖的 __setitem__ 方 法：'three' 的值没有重复

# 直接子类化内置类型（如 dict、list 或 str）容易出错， 因为内置类型的方法通常会忽略用户覆盖的方法。不要子类化内置 类型，用户自己定义的类应该继承 collections 模块中的类，例如 UserDict、UserList 和 UserString，这些类做了特殊设计，因 此易于扩展。

import collections
class DoppleDict2(collections.UserDict):  # 就正常了
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)




if __name__ == '__main__':
    print(TomboList.__mro__)  # 检查继承顺序