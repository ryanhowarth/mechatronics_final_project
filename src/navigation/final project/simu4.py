#!/usr/bin/python
import numpy as np
import time
import cv2
import mapping
def color(m, w, b):
	row,col=m.shape
	for i in xrange(row):
		for j in xrange(col):
			if m[i,j]:
				m[i,j]=w
			else:
				m[i,j]=b

def move_f(robot):
    if robot[1]=='L':
        robot[0][1]-=1
    elif robot[1]=='R':
        robot[0][1]+=1
    elif robot[1]=='U':
        robot[0][0]-=1
    elif robot[1]=='D':
        robot[0][0]+=1

def move_b(robot):
    if robot[1]=='L':
        robot[0][1]+=1
    elif robot[1]=='R':
        robot[0][1]-=1
    elif robot[1]=='U':
        robot[0][0]+=1
    elif robot[1]=='D':
        robot[0][0]-=1

def turn_r(robot):
    if robot[1]=='L':
        robot[1]='U'
    elif robot[1]=='R':
        robot[1]='D'
    elif robot[1]=='U':
        robot[1]='R'
    elif robot[1]=='D':
        robot[1]='L'

def turn_l(robot):
    if robot[1]=='L':
        robot[1]='D'
    elif robot[1]=='R':
        robot[1]='U'
    elif robot[1]=='U':
        robot[1]='L'
    elif robot[1]=='D':
        robot[1]='R'        

def dect_dist(robot, side, maze):#detect distance, side='F', 'L', 'R'
    dist=0
    if robot[1]=='U':
        if side=='F':
            while maze[robot[0][0]-4-dist,robot[0][1]]:
                dist+=1
                if dist==10:
                    break
        elif side=='L':
            while maze[robot[0][0],robot[0][1]-4-dist]:
                dist+=1
                if dist==10:
                    break
        elif side=='R':
            while maze[robot[0][0],robot[0][1]+4+dist]:
                dist+=1
                if dist==10:
                    break
    elif robot[1]=='D':
        if side=='F':
            while maze[robot[0][0]+4+dist,robot[0][1]]:
                dist+=1
                if dist==10:
                    break
        elif side=='L':
            while maze[robot[0][0],robot[0][1]+4+dist]:
                dist+=1
                if dist==10:
                    break
        elif side=='R':
            while maze[robot[0][0],robot[0][1]-4-dist]:
                dist+=1
                if dist==10:
                    break
    elif robot[1]=='L':
        if side=='F':
            while maze[robot[0][0],robot[0][1]-4-dist]:
                dist+=1
                if dist==10:
                    break
        elif side=='L':
            while maze[robot[0][0]+4+dist,robot[0][1]]:
                dist+=1
                if dist==10:
                    break
        elif side=='R':
            while maze[robot[0][0]-4-dist,robot[0][1]]:
                dist+=1
                if dist==10:
                    break
    elif robot[1]=='R':
        if side=='F':
            while maze[robot[0][0],robot[0][1]+4+dist]:
                dist+=1
                if dist==10:
                    break
        elif side=='L':
            while maze[robot[0][0]-4-dist,robot[0][1]]:
                dist+=1
                if dist==10:
                    break
        elif side=='R':
            while maze[robot[0][0]+4+dist,robot[0][1]]:
                dist+=1
                if dist==10:
                    break
    return dist

def frame(robot):
	binary_out=maze.copy()

	if not dlvd_gift:
		binary_out[(tree_coor[0]-2):(tree_coor[0]+3),(tree_coor[1]-2):(tree_coor[1]+3)]=xmas_tree
	else:
		binary_out[(tree_coor[0]-2):(tree_coor[0]+3),(tree_coor[1]-2):(tree_coor[1]+3)]=xmas_gift
	if not got_gift:
		binary_out[(gift_coor[0]-2):(gift_coor[0]+3),(gift_coor[1]-2):(gift_coor[1]+3)]=xmas_gift
	if robot[1]=='U':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_u
	elif robot[1]=='D':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_d
	elif robot[1]=='R':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_r
	elif robot[1]=='L':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_l
	return cv2.resize(binary_out, (0,0), fx=3, fy=3)
	
maze=np.array(#48*48
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
     [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],dtype=np.uint8)

robot_u=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,0,0,0,1,1],
	[1,0,0,0,0,0,1],
	[0,0,0,0,0,0,0],
	[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1]],dtype=np.uint8)

robot_d=np.array(
	[[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1],
	[0,0,0,0,0,0,0],
	[1,0,0,0,0,0,1],
	[1,1,0,0,0,1,1],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

robot_l=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,0,0,1,1,1],
	[1,0,0,0,0,0,0],
	[0,0,0,0,0,0,0],
	[1,0,0,0,0,0,0],
	[1,1,0,0,1,1,1],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

robot_r=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,1,0,0,1,1],
	[0,0,0,0,0,0,1],
	[0,0,0,0,0,0,0],
	[0,0,0,0,0,0,1],
	[1,1,1,0,0,1,1],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

xmas_tree=np.array(
        [[0,0,0,0,0],
        [0,1,1,1,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0]],dtype=np.uint8)

xmas_gift=np.array(
        [[0,0,0,0,0],
        [0,0,1,0,0],
        [0,1,1,1,0],
        [0,0,1,0,0],
        [0,0,0,0,0]],dtype=np.uint8)

tree_coor=(4,30)#(42,5)
gift_coor=(42,5)#(4,30)

color(maze, 200, 0)
color(robot_u, 200, 20)
color(robot_d, 200, 20)
color(robot_l, 200, 20)
color(robot_r, 200, 20)
xmax_tree_color=100
xmax_gift_color=150
color(xmas_gift, 255,xmax_gift_color)
color(xmas_tree, 255,xmax_tree_color)
got_gift=False
found_tree=False
dlvd_gift=False

cv2.namedWindow('maze')
'''
m=cv2.resize(maze, (0,0), fx=3, fy=3)
cv2.imshow('maze',m)
cv2.waitKey(0)
'''
robot=[[42,42],'L']#start point as [42,42], direction is Left

map_dic={1:[[0,0,0],[0,0,0],0,'N']}
tree_lst=[1,0,1,'f']#current 1, previous 0, node index 1, forward

path_lst=[False,False,False]
turn_left=False
space_for_turn_left=0
space_for_turn_right=0
'''detct the paths of current position'''
if dect_dist(robot, 'L', maze)>5:
    path_lst[0]=True
    turn_left=True
    space_for_turn=4
else:
    path_lst[0]=False
if dect_dist(robot, 'F', maze)>5:
    path_lst[1]=True
else:
    path_lst[1]=False
if dect_dist(robot, 'R', maze)>5:
    path_lst[2]=True
else:
    path_lst[2]=False

mapping.node_proc(map_dic, tree_lst, path_lst)
print map_dic

while True:
#    time.sleep(0.3)
    if turn_left:#ready to turn, turn, finish turning
        move_f(robot)
	img=frame(robot)
	cv2.imshow('maze',img)
	cv2.waitKey(0)
        print 'forward ',robot[0]
        if dect_dist(robot, 'F', maze)>5:
            path_lst[1]=True
        else:
            path_lst[1]=False
        if dect_dist(robot, 'R', maze)>5:
            path_lst[2]=True
	    #space_for_turn_right+=1
        else:
            path_lst[2]=False
	    #space_for_turn_right=0
        if dect_dist(robot, 'L', maze)>5:
            path_lst[0]=True
            space_for_turn_left+=1
            if space_for_turn_left==5:#enough space to turn,
                turn_l(robot)#turn left
		if path_lst[1] or path_lst[2]:#if middle path or right path exists, it is an intersection
		    print tree_lst
		    mapping.node_proc(map_dic, tree_lst, path_lst)#add this node into the map_dic or check this node
		    print map_dic
                    if tree_lst[3]=='e':#end
                        break#reach the root node
		img=frame(robot)
	        cv2.imshow('maze',img)
        	cv2.waitKey(0)
                space_for_turn_left=-5#reset the space as -5 to prevent unnecessary left turn afterwards
                print 'turn left'
        else:#not enough space to turn
            path_lst[0]=False
            turn_left=False
            space_for_turn_left=0#reset the space
    else:#move straight
        move_f(robot)
	img=frame(robot)
        cv2.imshow('maze',img)
        cv2.waitKey(0)
        print 'forward',robot[0]

        if dect_dist(robot, 'F', maze)>5:
            path_lst[1]=True
        else:
            path_lst[1]=False
        if dect_dist(robot, 'R', maze)>5:
            path_lst[2]=True
	    space_for_turn_right+=1
	    #print 'right space ',space_for_turn_right
	    if space_for_turn_right==9:#robot moves straight, however it is an intersection
		#print space_for_turn_right
		print tree_lst
		mapping.node_proc(map_dic, tree_lst, path_lst)#add this node into the map_dic
		print map_dic
		space_for_turn_right=0#reset the value
		if tree_lst[3]=='e':#end
			break#reach the root node
        else:
            path_lst[2]=False
	    space_for_turn_right=0
        if dect_dist(robot, 'L', maze)>5:
            path_lst[0]=True
            turn_left=True#get read to turn left
            space_for_turn_left=1
	    space_for_turn_right=0#if left path exists, use another way to check the right path
        else:
            path_lst[0]=False

        if not path_lst[1] and dect_dist(robot, 'F', maze)==1:#end ahead
            if path_lst[0]:#if left path exists, the robot already turned
                pass#this case will not happen
            else:#no left path
                if path_lst[2]:#right path,
                    turn_r(robot)#turn right
		    space_for_turn_right=0
		    img=frame(robot)
		    cv2.imshow('maze',img)
	            cv2.waitKey(0)
                    print 'turn right'
                else:#dead end
                    turn_r(robot)#turn right
		    img=frame(robot)
                    cv2.imshow('maze',img)
                    cv2.waitKey(0)
                    turn_r(robot)#turn right
		    img=frame(robot)
                    cv2.imshow('maze',img)
                    cv2.waitKey(0)
                    print 'deadend, turn around'
		    print tree_lst
		    mapping.node_proc(map_dic, tree_lst, path_lst)#add this node into the map_dic or check this node
		    print map_dic
                    if tree_lst[3]=='e':#end
                        break#reach the root node
		
cv2.destroyAllWindows()

