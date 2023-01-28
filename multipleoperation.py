#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import import_ipynb
from rotate_translate import node
import math

def round_up(n, decimals=2):
    multiplier = 10 ** decimals
    n = math.ceil(n * multiplier) / multiplier
    return n

def re_arrange(objects, type):
    if(type == "front"):
        objects.sort(key=lambda x: x[0][1][0], reverse=True)
    else:
        objects.sort(key=lambda x: x[0][1][0])

def draw_contour(img, out):
    imgrey = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgrey, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy, contours = zip(*sorted(zip(hierarchy[0], contours), key=lambda x: cv2.contourArea(x[1]), reverse=True))
    for i, c in enumerate(contours):
        if (hierarchy[i][3] != -1 or (hierarchy[i][3] == -1 and hierarchy[i][2] == -1)):
            M = cv2.moments(c)
            if(M["m00"] != 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                area = cv2.contourArea(c)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                cv2.drawContours(img, [c], 0, (0, 0, 255), 1)
    cv2.imwrite(out, img)

def add_part(objects, part, pos, type, ratio):
    if(type == "front"):
        part[0].translate(round_up((part[1][0]-pos[0]) * ratio),0, round_up((pos[1]-part[1][1]) * ratio))
    if(type == "side"):
        part[0].translate(0, round_up((part[1][0]-pos[0]) * ratio),round_up((pos[1]-part[1][1]) * ratio))
    if(type == "top"):
        part[0].translate(round_up((part[1][1]-pos[1]) * ratio),round_up((part[1][0]-pos[0]) * ratio), 0)
    for i, object in enumerate(objects):
        if(cv2.pointPolygonTest(object[0][2], part[1], False) >= 0):
            part[0].operation = "difference"
            object.append(part)
            return
    objects.append([part])
    return

def combining(front_parts, side_parts, top_parts, roundOffApprox):
    for i, front in enumerate(front_parts):
        first = 0
        for j, part_f in enumerate(front):
            if(len(part_f) >= 6):
                continue
            if(first == 1):
                if(part_f[0].shape == "cube"):
                    if(front[0][0].shape == "cube"):
                        part_f[0].b = front[0][0].b
                    else:
                        part_f[0].b = front[0][0].h
                    if(front[0][0].rz != 0):
                        part_f[0].b = front[0][3]
                if(part_f[0].shape == "cylinder"):
                    if(front[0][0].shape == "cube"):
                        part_f[0].h = front[0][0].b
                    else:
                        part_f[0].h = front[0][0].h
                    if(front[0][0].rz != 0):
                        part_f[0].h = front[0][3]
            found = 0
            for k, side in enumerate(side_parts):
                add_rest = 0
                for l, part_s in enumerate(side):
                    if(add_rest == 1 and part_s[3] != -1):
                        part_s.append("used")
                        part_s[3] = -1
                        part_s[0].tx = part_f[0].tx
                        if(part_s[0].shape == "cylinder"):
                            part_s[0].h = part_f[4]
                        elif(part_s[0].shape == "cube"):
                            part_s[0].b = part_f[4]
                        front.append(part_s)
                        continue
                    if(abs(part_f[3]-part_s[3]) < roundOffApprox and found == 0):
                        found = 1
                        if(j == 0):
                            first = 1
                        if(l != 0):
                            part_s[0].operation = "union"
                        if(part_f[0].shape == "cube"):
                            if(part_s[0].shape == "cube"):
                                for top in top_parts:
                                    for m, part_t in enumerate(top):
                                        if(abs(part_t[3] - part_f[4]) < roundOffApprox and len(part_t) == 5):
                                            if(m != 0):
                                                part_t[0].operation = "union"
                                            if(j == 0):
                                                part_t[0].operation = "None"
                                            if(part_t[0].shape == "cylinder"):
                                                part_t[0].h = part_f[0].h
                                                part_t[0].tz = part_f[0].tz
                                                part_t[1] = i
                                                part_t[2] = -1
                                                part_t.append("used")
                                                part_f[0] = part_t[0]
                                                part_s[3] = -1
                                                add_rest = 1
                                                break
                                            if(part_t[0].shape == "cube" and part_s[0].ry == 0 and part_f[0].ry == 0 and part_t[0].rz != 0 and abs(part_t[0].rz) != 90):
                                                part_t[0].b = part_f[0].h
                                                part_t[0].tz = part_f[0].tz
                                                part_t[1] = i
                                                part_t[2] = -1
                                                part_t.append("used")
                                                part_f[0] = part_t[0]
                                                part_f[3] = part_t[3]
                                                part_s[3] = -1
                                                add_rest = 1
                                                break
                                    else:
                                        continue
                                    break
                            if(part_s[3] == -1):
                                continue
                            if(part_s[0].shape == "cylinder"):
                                part_s[0].h = part_f[0].l
                                part_s[0].tx = part_f[0].tx
                                part_s[0].ry = part_f[0].ry
                                if(j == 0):
                                    part_s[0].operation = "None"
                                part_f[0] = part_s[0]
                                part_s[3] = -1
                                add_rest = 1
                                continue
                            if(part_s[0].shape == "cube"):
                                if(part_f[0].ry != 0 or part_s[0].ry == 0):
                                    part_f[0].b = part_s[0].l
                                    part_f[0].ty = part_s[0].ty
                                    part_s[3] = -1
                                    add_rest = 1
                                    continue
                                else:
                                    part_s[0].b = part_f[0].l
                                    part_s[0].tx = part_f[0].tx
                                    part_f[0] = part_s[0]
                                    part_s[3] = -1
                                    add_rest = 1
                                    continue
                        if(part_f[0].shape == "cylinder"):
                            if(part_s[0].shape == "cube"):
                                part_f[0].h = part_s[0].l
                                part_f[0].ty = part_s[0].ty
                                part_f[0].rx = part_s[0].ry
                        part_s[3] = -1
                        add_rest = 1
                        continue
                if(found == 1):
                    break
            if(found == 0):
                for top in top_parts:
                    for m, part_t in enumerate(top):
                        if((abs(part_t[3]-part_f[4]) < roundOffApprox) and len(part_t) == 5):
                            if(abs(part_f[0].tx - part_t[0].tx) > 0.5):
                                continue
                            if(j == 0):
                                first = 1
                            if(m != 0):
                                part_t[0].operation = "union"
                            if(part_f[0].shape == "cylinder"):
                                if(part_t[0].shape == "cube"):
                                    part_f[0].h = part_t[0].h
                                    part_f[0].ty = part_t[0].ty
                                    part_f[0].rz = part_t[0].rz
                                    part_t[0].b = part_f[3]
                                    part_t[0].tz = part_f[0].tz
                                    part_t[1] = i
                                    part_t[2] = -1
                                    part_t.append("used")
                                    break
                            if(part_f[0].shape == "cube"):
                                part_t[0].tz = part_f[0].tz
                                if(part_t[0].shape == "cube"):
                                    part_t[0].b = part_f[0].h
                                    if(part_t[0].rz != 0):
                                        part_f[0] = part_t[0]
                                    else:
                                        part_f[0].b = part_t[0].l
                                        part_f[0].ty = part_t[0].ty
                                elif(part_t[0].shape == " cylinder"):
                                    part_t[0].ry = part_f[0].ry
                                    part_t[0].h = part_f[0].h
                                    part_f[0] = part_t[0]
                                part_t[1] = j
                                part_t[2] = -1
                                part_t.append("used")
                                break
                    else:
                        continue
                    break
    for side in side_parts:
        if(side[0][3] != -1):
            addCompleteList = []
            for part_s in side:
                if(part_s[3] == -1):
                    break
                for k, top in enumerate(top_parts):
                    for l, part_t in enumerate(top):
                        if((abs(part_s[4]-part_t[4]) < roundOffApprox) and len(part_t) == 5):
                            if(part_s[0].shape == "cube"):
                                part_t[0].tz = part_s[0].tz
                                if(part_t[0].shape == "cube"):
                                    part_t[0].b = part_s[0].h
                                    if(part_t[0].rz != 0):
                                        part_s[0] = part_t[0]
                                    else:
                                        part_s[0].b = part_t[0].h
                                        part_s[0].tx = part_t[0].tx
                                elif(part_t[0].shape == " cylinder"):
                                    part_t[0].rx = part_s[0].ry
                                    part_t[0].h = part_s[0].h
                                    part_s[0] = part_t[0]
                                part_t[1] = len(front_parts)
                                part_t[2] = -1
                                part_t.append("used")
                            if(part_s[0].shape == "cylinder"):
                                if(part_t[0].shape == "cube"):
                                    part_s[0].h = part_t[0].h
                                    part_s[0].tx = part_t[0].tx
                                    part_s[0].rz = part_t[0].rz
                                    part_t[0].b = part_s[3]
                                    part_t[0].tz = part_s[0].tz
                                    part_t[1] = len(front_parts)
                                    part_t[2] = -1
                                    part_t.append("used")
                addCompleteList.append(part_s)
            front_parts.append(addCompleteList)
    for top in top_parts:
        height = -1
        tz = -1
        position = -1
        for part_t in top:
            if(height != -1 and len(part_t) == 5):
                if(part_t[0].shape == "cylinder"):
                    part_t[0].h = height
                    part_t[0].tz = tz
                elif (part_t[0].shape == "cube"):
                    part_t[0].b = height
                    part_t[0].tz = tz
                try:
                    front_parts[position].append(part_t)
                except:
                    print("Error occurred")
            try:
                class Spam(int):
                    pass
                if(isinstance(Spam(part_t[2]), int)):
                    tz = part_t[0].tz
                    position = part_t[1]
                    if(part_t[0].shape == "cylinder"):
                        height = part_t[0].h
                    elif (part_t[0].shape == "cube"):
                        height = part_t[0].b
            except TypeError:
                pass
    return front_parts

def detect(c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    cylinder_type = 0
    if len(approx) == 3:
        shape = "triangle"
        cylinder_type = 3
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        rect = cv2.minAreaRect(c)
        ar = rect[1][0] / float(rect[1][1])
        shape = "square" if ar >= 0.999 and ar <= 1.001 else "rectangle"
    elif len(approx) == 5:
        shape = "pentagon"
        cylinder_type = 5
    elif len(approx) == 6:
        shape = "hexagon"
        cylinder_type = 6
    else:
        shape = "circle"
        cylinder_type = 1
    return shape, cylinder_type

def valid_contours(img, type, ratio):
    objects = []
    imgrey = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgrey, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy, contours = zip(*sorted(zip(hierarchy[0], contours), key=lambda x: cv2.contourArea(x[1]), reverse=True))
    for i, c in enumerate(contours):
        if (hierarchy[i][3] != -1 or (hierarchy[i][3] == -1 and hierarchy[i][2] == -1)):
            M = cv2.moments(c)
            if(M["m00"] != 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                area = cv2.contourArea(c)
                area = area * ratio
                rect = cv2.minAreaRect(c)
                if(area <= 4*ratio):
                    break
                box = cv2.boxPoints(rect)
                rectLength = round_up(rect[1][0] * ratio)
                rectBreadth = round_up(rect[1][1] * ratio)
                x, y, w, h = cv2.boundingRect(c)
                w = round_up(w * ratio)
                h = round_up(h * ratio)
                if(len(objects) == 0):
                    pos = [cX, cY]
                cv2.drawContours(img, [c], 0, (0, 0, 255), 1)
                shape, cylinder_type = detect(c)
                part = []
                if(shape == "square"):
                    part.append(node(shape="cube", l=rectLength,b=rectLength, h=rectLength))
                    if(type == "front"):
                        part[0].rotate(0, rect[2], 0)
                    elif(type == "side"):
                        part[0].rotate(0, rect[2], 90)
                    elif(rect[2] == 0):
                        part[0].rotate(90, 0, 90)
                    else:
                        part[0].rotate(90, 0, rect[2])
                    part.append(tuple([cX, cY]))
                    part.append(c)
                    part.append(h)
                    part.append(w)
                    add_part(objects, part, pos, type, ratio)
                elif(shape == "rectangle"):
                    if(type == "front"):
                        if(rect[2] == -90):
                            part.append(node(shape="cube", l=rectBreadth, b=rectBreadth, h=rectLength))
                            part[0].rotate(0, 0, 0)
                        else:
                            part.append(node(shape="cube", l=rectLength, b=rectLength, h=rectBreadth))
                            part[0].rotate(0, rect[2], 0)
                    elif(type == "side"):
                        if(rect[2] == -90):
                            part.append(node(shape="cube", l=rectBreadth, b=rectBreadth, h=rectLength))
                            part[0].rotate(0, 0, 90)
                        else:
                            part.append(node(shape="cube", l=rectLength, b=rectLength, h=rectBreadth))
                            part[0].rotate(0, rect[2], 90)
                    elif(rect[2] == -90):
                        part.append(node(shape="cube", l=rectBreadth,b=rectBreadth, h=rectLength))
                        part[0].rotate(90, 0, 90)
                    elif(rect[2] == 0):
                        part.append(node(shape="cube", l=rectLength,b=rectLength, h=rectBreadth))
                        part[0].rotate(90, 0, 90)
                    else:
                        part.append(node(shape="cube", l=rectLength,b=rectLength, h=rectBreadth))
                        part[0].rotate(90, 0, rect[2])
                    part.append(tuple([cX, cY]))
                    part.append(c)
                    part.append(h)
                    part.append(w)
                    add_part(objects, part, pos, type, ratio)
                elif(cylinder_type > 0):
                    if(shape == "circle"):
                        _, radius = cv2.minEnclosingCircle(c)
                        radius = round_up(radius * ratio)
                        part.append(node(shape="cylinder", r=radius, r1=radius, h=rectLength))
                        if(type == "front"):
                            part[0].rotate(90, 0, 0)
                        elif(type == "side"):
                            part[0].rotate(0, 90, 0)
                        part.append(tuple([cX, cY]))
                        part.append(c)
                        part.append(h)
                        part.append(w)
                        add_part(objects, part, pos, type, ratio)
                    else:
                        _, radius = cv2.minEnclosingCircle(c)
                        radius = round_up(radius * ratio)
                        part.append(node(shape="cylinder", r=radius,r1=radius, h=rectLength, fn=cylinder_type))
                        if(type == "front"):
                            part[0].rotate(90, -90 - rect[2], 0)
                        elif(type == "side"):
                            part[0].rotate(0, 90, 0)
                        else:
                            part[0].rotate(0, 0, rect[2])
                        part.append(tuple([cX, cY]))
                        part.append(c)
                        part.append(h)
                        part.append(w)
                        add_part(objects, part, pos, type, ratio)
                else:
                    print("shape not detected")
    return objects

