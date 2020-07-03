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

实例：


