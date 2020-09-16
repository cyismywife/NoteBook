1， 三元表达式 + 推导式

[i for i in range(10) if i%2==0]  最常见的
 

但是如果需要添加else，则需要稍微修改一下，把判断语句放在f循环之前
错误的写法：
((value for _, value in item.items() if not isinstance(value, list) else value[0])) 此处会提示语法错误

正确的写法
(value if not isinstance(value, list) else value[0] for _, value in item.items()) 



2， 

class BinaryTree:
	# 二叉树
    def __init__(self, rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self, newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.left = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.right = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, obj):
        self.key = obj

    def getRootVal(self):
        return self.key


def buildParseTree(fpexp):
	# 将算数表达式解析成二叉树
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()
        elif i not in '+-*/)':
            currentTree.setRootVal(eval(i))
            parent = pStack.pop()
            currentTree = parent
        elif i in '+-*/':
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError('Unknown Operator: ' + i)

    return eTree


def evaluate(parseTree):
	# 计算二叉解析树的递归函数
    opers = {'+':operator.add, '-':operator.sub,
             '*':operator.mul, '/':operator.truediv}
    leftC = parseTree.getLeftChild()
    rightC = parseTree.getRightChild()

    if leftC and rightC:
        fn = opers[parseTree.getRootVal()]
        return fn(evaluate(leftC), evaluate(rightC))
    else:
        return parseTree.getRootVal()


if __name__ == '__main__':
	dd = '( ( 3 + ( 4 * 5 ) ) - 9 )'
    cc = buildParseTree(dd)
    ee = evaluate(cc)
    print(ee)  # 输出： 14
