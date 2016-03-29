#!/usr/bin/python

# dictionary format
# dic[X][0] is the children node indices. Index 0 is left, Index 1 is middle, Index 2 is right
# dic[X][1] is the tree/present flags
# dic[X][2] is the index of the parent node
# dic[X][3] is the "L", "M", or "R" of the parent node (possibly redundant)

# tree_lst form: [current node, previous node, largest node index, forward or back]
def node_proc(dic, tree_lst, path_lst): #current node, node index, back or forward

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
                dic[tree_lst[2]]=createNode(tree_lst[0],i) 

                # If we haven't determined the next node yet (we only want to do this once)
                if nextNodeUnset:
                    # If it's not a dead end, the next node is the left or middle nodes (indices 0 or 1)
                    if i != 2:
                        tree_lst[0]=dic[tree_lst[0]][0][i]
                        nextNodeUnset = False # only assign the next node once
                    # Otherwise, it is a dead end and the next node is actually the parent node
                    else
                        tree_lst[0]=dic[tree_lst[0]][2]
                        tree_lst[3]='b'

    # Otherwise it's moving backward        
    else:
        # If root is reached, terminate. This should not happen in real trials
        if dic[tree_lst[0]][3]=='N':
            tree_lst[3]='e'

        # Otherwise, continue to navigate
        else:

            # The old current node becomes the new previous node
            tree_lst[1]=tree_lst[0]

            # Coming back from the left node, next will be middle or right (both going forward)
            if dic[tree_lst[1]][3]=='L':

                # If middle exists, go middle
                if dic[tree_lst[0]][0][1]:
                    tree_lst[0] = dic[tree_lst[0]][0][1]
                # Otherwise right must exist, go right
                else:
                    tree_lst[0]=dic[tree_lst[0]][0][2]  
                
                tree_lst[3]='f' # Go forward for either case
            
            # Coming back from middle node, next will be right or backwards
            elif dic[tree_lst[1]][3]=='M':#back from the middle child

                # If right exists, go right
                if dic[tree_lst[0]][0][2]:
                    tree_lst[0]=dic[tree_lst[0]][0][2]
                    tree_lst[3]='f' # Go forward in this case
                # Otherwise continue going backwards (to previous parent node)
                else:
                    tree_lst[0]=dic[tree_lst[0]][2]    

            # Coming back from right node, continute going backwards (to previous parent node)
            else:
                tree_lst[0]=dic[tree_lst[0]][2]
                                     
    
def lmrNode(index):
    if index==0:
        return 'L'
    elif index==1:
        return 'M'
    else:
        return 'R'

def createNode(parent, directionIdx):
    return [[0,0,0],[0,0,0],parent, lmrNode(directionIdx)]