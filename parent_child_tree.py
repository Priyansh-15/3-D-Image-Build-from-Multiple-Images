#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb
from rotate_translate import node

def writetofile(filename, string):
    file = open(filename, "a")
    file.write(string)
    file.close()

def createtree(nodes, filename):
    if(len(nodes) == 0):
        print("No shapes detected")
        return
    subtree = []
    string = ''
    present = node()
    present.left = nodes[0]
    nodes[0].name()
    present.string = nodes[0].string
    if(len(nodes) == 1):
        writetofile(filename, present.string)
    for i, object in enumerate(nodes[1:]):
        object.name()
        if(object.operation != 'None'):
            if(present.right == 'None'):
                present.right = object
                present.string = object.operation + "() {\n\t" + present.string + '\n\t' + object.string + '}\n'
                string = present.string
            else:
                temp = present
                present = node()
                present.left = temp
                present.string = temp.string
                present.right = object
                present.string = object.operation + "() {\n\t" + present.left.string + '\n\t' + object.string + '}\n'
                string = present.string
        else:
            if(present.right == 'None'):
                writetofile(filename, present.string)
            subtree.append(present)
            writetofile(filename, string)
            string = ''
            present = node()
            present.left = object
            present.string = object.string
            if(i == len(nodes)-2):
                writetofile(filename, present.string)
    if(string != ''):
        writetofile(filename, string)
    subtree.append(present)
    print("Subtree:", len(subtree))

