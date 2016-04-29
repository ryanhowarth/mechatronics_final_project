#!/usr/bin/python
import Robot

flag=True
while flag:
  item=detectItem()
  print item
  if item=='gift':
      pickedup=False
      while not pickedup:
        pickedup=approachGift()
      dropped=False
      while not dropped:
        if pixyDetectItem()=='tree':
          dropped=approachTree()
          flag=False
  sleep(0.5)
