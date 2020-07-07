程序假死
一个例子： 窗口程序的假死


（1）同步假死
代码如下：
import tkinter as tk          # 导入 Tkinter 库
import time
 
class Form:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry('500x300')
        self.root.title('窗体程序')  #设置窗口标题
 
        self.button=tk.Button(self.root,text="开始计算",command=self.calculate)
        self.label=tk.Label(master=self.root,text="等待计算结果")
 
        self.button.pack()
        self.label.pack()
        self.root.mainloop()
 
    def calculate(self):
        time.sleep(3)  #模拟耗时计算
        self.label["text"]=300
 
if __name__=='__main__':
    form=Form()

运行的结果就是，我单机一下“开始计算”按钮，然后窗体会假死，这时候无法移动窗体、也无法最大化最小化、3秒钟之后，“等待计算结果”的label会显示出3，然后前面移动的窗体等操作接着发生
上面的窗口会假死，无可厚非
因为，所有的操作都是同步方法，只有一个线程，负责维护窗体状态的线程和执行好使计算的线程是同一个，当遇到time.sleep()的时候自然会遇到阻塞



（2）异步假死

import tkinter as tk          # 导入 Tkinter 库
import asyncio
 
class Form:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry('500x300')
        self.root.title('窗体程序')  #设置窗口标题
        
        self.button=tk.Button(self.root,text="开始计算",command=self.get_loop)
        self.label=tk.Label(master=self.root,text="等待计算结果")
 
        self.button.pack()
        self.label.pack()
 
        self.root.mainloop()
     
    #定义一个异步方法，模拟耗时计算任务
    async def calculate(self):
        await asyncio.sleep(3)
        self.label["text"]=300
    
    #asyncio任务只能通过事件循环运行，不能直接运行异步函数
    def get_loop(self):
        self.loop=asyncio.get_event_loop()
        self.loop.run_until_complete(self.calculate())
        self.loop.close()
 
 
if __name__=='__main__':
    form=Form()


我们发现，窗体依然会造成阻塞，情况和前面的同步方法是一样的，为什么会这样呢？因为这个地方虽然启动了事件循环，但是拥有事件循环的那个线程同时还需要维护窗体的状态，
始终只有一个线程在运行，当单击“开始计算”按钮，开始执行get_loop函数，在get_loop里面启动异步方法calculate，然后遇到await，这个时候事件循环暂停，
但是由于事件循环只注册了calculate一个异步方法，也没其他事情干，所以只能等待，造成假死阻塞。


（3）最终的结局方案： tkinter+threading+asyncio

import tkinter as tk          # 导入 Tkinter 库
import time
import asyncio
import threading
 
class Form:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry('500x300')
        self.root.title('窗体程序')  #设置窗口标题
        
        self.button=tk.Button(self.root,text="开始计算",command=self.change_form_state)
        self.label=tk.Label(master=self.root,text="等待计算结果")
 
        self.button.pack()
        self.label.pack()
 
        self.root.mainloop()
 
    async def calculate(self):
        await asyncio.sleep(3)
        self.label["text"]=300
 
    def get_loop(self,loop):
        self.loop=loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    def change_form_state(self):
        coroutine1 = self.calculate()
        new_loop = asyncio.new_event_loop()                        #在当前线程下创建时间循环，（未启用），在start_loop里面启动它
        t = threading.Thread(target=self.get_loop,args=(new_loop,))   #通过当前线程开启新的线程去启动事件循环
        t.start()
 
        asyncio.run_coroutine_threadsafe(coroutine1,new_loop)  #这几个是关键，代表在新线程中事件循环不断“游走”执行
 
 
if __name__=='__main__':
    form=Form()

运行上面的代码，我们发现，此时点击“开始计算”按钮执行耗时任务，没有造成窗体的任何阻塞，我可以最大最小化、移动等等，然后3秒之后标签会自动显示运算结果。为什么会这样？

上面的代码中，get_loop()、change_form_state()、__init__()都是定义在主线程中的，窗体的状态维护也是主线程，二耗时计算calculate()是一个异步协程函数。

现在单击“开始计算按钮”，这个事件发生之后，会触发主线程的chang_form_state函数，然后在该函数中，会创建新的线程，
通过新的线程创建一个事件循环，然后将协程函数注册到新线程中的事件循环中去，达到的效果就是，主线程做主线程的，新线程做新线程的，不会造成任何阻塞。
