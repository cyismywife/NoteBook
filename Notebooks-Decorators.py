装饰器相关

1， 装饰器是可调用的对象，其参数是另一个函数(被装饰的函数)。
装饰器可能会处理被装饰的函数，然后把它放回，或者将其替换成另一个函数或可调用对象。

def deco(func):
    def inner():
        print('running inner()')
    return inner

@deco
def target():
    print('running target()')

target()   # 输出：running inner() 

综上，装饰器的一大特性是，能把被装饰的函数替换成其他函数，
第二个特性是， 装饰器在加载模块时立即执行。


2， 只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。


3， 闭包
是指延伸了作用域的函数，其中包括函数定义体中引用，但是不在定义体中定义的非全局变量。
函数是不是匿名的没有关系，关键是它能访问定义体之外的非全局变量。


4， nonlocal 关键字

例子：
def make_averager():
    count = 0
    total = 0
    services = []

    def averager(new_value):
        nonlocal count, total
        services.append(new_value)  # 为什么services不需要nonlocal
        count += 1
        total += new_value
        return total / count

    return averager

问题是，当count是数字或任何不可变类型时，count += 1 语句的作用其实与count = count + 1一样。
因此，我们在averager的定义体中为count赋值了， 这会把count变成局部变量。total变量也会受这个问题影响。

那为什么services不会呢，因为我们并没有给services赋值，我们只是调用了services.append, 也就是说，
我们利用了列表是可变的对象这一事实。

但对于数字、字符串、元祖等不可变类型来说，只能读取，不能更新，如果尝试重新绑定，例如count += 1，其实会隐式创建局部变量count，
这样，count就不是自由变量了，因此不会保存在闭包中。

为了解决这个问题，Python3引入了nonlocal关键字，它的作用是把变量标记为自由变量，即使在函数中为变量赋予了新值，也会变成自由变量。
如果为nonlocal声明的变量赋予新值，闭包中保存的绑定会更新。


5， 装饰器
它的典型行为： 把被装饰的函数替换成新函数，二者接受相同的参数，而且(通常)返回被装饰的函数本该返回的值
同时，还会做些额外操作。


6，叠放装饰器
@d1
@d2
def f():
    print('f')
    
就相当于：
def f():
    print('f')
f = d1(d2(f))


7， 参数化装饰器
答案： 创建一个装饰器工厂函数，把参数传给它， 返回一个装饰器， 然后再把它应用到要装饰的函数上。

registry = set()
def register(active=True):
    def decorate(func):   # decorate 这个内部函数是真正的装饰器；注意，它的参数是一个函数
        print('running register(active=%s) -> decorate(%s)') % (active, func)
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate

@register(active=False)  # @register工厂函数必须作为函数调用，并且传入所需的参数
def f1():
    print('running f1()')

@register()  # 即使不传入参数，register也必须作为函数调用
def f2():
    print('running f2()')

def f3():
    print('running f3()')
