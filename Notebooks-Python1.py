1， Python多线程与多线程中join()的用法


Python多线程与多进程中join()方法的效果是相同的。
下面仅以多线程为例：
首先需要明确几个概念：

知识点一：
当一个进程启动之后，会默认产生一个主线程，因为线程是程序执行流的最小单元，当设置多线程时，主线程会创建多个子线程，在python中，默认情况下（其实就是setDaemon(False)），主线程执行完自己的任务以后，就退出了，此时子线程会继续执行自己的任务，直到自己的任务结束，例子见下面一。

知识点二：
当我们使用setDaemon(True)方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行，可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止，例子见下面二。

知识点三：
此时join的作用就凸显出来了，join所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程在终止，例子见下面三。

知识点四：
join有一个timeout参数：

当设置守护线程时，含义是主线程对于子线程等待timeout的时间将会杀死该子线程，最后退出程序。所以说，如果有10个子线程，全部的等待时间就是每个timeout的累加和。简单的来说，就是给每个子线程一个timeout的时间，让他去执行，时间一到，不管任务有没有完成，直接杀死。
没有设置守护线程时，主线程将会等待timeout的累加和这样的一段时间，时间一到，主线程结束，但是并没有杀死子线程，子线程依然可以继续执行，直到子线程全部结束，程序退出。



一：Python多线程的默认情况
import threading
import time

def run():
    time.sleep(2)
    print('当前线程的名字是： ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':

    start_time = time.time()

    print('这是主线程：', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.start()

    print('主线程结束！' , threading.current_thread().name)
    print('一共用时：', time.time()-start_time)
其执行结果如下
这是主线程： MainThread
主线程结束！ MainThread
一共用时： 0.0010058879852294922
当前线程的名字是：Thread-1
当前线程的名字是：Thread-4 
当前线程的名字是：Thread-3   
当前线程的名字是：Thread-2
当前线程的名字是：  Thread-5

关键点：

我们的计时是对主线程计时，主线程结束，计时随之结束，打印出主线程的用时。
主线程的任务完成之后，主线程随之结束，子线程继续执行自己的任务，直到全部的子线程的任务全部结束，程序结束。

二：设置守护线程
import threading
import time

def run():

    time.sleep(2)
    print('当前线程的名字是： ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':

    start_time = time.time()

    print('这是主线程：', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    print('主线程结束了！' , threading.current_thread().name)
    print('一共用时：', time.time()-start_time)
其执行结果如下，注意请确保setDaemon()在start()之前。
这是主线程： MainThread
主线程结束了！ MainThread
一共用时： 0.0009968280792236328

关键点：

非常明显的看到，主线程结束以后，子线程还没有来得及执行，整个程序就退出了。

三：join的作用
import threading
import time

def run():

    time.sleep(2)
    print('当前线程的名字是： ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':

    start_time = time.time()

    print('这是主线程：', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

    print('主线程结束了！' , threading.current_thread().name)
    print('一共用时：', time.time()-start_time)
其执行结果如下：
这是主线程： MainThread
当前线程的名字是： Thread-2
当前线程的名字是： Thread-1  
当前线程的名字是： Thread-5
当前线程的名字是： Thread-4 
当前线程的名字是： Thread-3
主线程结束了！ MainThread
一共用时： 4.002542495727539

关键点：

可以看到，主线程一直等待全部的子线程结束之后，主线程自身才结束，程序退出。



把多线程用类的方式实现，如下：
import time
import threading

def get_detail_html(url):
    print('get detail html start')
    time.sleep(2)
    print('get detail html end')


def get_detail_url(url):
    print('get detail url start')
    time.sleep(2)
    print('get deteil url end')


class GetDetailHtml(threading.Thread):

    def __init__(self, name):
        # threading.Thread.__init__(self, name=name)
        super(GetDetailHtml, self).__init__(name=name)
        
    def run(self):
        print('get detail html start')
        time.sleep(2)
        print('get detail html end')


class GetDetailUrl(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        print('get detail url start')
        time.sleep(2)
        print('get deteil url end')


if __name__ == '__main__':
    # cai1 = threading.Thread(target=get_detail_html, args=('', ))
    # cai2 = threading.Thread(target=get_detail_url, args=('', ))
    cai1 = GetDetailHtml('get_detail_html')
    cai2 = GetDetailUrl('get_detail_url')
    t0 = time.time()
    # cai1.setDaemon(True) # 将 cai1设置成守护线程，意思就是只要主线程退出，该守护线程会离开被kill
    cai1.start()
    cai2.start()

    cai1.join()  # join() 方法
    cai2.join()
    print(time.time() - t0)


threading.currentThread()
threading.current_thread() 返回线程本身



2 ， threading.Condition 条件变量，（解决线程间的同步问题）

很详细的说明
# https://www.jianshu.com/p/5d2579938517


import threading
from threading import Condition


class XiaoAi(threading.Thread):

    def __init__(self, name, cond):
        super().__init__(name=name)
        self.cond = cond

    def run(self):
        with self.cond:

            self.cond.wait()
            print('{}: 在1 '.format(self.name))
            self.cond.notify()

            self.cond.wait()
            print('{}: 在2 '.format(self.name))
            self.cond.notify()

            self.cond.wait()
            print('{}: 在3 '.format(self.name))
            self.cond.notify()

            self.cond.wait()
            print('{}: 在4 '.format(self.name))
            self.cond.notify()

            self.cond.wait()
            print('{}: 在5 '.format(self.name))
            self.cond.notify()


class TianMao(threading.Thread):

    def __init__(self, cond, name):
        super().__init__(name=name)
        self.cond = cond

    def run(self):
        with self.cond:
            print('{}: 在吗1'.format(self.name))
            self.cond.notify()
            self.cond.wait()

            print('{}: 在吗2'.format(self.name))
            self.cond.notify()
            self.cond.wait()

            print('{}: 在吗3'.format(self.name))
            self.cond.notify()
            self.cond.wait()

            print('{}: 在吗4'.format(self.name))
            self.cond.notify()
            self.cond.wait()

            print('{}: 在吗5'.format(self.name))
            self.cond.notify()
            self.cond.wait()


if __name__ == '__main__':
    cond = Condition()
    xiaoai = XiaoAi(cond=cond, name='小爱')
    tianmao = TianMao(cond=cond, name='天猫同学')

    # 启动顺序很重要
    # 在调用with cond之后才能调用wait或者notify方法

    # condition有两层锁， 一把底层锁会在线程调用了wait方法的时候释放，
    # 上面的锁会在每次调用wait的时候分配一把并放入到cond的等待队列中，等到notify方法的唤醒
    xiaoai.start()
    tianmao.start()


3， threading.Semaphore

#Semaphore 是用于控制进入数量的锁
#文件， 读、写， 写一般只是用于一个线程写，读可以允许有多个

import time
import threading


class HtmlSpider(threading.Thread):
    def __init__(self, url, sem):
        super(HtmlSpider, self).__init__()
        self.url = url
        self.sem = sem

    def run(self):
        time.sleep(2)
        print('got html text success')
        self.sem.release()


class UrlProducer(threading.Thread):
    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        for i in range(20):
            self.sem.acquire()
            html_thread = HtmlSpider('https://www.baidu.com/%d' % i, self.sem)
            html_thread.start()


if __name__ == '__main__':
    sem = threading.Semaphore(3)
    urlpro = UrlProducer(sem)
    urlpro.start()



4, concurrent 模块

import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
from concurrent.futures import Future
from multiprocessing import Pool

#未来对象，task的返回容器


#线程池， 为什么要线程池
#主线程中可以获取某一个线程的状态或者某一个任务的状态，以及返回值
#当一个线程完成的时候我们主线程能立即知道

#futures可以让多线程和多进程编码接口一致


def geturldetail(times):
    time.sleep(times)
    print('get page {} success'.format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)  # 获取线程池


# 通过submit函数提交执行的函数到线程池中, submit 是立即返回
task1 = executor.submit(geturldetail, (3))
task2 = executor.submit(geturldetail, (2))


# #done方法用于判定某个任务是否完成
print(task1.done())
print(task2.cancel())
time.sleep(3)
print(task1.done())
#输出
# False
# False
# get page 2 success
# get page 3 success
# True

# #result方法可以获取task的执行结果
print(task1.result())
#输出
# get page 2 success
# get page 3 success
# 3


# 获取已经成功的task的返回
urls = [3, 2, 4]
all_task = [executor.submit(geturldetail, (url)) for url in urls]
for future in as_completed(all_task):
    data = future.result()
    print('get {}'.format(data))

# 输出
get page 2 success
get 2
get page 3 success
get 3
get page 4 success
get 4


# 通过 executor的map获取已经成功完成的task
urls = [3, 2, 4]
for future in executor.map(geturldetail, urls):
    print('get {}'.format(future))  # 输出的结果跟urls的元素顺序有关
#输出
get page 2 success
get page 3 success
get 3
get 2
get page 4 success
get 4

# 阻塞主线程
urls = [3, 2, 4]
all_task = [executor.submit(geturldetail, (url)) for url in urls]
print('main')
#输出
main
get page 2 success
get page 3 success
get page 4 success
#而
urls = [3, 2, 4]
all_task = [executor.submit(geturldetail, (url)) for url in urls]
wait(all_task) # 会阻塞主线程，等到all_task全部执行完，再执行主线程
print('main')
输出：
main
get page 2 success
get page 3 success
get page 4 success



5， 生成器进阶

def get_func():
    # 下面这句话包含两个意思
    # 1， 可以 [yield 'https://www.baidu.com'] 可以产出值
    # 2， html 放在yield前面可以接受调用方传进来的值
    html = yield 'https://www.baidu.com'
    print(html)
    yield 2
    yield 'maozhu'
    return 'duoduo'


if __name__ == '__main__':
    gen = get_func()
    # 在调用send发送非none值之前，我们必须启动一次生成器， 方式有两种1. gen.send(None), 2. next(gen)
    url = gen.send(None)
    print(url)  # 输出: https://www.baidu.com
    html = 'I miss Caiye'
    print(gen.send(html)) #send方法可以传递值进入生成器内部，同时还可以重启生成器执行到下一个yield位置
    # 上面的语句输出 I am caiye 和 2
    print(gen.send(None))
    
    # 捕获return的返回值
    try: 
        print(gen.send(None))
    except StopIteration as e:
        sss = e.value
        print(sss)

输出：
https://www.baidu.com
I miss Caiye
2
maozhu
duoduo


6， yield from

# python3.3新加入yield from 语法
from itertools import chain # 可以把n个可以可迭代对象连接在一起遍历


my_list = [1, 2, 3]
my_dict = {
    'first': 'caiye',
    'second': 'maozhu'
}

for value in chain(my_list, my_dict, range(6, 9)):
    print(value)

# 输出
1
2
3
first
second
6
7
8

现在我们自己实现一个chain函数
def my_func(*args, **kwargs):
    for i in args:
        for value in i:
            yield value

for value in my_func(my_list, my_dict, range(6, 9)):
    print(value) 


现在我们使用yield from 来简化my_func函数
def my_func(*args, **kwargs):
    for i in args:
        yield from i # yield from 后面跟的是iterable对象


首先来了解一下yield from 和 yield 的区别


def g1(iterable):
    yield iterable

def g2(iterable):
    yield from iterable

for value in g1(range(10)):
    print(value)  # 输出的是：range(0, 10)
for value in g2(range(10)):
    print(value)  # 输出的就是： 0 1 2 3 4 5 6 7 8 9

总结，“ 生成器 、元组、 列表、range（）函数产生的序列等可迭代对象”返回另外一个生成器。而yield只是返回一个元素
yield from iterable本质上等于 for item in iterable: yield item的缩写版

例子1：
def my_generator():
    for i in range(5):
        if i==2:
            return '我被迫中断了'
        else:
            yield i
 
def wrap_my_generator(generator):  #定义一个包装“生成器”的生成器，它的本质还是生成器
    result=yield from generator    #自动触发StopIteration异常，并且将return的返回值赋值给yield from表达式的结果，即result
    print(result)
 
def main(generator):
    for j in generator:
        print(j)
 
g=my_generator()
wrap_g=wrap_my_generator(g)
main(wrap_g)  #调用
'''运行结果为：
0
1
我被迫中断了
'''

例子2：
from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    # 子生成器
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)

def grouper(result, key):
    # 委派生成器
    while True:
        result[key] = yield from averager()

def main(data):
    # 调用方
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value) # 这里会把value的值通过委派生成器(相当于管道)直接赋值给子生成器中的term(term = yield)，而grouper函数中没有对数据做任何处理
        group.send(None)
    return results

data = {'上海':[88, 77, 88, 99], '南京':[22, 11, 22, 33]}
print(main(data))

委派生成器在 yield from 表达式处暂停时，调用方可以直接把数据发给子生成器，子生成器再把产出的值发给调用方。
子生成器返回之后，解释器会抛出StopIteration 异常，并把返回值附加到异常对象上，此时委派生成器会恢复。
总结：（1）yield from主要设计用来向子生成器委派操作任务，但yield from可以向任意的可迭代对象委派操作；
（2）委派生成器（group）相当于管道，所以可以把任意数量的委派生成器连接在一起---
一个委派生成器使用yield from 调用一个子生成器，而那个子生成器本身也是委派生成器，使用yield from调用另一个生成器。



7 asyncio python的协程模块
协程(coroutine) ---- 本质上就是一个函数， 怎么判断一个函数是不是协程？通过asyncio.iscoroutine（obj）和asyncio.iscoroutinefunction(func)加以判断，返回true，则是。


一， 事件循环
协程函数，不是像普通函数那样直接调用运行，必须要注册到事件循环中，然后由事件循环去运行，单独运行协程函数是不会有结果的
看下面这个例子：
import time
import asyncio
async def say_after_time(delay,what):
        await asyncio.sleep(delay)
        print(what)
 
async def main():
        print(f"开始时间为： {time.time()}")
        await say_after_time(1,"hello")
        await say_after_time(2,"world")
        print(f"结束时间为： {time.time()}")
 
loop=asyncio.get_event_loop()    #创建事件循环对象
#loop=asyncio.new_event_loop()   #与上面等价，创建新的事件循环
loop.run_until_complete(main())  #通过事件循环对象运行协程函数
loop.close()

（1）获取事件循环对象的几种方式：

下面几种方式可以用来获取、设置、创建事件循环对象loop

loop=asyncio.get_running_loop() 返回（获取）在当前线程中正在运行的事件循环，如果没有正在运行的事件循环，则会显示错误；它是python3.7中新添加的

loop=asyncio.get_event_loop() 获得一个事件循环，如果当前线程还没有事件循环，则创建一个新的事件循环loop；

loop=asyncio.set_event_loop(loop) 设置一个事件循环为当前线程的事件循环；

loop=asyncio.new_event_loop() 创建一个新的事件循环

（2）通过事件循环运行协程函数的两种方式：

（1）方式一：创建事件循环对象loop，即asyncio.get_event_loop()，通过事件循环运行协程函数

（2）方式二：直接通过asyncio.run(function_name)运行协程函数。但是需要注意的是，首先run函数是python3.7版本新添加的，前面的版本是没有的；
其次，这个run函数总是会创建一个新的事件循环并在run结束之后关闭事件循环，
所以，如果在同一个线程中已经有了一个事件循环，则不能再使用这个函数了，因为同一个线程不能有两个事件循环，
而且这个run函数不能同时运行两次，因为他已经创建一个了。即同一个线程中是不允许有多个事件循环loop的。

asyncio.run（）是python3.7 新添加的内容，也是后面推荐的运行任务的方式，因为它是高层API，后面会讲到它与asyncio.run_until_complete()的差异性，run_until_complete()是相对较低层的API。

注意：到底什么是事件循环？如何理解？

可以这样理解：线程一直在各个协程方法之间永不停歇的游走，遇到一个yield from 或者await就悬挂起来，然后又走到另外一个方法，依次进行下去，知道事件循环所有的方法执行完毕。
实际上loop是BaseEventLoop的一个实例，我们可以查看定义，它到底有哪些方法可调用。


二， 什么是awaitable对象——即可暂停等待的对象

有三类对象是可等待的，即 coroutines, Tasks, and Futures.
coroutine：本质上就是一个函数，一前面的生成器yield和yield from为基础，不再赘述；
Tasks: 任务，顾名思义，就是要完成某件事情，其实就是对协程函数进一步的封装；
Future：它是一个“更底层”的概念，他代表一个一步操作的最终结果，因为一步操作一般用于耗时操作，结果不会立即得到，会在“将来”得到异步运行的结果，故而命名为Future。
三者的关系，coroutine可以自动封装成task，而Task是Future的子类。


三，什么是task任务
如前所述，Task用来 并发调度的协程，即对协程函数的进一步包装？那为什么还需要包装呢？
因为单纯的协程函数仅仅是一个函数而已，将其包装成任务，任务是可以包含各种状态的，异步编程最重要的就是对异步操作状态的把控了。

（1）创建任务（两种方法）：
方法一：task = asyncio.create_task(coro())   # 这是3.7版本新添加的
方法二：task = asyncio.ensure_future(coro())
也可以使用
loop.create_future()
loop.create_task(coro)

（2）获取某一个任务的方法：
方法一：task=asyncio.current_task(loop=None)
返回在某一个指定的loop中，当前正在运行的任务，如果没有任务正在运行，则返回None；
如果loop为None，则默认为在当前的事件循环中获取，
方法二：asyncio.all_tasks(loop=None)
返回某一个loop中还没有结束的任务

task 详解：
（1）他是作为一个python协程对象，和Future对象很像的这么一个对象，但不是线程安全的；他继承了Future所有的API，，除了Future.set_result()和Future.set_Exception()；
（2）使用高层API  asyncio.ccreate_task()创建任务，或者是使用低层API loop.create_task()或者是loop.ensure_future()创建任务对象；
（3）相比于协程函数，任务时有状态的，可以使用Task.cancel()进行取消，这会触发CancelledError异常，使用cancelled()检查是否取消。


四，什么是future？
Future是一个较低层的可等待（awaitable）对象，他表示的是异步操作的最终结果，当一个Future对象被等待的时候，协程会一直等待，直到Future已经运算完毕。
Future是Task的父类，一般情况下，已不用去管它们两者的详细区别，也没有必要去用Future，用Task就可以了，
返回 future 对象的低级函数的一个很好的例子是 loop.run_in_executor().



8， python asyncio wait和gather

两者都是在协程需要并发的时候使用。

wait接受一个协程列表，返回done, peding两个集合，done里面是完成任务的协程，pending表示仍在跑的协程，通过协程.result()的方法来获取完成的结果。<coroutine object wait at 0x1095a17c8>


gather以gather(cro1, cro2, cro3, cro4…)的方式接受协程，返回的是一个结合了这么多个任务的协程<_GatheringFuture pending>，如果协程有返回值，则会返回协程充公运行之后的结果。
gather的返回值是它所绑定的所有任务的执行结果，而且顺序是不变的，即返回的result的顺序和绑定的顺序是保持一致的。
除此之外，它是awaitable的，所以，如果需要获取多个任务的返回值，既然是awaitable的，就需要将它放在一个函数里面，所以我们引入一个包装多个任务的入口main，这也是python3.7的思想


async def func1(num):
    print('--func1 start--')
    await asyncio.sleep(num)
    print('--func1 done--')
    return 'func1 ok'

async def func2(num):
    print('--func2 start--')
    await asyncio.sleep(num)
    print('--func2 done--')
    return 'func2 ok'

async def main():
    task1 = asyncio.ensure_future(func1(3))
    task2 = asyncio.ensure_future(func2(5))
    tasks = [task1, task2]
    res = await asyncio.gather(*tasks)
    return res
    # done, pending = await asyncio.wait(tasks)
    # for t in done:
    #     print(t.result())
    # print(done)
    # print(pending)

if __name__ == '__main__':
    
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())
    print(result)


9，获取协程的返回值

（1）直接通过result() 获取
async def caiye(sleep_time):
    print('i will start!')
    await asyncio.sleep(sleep_time)
    print('ending...')
    return 'caiye'

loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(caiye(3))]
loop.run_until_complete(asyncio.wait(task))
for i in task:
    print(i.result())
# 输出
i will start!
ending...
caiye  # return返回值

（2）通过定义回调函数

import asyncio
import time
 
 
async def hello1(a,b):
    print("Hello world 01 begin")
    await asyncio.sleep(3)  #模拟耗时任务3秒
    print("Hello again 01 end")
    return a+b
 
def callback(future):   #定义的回调函数
    print(future.result())
 
loop = asyncio.get_event_loop()                #第一步：创建事件循环
task=asyncio.ensure_future(hello1(10,5))       #第二步:将多个协程函数包装成任务
task.add_done_callback(callback)                      #并被任务绑定一个回调函数
 
loop.run_until_complete(task)                  #第三步：通过事件循环运行
loop.close()                                   #第四步：关闭事件循环
# '''运行结果为：
# Hello world 01 begin
# Hello again 01 end
# 15


10，协程标准模板
（四步走）（针对python3.7之前的版本）
第一步·：构造事件循环
loop=asyncio.get_running_loop() #返回（获取）在当前线程中正在运行的事件循环，如果没有正在运行的事件循环，则会显示错误；它是python3.7中新添加的
loop=asyncio.get_event_loop() #获得一个事件循环，如果当前线程还没有事件循环，则创建一个新的事件循环loop；
loop=asyncio.set_event_loop(loop) #设置一个事件循环为当前线程的事件循环；
loop=asyncio.new_event_loop()  #创建一个新的事件循环

第二步：将一个或者是多个协程函数包装成任务Task
#高层API
task = asyncio.create_task(coro(参数列表))   # 这是3.7版本新添加的
task = asyncio.ensure_future(coro(参数列表)) 
 
#低层API
loop.create_future(coro)
loop.create_task(coro)


第三步：通过事件循环运行
loop.run_until_complete(asyncio.wait(tasks))  #通过asyncio.wait()整合多个task
loop.run_until_complete(asyncio.gather(tasks))  #通过asyncio.gather()整合多个task
loop.run_until_complete(task_1)  #单个任务则不需要整合
loop.run_forever()  #但是这个方法在新版本已经取消，不再推荐使用，因为使用起来不简洁
 

# 使用gather或者wait可以同时注册多个任务，实现并发,但他们的设计是完全不一样的，在前面的2.1.(4)中已经讨论过了，主要区别如下：
# （1）参数形式不一样
# gather的参数为 *coroutines_or_futures,即如这种形式
#       tasks = asyncio.gather(*[task1,task2,task3])或者
#       tasks = asyncio.gather(task1,task2,task3)
#       loop.run_until_complete(tasks)
# wait的参数为列表或者集合的形式，如下
#       tasks = asyncio.wait([task1,task2,task3])
#       loop.run_until_complete(tasks)
# （2）返回的值不一样
# gather的定义如下，gather返回的是每一个任务运行的结果，
#       results = await asyncio.gather(*tasks) 
# wait的定义如下,返回dones是已经完成的任务，pending是未完成的任务，都是集合类型
#  done, pending = yield from asyncio.wait(fs)


第四步：关闭事件循环

loop.close()
 
'''
以上示例都没有调用 loop.close，好像也没有什么问题。所以到底要不要调 loop.close 呢？
简单来说，loop 只要不关闭，就还可以再运行：
loop.run_until_complete(do_some_work(loop, 1))
loop.run_until_complete(do_some_work(loop, 3))
loop.close()
但是如果关闭了，就不能再运行了：
loop.run_until_complete(do_some_work(loop, 1))
loop.close()
loop.run_until_complete(do_some_work(loop, 3))  # 此处异常
建议调用 loop.close，以彻底清理 loop 对象防止误用
'''

两步走（针对python3.7）
第一步：构建一个入口函数main
他也是一个异步协程函数，即通过async定义，并且要在main函数里面await一个或者是多个协程，
同前面一样，我可以通过gather或者是wait进行组合，对于有返回值的协程函数，一般就在main里面进行结果的获取。

第二步：启动主函数main
这是python3.7新添加的函数，就一句话，即
asyncio.run(main())



11 、Future对象的常用方法

（1）result()。返回Future执行的结果返回值
如果Future被执行完成，如果使用set_result()方法设置了一个结果，那个设置的value就会被返回；
如果Future被执行完成，如果使用set_exception()方法设置了一个异常，那么使用这个方法也会触发异常；
如果Future被取消了，那么使用这个方法会触发CancelledError异常；
如果Future的结果不可用或者是不可达，那么使用这个方法也会触发InvalidStateError异常；

（2）set_result(result)

标记Future已经执行完毕，并且设置它的返回值。

（3）set_exception(exception)

标记Future已经执行完毕，并且触发一个异常。

（4）done()

如果Future1执行完毕，则返回 True 。

（5）cancelled()

判断任务是否取消。

（6）add_done_callback(callback, *, context=None)

在Future完成之后，给它添加一个回调方法，这个方法就相当于是loop.call_soon()方法，参见前面，如下例子：
如果要回调带有关键字参数的函数，也需要使用partial方法哦。

（7）remove_done_callback(callback)

（8）cancel()

（9）exception()

（10）get_loop()  返回Future所绑定的事件循环

Future补充
asyncio中的Future类是模仿concurrent.futures.Future类而设计的，关于concurrent.futures.Future，可以查阅相关的文档。它们之间的主要区别是：

（1）asyncio.Future对象是awaitable的，但是concurrent.futures.Future对象是不能够awaitable的；
（2）asyncio.Future.result()和asyncio.Future.exception()是不接受关键字参数timeout的；
（3）当Future没有完成的时候，asyncio.Future.result()和asyncio.Future.exception()将会触发一个InvalidStateError异常；
（4）使用asyncio.Future.add_done_callback()注册的回调函数不会立即执行，它可以使用loop.call_soon代替；
（5）asyncio里面的Future和concurrent.futures.wait()以及concurrent.futures.as_completed()是不兼容的。



12， 协程的四种状态
协程函数相比于一般的函数来说，我们可以将协程包装成任务Task，任务Task就在于可以跟踪它的状态，我就知道它具体执行到哪一步了，
一般来说，协程函数具有4种状态，可以通过相关的模块进行查看，请参见前面的文章，他的四种状态为：

Pending
Running
Done
Cacelled

 创建future的时候，task为pending，事件循环调用执行的时候当然就是running，调用完毕自然就是done，
如果需要停止事件循环，中途需要取消，就需要先把task取消，即为cancelled。



13 多线程结合asyncio解决调用时的假死  （查看program_playdead.py 文件中的实例，更加直观）

1、asyncio专门实现Concurrency and Multithreading（多线程和并发）的函数介绍

为了让一个协程函数在不同的线程中执行，我们可以使用以下两个函数
（1）loop.call_soon_threadsafe(callback, *args)，这是一个很底层的API接口，一般很少使用，本文也暂时不做讨论。
（2）asyncio.run_coroutine_threadsafe(coroutine，loop)

第一个参数为需要异步执行的协程函数，第二个loop参数为在新线程中创建的事件循环loop，注意一定要是在新线程中创建哦，该函数的返回值是一个concurrent.futures.Future类的对象，用来获取协程的返回结果。

future = asyncio.run_coroutine_threadsafe(coro_func(), loop)   # 在新线程中运行协程

result = future.result()   #等待获取Future的结果


实例：
import asyncio, time, threading


# 需要执行的耗时异步任务
async def func(num):
    print(f'准备调用func,大约耗时{num}')
    await asyncio.sleep(num)
    print(f'耗时{num}之后,func函数运行结束')


# 定义一个专门创建事件循环loop的函数，在另一个线程中启动它
def start_loop(loop):
    asyncio.set_event_loop(loop)
    print(threading.current_thread())  # 此处表明这是个新的线程
    loop.run_forever()
    # print(threading.current_thread())


# 定义一个main函数
def main():
    coroutine1 = func(3)
    coroutine2 = func(2)
    coroutine3 = func(1)

    new_loop = asyncio.new_event_loop()  # 在当前线程下创建时间循环，（未启用），在start_loop里面启动它
    t = threading.Thread(target=start_loop, args=(new_loop,))  # 通过当前线程开启新的线程去启动事件循环
    t.start()

    asyncio.run_coroutine_threadsafe(coroutine1, new_loop)  # 这几个是关键，代表在新线程中事件循环不断“游走”执行
    asyncio.run_coroutine_threadsafe(coroutine2, new_loop)
    asyncio.run_coroutine_threadsafe(coroutine3, new_loop)

    print(threading.currentThread()) # 主线程

    for i in "iloveu":
        print(str(i) + "    ")


if __name__ == "__main__":
    main()


输出：
<Thread(Thread-1, started 15660)>
准备调用func,大约耗时3
准备调用func,大约耗时2
准备调用func,大约耗时1
<_MainThread(MainThread, started 8492)>
i    
l    
o    
v    
e    
u    
耗时1之后,func函数运行结束
耗时2之后,func函数运行结束
耗时3之后,func函数运行结束





