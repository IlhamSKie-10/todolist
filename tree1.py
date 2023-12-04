class Node:
    def __init__(self, key):
         self.left = None
         self.key = key
         self.right = None
    
class Tree:
    def insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if key < root.key:
                root.left = self.insert(root.left, key)
            elif key > root.key:
                root.right = self.insert(root.right, key)
        return root
    
    def inorder_traversal(self, root):
        hasil = []
        if root:
            hasil += self.inorder_traversal(root.left)
            hasil.append(root.key)
            hasil += self.inorder_traversal(root.right)
        return hasil
            
tree = Tree()
root = None
keys = [100,90,80,60,40,34,20,11,15]

for  key in keys:
    root = tree.insert(root, key)
    
print("urutan : ", tree.inorder_traversal(root))
    
            
        