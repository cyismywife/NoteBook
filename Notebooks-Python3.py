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



3， 更加容易理解的二叉树实现
class TreeNode:
    """定义树节点类"""
    def __init__(self, value, tLeft=None, tRight=None):
        self.value = value
        self.tLeft = tLeft
        self.tRight = tRight

class BinTree:
    """构造二叉树"""
    def __init__(self):
        self.root = None
        self.ls = []  # 定义列表，用于存储节点地址

    def add(self, value):
        """定义add方法， 向树结构中添加元素"""
        node = TreeNode(value)                   # 实例化树节点
        if self.root == None:
            self.root = node                     # 若根节点为None，添加根节点，并将根节点的地址值添加到self.ls中
            self.ls.append(self.root)
        else:
            rootNode = self.ls[0]                # 将第一个元素设为根节点
            if rootNode.tLeft == None:           # 若根节点的左子树为Node，添加左节点，并将其地址值添加到self.ls中
                rootNode.tLeft = node
                self.ls.append(rootNode.tLeft)
            elif rootNode.tRight == None:         # 若根节点的右子树为Node，添加右节点，并将其地址值添加到self.ls中
                rootNode.tRight = node
                self.ls.append(rootNode.tRight)
                self.ls.pop(0)                   # 弹出self.ls第一个位置处的元素

    def preOrder(self, root):
        """前序遍历(根左右)，递归实现"""
        if root == None:
            return
        print(root.value)
        self.preOrder(root.tLeft)
        self.preOrder(root.tRight)

    def inOrder(self, root):
        """中序遍历(左根右)，递归实现"""
        if root == None:
            return
        self.inOrder(root.tLeft)
        print(root.value)
        self.inOrder(root.tRight)

    def postOrder(self, root):
        """后序遍历(左右根)，递归实现"""
        if root == None:
            return
        self.postOrder(root.tLeft)
        self.postOrder(root.tRight)
        print(root.value)

    def preOrderStack(self, root):
        if root == None:
            return
        stack