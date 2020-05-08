"""
Name: interview.py
Author: lsy
Time: 2020/4/28
"""



class Tree():
    def __int__(self, left, right, root):
        self.left = None
        self.right = None
        self.root = None



def make_tree(self):
    # 假设得到相对应的依赖，并且把每个依赖的root存到array里面
    # 假设:
    roots = ['A', 'F']
    #
    leafs = {
        'A': ['B','C'],
        'C': ['D']
    }

    for root in roots:
        tree = Tree(None, None, root)
        nodes = leafs[root]
        for node in nodes:
            if node in leafs.keys():
                # 把该node当做一个root节点，再次生成一个tree
                tree.right = Tree(None, None, node)
            else:
                tree.left = node


def compare_tree(t1, t2):
    """
    compare the trees
    :param t1:
    :param t2:
    :return:
    """

    # by using loop
    if t1 is None or t2 is None:
        return
    if (t1.left == t2.left) or (t1.right == t2.left)
        or (t1.left == t2.right) or (t1.right == t2.right)
        # 从t1删除，或者从t2删除
        del node from t1

    compare_tree(t1.left, t2.left)
    compare_tree(t1.right, t2.right)
    compare_tree(t1.left, t2.right)
    compare_tree(t1.root, t2.root)



finished = []

def complie(tree, node):
    """
    make a complie function
    1. 先编译最底层的依赖
    2. loop循环上层的所有的依赖进行编译
    3. 编译完所有的源码

    可以使用递归的方式
    :param tree:
    :return:
    """

    if node is None:
        return

    complie(tree, tree.left)
    complie(tree, tree.right)
    complie(tree, tree.root)
    # 放到服务器并发

    if node.depe not in finished:
        return
    else:
        make_complie(node)
        finished.append(node)
