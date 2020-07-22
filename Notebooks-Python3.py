1， 三元表达式 + 推导式

[i for i in range(10) if i%2==0]  最常见的
 

但是如果需要添加else，则需要稍微修改一下，把判断语句放在f循环之前
错误的写法：
((value for _, value in item.items() if not isinstance(value, list) else value[0])) 此处会提示语法错误

正确的写法
(value if not isinstance(value, list) else value[0] for _, value in item.items()) 





