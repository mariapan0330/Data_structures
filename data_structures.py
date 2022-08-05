import os
# =============== Problem 1: Linked Lists ===============
# Using the above examples as a guide, create your own interpretation of the a Linked List class.
# You can not use the code above exactly, but again it can be used as a guide. 
# This problem requires you to think about how a linked list works and create one using your own logic.
# *Remember* A Linked List is a list of Nodes that point to the next node in the chain.
# The first Node starts out as Empty(None) and each node after points to the next.
# Your Linked List should have a traverse method and have the ability to add a new node

class Bead:

    def __init__(self, value):
        self.this_val = value
        self.next = None
    
class Linked_List:
    
    def __init__(self):
        self.current = None


    def _get_bead(self, target):
        # learned that you have to save self.current to a separate variable when checking
        # because otherwise it will set the actual current value to the "next" value
        # and it'll eliminate all the previous beads
        check = self.current
        while check != None:
            if check.this_val == target:
                return check
            check = check.next
        return None # if you checked all of them and can't find the target.

    
    def new_bead_at_front(self, new_val):
        new_bead = Bead(new_val)
        new_bead.next, self.current = self.current, new_bead

    
    def new_bead_at_end(self, new_val):
        # string along til you find the bead without a buddy
        new_bead = Bead(new_val)
        if self.current == None: # there's nothing there :O
            self.current = new_bead
        else:
            me = self.current

            while me.next != None:
                me = me.next # move along

            me.next = new_bead # if next is None, next is now the new bead.

    
        
    def insert_after(self, prev_val, new_val):
        # Wait! You need a way to find the new location.
        # So, make a "get_bead" function that can return a target bead one with that value exists.
        prev_bead = self._get_bead(prev_val)
        if prev_bead == None:
            print(f"{prev_val} is not in the chain!")
            return
        
        # If you do find the prev_val, you can continue:
        new_bead = Bead(new_val)
        # New bead hasn't been attached yet
        # To attach it, link it to whatever the prev_bead was attached to,
        # then set the prev_bead's next to the new bead.
        new_bead.next = prev_bead.next
        prev_bead.next = new_bead


    def print_list(self):
        # traverse the list, printing out everything you find.
        while self.current:
            print(self.current.this_val)
            self.current = self.current.next




# =============== Problem 2: Binary Search Tree ===============
# Using the above examples as a guide, create your own interpretation of the a Binary Search Tree class.
# You can not use the code above exactly, but again it can be used as a guide.
# This problem requires you to think about how a Binary Search Tree works and create one using your own logic.
# *Remember* Binary Search Trees start with a head node and each node to the left of that will be smaller,
# each node to the right of it will be greater. The far left node should be the lowest number(if one exists) that is available.
# The far right node (if one exists) should be the greatest number

class BST:

    def __init__(self, val):
        self.this_val = val
        self.youngest_child = None
        self.oldest_child = None
    

    def new_child(self, new_val):
        if new_val < self.this_val: # left branch
            if self.youngest_child == None:
                self.youngest_child = BST(new_val)
            else: # if it already has a younger child, try to give that child a new child 
                self.youngest_child.new_child(new_val)
        else: # right branch (or if there's no branches at all)
            if self.oldest_child == None:
                self.oldest_child = BST(new_val)
            else: # if it already has a younger child, try to give that child a new child 
                self.oldest_child.new_child(new_val)


    def send_search_party(self, target):
        if target < self.this_val: 
            # if target is younger and there is no younger child, return False
            # if target is younger and there is a younger child, send the search party there
            return False if self.youngest_child == None else self.youngest_child.send_search_party(target)
        
        elif target > self.this_val:
            return False if self.oldest_child == None else self.oldest_child.send_search_party(target)
        
        else: # if the target is not older or younger than the current child, then you've found the child.
            return True


    def find_very_oldest_child_val(self):
        # if the child has no older children, then it's the oldest
        # this metaphor is falling apart
        return self.this_val if self.oldest_child == None else self.oldest_child.find_very_oldest_child_val()
        


    def find_very_youngest_child_val(self):
        # if the child has no younger children, then it's the youngest
        return self.this_val if self.youngest_child == None else self.youngest_child.find_very_youngest_child_val()


    def kill_child(self, target, parent=None):
        # told you this metaphor is falling apart :((
        # anyway
        if target < self.this_val:
        # move left, & call kill_child again with the younger child as current and current as parent
            if self.youngest_child != None:
                self.youngest_child.kill_child(target, self)
        
        elif target > self.this_val:
        # move right, & call kill_child again with the older child as current and current as parent
            if self.oldest_child != None:
                self.oldest_child.kill_child(target, self)
            # otherwise, if the oldest_child
        
        # =============== TARGET ACQUIRED ===============
        # if the target value is neither bigger nor smaller than current val, then target is locked (it's me!, or our current position in the tree)
#                o
#              /   \
#             o     o
#            / \     \
#           o   o     o
#          / 
#         o   

        else: 
            if self.youngest_child and self.oldest_child:
            # if this child has two children, the oldest descendant of the youngest child becomes me
            # oh god this metaphor
                self.this_val = self.youngest_child.find_very_oldest_child_val()
                # Now that the oldest descendant of the younger child is me, we gotta kill the original clone of my new self
                self.oldest_child.kill_child(self.this_val, self) # oh the humanity
            
            elif parent == None:
                # if target has no parents, check if it has a younger or older child
                # (if it has BOTH, it never would have entered this elif statement)
                if self.youngest_child:
                    self.this_val = self.youngest_child.this_val
                    self.oldest_child = self.youngest_child.oldest_child
                    self.youngest_child = self.youngest_child.youngest_child
                
                elif self.oldest_child:
                    self.this_val = self.oldest_child.this_val
                    self.youngest_child = self.oldest_child.youngest_child
                    self.oldest_child = self.oldest_child.oldest_child
                
                else: # if target has no parents and no children, kill itself. :((
                    self.this_val = None
            
            elif self == parent.youngest_child:
            # If i am the younger child, and I have a younger child, then make my parent the parent of my younger child
            # IF I HAVE TWO CHILDREN I WOULD NEVER ENTER THIS ELIF STATEMENT
                if self.youngest_child:
                    parent.youngest_child = self.youngest_child
                else:
                    parent.youngest_child = self.oldest_child 
                    # If target has older child, then self.oldest_child = oldest_child object
                    # If target does not have any children, then self.oldest_child = None.

            elif self == parent.oldest_child:
            # IF I HAVE TWO CHILDREN I WOULD NEVER ENTER THIS ELIF STATEMENT
            # Q? if i am the older child, and I have an older child, then make my parent the parent of my younger child. WHAT? Why?
            # okay i swapped them and it works
                if self.oldest_child:
                    parent.oldest_child = self.oldest_child
                else:
                    parent.oldest_child = self.youngest_child




# =============== Problem 1: LINKED LIST TEST ===============

os.system('cls')
print("=== Linked List === ")
chain = Linked_List()
chain.new_bead_at_front("yellow")
chain.new_bead_at_front("orange")
chain.new_bead_at_end("green")
chain.new_bead_at_front("red")
chain.new_bead_at_end("purple")
chain.insert_after("green",'blue')
chain.insert_after("green",'teal')
chain.print_list()



# =============== Problem 2: BST TEST ===============

print("\n=== Binary Search Tree ===")
fam_tree = BST("James")
fam_tree.new_child("Fred")
fam_tree.new_child("Lily")
fam_tree.new_child("Hamlet")
fam_tree.new_child("Bert")
fam_tree.new_child("Mark")
fam_tree.new_child("Aaron")
fam_tree.new_child("Caesar")
fam_tree.new_child("Ingrid")
# --- Find children --- 
print("Fred: ", fam_tree.send_search_party("Fred"))
print("Hamlet: ",fam_tree.send_search_party("Hamlet"))
print("Ingrid: ", fam_tree.send_search_party("Ingrid"))
# --- Kill Hamlet --- (again)
print("--- Kill Hamlet ---")
fam_tree.kill_child("Hamlet")
print("Fred: ", fam_tree.send_search_party("Fred"))
print("Hamlet: ", fam_tree.send_search_party("Hamlet"))
print("Ingrid: ", fam_tree.send_search_party("Ingrid"))


#                James
#               /     \
#             Fred     Lily
#            /    \        \
#          Bert   Hamlet    Mark
#          /  \       \
#     Aaron  Caesar   Ingrid