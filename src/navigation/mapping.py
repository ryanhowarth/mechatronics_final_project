#!/usr/bin/python

# dictionary format
# dic[X][0] is the children node indices. Index 0 is left, Index 1 is middle, Index 2 is right
# dic[X][1] is the tree/present flags
# dic[X][2] is the index of the parent node
# dic[X][3] is the "L", "M", or "R" of the parent node (possibly redundant)

# tree_lst form: [current node, previous node, largest node index, forward or back]
def node_proc(dic, tree_lst, path_lst, treeGiftPath): #current node, node index, back or forward

	# Check if node is moving forward
	if tree_lst[3]=='f':

		# The old current node becomes the new previous node
		tree_lst[1]=tree_lst[0]

		nextNodeUnset = True

		# Assume deadend, this will like change in 41-42
		nextNode=dic[tree_lst[0]][2]
		tree_lst[3]='b'

		# Add the child nodes into the dictionary
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
						nextNode = dic[tree_lst[0]][0][i]
						tree_lst[3]='f'
						nextNodeUnset = False # only assign the next node once 
		tree_lst[0] = nextNode

	# Otherwise it's moving backward        
	else:
		# If root is reached, terminate. This should not happen in real trials
		if dic[tree_lst[0]][3]=='N':
			tree_lst[3]='e'

		# Otherwise, continue to navigate
		else:

			# Coming back from the left node, next will be middle or right (both going forward)
			if dic[tree_lst[1]][3]=='L':
				tree_lst[1]=tree_lst[0]

				# If middle exists, current node gets middle. Else, current node gets left
				tree_lst[0] = dic[tree_lst[0]][0][1] if dic[tree_lst[0]][0][1] else dic[tree_lst[0]][0][2]
				
				tree_lst[3]='f' # Go forward for either case
			
			# Coming back from middle node, next will be right or backwards
			elif dic[tree_lst[1]][3]=='M':#back from the middle child
				tree_lst[1]=tree_lst[0]

				# If right exists, go right
				if dic[tree_lst[0]][0][2]:
					tree_lst[0]=dic[tree_lst[0]][0][2]
					tree_lst[3]='f' # Go forward in this case
				# Otherwise continue going backwards (to previous parent node)
				else:
					tree_lst[0]=dic[tree_lst[0]][2]    
				
			# Coming back from right node, continute going backwards (to previous parent node)
			else:
				tree_lst[1]=tree_lst[0]
				tree_lst[0]=dic[tree_lst[0]][2]

	if treeGiftPath[1]:
		if tree_lst[3]=='f':
			print 'add!'
			treeGiftPath[tree_lst[4]] = tree_lst[1]
			tree_lst[4] += 1
		else:
			print 'remove!'
			del treeGiftPath[tree_lst[1]]
			tree_lst[4] -= 1
		print treeGiftPath

									 
	
def lmrNode(index):
	if index==0:                 
		return 'L'
	elif index==1:
		return 'M'
	else:
		return 'R'

def createNode(parent, directionIdx):
	return [[0,0,0],[0,0,0], parent, lmrNode(directionIdx)]
'''
def search_path(dic,tree_lst):#return a list of turns
	path_idx_dic={'L':0,'M':1,'R':2}
	cur_node=tree_lst[0]
	pre_node=tree_lst[1]
	edge_lst=[(cur_node,pre_node)]
	node_flag_lst=[True]*tree_lst[2]
	node_flag_lst[cur_node-1]=False
	cur_edge=0
	while cur_edge<len(edge_lst):#get a list of edges, the last edge in the list contains the xmas tree
		cur_node=edge_lst[cur_edge][1]
		next_node=dic[cur_node][2]#check the parent node of current node
		if next_node and node_flag_lst[next_node-1]:#if not root node and this node has not been checked
			edge_lst.append((cur_node,next_node))#add the edge to the list
			node_flag_lst[next_node-1]=False#node checked
			if dic[next_node][1][path_idx_dic[dic[cur_node][3]]]:#if the tree is inside the edge
				break#the edge has been found, break the while
		for i in xrange(3):#check 3 child node of the current node
			next_node=dic[cur_node][0][i]
			if next_node and node_flag_lst[next_node-1]:#if child node exists and has not been checked
				edge_lst.append((cur_node,next_node))
				node_flag_lst[next_node-1]=False
				if dic[cur_node][1][i]:
					break   
		cur_edge+=1
	#the last edge in the list has the tree, start from this edge to find the path
	link_node=edge_lst[-1][1]
	for i in xrange(len(edge_lst)-1,-1,-1):     
		if edge_lst[i][1]==link_node:
			link_node=edge_lst[i][0]
		else:
			del edge_lst[i]
	#the edge_lst should only contain the path from the present to the tree now
	turn_lst=[]
	turn_dic={('R','P'):'L',('M','P'):'M',('L','P'):'R',('R','M'):'R',('R','L'):'M',('M','L'):'R'}
	for i in xrange(1,len(edge_lst)):
		if dic[edge_lst[i-1][0]][2]==edge_lst[i-1][1] and dic[edge_lst[i][0]][2]==edge_lst[i][1]:#c->p->p
			turn=turn_dic[(dic[edge_lst[i-1][0]][3],'P')]
			turn_lst.append(turn)
		elif dic[edge_lst[i-1][0]][2]==edge_lst[i-1][1] and dic[edge_lst[i][0]][2]!=edge_lst[i][1]:#c->p->c
			turn=turn_dic[(dic[edge_lst[i-1][0]][3],dic[edge_lst[i][1]][3])]
						turn_lst.append(turn)
		elif dic[edge_lst[i-1][0]][2]!=edge_lst[i-1][1] and dic[edge_lst[i][0]][2]!=edge_lst[i][1]:#p->c->c
			turn=dic[edge_lst[i][1]][3]
			turn_lst.append(turn)
		else:
			pass
	return turn_lst
	'''