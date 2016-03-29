#!/usr/bin/python

# dictionary format
# dic[X][0] is the children node indices. Index 0 is left, Index 1 is middle, Index 2 is right
# dic[X][1] is the tree/present flags
# dic[X][2] is the index of the parent node
# dic[X][3] is the "L", "M", or "R" of the parent node (possibly redundant)

# tree_lst form: [current node, previous node, largest node index, forward or back]
def node_proc(dic, tree_lst, path_lst): #current node, node index, back or forward
    '''tree_lst=[current node, previous node, node index, forward or back]'''

    # Check if node is moving forward
    if tree_lst[3]=='f':

        # The old current node becomes the new previous node
        tree_lst[1]=tree_lst[0]

        # Add the child nodes into the dictionary
        nextNodeUnset = True
        for i in xrange(3):

            # Check if new direction is detected
            if path_lst[i]: 
                # Update node number of node to be added
                tree_lst[2] += 1 

                # Assign child node to parent node
                dic[tree_lst[0]][0][i]=tree_lst[2]

                # Create child node and add to dictionary           
                dic[tree_lst[2]]=[[0,0,0],[0,0,0],tree_lst[0], lmrNode(i)]#add node into dictionary, child index, xmas tree flag, parent node, which path

                # If we haven't determined the next node yet (we only want to do this once)
                if nextNodeUnset:
                    # If it's not a dead end, the next node is the left or middle nodes (indices 0 or 1)
                    if i != 2:
                        tree_lst[0]=dic[tree_lst[0]][0][i]
                        nextNodeUnset = False # only assign the next node once
                    # Otherwise, it is a dead end and the next node is actually the parent node
                    else
                        tree_lst[0]=dic[tree_lst[0]][2]
                        tree_lst[3]='b'#backward

            
    else: #backward
        if dic[tree_lst[0]][3]=='N':#current node is the root node
            tree_lst[3]='e'#end
        else:
            if dic[tree_lst[1]][3]=='R':#back from the right child
                tree_lst[1]=tree_lst[0]#current node as the previous node
                tree_lst[0]=dic[tree_lst[0]][2]#set the parent node as the next node
            elif dic[tree_lst[1]][3]=='M':#back from the middle child
                tree_lst[1]=tree_lst[0]#current node as the previous node
                if dic[tree_lst[0]][0][2]:#right child exists
                    tree_lst[0]=dic[tree_lst[0]][0][2]#set the child node as the next node
                    tree_lst[3]='f'#forward
                else:#no right child, go backwards
                    tree_lst[0]=dic[tree_lst[0]][2]#set the parent node as the next node
            elif dic[tree_lst[1]][3]=='L':#back from the left child
                tree_lst[1]=tree_lst[0]#current node as the previous node
                if dic[tree_lst[0]][0][1]:#middle child exists
                    tree_lst[0]=dic[tree_lst[0]][0][1]
                    tree_lst[3]='f'#forward
                else:#no middle child, only right node
                    tree_lst[0]=dic[tree_lst[0]][0][2]
                    tree_lst[3]='f'#forward
    

def lmrNode(index):
    if index==0:
        return 'L'
    elif index==1:
        return 'M'
    else:
        return 'R'