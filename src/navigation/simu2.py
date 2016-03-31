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

color(maze, 200, 0)
color(robot_u, 200, 20)
color(robot_d, 200, 20)
color(robot_l, 200, 20)
color(robot_r, 200, 20)


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
space_for_turn=0
'''detct the paths of current position'''
if dect_dist(robot, 'L', maze)>3:
    path_lst[0]=True
    turn_left=True
    space_for_turn=4
else:
    path_lst[0]=False
if dect_dist(robot, 'F', maze)>3:
    path_lst[1]=True
else:
    path_lst[1]=False
if dect_dist(robot, 'R', maze)>3:
    path_lst[2]=True
else:
    path_lst[2]=False

mapping.node_proc(map_dic, tree_lst, path_lst)

while True:
#    time.sleep(0.3)
    if turn_left:#ready to turn, turn, finish turning
        move_f(robot)
	img=frame(robot)
	cv2.imshow('maze',img)
	cv2.waitKey(0)
        print 'forward ',robot[0]
        if dect_dist(robot, 'F', maze)>3:
            path_lst[1]=True
        else:
            path_lst[1]=False
        if dect_dist(robot, 'R', maze)>3:
            path_lst[2]=True
        else:
            path_lst[2]=False
        if dect_dist(robot, 'L', maze)>3:
            path_lst[0]=True
            space_for_turn+=1
            if space_for_turn==5:#enough space to turn,
                turn_l(robot)#turn left
		img=frame(robot)
	        cv2.imshow('maze',img)
        	cv2.waitKey(0)
                space_for_turn=-5#reset the space as -5 to prevent unnecessary left turn afterwards
                print 'turn left'
        else:#not enough space to turn
            path_lst[0]=False
            turn_left=False
            space_for_turn=0#reset the space
    else:#move straight
        move_f(robot)
	img=frame(robot)
        cv2.imshow('maze',img)
        cv2.waitKey(0)
        print 'forward',robot[0]
        if dect_dist(robot, 'L', maze)>3:
            path_lst[0]=True
            turn_left=True
            space_for_turn=1
        else:
            path_lst[0]=False
        if dect_dist(robot, 'F', maze)>3:
            path_lst[1]=True
        else:
            path_lst[1]=False
        if dect_dist(robot, 'R', maze)>3:
            path_lst[2]=True
        else:
            path_lst[2]=False
        if not path_lst[1] and dect_dist(robot, 'F', maze)==1:#end ahead
            if path_lst[0]:
                pass
            else:
                if path_lst[2]:#right path,
                    turn_r(robot)#turn right
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
                    print 'turn around'

cv2.destroyAllWindows()

