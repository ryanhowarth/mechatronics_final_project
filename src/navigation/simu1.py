#!/usr/bin/python
import numpy as np
import time
import mapping

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
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
#print map
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

def dect_dist(robot, side, maze):#side='F', 'L', 'R'
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

#print tree_lst
#print map_dic
while True:
    time.sleep(0.3)
    if turn_left:#ready to turn, turn, finish turning
        move_f(robot)
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
                space_for_turn=-5#reset the space as -5 to prevent unnecessary left turn afterwards
                print 'turn left'
        else:#not enough space to turn
            path_lst[0]=False
            turn_left=False
            space_for_turn=0#reset the space
    else:#move straight
        move_f(robot)
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
                    print 'turn right'
                else:#dead end
                    turn_r(robot)#turn right
                    turn_r(robot)#turn right
                    print 'turn around'