# -------------- BinaryTree class --------------
class BinaryTree():

    # -------------- nested class _Node and its methods
    class _Node:
        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
        def element(self):
            return self._element  
        def parent(self):
            return self._parent  
        def left(self):
            return self._left 
        def right(self):
            return self._right
        
    # ----------------- methods for class BinaryTree 
    def __init__(self, traversal_method='inorder'):
        self._root = None
        self._size = 0
        self._traversal_method = traversal_method

    def __len__(self):
        return self._size

    def add_root(self, e):
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._root
    
    def add_left(self, parent_node, e):
        if parent_node is None:
            raise ValueError('parent_node is empty')
        self._size += 1
        me_node = self._Node(e, parent_node)
        parent_node._left = me_node
        return me_node
    
    def add_right(self, parent_node, e):
        if parent_node is None:
            raise ValueError('parent_node is empty')
        self._size += 1
        me_node = self._Node(e, parent_node)
        parent_node._right = me_node
        return me_node
    
    def root(self):
        return self._root   

    def parent(self, node):
        if node is None:
            raise ValueError('node is empty')
        return node.parent()
    
    def left(self, node):
        if node is None:
            raise ValueError('node is empty')
        return node.left()
    
    def right(self, node):
        if node is None:
            raise ValueError('node is empty')
        return node.right()

    def traversal_method(self):
        return self._traversal_method
    
    def set_traversal_method(self, traversal_method):
        self._traversal_method = traversal_method

    def num_children(self, node):
        left_count = 1 if node.left() is not None else 0
        right_count = 1 if node.right() is not None else 0
        return left_count + right_count
    
    def children(self, node):
        if node.left() is not None:
            yield node.left()
        if node.right() is not None:
            yield node.right()   
    
    def descendants_order_by(self, node, method="inorder"):
        return self.traversal(node, method)

    def get_index_from_list(self, element, list):
        for i in range(len(list)-1):
            if element == list[i]:
                return i
        return -1

    # create and return a new tree which is a copy of the existing source tree or subtree 
    def copy_tree(self, rooted_note):
        new_tree = BinaryTree()
        if rooted_note is None:
           return new_tree
        
        # store source and new mapping nodes (corresponding nodes share same index values)
        source_nodes = []
        copied_nodes = []
        total_nodes = 0

        # for each node in source tree, create a new node containing the same element (for new tree), 
        #   copy the mapping nodes to source_nodes & source_nodes
        for src_node in self.descendants_order_by(rooted_note, method="preorder"): 
            total_nodes += 1
            new_node = new_tree._Node(src_node.element())
            source_nodes.append(src_node)
            copied_nodes.append(new_node)  

        # copy tree linking data (i.e., parents / lefts / rights / _root if exist) 
        #   from nodes in source tree to nodes in new tree 
        for src_node in self.descendants_order_by(rooted_note, method="preorder"): 
            cpy_node = copied_nodes[self.get_index_from_list(src_node, source_nodes)]

            if src_node is rooted_note:
               new_tree._root = cpy_node

            src_parent = src_node._parent
            if not src_parent is None:
               cpy_parent = copied_nodes[self.get_index_from_list(src_parent, source_nodes)]
               cpy_node._parent = cpy_parent

            src_left = src_node._left
            if not src_left is None:
               cpy_left = copied_nodes[self.get_index_from_list(src_left, source_nodes)]
               cpy_node._left = cpy_left

            src_right = src_node._right
            if not src_right is None:
               cpy_right = copied_nodes[self.get_index_from_list(src_right, source_nodes)]
               cpy_node._right = cpy_right

        new_tree._size = total_nodes
        return new_tree

    def __iter__(self):
        return self.traversal(self.root())

    def is_root(self, node):
        return self.root() == node
    
    def is_leaf(self, node):
        return self.num_children(node) == 0
    
    def is_empty(self):
        return len(self) == 0         
    
    def sibling(self, node):
        if node is None: return None
        parent = self.parent(node)
        if parent is None: 
           return None   
        else:
           if node == self.left(parent):
              return self.right(parent)
           else:
              return self.left(parent) 
    
    def replace(self, node, e):
        old = node._element
        node._element = e
        return old
   
    # delete a node if it has no more than one child, 
    #  shift its child (either left or right) up one level
    def delete(self, node):
      
        if node is None:
            raise ValueError('node is empty')
        
        if self.num_children(node) == 2:
            raise ValueError('node has two children')
    
        child = node.left() if node.left() else node.right()
        if child is not None:
           child._parent = node._parent
        if node is self._root:
           self._root = child
        else:
           parent = node._parent
           if node is parent._left:
              parent._left = child
           else:
              parent._right = child
        self._size -= 1
        node._parent = node  # deprecated node
        return node._element
    
    # delete a node and its subtree 
    def delete_subtree_rooted_from_node(self, node): 
      
        if node is None:
           raise ValueError('node is empty')
        
        # for each descendant_node in inorder traversal: delete/deprecated the descendant_node
        for descendant_node in self.descendants_order_by(node, method="inorder"): # in inorder to delete subtree node by node        
            parent = descendant_node.parent()
            
            if parent._left == descendant_node:
               # if descendant_node is its parent's left child, set its parent's left child empty
               parent._left = None  
            elif parent._right == descendant_node:
               # if descendant_node is its parent's right child, set its parent's right child empty
               parent._right = None  
            
            self._size -= 1
            descendant_node._parent = descendant_node # deprecated node
                   
    def __iter__(self):
        return self.traversal(self.root(), self.traversal_method())

    def traversal(self, node_as_root, method=None):
        if node_as_root is None:
           return []

        if method not in ['preorder', 'inorder', 'postorder', 'breadthfirst']:
           method = self.traversal_method    # use self.traversal_method when method is not passed

        if method == 'breadthfirst':
            queue = []                        # use queue (FIFO) during traversal
            queue.append(node_as_root)        # push root to queue
            while len(queue) > 0:
                node = queue.pop(0)           # pop the first node from queue 
                yield node
                if self.left(node) is not None: 
                    # when node has left node => push left child node to queue (Note: left child first)   
                   queue.append(self.left(node))      
                if self.right(node) is not None:   
                   # when node has right node => push right child node to queue (Note: right child last)       
                   queue.append(self.right(node))      
        else:
            # 'preorder', 'inorder', 'postorder'
            stack = []                       # use stack (LIFO) during traversal   
            const_first_pushed = 1
            stack.append((node_as_root, const_first_pushed))   # push root to stack, marked as 1st time pushed

            while len(stack) > 0:
                (node, pushed_which_time) = stack.pop()        # pop from stack (last node)

                if pushed_which_time > const_first_pushed or (self.left(node) is None and self.right(node) is None):     
                # is 2nd time pushed OR the node has no children => yield node to return collection
                   yield node
                else:   
                # node is NOT 2nd time pushed, AND the node has at least one child => 
                #   need to push the node and any of its children to stack, in reverse order (due to LIFO stack) per traversal method's value (preorder or inorder or postorder) 
                #   example: when we want to print in postorder Left=>Right=>Node, we will push stack in the order of Node=>Right=>Left    
                   pushed_which_time += 1 # add 1 to its pushed_which_time value (so that next time we know it is time to output the node when it gets popped again)    
              
                   if method == 'postorder': 
                      # push node for postorder (Note that 1 was added to its pushed_which_time value above)                             
                      stack.append((node, pushed_which_time)) 
                  
                   if self.right(node) is not None:  
                      # when the node has right node => push right child node to stack, marked as 1st time pushed  
                      stack.append((self.right(node), const_first_pushed))      
                   if method == 'inorder': 
                      # push the node for inorder (Note that 1 was added to its pushed_which_time value above)                                      
                      stack.append((node, pushed_which_time)) 
                   if self.left(node) is not None:  
                      # when the node has left node => push left child to stack, marked as 1st time pushed
                      stack.append((self.left(node), const_first_pushed)) 
                   if method == 'preorder': 
                      # push the node for preorder (Note that 1 was added to its pushed_which_time value above)                             
                      stack.append((node, pushed_which_time)) 

    # attach trees t1 and t2 as left and right subtrees of external node
    def attach(self, node, t1, t2): 

        if not self.is_leaf(node):
           raise ValueError('node must be leaf')
        if not type(self) is type(t1) is type(t1):
            raise TypeError('Tree types must match')
        
        self._size += len(t1) + len(t2)
        if not t1.is_empty(): 
            t1._root._parent = node # point t1._root's parent to the node 
            node._left = t1._root   # point the node's left to t1._root
            t1._root = None         # empty t1
            t1._size = 0            
        if not t2.is_empty():
            t2._root._parent = node # point t2._root's parent to the node
            node._right = t2._root  # point the node's right to t2._root
            t2._root = None         # empty t2
            t2._size = 0           

    def print_tree_traversal(self, info, method):
        print("** " + info + " " + method + " traversal " + ": " + "".join(','  + node.element() for node in self.traversal(self.root(), method))[1:])


# -------------- testing code for methods in BinaryTree class --------------
# Build Tree T
T = BinaryTree()
root = T.add_root('50')
L = T.add_left(T.root(), '30')
R = T.add_right(T.root(), '70')
LL = T.add_left(L, '20')
LR = T.add_right(L, '40')
RL = T.add_left(R, '60')
RR = T.add_right(R, '80')
LLL = T.add_left(LL, '15')
LRL = T.add_left(LR, '35')
print("\n")
print(" action: built tree T")
print(" ========== Treverse Tree T in " + T.traversal_method() + " : " + "".join(','  + node.element() for node in T)[1:])

# replace method
T.replace(R, '71')
print(" action: replaced R from 70 to 71")
T.print_tree_traversal('Tree T', 'inorder')

T.print_tree_traversal('Tree T', 'breadthfirst')
T.print_tree_traversal('Tree T', 'preorder')
T.print_tree_traversal('Tree T', 'postorder')

# delete method: delete a node
T.delete(LR)
print(" action: deleted LR (i.e. 40)")
T.print_tree_traversal('Tree T', 'inorder')

# add_right: add a new node with element 25 to the right of a node LL
LLR = T.add_right(LL, '25')
print(" action: added right at LL (i.e. 25)")

T.print_tree_traversal('Tree T', 'inorder')
T.print_tree_traversal('Tree T', 'preorder')
T.print_tree_traversal('Tree T', 'postorder')

# Build Tree T1
T1 = BinaryTree()
T1_root = T1.add_root('23')
T1_L = T1.add_left(T1.root(), '22')
T1_R = T1.add_right(T1.root(), '24')
print(" action:  built Tree T1")
T1.print_tree_traversal('Tree T1', 'inorder')

# Build Tree 2
T2 = BinaryTree()
T2_root = T2.add_root('26')
T2_R = T2.add_right(T2.root(), '28')
T2_RL = T2.add_left(T2_R, '27')
T2_RR = T2.add_right(T2_R, '29')
print(" action: built Tree T2")
T2.print_tree_traversal('Tree T2', 'inorder')

# attach method: attach trees T1 and T2 to a leaf node as left and right
T.attach(LLR, T1, T2)
print(" action: attached T1 and T2 to T on LLR (i.e. 25)")
T.print_tree_traversal('Tree T', 'inorder')
T.print_tree_traversal('Tree T', 'postorder')

# copy_tree method: copy entire tree to a new tree 
new_T3 = T.copy_tree(T.root())
print(" action: copied entire tree T to new_T3")
new_T3.print_tree_traversal('Tree new_T3', 'inorder')

# copy_tree method: copy a sub tree to a new tree
new_T4 = T.copy_tree(L)
print(" action: copied subtree from L containing value 30 in tree T to new_T4")
new_T4.print_tree_traversal('Tree new_T4', 'inorder')

# delete_subtree_rooted_from_node method: delete a sub tree (including rooted note and all descendent nodes)
T.delete_subtree_rooted_from_node(L)
print(" action: deleted subtree (from rooted node L, i.e. 30) from T")
T.print_tree_traversal('Tree T', 'inorder')

print("\n")