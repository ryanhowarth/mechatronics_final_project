#!/usr/bin/python
def node_proc(dic, tree_lst, path_lst):#current node, node index, back or forward
    '''tree_lst=[current node, previous node, node index, forward or back]'''
    if tree_lst[3]=='b':#backward
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
    elif tree_lst[3]=='f':#forward
        '''add the child nodes into the dic'''
        for i in xrange(3):
            if path_lst[i]:#add child node into the dictionary
                tree_lst[2]+=1#get the new number of the node
                dic[tree_lst[0]][0][i]=tree_lst[2]#include the index of every child node
                dic[tree_lst[2]]=[[0,0,0],[0,0,0],tree_lst[0],'N']#add node into dictionary, child index, xmas tree flag, parent node, which path
                if i==0:
                    dic[tree_lst[2]][3]='L'
                elif i==1:
                    dic[tree_lst[2]][3]='M'
                elif i==2:
                    dic[tree_lst[2]][3]='R'
        '''decide the next node'''
        if path_lst[0]:#left child exists
            tree_lst[1]=tree_lst[0]#set the current node as the previous node
            tree_lst[0]=dic[tree_lst[0]][0][0]
        elif path_lst[1]:#no left child, only middle child or m-child & r-child
            tree_lst[1]=tree_lst[0]
            tree_lst[0]=dic[tree_lst[0]][0][1]
        else:#dead end
            tree_lst[1]=tree_lst[0]
            tree_lst[0]=dic[tree_lst[0]][2]#set the parent node as the next node
            tree_lst[3]='b'#backward
