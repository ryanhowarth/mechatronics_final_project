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

def dect_obj(robot, maze):
	if robot[1]=='U':
		for i in xrange(robot[0][1]-5,robot[0][1]+6):
			if maze[robot[0][0]-4][i]==xmax_tree_color:
				return 'T'
			elif maze[robot[0][0]-4][i]==xmax_gift_color:
				return 'G'
			else:
				pass
	elif robot[1]=='D':
		for i in xrange(robot[0][1]-5,robot[0][1]+6):
                        if maze[robot[0][0]+4][i]==xmax_tree_color:
                                return 'T'                      
                        elif maze[robot[0][0]+4][i]==xmax_gift_color:
                                return 'G'
                        else:
                                pass
	elif robot[1]=='L':
		for i in xrange(robot[0][0]-5,robot[0][0]+6):
                        if maze[i][robot[0][1]-4]==xmax_tree_color:
                                return 'T'                      
                        elif maze[i][robot[0][1]-4]==xmax_gift_color:
                                return 'G'
                        else:
                                pass
	elif robot[1]=='R':
		for i in xrange(robot[0][0]-5,robot[0][0]+6):
                        if maze[i][robot[0][1]+4]==xmax_tree_color:
                                return 'T'
                        elif maze[i][robot[0][1]+4]==xmax_gift_color:
                                return 'G'
                        else:
                                pass
	else:
		pass
	return 'N'#no object ahead

def frame(robot):
	binary_out=cur_maze.copy()

#	if not dlvd_gift:
#		binary_out[(tree_coor[0]-2):(tree_coor[0]+3),(tree_coor[1]-2):(tree_coor[1]+3)]=xmas_tree
#	else:
#		binary_out[(tree_coor[0]-2):(tree_coor[0]+3),(tree_coor[1]-2):(tree_coor[1]+3)]=xmas_gift
#	if not got_gift:
#		binary_out[(gift_coor[0]-2):(gift_coor[0]+3),(gift_coor[1]-2):(gift_coor[1]+3)]=xmas_gift
	if robot[1]=='U':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_u
	elif robot[1]=='D':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_d
	elif robot[1]=='R':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_r
	elif robot[1]=='L':
		binary_out[(robot[0][0]-3):(robot[0][0]+4),(robot[0][1]-3):(robot[0][1]+4)]=robot_l
	return cv2.resize(binary_out, (0,0), fx=3, fy=3)

def get_maze():
	binary_out=maze.copy()
	if not dlvd_gift:
                binary_out[(tree_coor[0]-2):(tree_coor[0]+3),(tree_coor[1]-2):(tree_coor[1]+3)]=xmas_tree
        else:
                binary_out[(tree_coor[0]-2):(tree_coor[0]+3),(tree_coor[1]-2):(tree_coor[1]+3)]=xmas_gift
        if not got_gift:
                binary_out[(gift_coor[0]-2):(gift_coor[0]+3),(gift_coor[1]-2):(gift_coor[1]+3)]=xmas_gift
	return binary_out

def load_robot():
	print 'load'	
	robot_u[:,:]=robot_ug
	robot_d[:,:]=robot_dg
	robot_l[:,:]=robot_lg
	robot_r[:,:]=robot_rg
def unload_robot():
	print 'unload'
        robot_u[:,:]=robot_ue
        robot_d[:,:]=robot_de
        robot_l[:,:]=robot_le
        robot_r[:,:]=robot_re

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

robot_ue=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,0,0,0,1,1],
	[1,0,0,0,0,0,1],
	[0,0,0,0,0,0,0],
	[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1]],dtype=np.uint8)

robot_de=np.array(
	[[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1],
	[1,1,0,0,0,1,1],
	[0,0,0,0,0,0,0],
	[1,0,0,0,0,0,1],
	[1,1,0,0,0,1,1],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

robot_le=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,0,0,1,1,1],
	[1,0,0,0,0,0,0],
	[0,0,0,0,0,0,0],
	[1,0,0,0,0,0,0],
	[1,1,0,0,1,1,1],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

robot_re=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,1,0,0,1,1],
	[0,0,0,0,0,0,1],
	[0,0,0,0,0,0,0],
	[0,0,0,0,0,0,1],
	[1,1,1,0,0,1,1],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

robot_ug=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,0,0,0,1,1],
	[1,0,0,0,0,0,1],
	[0,0,0,1,0,0,0],
	[1,0,1,1,1,0,1],
	[1,0,0,1,0,0,1],
	[1,0,0,0,0,0,1]],dtype=np.uint8)

robot_dg=np.array(
	[[1,0,0,0,0,0,1],
	[1,0,0,1,0,0,1],
	[1,0,1,1,1,0,1],
	[0,0,0,1,0,0,0],
	[1,0,0,0,0,0,1],
	[1,1,0,0,0,1,1],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

robot_lg=np.array(
	[[1,1,1,0,1,1,1],
	[1,1,0,0,0,0,0],
	[1,0,0,0,1,0,0],
	[0,0,0,1,1,1,0],
	[1,0,0,0,1,0,0],
	[1,1,0,0,0,0,0],
	[1,1,1,0,1,1,1]],dtype=np.uint8)

robot_rg=np.array(
	[[1,1,1,0,1,1,1],
	[0,0,0,0,0,1,1],
	[0,0,1,0,0,0,1],
	[0,1,1,1,0,0,0],
	[0,0,1,0,0,0,1],
	[0,0,0,0,0,1,1],
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

#tree_coor=(42,3)
#gift_coor=(5,26)

#tree_coor=(42,6)
#gift_coor=(5,31)

tree_coor=(5,31)
gift_coor=(42,6)

#tree_coor=(5,26)
#gift_coor=(42,3)
color(maze, 200, 0)
color(robot_ue, 200, 20)
color(robot_de, 200, 20)
color(robot_le, 200, 20)
color(robot_re, 200, 20)
color(robot_ug, 200, 20)
color(robot_dg, 200, 20)
color(robot_lg, 200, 20)
color(robot_rg, 200, 20)

robot_u=robot_ue.copy()
robot_d=robot_de.copy()
robot_l=robot_le.copy()
robot_r=robot_re.copy()

xmax_tree_color=100
xmax_gift_color=150
color(xmas_gift, 255,xmax_gift_color)
color(xmas_tree, 255,xmax_tree_color)
got_gift=False
found_tree=False
dlvd_gift=False
cur_maze=get_maze()#current maze, including walls, tree and present
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
turn_lst=[]
turn_left=False
move_state='S'
turn_dir='N'
space_for_turn_left=0
space_for_turn_right=0
space_from_center=6
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
mapping.print_node(map_dic)

while True:
#    time.sleep(0.3)
    if move_state=='L' or move_state=='R' or move_state=='F':#makeing left/right turn
        move_f(robot)
	space_from_center+=1
	img=frame(robot)
	cv2.imshow('maze',img)
	cv2.waitKey(0)
        print 'forward ',robot[0]
	
	if dect_dist(robot, turn_dir, maze)>5:
		obj=dect_obj(robot,cur_maze)#detect present or tree
		if obj=='T' or obj=='G':
                	print 'deadend'
			print move_state
			if not got_gift:#haven't got the gift, map the maze
				print tree_lst
				if obj!='G':
					mapping.node_proc(map_dic, tree_lst, [False,False,False])#add this node into the map_dic or check this node
				if obj=='T':#found the tree
					found_tree=True
					mapping.found_tree(map_dic, tree_lst)#label the tree node in the map
				mapping.print_node(map_dic)
				if obj=='G':#found the gift
					got_gift=True
					load_robot()
					cur_maze=get_maze()#update the background
					if found_tree:
						turn_lst=mapping.search_path(map_dic,tree_lst)
					print turn_lst
				print tree_lst
			else:#already got the gift, the robot is at the tree
				dlvd_gift=True
				unload_robot()
				cur_maze=get_maze()
				break			

			turn_r(robot)#turn right
                	img=frame(robot)
                	cv2.imshow('maze',img)
                	cv2.waitKey(0)
                	turn_r(robot)#turn right
                	img=frame(robot)
                	cv2.imshow('maze',img)
                	cv2.waitKey(0)

			move_state='C'#move to the center of a intersection or corner
		else:
			pass
	else:#finish turning
		obj=dect_obj(robot,cur_maze)#detect present or tree
                if obj=='T' or obj=='G':    
                        print 'deadend'
			print move_state
			if not got_gift:#haven't got the gift, map the maze
				print tree_lst
				if obj!='G':
					mapping.node_proc(map_dic, tree_lst, [False,False,False])#add this node into the map_dic or check this node
				if obj=='T':#found the tree
					found_tree=True
					mapping.found_tree(map_dic, tree_lst)#label the tree node in the map
				mapping.print_node(map_dic)
				if obj=='G':#found the gift
					got_gift=True
					load_robot()
					cur_maze=get_maze()#update the background
					if found_tree:
						turn_lst=mapping.search_path(map_dic,tree_lst)
					print turn_lst
				print tree_lst
			else:#already got the gift, the robot is at the tree
				dlvd_gift=True
				unload_robot()
				cur_maze=get_maze()
				break			

			turn_r(robot)#turn right
                        img=frame(robot)
                        cv2.imshow('maze',img)
                        cv2.waitKey(0)
                        turn_r(robot)#turn right
                        img=frame(robot)
                        cv2.imshow('maze',img)
                        cv2.waitKey(0)

                        move_state='C'#move to the center of a intersection or corner
                else:
			space_from_center=6
                   	move_state='S'#move straight    	
	
    elif move_state=='C':
        move_f(robot)
        space_from_center-=1
        img=frame(robot)
        cv2.imshow('maze',img)
        cv2.waitKey(0)
        print 'forward ',robot[0]
	if space_from_center:#not center yet
		pass
	else:
                if dect_dist(robot, 'L', maze)>5:
                    path_lst[0]=True
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
		if path_lst[0]:#left path
			if path_lst[1] or path_lst[2]:#intersection
				if not got_gift:#has not got the gift, map the maze
					print tree_lst
					mapping.node_proc(map_dic, tree_lst, path_lst)#add this node into the map_dic
					mapping.print_node(map_dic)
					print tree_lst
				if turn_lst:#has the gift and has found the tree, so the turn_lst is not empty
					turn=turn_lst.pop(0)
					if turn=='M':
						move_state='F'
						turn_dir='L'
					elif turn=='L':
						move_state='L'
		                                turn_dir='L'
                		                turn_l(robot)#turn left
                                		img=frame(robot)
		                                cv2.imshow('maze',img)
                		                cv2.waitKey(0)
					elif turn=='R':
						move_state='R'
                                                turn_dir='R'
                                                turn_r(robot)#turn right
                                                img=frame(robot)
                                                cv2.imshow('maze',img)
                                                cv2.waitKey(0)
				else:#has the gift, hasn't found the tree or has not the gift
					move_state='L'
					turn_dir='L'
					turn_l(robot)#turn left
					img=frame(robot)
					cv2.imshow('maze',img)
					cv2.waitKey(0)	
			else:#only left path
				move_state='L'
				turn_dir='L'
				turn_l(robot)#turn left
				img=frame(robot)
				cv2.imshow('maze',img)
				cv2.waitKey(0)	
		elif path_lst[1]:#middle path and right path
			if not got_gift:#do mapping
				print tree_lst
				mapping.node_proc(map_dic, tree_lst, path_lst)#add this node into the map_dic
				mapping.print_node(map_dic)
				print tree_lst
			if turn_lst:
				turn=turn_lst.pop(0)
				if turn=='M':
					move_state='F'
                                        turn_dir='R'
				elif turn=='R':
					move_state='R'
                                        turn_dir='R'
                                        turn_r(robot)#turn right
                                        img=frame(robot)
                                        cv2.imshow('maze',img)
                                        cv2.waitKey(0)
				else:
					print 'turn error'
			else:
				move_state='F'
				turn_dir='R'
		elif path_lst[2]:#only right path
			move_state='R'
			turn_dir='R'
                        turn_r(robot)#turn left
                        img=frame(robot)
                        cv2.imshow('maze',img)
                        cv2.waitKey(0)
    elif move_state=='S':
        move_f(robot)
        img=frame(robot)
        cv2.imshow('maze',img)
        cv2.waitKey(0)
        print 'forward',robot[0]
	obj=dect_obj(robot,cur_maze)#detect present or tree
	if dect_dist(robot, 'F', maze)>1:#opening head and no obj ahead
            path_lst[1]=True
        else:
            path_lst[1]=False
	if dect_dist(robot, 'L', maze)>5:#opening head and no obj ahead
            path_lst[0]=True
        else:
            path_lst[0]=False
	if dect_dist(robot, 'R', maze)>5:#opening head and no obj ahead
            path_lst[2]=True
        else:
            path_lst[2]=False
	if obj=='T' or obj=='G' or not path_lst[1]:#dead end
		path_lst[1]=False

	        print 'deadend'
		print move_state
		if not got_gift:#haven't got the gift, map the maze
	        	print tree_lst
			if obj!='G':#if got gift, no need to map
		        	mapping.node_proc(map_dic, tree_lst, path_lst)#add this node into the map_dic or check this node
			if obj=='T':#found the tree
				found_tree=True
		               	mapping.found_tree(map_dic, tree_lst)#label the tree node in the map
		       	mapping.print_node(map_dic)
			if obj=='G':#found the gift
				got_gift=True
				load_robot()
				cur_maze=get_maze()#update the background
				if found_tree:#search path if the tree has been found
					turn_lst=mapping.search_path(map_dic,tree_lst)
				print turn_lst
			print tree_lst
		else:#already got the gift, the robot is at the tree or deadend
			if obj=='T':#if at the tree, put the gift on the tree
				dlvd_gift=True
				unload_robot()
				cur_maze=get_maze()
				break			

		turn_r(robot)#turn right
                img=frame(robot)
	    	cv2.imshow('maze',img)
		cv2.waitKey(0)
		turn_r(robot)#turn right
		img=frame(robot)
	        cv2.imshow('maze',img)
	        cv2.waitKey(0)

	        if tree_lst[3]=='e':#end
			break#reach the root node
	if path_lst[0] or path_lst[2]:#at an intersection or corner
		space_from_center-=1
		move_state='C'
	
for i in xrange(5):
	img=frame(robot)
        cv2.imshow('maze',img)
        cv2.waitKey(0)
	
cv2.destroyAllWindows()

