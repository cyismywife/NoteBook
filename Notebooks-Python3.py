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
                # 下面这句很关键
                self.ls.pop(0)                   # 弹出self.ls第一个位置处的元素， 就是为了始终从树的左节点开始添加

                # 仔细说明一下，我们现在需要把0-9等10个元素解析成熟，开始self.is 为空列表。 首次添加的时候，ls变成了[0]
                # 第二次添加的时候ls变成了[0,1]， 第三次添加的时候，还未执行最后一句时候，ls为[0, 1, 2], 如果没有最后一句弹出ls中的第一个元素
                	# 那么等到第四次添加元素的时候，依旧还是会根节点的左节点上添加3这个元素，正确的应该是在1这个节点的左节点上面添加才是，
                		# 所以才需要执行最后一句

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
        """前序遍历（根左右）， 堆栈实现"""
        if root == None:
            return
        stack = []
        result = []
        node = root

        while node or stack:
            while node:    # 寻找当前节点的的左节点，并将其地址添加到stack中
                result.append(node.value)
                stack.append(node)
                node = node.tLeft   # 当某节点不再有左子节点的时候，退出内循环
            node = stack.pop()
            node = node.tRight
        print(result)

    def postOrderStack(self,root):
        """后序遍历（左右根）：堆栈实现。后序遍历的访问顺序（左右根）
        可以看成讲先序遍历顺序（根左右）改为（根右左）后的逆序（左右根）"""
        if root == None:
            return

        stack = []
        seq = []
        result = []
        node = root
        while node or stack:
            while node:
                seq.append(node.value)
                stack.append(node)
                node = node.tRight
            node = stack.pop()
            node = node.left
        while seq:                      # 若seq不为[]，讲seq中的元素逆序添加到result中
            result.append(seq.pop())
        print(result)

    def printLeafNode(self, root):
        """打印二叉树的叶子结点"""
        if root == None:
            return
        if root.tLeft == None and root.tRight == None:
            print(root.value)
        self.printLeafNode(root.tLeft)
        self.printLeafNode(root.tRight)



if __name__ == '__main__':
    myCaiye = BinTree()
    for i in range(9):
        myCaiye.add(i)

    myCaiye.preOrderStack(myCaiye.root)
    myCaiye.preOrder(myCaiye.root)