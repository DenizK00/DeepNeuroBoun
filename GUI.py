# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 22:08:37 2021

@author: Deniz
"""


import deeplabcut
from tkinter import *                    
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import tkinter.font as font
import numpy as np
import cv2
import keyboard
import time
from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import seaborn as sns
from PIL import Image, ImageTk
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import math
import pickle
from moviepy.editor import VideoFileClip
from pathlib import Path
from deeplabcut.utils import auxiliaryfunctions
import fileinput
from operator import add
import cmath
import shutil
import os
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pylab as pl

root = Tk()
root.title("Tab Widget")

root.geometry("1920x1080")
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Select Video')
tabControl.add(tab2, text ='Analyze Video')
tabControl.pack(expand = 1, fill ="both")
  

def Showimage(imgCV_in,canva,layout="null"):
    """
    Showimage() is a function used to display OpenCV images in the canvas control of tkinter.
         Need to import the library before use
    import cv2 as cv
    from PIL import Image,ImageTktkinter
         And note that due to the needs of the response function, this function defines a global variable imgTK, please do not use this variable name in other places!
         Parameters:
         imgCV_in: OpenCV image variable to be displayed
         canva: tkinter canvas canvas variable for display
         layout: The format of the display. The options are:
                 "fill": The image automatically adapts to the canvas size and is completely filled, which may cause the screen to stretch
                 "fit": According to the size of the canvas, the image is displayed to the maximum extent without stretching the image, which may cause blank edges
                 Given other parameters or not, it will be displayed in the original image size, which may be incomplete or left blank
    """
    global imgTK
    global for_deletion
    
    canvawidth = int(canva.winfo_reqwidth())
    canvaheight = int(canva.winfo_reqheight())
    sp = imgCV_in.shape
    cvheight = sp[0]#height(rows) of image
    cvwidth = sp[1]#width(colums) of image
    if (layout == "fill"):
        imgCV = cv2.resize(imgCV_in,(canvawidth,canvaheight), interpolation=cv2.INTER_AREA)
    elif(layout == "fit"):
        if (float(cvwidth/cvheight) > float(canvawidth/canvaheight)):
            imgCV = cv2.resize(imgCV_in,(canvawidth,int(canvawidth*cvheight/cvwidth)), interpolation=cv2.INTER_AREA)
        else:
            imgCV = cv2.resize(imgCV_in,(int(canvaheight*cvwidth/cvheight),canvaheight), interpolation=cv2.INTER_AREA)
    else:
        imgCV = imgCV_in
    imgCV2 = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGBA)#Convert color from BGR to RGBA
    current_image = Image.fromarray(imgCV2)#Convert image into Image object
    imgTK = ImageTk.PhotoImage(image=current_image)#Convert image object to imageTK object
    for_deletion = canva.create_image(0,0,anchor = NW, image = imgTK)


def choose_video():
  global click_count
  global canva
  global polygon_coordinates
  global click2
  global point_list_line
  global text_label
  global will_be_deleted
  global FPS
  global will_be_edited
  global frame
  global delete_all
  global duration
  global choose_csv_bt
  global filename
  global frame2
  global cap
  
  choose_lb.destroy()
  load_polygons_bt.destroy()
  choose_video_bt.destroy()
  yes_bt.destroy()
  
  if not "analyzed_bool" in globals():
    temp_lb = Label(tab1, text="Choose the Video")
    temp_lb.config(font=("Courier", 30))
    temp_lb.place(x=750, y=100)
    
    filename = askopenfilename()

    temp_lb.destroy()
  
  else:
    filename = path_video_file
    analysis_clip.close()
    cap0.release()
  
  clip = VideoFileClip(filename)
  duration = float(clip.duration)
  
  cap = cv2.VideoCapture(filename)
  FPS = cap.get(cv2.CAP_PROP_FPS)
  print(FPS)
  cap.set(1, 10)
  reto, frame2 = cap.read()
  cap.set(1, 500) # frame 200
  ret, frame = cap.read()
  
  canva_height = frame.shape[0]
  canva_width = frame.shape[1]
  canva = Canvas(root, height = canva_height, width = canva_width) # declare canva in showImage 1280
  canva.place(x=200, y=200)
  
  Showimage(frame, canva, "fill") # fill
  canva.update()
  canva.update()
  click_count = 0

  polygon_coordinates = {}
  
  """pix to cm"""

  text_label = Label(tab1, text="Draw a line to calibrate")
  text_label.config(font=("Courier", 30))
  text_label.place(x=700, y=100)
  
  click2 = 0
  point_list_line = []
  will_be_deleted = []
  will_be_edited = {}
  delete_all = []
  
  root.bind("<Button-1>", draw_line)
  # root.bind('<Button-1>', free_draw)
  # choose_csv_bt = Button(tab2, text="Choose CSV", command=choose_csv)
  # choose_csv_bt["font"] = myFont
  # choose_csv_bt.place(x=960, y=540)
  
  
  if not "analyzed_bool" in globals():
    choose_csv_bt = Button(tab2, text="Choose CSV", command=choose_csv)
    choose_csv_bt["font"] = myFont
    choose_csv_bt.place(x=960, y=540)
  else:
    choose_csv_bt = Button(tab2, text="Analyze the Video", command=choose_csv)
    choose_csv_bt["font"] = myFont
    choose_csv_bt.place(x=920, y=540)


def complete():
  tabControl.select(1)
  root.unbind("<Button-1>")
  root.unbind("<B1-Motion>")
  root.unbind("<ButtonRelease-1>")
  
  if experiment == "EPM":
    polygons.append(Polygon(open_arm_points_shapely))
    polygons.append(Polygon(closed_arm_points_shapely))
    if "angle_lb" in globals():  
      angle_lb.destroy()
    #root.unbind("")
  if experiment == "OFT":
    polygons.append(Polygon(outer_box_points_shapely))
    polygons.append(Polygon(inside_box_points_shapely))
  if experiment == "RAM":
    polygons.append(Polygon(arm1_points_shapely))
    polygons.append(Polygon(arm2_points_shapely))
    polygons.append(Polygon(arm3_points_shapely))
    polygons.append(Polygon(arm4_points_shapely))
    polygons.append(Polygon(arm5_points_shapely))
    polygons.append(Polygon(arm6_points_shapely))
    polygons.append(Polygon(arm7_points_shapely))
    polygons.append(Polygon(arm8_points_shapely))

  canva.destroy()
  
  
def plot_trajectories():
  
  plot_df = pd.read_csv(csvPath)  
  
  plot_df = plot_df.iloc[2:, 1:].astype(float).reset_index(drop=True)
  #plot_df = plot_df[[k for i, k in enumerate(plot_df.columns, 1) if i % 3 != 0]]
  
  plot_df = plot_df.iloc[from_frame:to_frame]
  print("Old length", len(plot_df))
  
  plot_df.columns = ["X", "Y", "likelihood"]
  
  fig = plt.figure(figsize=(10, 9), dpi=100)
  if experiment == "MWM":
      plot_df = plot_df[plot_df["likelihood"] > 0.6]
  else:
      plot_df = plot_df[plot_df["likelihood"] > 0.85]
  print("New length", len(plot_df))
  cmap = plt.cm.get_cmap("jet", len(plot_df))
  colors = list(range(1, (len(plot_df) + 1)))
  plt.scatter(plot_df["X"], plot_df["Y"], s=5, c=colors, cmap=cmap)
  # plt.scatter(Xs, Ys, s=5, c=colors, cmap=cmap)
  plt.gca().invert_yaxis()
  # ticks = np.linspace(int(from_sec), int(to_sec), 5, endpoint=True)
  norm = matplotlib.colors.Normalize(vmin=0, vmax= (int(to_sec) - int(from_sec)))

  cbar = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap))
  # plt.clim(0, (to_sec - from_sec))
  plt.show()
  
  if experiment == "EPM":
      c0.create_polygon(open_arm_points, fill="", outline="green", width=2)
      c0.create_polygon(closed_arm_points, fill="", outline="green", width=2)
    
  elif experiment == "TYM":
      c0.create_polygon(first_arm_points, fill="", outline="green", width=2)
      c0.create_polygon(right_arm_points, fill="", outline="green", width=2)
      c0.create_polygon(left_arm_points, fill="", outline="green", width=2)
  elif experiment == "RAM":
      c0.create_polygon(arm1_points, fill="", outline="green", width=2)
      c0.create_polygon(arm2_points, fill="", outline="green", width=2)
      c0.create_polygon(arm3_points, fill="", outline="green", width=2)
      c0.create_polygon(arm4_points, fill="", outline="green", width=2)
      c0.create_polygon(arm5_points, fill="", outline="green", width=2)
      c0.create_polygon(arm6_points, fill="", outline="green", width=2)
      c0.create_polygon(arm7_points, fill="", outline="green", width=2)
      c0.create_polygon(arm8_points, fill="", outline="green", width=2)
      
  elif experiment == "MWM":
      create_circle(center_x, center_y, 9, c0, delete=True)
      create_circle(center_x, center_y, R, c0, no_fill=True)
      create_circle(center_x, center_y, center_circle_r, c0, no_fill=True)
      c0.create_line(point1_x, point1_y, point3_x, point3_y, width=4, fill="green")
      c0.create_line(point2_x, point2_y, point4_x, point4_y, width=4, fill="green")
      sector_4x = point1_x + 20
      sector_4y = (point1_y + point2_y) / 2 + 30
      sector_3x = point3_x - 100
      sector_3y = (point2_y + point3_y) / 2 + 30
      sector_2x = point3_x - 100
      sector_2y = (point3_y + point4_y) / 2 - 40
      sector_1x = point1_x + 20
      sector_1y = (point4_y + point1_y) / 2 - 40
      
      sector4_lb = Label(c0, text="IV")
      sector4_lb.config(font=("Courier", 50))
      sector4_lb.place(x=sector_4x, y=sector_4y)
      
      sector3_lb = Label(c0, text="III")
      sector3_lb.config(font=("Courier", 50))
      sector3_lb.place(x=sector_3x, y=sector_3y)
      
      sector2_lb = Label(c0, text="II")
      sector2_lb.config(font=("Courier", 50))
      sector2_lb.place(x=sector_2x, y=sector_2y)
      
      sector1_lb = Label(c0, text="I")
      sector1_lb.config(font=("Courier", 50))
      sector1_lb.place(x=sector_1x, y=sector_1y)
      
  elif experiment == "OFT":
    c0.create_polygon(inner_box_points, fill="", outline="green", width=3)
    c0.create_polygon(outer_box_points, fill="", outline="green", width=3)

  # myxs = [x for x in df.iloc[:, 0] if x % 10 == 0]
  # myys = [y for y in df.iloc[:, 1] if y % 10 == 0]
  # plt.plot(myxs, myys)
  # plt.show()
  # draw_points()
          
          
          
  c0.update()
  c0.postscript(file="latest_plot.ps", colormode="color")

def choose_csv():
  global df
  global cols_to_delete
  global q1_list
  global speeds
  global save_polygons_bt
  global plot_trajectories_bt
  global color
  global real_speed_avg
  global Xs
  global Ys
  global csvPath
  
  if "choose_csv_bt" in globals():
    choose_csv_bt.destroy()
  
  if not "analyzed_bool" in globals():
    csvPath = askopenfilename()
    df = pd.read_csv(csvPath)
  else:
    csvPath = csv_file
    df = pd.read_csv(csvPath)
  
  df = df.iloc[2:, 1:].astype(float).reset_index(drop=True)
  df = df[[k for i, k in enumerate(df.columns, 1) if i % 3 != 0]]
  
  df = df.iloc[from_frame:to_frame]
  
  Xs = df.iloc[:, 0]
  Ys = df.iloc[:, 1]
  
  #df.columns = ["X", "Y", "likelihood"]
  
  save_polygons_bt = Button(tab2, text="Save Maze", command=save_polygons, height=2, width=13)
  save_polygons_bt["font"] = myFont
  save_polygons_bt.place(x=1600, y = 800)
  
  plot_trajectories_bt = Button(tab2, text="Plot Trajectories", command=plot_trajectories, height=2, width=13)
  plot_trajectories_bt["font"] = myFont
  plot_trajectories_bt.place(x=1600, y = 850)
  
  """Total Distance"""
 
  if experiment == "Free Draw":
    for i in range(len(polygons)):
      globals()["polygon_" + str(i) + "_speeds"] = []
      
  total_distance = 0
  speeds = []
  
  x0 = Xs.iloc[0]
  y0 = Ys.iloc[0]
  
  if experiment == "EPM":
    global openCloseCross
    global closeOpenCross
    global openOpenCross
    global closeCloseCross
    global oc_cross_times
    global co_cross_times
    global oo_cross_times
    global cc_cross_times
    global cross_dict
    
    openCloseCross = 0
    closeOpenCross = 0
    openOpenCross = 0
    closeCloseCross = 0
    
    oc_cross_times = []
    co_cross_times = []
    oo_cross_times = []
    cc_cross_times = []
    
  if experiment == "RAM":
    global cross_dict
    
    cross_dict = {}
    
    def in_center(x, y):
      blean = (polygons[0].contains(Point(x, y))) or (polygons[1].contains(Point(x, y))) or (polygons[2].contains(Point(x, y))) or (polygons[3].contains(Point(x, y))) \
        or (polygons[4].contains(Point(x, y))) or (polygons[5].contains(Point(x, y))) or (polygons[6].contains(Point(x, y))) or (polygons[7].contains(Point(x, y)))
      if blean == True:
        return False
      elif blean == False:
        return True
    
  real_speeds = []
  for i in range(1, len(df)):
    x1 = Xs.iloc[i]
    y1 = Ys.iloc[i]
    
    x_diff = abs(x1 - x0)
    y_diff = abs(y1 - y0)
    
    distance = math.sqrt((x_diff ** 2 + y_diff ** 2))
    if distance < 30:
      total_distance += distance
    
    speed = (distance * ratio) / (1 / FPS) * 60
    speeds.append(speed)
    
    """only when moving"""
    if (x_diff + y_diff > 0.35) and (x_diff + y_diff < 30):
      real_speeds.append(speed)
    
    if experiment == "EPM":      
      # 0 is the open arm
      if ((polygons[0].contains(Point(x0, y0))) and (polygons[0].contains(Point(x1, y1)))) and ((polygons[1].contains(Point(x0, y0))) and polygons[1].contains(Point(x1, y1))):
        center_speeds.append(speed)
        # print("At the center at time", i / FPS)

      elif (polygons[0].contains(Point(x0, y0))) and (polygons[0].contains(Point(x1, y1))):
        if (x_diff + y_diff > 0.35) and (x_diff + y_diff < 30):
          open_arm_speeds.append(speed)
          
      elif ((polygons[1].contains(Point(x0, y0))) and polygons[1].contains(Point(x1, y1))):
        if (x_diff + y_diff > 0.35) and (x_diff + y_diff < 30):
          closed_arm_speeds.append(speed)
        
      """Crossings"""
      if (polygons[0].contains(Point(x0, y0)) and not polygons[1].contains(Point(x0, y0))) and (polygons[0].contains(Point(x1, y1)) and polygons[1].contains(Point(x1, y1))):
        _from = "open"
      elif (polygons[1].contains(Point(x0, y0)) and not polygons[0].contains(Point(x0, y0))) and (polygons[0].contains(Point(x1, y1)) and polygons[1].contains(Point(x1, y1))):
        _from = "close"
        
      if (polygons[0].contains(Point(x0, y0)) and polygons[1].contains(Point(x0, y0))) and (polygons[1].contains(Point(x1, y1)) and not polygons[0].contains(Point(x1, y1))):
        if "_from" in locals():
          if _from == "open":
            openCloseCross += 1
            print("open to close crossing at", i / FPS)
            oc_cross_times.append(str(round(from_sec + (i/FPS), 2)))
          elif _from == "close":
            closeCloseCross +=1
            cc_cross_times.append(str(round(from_sec + (i/FPS), 2)))
            
      elif (polygons[0].contains(Point(x0, y0)) and polygons[1].contains(Point(x0, y0))) and (polygons[0].contains(Point(x1, y1)) and not polygons[1].contains(Point(x1, y1))):
        if "_from" in locals():
          if _from == "close":
            closeOpenCross += 1
            print("close to open crossing at", i / FPS)
            co_cross_times.append(str(round(from_sec + (i/FPS), 2)))
          elif _from == "open":
            openOpenCross += 1
            oo_cross_times.append(str(round(from_sec + (i/FPS), 2)))
            
    if experiment == "RAM":
      
      """Crossings"""
      if in_center(x0, y0) and (not (in_center(x1, y1))):
        if polygons[0].contains(Point(x1, y1)):
          arm_num = "1"
        elif polygons[7].contains(Point(x1, y1)):
          arm_num = "6"
        elif polygons[6].contains(Point(x1, y1)):
          arm_num = "7"
        elif polygons[5].contains(Point(x1, y1)):
          arm_num = "8"
        elif polygons[4].contains(Point(x1, y1)):
          arm_num = "5"
        elif polygons[3].contains(Point(x1, y1)):
          arm_num = "2"
        elif polygons[2].contains(Point(x1, y1)):
          arm_num = "3"
        elif polygons[1].contains(Point(x1, y1)):
          arm_num = "4"
        else:
          arm_num = "none"
          
        ToC = str(round(from_sec + (i/FPS), 2))
        cross_dict[ToC] = arm_num
        
    if experiment == "OFT":
      if (polygons[0].contains(Point(x0, y0))) and polygons[0].contains(Point(x1, y1)):
        if (polygons[1].contains(Point(x0, y0))) and polygons[1].contains(Point(x1, y1)):
          inside_box_speeds.append(speed)
        else:
          outer_box_speeds.append(speed)
          
    if experiment == "TYM":
      if (polygons[0].contains(Point(x0, y0))) and polygons[0].contains(Point(x1, y1)):
        first_arm_speeds.append(speed)
      elif (polygons[1].contains(Point(x0, y0))) and polygons[1].contains(Point(x1, y1)):
        right_arm_speeds.append(speed)
      elif (polygons[2].contains(Point(x0, y0))) and polygons[2].contains(Point(x1, y1)):
        left_arm_speeds.append(speed)
        
        
    if experiment == "Free Draw":
      for i in range(len(polygons)):
        if (polygons[i].contains(Point(x0, y0))) and (polygons[i].contains(Point(x1, y1))):
          globals()["polygon_" + str(i) + "_speeds"].append(speed)
        
    x0 = x1
    y0 = y1
    
  real_speed_avg = sum(real_speeds) / len(real_speeds)
    
  if experiment == "EPM":
    if len(oo_cross_times) > 0: 
        previous_oo = float(oo_cross_times[0])
        oo_cross_times_cleaned = []
        oo_cross_times_cleaned.append(str(previous_oo))
        for i in oo_cross_times:
            if abs(float(i) - previous_oo) > 0.8: # 1.5
                oo_cross_times_cleaned.append(i)
            previous_oo = float(i)
            
        oo_cross_times = oo_cross_times_cleaned
    
    if len(cc_cross_times) > 0:
        previous_cc = float(cc_cross_times[0])
        cc_cross_times_cleaned = []
        cc_cross_times_cleaned.append(str(previous_cc))
        for i in cc_cross_times:
            if abs(float(i) - previous_cc) > 0.8: # 1.5
                cc_cross_times_cleaned.append(i)
            previous_cc = float(i)
            
        cc_cross_times = cc_cross_times_cleaned



  total_distance = total_distance * ratio  
  average_speed_cmm = sum(speeds) / len(speeds)
  average_speed_kmh = average_speed_cmm * 0.036
  
  if experiment == "MWM":
    q1_list = []
    q2_list = []
    q3_list = []
    q4_list = []
    center_circle_list = []
    periphery_list = []
    for i in range(len(df)):
      x = Xs.iloc[i]
      y = Ys.iloc[i]
      r = math.sqrt((abs(center_x - Xs.iloc[i]) ** 2 + abs(center_y - Ys.iloc[i]) ** 2))
      if r <= R:
        if (platform_centerX > center_x) and (platform_centerY < center_y):
          if (x < point1_x and x > point4_x) and (y > point4_y and y < point1_y):
            q1_list.append(df.iloc[i])
          elif (x < point4_x and x > point3_x) and (y > point4_y and y < point3_y):
            q2_list.append(df.iloc[i])
          elif (x < point2_x and x > point3_x) and (y > point3_y and y < point2_y):
            q3_list.append(df.iloc[i])
          elif (x < point1_x and x > point2_x) and (y > point1_y and y < point2_y):
            q4_list.append(df.iloc[i])
            
        elif (platform_centerX < center_x) and (platform_centerY < center_y):
          if (x < point1_x and x > point4_x) and (y < point4_y and y > point1_y):
            q1_list.append(df.iloc[i])
          elif (x < point3_x and x > point4_x) and (y > point4_y and y < point3_y):
            q2_list.append(df.iloc[i])
          elif (x < point2_x and x > point3_x) and (y < point3_y and y > point2_y):
            q3_list.append(df.iloc[i])
          elif (x < point2_x and x > point1_x) and (y > point1_y and y < point2_y):
            q4_list.append(df.iloc[i])
          
        elif (platform_centerX < center_x) and (platform_centerY > center_y):
          if (x > point1_x and x < point4_x) and (y < point4_y and y > point1_y):
            q1_list.append(df.iloc[i])
          elif (x < point3_x and x > point4_x) and (y < point4_y and y > point3_y):
            q2_list.append(df.iloc[i])
          elif (x > point2_x and x < point3_x) and (y < point3_y and y > point2_y):
            q3_list.append(df.iloc[i])
          elif (x < point2_x and x > point1_x) and (y < point1_y and y > point2_y):
            q4_list.append(df.iloc[i])
            
        elif (platform_centerX > center_x) and (platform_centerY > center_y):
          if (x > point1_x and x < point4_x) and (y > point4_y and y < point1_y):
            q1_list.append(df.iloc[i])
          elif (x > point3_x and x < point4_x) and (y < point4_y and y > point3_y):
            q2_list.append(df.iloc[i])
          elif (x > point2_x and x < point3_x) and (y > point3_y and y < point2_y):
            q3_list.append(df.iloc[i])
          elif (x > point2_x and x < point1_x) and (y < point1_y and y > point2_y):
            q4_list.append(df.iloc[i])
            
        else:
          print("**********************************")
          print("Point1:", point1_x, point1_y)
          print("Point2:", point2_x, point2_y)
          print("Point3:", point3_x, point3_y)
          print("Point4:", point4_x, point4_y)
          print("**********************************")
        
      if r < center_circle_r:
        center_circle_list.append(df.iloc[i])
      elif r > center_circle_r:
        periphery_list.append(df.iloc[i])
    
    average_speed_kmh_lb = Label(tab2, text= "Average speed of the animal is " + str(round(real_speed_avg, 2)) + " cm/min")
    average_speed_kmh_lb.config(font=("Courier", 30))
    average_speed_kmh_lb.place(x=200, y=360)
    
    total_distance_lb = Label(tab2, text="Total distance: " + str(round(total_distance, 2)) + " centimeters")
    total_distance_lb.config(font=("Courier", 30))
    total_distance_lb.place(x=200, y=400)
    
    q1_lb = Label(tab2, text=str(round(len(q1_list) / FPS, 2)) + " Seconds in the first quadrant")
    q1_lb.config(font=("Courier", 30))
    q1_lb.place(x = 200, y=450)
    
    q2_lb = Label(tab2, text=str(round(len(q2_list) / FPS, 2)) + " Seconds in the second quadrant")
    q2_lb.config(font=("Courier", 30))
    q2_lb.place(x = 200, y=490)
    
    q3_lb = Label(tab2, text=str(round(len(q3_list) / FPS, 2)) + " Seconds in the third quadrant")
    q3_lb.config(font=("Courier", 30))
    q3_lb.place(x = 200, y=530)
    
    q4_lb = Label(tab2, text=str(round(len(q4_list) / FPS, 2)) + " Seconds in the fourth quadrant")
    q4_lb.config(font=("Courier", 30))
    q4_lb.place(x = 200, y=570)
    
    center_lb = Label(tab2, text=str(round(len(center_circle_list) / FPS, 2)) + " Seconds in the Center")
    center_lb.config(font=("Courier", 30))
    center_lb.place(x = 200, y=610)
    
    periphery_lb = Label(tab2, text=str(round(len(periphery_list) / FPS, 2)) + " Seconds in the Periphery")
    periphery_lb.config(font=("Courier", 30))
    periphery_lb.place(x = 200, y=650)
    return 0
      
  
  for i in range(1, len(polygons) + 1):
    globals()["Polygon_" + str(i) + "_List"] = []
  
  for i in range(len(polygons)):
    for j in range(len(df)):
      x = Xs.iloc[j]
      y = Ys.iloc[j]
      point = Point(x,y)
      
      if polygons[i].contains(point):
        globals()["Polygon_" + str(i + 1) + "_List"].append(df.iloc[j])
        
        if experiment == "EPM":
          if polygons[0].contains(point) and polygons[1].contains(point):
            center_list.append(df.iloc[j])
          else:
            if i == 0:
              if y < open_arm_y_threshold:
                open_arm1_list.append(df.iloc[j])
              elif y > open_arm_y_threshold:
                open_arm2_list.append(df.iloc[j])
            elif i == 1:
              if x > closed_arm_x_threshold:
                closed_arm2_list.append(df.iloc[j])
              elif x < closed_arm_x_threshold:
                closed_arm1_list.append(df.iloc[j])
    
        
  average_speed_kmh_lb = Label(tab2, text= "Average speed of the animal is " + str(round(real_speed_avg, 2)) + " cm/min" + " (" + str(round(average_speed_cmm, 2)) + " cm/min overall)")
  average_speed_kmh_lb.config(font=("Courier", 30))
  average_speed_kmh_lb.place(x=200, y=160)
     
  total_distance_lb = Label(tab2, text="Total distance: " + str(round(total_distance, 2)) + " centimeters")
  total_distance_lb.config(font=("Courier", 30))
  total_distance_lb.place(x=200, y=200)
  
  if experiment == "Free Draw":
    for i in range(len(polygons)):
      globals()["Label" + str(i)] = Label(tab2, text="Polygon " + str(i + 1) + " includes the point in " + str(round(len(globals()["Polygon_" + str(i + 1) + "_List"]) / FPS, 2)) + " Seconds")
      globals()["Label" + str(i)].config(font=("Courier", 30))
      globals()["Label" + str(i)].place(x = 200, y=250 + i * 80)
      
      try:
        globals()["Label_s" + str(i)] = Label(tab2, text="Average speed in Polygon " + str(i) + ": " + str(round(sum(globals()["polygon_" + str(i) + "_speeds"]) / len(globals()["polygon_" + str(i) + "_speeds"]), 2)) + " cm/min")
      except ZeroDivisionError:
        globals()["Label_s" + str(i)] = Label(tab2, text="Average speed in Polygon " + str(i) + ": " + str(0.0) + " cm/min")
      globals()["Label_s" + str(i)].config(font=("Courier", 30))
      globals()["Label_s" + str(i)].place(x = 200, y=290 + i * 80)
      
      
  if experiment == "EPM":
    open_arm_lb = Label(tab2, text=str(round(round(len(open_arm1_list) / FPS, 2) + round(len(open_arm2_list) / FPS, 2), 2)) + " Seconds in open arm")
    #open_arm_lb = Label(tab2, text=str(round(len(open_arm_speeds) / FPS, 2)) + " Total Seconds in open arm")
    open_arm_lb.config(font=("Courier", 30))
    open_arm_lb.place(x = 200, y=250)
    
    mini_maze_canvas = Canvas(tab2, height = 350, width=350)
    mini_maze_canvas.place(x=1370, y=240)
    mini_maze_canvas.create_rectangle(145, 10, 205, 340, fill='', outline="green", width=3)
    mini_maze_canvas.create_rectangle(10, 145, 340, 205, fill='', outline="green", width=3)
    
    mm_arm1_lb = Label(mini_maze_canvas, text="1")
    mm_arm1_lb.config(font=("Courier", 34))
    mm_arm1_lb.place(x=157, y = 20)
    
    mm_arm2_lb = Label(mini_maze_canvas, text="2")
    mm_arm2_lb.config(font=("Courier", 34))
    mm_arm2_lb.place(x=300, y = 149)
    
    mm_arm3_lb = Label(mini_maze_canvas, text="3")
    mm_arm3_lb.config(font=("Courier", 34))
    mm_arm3_lb.place(x=157, y = 280)
    
    mm_arm4_lb = Label(mini_maze_canvas, text="4")
    mm_arm4_lb.config(font=("Courier", 34))
    mm_arm4_lb.place(x=15, y = 149)
    
    open_arm1_lb = Label(tab2, text=str(round(len(open_arm1_list) / FPS, 2)) + " Seconds in arm 1 (open)")
    open_arm1_lb.config(font=("Courier", 30))
    open_arm1_lb.place(x = 200, y=290)
    
    open_arm2_lb = Label(tab2, text=str(round(len(open_arm2_list) / FPS, 2)) + " Seconds in arm 3 (open)")
    open_arm2_lb.config(font=("Courier", 30))
    open_arm2_lb.place(x = 200, y=330)
    
    try:
      open_arm_speed_lb = Label(tab2, text="Average speed in open arm " + str(round(sum(open_arm_speeds) / len(open_arm_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      open_arm_speed_lb = Label(tab2, text="Average speed in open arm " + str(0.0) + " cm/min")
    open_arm_speed_lb.config(font=("Courier", 30))
    open_arm_speed_lb.place(x = 200, y=370)
    
    closed_arm_lb = Label(tab2, text=str(round(round(len(closed_arm1_list) / FPS, 2) + round(len(closed_arm2_list) / FPS, 2), 2)) + " Seconds in closed arm")
    # closed_arm_lb = Label(tab2, text=str(round(len(closed_arm_speeds) / FPS, 2)) + " Total Seconds in closed arm")
    closed_arm_lb.config(font=("Courier", 30))
    closed_arm_lb.place(x = 200, y=410) 
    
    closed_arm1_lb = Label(tab2, text=str(round(len(closed_arm1_list) / FPS, 2)) + " Seconds in arm 4 (closed)")
    closed_arm1_lb.config(font=("Courier", 30))
    closed_arm1_lb.place(x = 200, y=450)
    
    closed_arm2_lb = Label(tab2, text=str(round(len(closed_arm2_list) / FPS, 2)) + " Seconds in arm 2 (closed)")
    closed_arm2_lb.config(font=("Courier", 30))
    closed_arm2_lb.place(x = 200, y=490)
    
    try:
      closed_arm_speed_lb = Label(tab2, text="Average speed in closed arm " + str(round(sum(closed_arm_speeds) / len(closed_arm_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      closed_arm_speed_lb = Label(tab2, text="Average speed in closed arm " + str(0.0) + " cm/min")
    closed_arm_speed_lb.config(font=("Courier", 30))
    closed_arm_speed_lb.place(x = 200, y=530)
    
    
    center_lb = Label(tab2, text=str(round(len(center_speeds) / FPS, 2)) + " Seconds in center")
    center_lb.config(font=("Courier", 30))
    center_lb.place(x = 200, y=570)
    
    try:
      center_speed_lb = Label(tab2, text="Average speed in center " + str(round(sum(center_speeds) / len(center_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      center_speed_lb = Label(tab2, text="Average speed in center " + str(0.0) + " cm/min")
    center_speed_lb.config(font=("Courier", 30))
    center_speed_lb.place(x = 200, y=610)
    
    openClose_lb = Label(tab2, text= "Open to close crossing: " + str(openCloseCross) + " times")
    openClose_lb.config(font=("Courier", 30))
    openClose_lb.place(x = 200, y=650)
    
    oc_crossing_times_lb = Label(tab2, text= "Open to close crossing at times: " + ", ".join(oc_cross_times))
    oc_crossing_times_lb.config(font=("Courier", 28))
    oc_crossing_times_lb.place(x = 200, y=690)
    
    closeOpen_lb = Label(tab2, text= "Close to open crossing: " + str(closeOpenCross) + " times")
    closeOpen_lb.config(font=("Courier", 30))
    closeOpen_lb.place(x = 200, y=730)
    
    co_crossing_times_lb = Label(tab2, text= "Close to open crossing at times: " + ", ".join(co_cross_times))
    co_crossing_times_lb.config(font=("Courier", 28))
    co_crossing_times_lb.place(x = 200, y=770)
    
    openOpen_lb = Label(tab2, text= "Open to open crossing: " + str(openOpenCross) + " times")
    openOpen_lb.config(font=("Courier", 30))
    openOpen_lb.place(x = 200, y=810)
    
    oo_crossing_times_lb = Label(tab2, text= "Open to open crossing at times: " + ", ".join(oo_cross_times))
    oo_crossing_times_lb.config(font=("Courier", 28))
    oo_crossing_times_lb.place(x = 200, y=850)
    
    closeClose_lb = Label(tab2, text= "Close to close crossing: " + str(closeCloseCross) + " times")
    closeClose_lb.config(font=("Courier", 30))
    closeClose_lb.place(x = 200, y=890)
    
    cc_crossing_times_lb = Label(tab2, text= "Close to close crossing at times: " + ", ".join(cc_cross_times))
    cc_crossing_times_lb.config(font=("Courier", 28))
    cc_crossing_times_lb.place(x = 200, y=930)
    
    canva_crossings = Canvas(tab2, height = 70, width = 1000)
    canva_crossings.place(x=200, y=70)
    canva_crossings.create_rectangle(10, 10, 950, 20, fill="#aeb3b0", outline="black")
    
    crossing_lb = Label(tab2, text= "Crossing")
    crossing_lb.config(font=("Times New Roman", 14, "italic"))
    crossing_lb.place(x=110, y= 71)
    
    time_lb = Label(tab2, text= "Real Time(s)")
    time_lb.config(font=("Times New Roman", 14, "italic"))
    time_lb.place(x=110, y= 100)
    
    canva_time_line = Canvas(tab2, height = 5, width = 1105)
    canva_time_line.place(x=100, y= 95)
    canva_time_line.create_line(0, 2, 1100, 2, fill="black", width=2)
    
    
    
    color="#02f262"
    cross_times_sum = (oc_cross_times + co_cross_times)
    inside_crosses = (oo_cross_times + cc_cross_times)
    total_cross_times = sorted([float(time) for time in cross_times_sum])
    current_time = 0
    for time in total_cross_times:
        print("Time is", time)
        if str(time) in oc_cross_times:
            if time == total_cross_times[-1]:
                canva_crossings.create_rectangle((float(time) * 3.4), 10, (to_sec * 3.4), 20, fill="#18b571")
            canva_crossings.create_rectangle(current_time, 10, (float(time) * 3.4), 20, fill="#14fa68")
        elif str(time) in co_cross_times:
            if time == total_cross_times[-1]:
                canva_crossings.create_rectangle((float(time) * 3.4), 10, (to_sec * 3.4), 20, fill="#14fa68")
            canva_crossings.create_rectangle(current_time, 10, (float(time) * 3.4), 20, fill="#18b571")
        current_time = float(time) * 3.4
        
    for time in inside_crosses:
      canva_crossings.create_line((float(time) * 3.4), 10, (float(time) * 3.4), 20, fill="magenta", width=4)
      locals()["label_ " + str(round(float(time), 4))] = Label(canva_crossings, text=str(round(float(time))), font=("Arial", 13))
      (locals()["label_ " + str(round(float(time), 4))]).config()
      (locals()["label_ " + str(round(float(time), 4))]).place(x=round(float(time) * 3.4, 2) - 6, y = 30)
      
    for time in oc_cross_times:
      create_circle(round(float(time) * 3.4, 2), 15, 6, canva_crossings)
      locals()["label_ " + str(round(float(time), 4))] = Label(canva_crossings, text=str(round(float(time))), font=("Arial", 13))
      (locals()["label_ " + str(round(float(time), 4))]).config()
      (locals()["label_ " + str(round(float(time), 4))]).place(x=round(float(time) * 3.4, 2) - 6, y = 30)
      
    color="#006400"
    for time in co_cross_times:
      create_circle(round(float(time) * 3.4, 2), 15, 6, canva_crossings)
      locals()["label_ " + str(round(float(time), 4))] = Label(canva_crossings, text=str(round(float(time))), font=("Arial", 13))
      (locals()["label_ " + str(round(float(time), 4))]).config()
      (locals()["label_ " + str(round(float(time), 4))]).place(x=round(float(time) * 3.4, 2) - 6, y = 30)
    # cross_bar_path = ("/".join((csv_file.split("/"))[:-1])) + "/Crossing_Bar.ps"

    
  if experiment == "OFT":
    outer_box_lb = Label(tab2, text=str(round((len(Polygon_1_List) - len(Polygon_2_List)) / FPS, 2)) + " Seconds in outer box")
    outer_box_lb.config(font=("Courier", 30))
    outer_box_lb.place(x = 200, y=250)
    
    try:
      outer_box_speed_lb = Label(tab2, text="Average speed in outer box " + str(round(sum(outer_box_speeds) / len(outer_box_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      outer_box_speed_lb = Label(tab2, text="Average speed in outer box " + str(0.0) + " cm/min")
    outer_box_speed_lb.config(font=("Courier", 30))
    outer_box_speed_lb.place(x = 200, y=290)
    
    inside_box_lb = Label(tab2, text=str(round(len(Polygon_2_List) / FPS, 2)) + " Seconds in inside box")
    inside_box_lb.config(font=("Courier", 30))
    inside_box_lb.place(x = 200, y=330)
    
    try: 
      inside_box_speed_lb = Label(tab2, text="Average speed in inside box " + str(round(sum(inside_box_speeds) / len(inside_box_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      inside_box_speed_lb = Label(tab2, text="Average speed in inside box " + str(0.0) + " cm/min")
    inside_box_speed_lb.config(font=("Courier", 30))
    inside_box_speed_lb.place(x = 200, y=370)
    
    
  if experiment == "TYM":
    first_arm_lb = Label(tab2, text=str(round(len(Polygon_1_List) / FPS, 2)) + " Seconds in first arm")
    first_arm_lb.config(font=("Courier", 30))
    first_arm_lb.place(x = 200, y=250)
    
    try:
      first_arm_speed_lb = Label(tab2, text="Average speed in first arm " + str(round(sum(first_arm_speeds) / len(first_arm_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      first_arm_speed_lb = Label(tab2, text="Average speed in first arm " + str(0.0) + " cm/min")
    first_arm_speed_lb.config(font=("Courier", 30))
    first_arm_speed_lb.place(x = 200, y=290)
    
    right_arm_lb = Label(tab2, text=str(round(len(Polygon_2_List) / FPS, 2)) + " Seconds in right arm")
    right_arm_lb.config(font=("Courier", 30))
    right_arm_lb.place(x = 200, y=330)
    
    try:
      right_arm_speed_lb = Label(tab2, text="Average speed in right arm " + str(round(sum(right_arm_speeds) / len(right_arm_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      right_arm_speed_lb = Label(tab2, text="Average speed in right arm " + str(0.0) + " cm/min")
    right_arm_speed_lb.config(font=("Courier", 30))
    right_arm_speed_lb.place(x = 200, y=370)
    
    left_arm_lb = Label(tab2, text=str(round(len(Polygon_3_List) / FPS, 2)) + " Seconds in left arm")
    left_arm_lb.config(font=("Courier", 30))
    left_arm_lb.place(x = 200, y=410)
    
    try:
      left_arm_speed_lb = Label(tab2, text="Average speed in left arm " + str(round(sum(left_arm_speeds) / len(left_arm_speeds), 2)) + " cm/min")
    except ZeroDivisionError:
      left_arm_speed_lb = Label(tab2, text="Average speed in left arm " + str(0.0) + " cm/min")
    left_arm_speed_lb.config(font=("Courier", 30))
    left_arm_speed_lb.place(x = 200, y=450)
    
    
  if experiment == "RAM":
    arm1_lb = Label(tab2, text=str(round(len(Polygon_1_List) / FPS, 2)) + " Seconds in arm 1")
    arm1_lb.config(font=("Courier", 30))
    arm1_lb.place(x = 200, y=250)
    
    arm2_lb = Label(tab2, text=str(round(len(Polygon_2_List) / FPS, 2)) + " Seconds in arm 2")
    arm2_lb.config(font=("Courier", 30))
    arm2_lb.place(x = 200, y=290)
    
    arm3_lb = Label(tab2, text=str(round(len(Polygon_3_List) / FPS, 2)) + " Seconds in arm 3")
    arm3_lb.config(font=("Courier", 30))
    arm3_lb.place(x = 200, y=330)
    
    arm4_lb = Label(tab2, text=str(round(len(Polygon_4_List) / FPS, 2)) + " Seconds in arm 4")
    arm4_lb.config(font=("Courier", 30))
    arm4_lb.place(x = 200, y=370)
    
    arm5_lb = Label(tab2, text=str(round(len(Polygon_5_List) / FPS, 2)) + " Seconds in arm 5")
    arm5_lb.config(font=("Courier", 30))
    arm5_lb.place(x = 200, y=410)
    
    arm6_lb = Label(tab2, text=str(round(len(Polygon_6_List) / FPS, 2)) + " Seconds in arm 6")
    arm6_lb.config(font=("Courier", 30))
    arm6_lb.place(x = 200, y=450)
    
    arm7_lb = Label(tab2, text=str(round(len(Polygon_7_List) / FPS, 2)) + " Seconds in arm 7")
    arm7_lb.config(font=("Courier", 30))
    arm7_lb.place(x = 200, y=490)
    
    arm8_lb = Label(tab2, text=str(round(len(Polygon_8_List) / FPS, 2)) + " Seconds in arm 8")
    arm8_lb.config(font=("Courier", 30))
    arm8_lb.place(x = 200, y=530)
    
    canva_crossings_ram = Canvas(tab2, height = 70, width = 1250)
    canva_crossings_ram.place(x=200, y=70)
    canva_crossings_ram.create_rectangle(10, 10, 1150, 30, fill="#aeb3b0", outline="black") # Change here
    
    for time, arm_num in cross_dict.items():
      canva_crossings_ram.create_line((float(time) * 3.6), 10, (float(time) * 3.6), 30, fill="magenta", width=6)
      locals()["label_ " + str(round(float(time), 4))] = Label(canva_crossings_ram, text=str(round(float(time))), font=("Arial", 13))
      (locals()["label_ " + str(round(float(time), 4))]).config()
      (locals()["label_ " + str(round(float(time), 4))]).place(x=round(float(time) * 3.6, 2) - 6, y = 40)
      
      if ("previous_arm" in globals()) or ("previous_arm" in locals()):
        locals()["cross_ " + str(round(float(time), 4))] = Label(tab2, text=previous_arm + "->" + arm_num, font=("Arial", 9))
        (locals()["cross_ " + str(round(float(time), 4))]).config()
        (locals()["cross_ " + str(round(float(time), 4))]).place(x=200 + round(float(time) * 3.6, 2) - 6, y = 50)
        
      previous_arm = arm_num
    
    
def set_file_name():
  global file_name
  
  file_name = file_name_entry.get()
  
  save_polygons_lb.destroy()
  file_name_entry.destroy()
  done_bt2.destroy()
  
  propDict = {"polygons":polygons, "experiment":experiment, "ratio":ratio, "fps":FPS}
  
  with open("C:/Users/PC/Desktop/GUI/Mazes/" + file_name + ".pickle", "wb") as f:
    pickle.dump(propDict, f)
    
  successfull_lb = Label(tab2, text="Maze is Saved Successfully")
  successfull_lb.config(font=("Courier", 22))
  successfull_lb.place(x=1300, y=800)


def save_polygons():
  global save_polygons_lb
  global file_name_entry
  global done_bt2
  
  save_polygons_bt.destroy()
  
  save_polygons_lb = Label(tab2, text="Name of the File")
  save_polygons_lb.config(font=("Courier", 22))
  save_polygons_lb.place(x=1500, y=750)
  
  file_name_entry = Entry(tab2, width=10)
  file_name_entry.config(font=("Courier", 22))
  file_name_entry.place(x=1510, y=800)
  
  done_bt2 = Button(tab2, text="Done", command=set_file_name,height=1, width=8)
  done_bt2["font"] = myFont
  done_bt2.place(x=1690, y=800)
  

def load_polygons():
  global from_entry
  global to_entry
  global polygons
  global experiment
  global ratio
  global FPS
  global open_arm_speeds
  global closed_arm_speeds
  global center_speeds
  global choose_csv_bt
  
  choose_lb.destroy()
  choose_video_bt.destroy()
  load_polygons_bt.destroy()
  yes_bt.destroy()
  
  choose2_lb = Label(tab1, text="Choose the pickle file")
  choose2_lb.config(font=("Courier", 30))
  choose2_lb.place(x=700, y=100)
  
  load_path = askopenfilename()
  
  choose2_lb.destroy()
  
  text_label_2 = Label(tab1, text="Please Select the Time Interval (format: 0.00)")
  text_label_2.config(font=("Courier", 30))
  text_label_2.place(x=440, y=100)
  
  """Creating time input boxes"""
  from_entry = Entry(tab1, width=8)
  from_entry.config(font=("Courier", 20))
  from_entry.place(x=1620, y=700)
  
  from_label = Label(tab1, text="From:")
  from_label.config(font=("Courier", 20))
  from_label.place(x=1527, y=700)
  
  to_entry = Entry(tab1, width=8)
  to_entry.config(font=("Courier", 20))
  to_entry.place(x=1620, y=740)
  
  to_label = Label(tab1, text="To:")
  to_label.config(font=("Courier", 20))
  to_label.place(x=1560, y=740)
  
  done_bt = Button(tab1, text="Done", command=set_time_2, height=2, width=8)
  done_bt["font"] = myFont
  done_bt.place(x=1760, y = 710)
  
  if not "analyzed_bool" in globals():
    choose_csv_bt = Button(tab2, text="Choose CSV", command=choose_csv)
    choose_csv_bt["font"] = myFont
    choose_csv_bt.place(x=960, y=540)
  else:
    choose_csv_bt = Button(tab2, text="Analyze the Video", command=choose_csv)
    choose_csv_bt["font"] = myFont
    choose_csv_bt.place(x=920, y=540)
  
  with open(load_path, "rb") as f:
    propDict = pickle.load(f)
  
  polygons = propDict["polygons"]
  experiment = propDict["experiment"]
  ratio = propDict["ratio"]
  FPS = propDict["fps"]
  
  if experiment == "EPM":
    open_arm_speeds = []
    closed_arm_speeds = []
    center_speeds = []
  
  
def edit_point_click_EPM(event):
  global closest_point
  global point_index
  global list_is
  
  if (event.x <= 1280) and (event.y <= 720):
    total_points = open_arm_points_shapely + closed_arm_points_shapely
    #all_points = total_points.copy()
    closest_point = total_points[0]
    smallest_distance = 1000000000
    for point in total_points:
      xDiff = (event.x - point[0]) ** 2
      yDiff = (event.y - point[1]) ** 2
      distance = (xDiff + yDiff) ** 1/2
      if distance < smallest_distance:
        smallest_distance = distance
        closest_point = point
    
    point_index = total_points.index(closest_point)
    list_is = "open"
    if point_index > 3:
      point_index = point_index % 4
      list_is = "closed"
      
    root.bind("<B1-Motion>", edit_point_hold_EPM)
    root.bind("<ButtonRelease-1>", edit_point_release_EPM)
    print(closest_point)
    canva.delete(will_be_edited[closest_point])
    
  
def edit_point_hold_EPM(event):
  global closest_point
  global canva
  global open_arm_polygon
  global closed_arm_polygon
  global angle_lb
  
  if (event.x <= 1280) and (event.y <= 720):
    for e in delete_all:
      canva.delete(e)
    
    new = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
    delete_all.append(new)
    
    ex_x_index = point_index * 2
    ex_y_index = point_index * 2 + 1
    
    if list_is == "open":    
      open_arm_points.insert(ex_x_index, event.x)
      open_arm_points.pop(ex_x_index + 1)
      open_arm_points.insert(ex_y_index, event.y)
      open_arm_points.pop(ex_y_index + 1)
      
      canva.delete(open_arm_polygon)
      open_arm_polygon = canva.create_polygon(open_arm_points, fill="", outline="green", width=3)
      
      if point_index % 4 == 0:
        vector_1 = [open_arm_points[0] - open_arm_points[2], open_arm_points[1] - open_arm_points[3]]
        vector_2 = [open_arm_points[6] - open_arm_points[0], open_arm_points[7] - open_arm_points[1]]
      elif point_index % 4 == 1:
        vector_1 = [open_arm_points[2] - open_arm_points[0], open_arm_points[3] - open_arm_points[1]]
        vector_2 = [open_arm_points[2] - open_arm_points[4], open_arm_points[3] - open_arm_points[5]]
      elif point_index % 4 == 2:
        vector_1 = [open_arm_points[4] - open_arm_points[2], open_arm_points[5] - open_arm_points[3]]
        vector_2 = [open_arm_points[4] - open_arm_points[6], open_arm_points[5] - open_arm_points[7]]
      elif point_index % 4 == 3:
        vector_1 = [open_arm_points[6] - open_arm_points[0], open_arm_points[7] - open_arm_points[1]]
        vector_2 = [open_arm_points[6] - open_arm_points[4], open_arm_points[7] - open_arm_points[5]]
        
      unit_vector_1 = vector_1 / np. linalg. norm(vector_1)
      unit_vector_2 = vector_2 / np. linalg. norm(vector_2)
      dot_product = np. dot(unit_vector_1, unit_vector_2)
      angle = np.rad2deg(np.arccos(dot_product))
      if "angle_lb" in globals():
        angle_lb.destroy()
      angle_lb = Label(root, text=str(round(angle, 3)))
      angle_lb.config(font=("Courier", 22))
      angle_lb.place(x=open_arm_points[point_index * 2] + 220, y=open_arm_points[point_index * 2 + 1] + 200)
        
    
    if list_is == "closed":
      closed_arm_points.insert(ex_x_index, event.x)
      closed_arm_points.pop(ex_x_index + 1)
      closed_arm_points.insert(ex_y_index, event.y)
      closed_arm_points.pop(ex_y_index + 1)
      
      canva.delete(closed_arm_polygon)
      closed_arm_polygon = canva.create_polygon(closed_arm_points, fill="", outline="green", width=3)
    
      if point_index % 4 == 0:
        vector_1 = [closed_arm_points[0] - closed_arm_points[2], closed_arm_points[1] - closed_arm_points[3]]
        vector_2 = [closed_arm_points[6] - closed_arm_points[0], closed_arm_points[7] - closed_arm_points[1]]
      elif point_index % 4 == 1:
        vector_1 = [closed_arm_points[2] - closed_arm_points[0], closed_arm_points[3] - closed_arm_points[1]]
        vector_2 = [closed_arm_points[2] - closed_arm_points[4], closed_arm_points[3] - closed_arm_points[5]]
      elif point_index % 4 == 2:
        vector_1 = [closed_arm_points[4] - closed_arm_points[2], closed_arm_points[5] - closed_arm_points[3]]
        vector_2 = [closed_arm_points[4] - closed_arm_points[6], closed_arm_points[5] - closed_arm_points[7]]
      elif point_index % 4 == 3:
        vector_1 = [closed_arm_points[6] - closed_arm_points[0], closed_arm_points[7] - closed_arm_points[1]]
        vector_2 = [closed_arm_points[6] - closed_arm_points[4], closed_arm_points[7] - closed_arm_points[5]]  
    
      unit_vector_1 = vector_1 / np. linalg. norm(vector_1)
      unit_vector_2 = vector_2 / np. linalg. norm(vector_2)
      dot_product = np. dot(unit_vector_1, unit_vector_2)
      angle = np.rad2deg(np.arccos(dot_product))
      if "angle_lb" in globals():
        angle_lb.destroy()
      angle_lb = Label(root, text=str(round(angle, 3)))
      angle_lb.config(font=("Courier", 22))
      angle_lb.place(x=closed_arm_points[point_index * 2] + 220, y=closed_arm_points[point_index * 2 + 1] + 200)
  
  
def edit_point_release_EPM(event):
  if (event.x <= 1280) and (event.y <= 720):
    will_be_edited[(event.x, event.y)] = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
    if "angle_lb" in globals():  
      angle_lb.destroy()
    
    if list_is == "open":
      open_arm_points_shapely.clear()
      n = 0
      while n + 1 < len(open_arm_points):
        open_arm_points_shapely.append((open_arm_points[n], open_arm_points[n + 1]))
        n+=2
    
    if list_is == "closed":
      closed_arm_points_shapely.clear()
      n = 0
      while n + 1 < len(closed_arm_points):
        closed_arm_points_shapely.append((closed_arm_points[n], closed_arm_points[n + 1]))
        n+=2
      
      
def draw_EPM(event):
  global EPM_click_count
  global text_label4
  global text_label5
  global open_arm_polygon
  global closed_arm_polygon
  global open_arm_y_threshold
  global closed_arm_x_threshold
  
  create_circle(event.x, event.y, 6, canva, edit=True)
  print(event.x, event.y) # DELETE ME
  if EPM_click_count < 3:
    print(event.x, event.y)
    open_arm_points.append(event.x)
    open_arm_points.append(event.y)
    open_arm_points_shapely.append((event.x, event.y))
    
  elif EPM_click_count == 3:
    open_arm_points.append(event.x)
    open_arm_points.append(event.y)
    open_arm_points_shapely.append((event.x, event.y))
    open_arm_polygon = canva.create_polygon(open_arm_points, fill="", outline="green", width=3)
    text_label3.destroy()
    text_label4 = Label(tab1, text="Select the corners of the closed arm")
    text_label4.config(font=("Courier", 30))
    text_label4.place(x=500, y=100)
    open_arm_y_threshold = (open_arm_points[1] + open_arm_points[3] + open_arm_points[5] + open_arm_points[7]) / 4
    
  elif EPM_click_count < 7:
    closed_arm_points.append(event.x)
    closed_arm_points.append(event.y)
    closed_arm_points_shapely.append((event.x, event.y))
    
  elif EPM_click_count == 7:
    closed_arm_points.append(event.x)
    closed_arm_points.append(event.y)
    closed_arm_points_shapely.append((event.x, event.y))
    closed_arm_polygon = canva.create_polygon(closed_arm_points, fill="", outline="green", width=3)
    text_label4.destroy()
    text_label5 = Label(tab1, text="Continue or Edit")
    text_label5.config(font=("Courier", 30))
    text_label5.place(x=740, y=100)
    closed_arm_x_threshold = (closed_arm_points[0] + closed_arm_points[2] + closed_arm_points[4] + closed_arm_points[6]) / 4
    
    continue_button = Button(tab1, text="Continue", command=complete, width=14)
    continue_button["font"] = myFont
    continue_button.place(x=1620, y=900)
    
    root.unbind("<Button-1>")
    root.bind("<Button-1>", edit_point_click_EPM)
    
    
  EPM_click_count += 1
  

def edit_point_click_OFT(event):
  global closest_point
  global point_index
  global inside_return
  global related_inside_point

  total_points = outer_box_points_shapely
  closest_point = total_points[0]
  smallest_distance = 1000000000
  for point in total_points:
    xDiff = (event.x - point[0]) ** 2
    yDiff = (event.y - point[1]) ** 2
    distance = (xDiff + yDiff) ** 1/2
    if distance < smallest_distance:
      smallest_distance = distance
      closest_point = point
      
  point_index = total_points.index(closest_point)
  related_inside_point = inside_box_points_shapely[point_index]
  
  root.bind("<B1-Motion>", edit_point_hold_OFT)
  root.bind("<ButtonRelease-1>", edit_point_release_OFT)
  print(closest_point)
  print("inside point:", related_inside_point)
  canva.delete(will_be_edited[closest_point])
  # canva.delete(will_be_edited[related_inside_point])
  
  
def edit_point_hold_OFT(event):
  global closest_point
  global canva
  global outer_box_rectangle
  global inside_box_rectangle
  global angle_lb
  
  for e in delete_all:
    canva.delete(e)
  
  new = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
  delete_all.append(new)
  
  ex_x_index = point_index * 2
  ex_y_index = point_index * 2 + 1
  
  outer_box_points.insert(ex_x_index, event.x)
  outer_box_points.pop(ex_x_index + 1)
  outer_box_points.insert(ex_y_index, event.y)
  outer_box_points.pop(ex_y_index + 1)
  
  if point_index == 0:
    new_inside_point_x = event.x + (abs(event.x - oTopRight_x)) * inner_ratio
    new_inside_point_y = event.y + (abs(event.y - oBottomLeft_y)) * inner_ratio
  elif point_index == 1:
    new_inside_point_x = event.x + (abs(event.x - oBottomRight_x)) * inner_ratio
    new_inside_point_y = event.y - (abs(event.y - oTopLeft_y)) * inner_ratio
  elif point_index == 2:
    new_inside_point_x = event.x - (abs(event.x - oBottomLeft_x)) * inner_ratio
    new_inside_point_y = event.y - (abs(oBottomRight_y - oTopRight_y)) * inner_ratio
  elif point_index == 3:
    new_inside_point_x = event.x - (abs(event.x - oTopLeft_x)) * inner_ratio
    new_inside_point_y = event.y + (abs(event.y - oBottomRight_y)) * inner_ratio
  
  inside_box_points.insert(ex_x_index, new_inside_point_x)
  inside_box_points.pop(ex_x_index + 1)
  inside_box_points.insert(ex_y_index, new_inside_point_y)
  inside_box_points.pop(ex_y_index + 1)
  
  canva.delete(outer_box_rectangle)
  outer_box_rectangle = canva.create_polygon(outer_box_points, fill="", outline="green", width=4)
  canva.delete(inside_box_rectangle)
  inside_box_rectangle = canva.create_polygon(inside_box_points, fill="", outline="red", width=4)
  
def edit_point_release_OFT(event):
  will_be_edited[(event.x, event.y)] = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
  if "angle_lb" in globals():  
    angle_lb.destroy()
      
  outer_box_points_shapely.clear()
  n = 0
  while n + 1 < len(outer_box_points):
    outer_box_points_shapely.append((outer_box_points[n], outer_box_points[n + 1]))
    n+=2
    
  inside_box_points_shapely.clear()
  m = 0
  while m + 1 < len(inside_box_points):
    inside_box_points_shapely.append((inside_box_points[m], inside_box_points[m + 1]))
    m+=2
  
def set_OFT_ratio():
  global inner_ratio
  global text_label3
    
  inner_ratio = float(e_OFT.get())
  
  e_OFT.destroy()
  ratio_cont_bt.destroy()
  
  text_label23.destroy()
  text_label3 = Label(tab1, text="Select the top left and the bottom right")
  text_label3.config(font=("Courier", 30))
  text_label3.place(x=120, y=100)
  
  root.bind("<Button-1>", draw_OFT)

def draw_OFT(event):
  global OFT_click_count
  global text_label4
  global text_label5
  global oTopLeft_x, oTopLeft_y
  global oBottomLeft_x, oBottomLeft_y
  global oBottomRight_x, oBottomRight_y
  global oTopRight_x, oTopRight_y
  global iTopLeft_x, iTopLeft_y
  global iBottomLeft_x, iBottomLeft_y
  global iBottomRight_x, iBottomRight_y
  global iTopRight_x, iTopRight_y
  global outer_box_rectangle
  global inside_box_rectangle


  create_circle(event.x, event.y, 6, canva, edit=True)
  if OFT_click_count == 0:
    oTopLeft_x = event.x
    oTopLeft_y = event.y
    outer_box_points.append(oTopLeft_x)
    outer_box_points.append(oTopLeft_y)
    outer_box_points_shapely.append((oTopLeft_x, oTopLeft_y))
    
  elif OFT_click_count == 1:
    oBottomRight_x = event.x
    oBottomRight_y = event.y
 
    
    oBottomLeft_x = oTopLeft_x
    oBottomLeft_y = oBottomRight_y
    outer_box_points_shapely.append((oBottomLeft_x, oBottomLeft_y))
    
    outer_box_points_shapely.append((oBottomRight_x, oBottomRight_y))
    
    oTopRight_x = oBottomRight_x
    oTopRight_y = oTopLeft_y
    outer_box_points_shapely.append((oTopRight_x, oTopRight_y))
    
    create_circle(oBottomLeft_x, oBottomLeft_y, 6, canva, edit=True)
    create_circle(oTopRight_x, oTopRight_y, 6, canva, edit=True)
    
    outer_box_points.append(oBottomLeft_x)
    outer_box_points.append(oBottomLeft_y)
    outer_box_points.append(oBottomRight_x)
    outer_box_points.append(oBottomRight_y)
    outer_box_points.append(oTopRight_x)
    outer_box_points.append(oTopRight_y)
    
    outer_box_rectangle = canva.create_polygon(outer_box_points, fill="", outline="green", width=4)
    text_label3.destroy()

    #polygons.append(Polygon(outer_box_points_shapely))
    
    iTopLeft_x = oTopLeft_x + (abs(oTopLeft_x - oTopRight_x)) * inner_ratio
    iTopLeft_y = oTopLeft_y + (abs(oTopLeft_y - oBottomLeft_y)) * inner_ratio
    # create_circle(iTopLeft_x, iTopLeft_y, 6, canva, edit=True)
    inside_box_points.append(iTopLeft_x)
    inside_box_points.append(iTopLeft_y)
    inside_box_points_shapely.append((iTopLeft_x, iTopLeft_y))
    
    iBottomLeft_x = oBottomLeft_x + (abs(oBottomLeft_x - oBottomRight_x)) * inner_ratio
    iBottomLeft_y = oBottomLeft_y - (abs(oTopLeft_y - oBottomLeft_y)) * inner_ratio
    # create_circle(iBottomLeft_x, iBottomLeft_y, 6, canva, edit=True)
    inside_box_points.append(iBottomLeft_x)
    inside_box_points.append(iBottomLeft_y)
    inside_box_points_shapely.append((iBottomLeft_x, iBottomLeft_y))
    
    iBottomRight_x = oBottomRight_x - (abs(oBottomLeft_x - oBottomRight_x)) * inner_ratio
    iBottomRight_y = oBottomRight_y - (abs(oTopRight_y - oBottomRight_y)) * inner_ratio
    # create_circle(iBottomRight_x, iBottomRight_y, 6, canva, edit=True)
    inside_box_points.append(iBottomRight_x)
    inside_box_points.append(iBottomRight_y)
    inside_box_points_shapely.append((iBottomRight_x, iBottomRight_y))
    
    iTopRight_x = oTopRight_x - (abs(oTopLeft_x - oTopRight_x)) * inner_ratio
    iTopRight_y = oTopRight_y + (abs(oTopRight_y - oBottomRight_y)) * inner_ratio
    # create_circle(iTopRight_x, iTopRight_y, 6, canva, edit=True)
    inside_box_points.append(iTopRight_x)
    inside_box_points.append(iTopRight_y)
    inside_box_points_shapely.append((iTopRight_x, iTopRight_y))
    
    inside_box_rectangle = canva.create_polygon(inside_box_points, fill="", outline="red", width=4)
    text_label5 = Label(tab1, text="Continue")
    text_label5.config(font=("Courier", 30))
    text_label5.place(x=820, y=100)
    #polygons.append(Polygon(inside_box_points_shapely))
    
    continue_button = Button(tab1, text="Continue", command=complete, width=14)
    continue_button["font"] = myFont
    continue_button.place(x=1620, y=900)
  
    root.unbind("<Button-1>")
    root.bind("<Button-1>", edit_point_click_OFT)
    
  OFT_click_count += 1
  

def edit_point_click_MWM(event):
  if ((event.x > center_x - 6) and (event.x < center_x + 6)) and ((event.y > center_y - 6) and (event.y < center_y + 6)):
    sector1_lb.place_forget()
    sector2_lb.place_forget()
    sector3_lb.place_forget()
    sector4_lb.place_forget()
    
    root.bind("<B1-Motion>", edit_point_hold_MWM)
    
    if not "done_release" in globals():
      root.bind("<ButtonRelease-1>", edit_point_release_MWM)
  
  elif ((event.x > point1_x - 6) and (event.x < point1_x + 6)) and ((event.y > point1_y - 6) and (event.y < point1_y + 6)):
    sector1_lb.place_forget()
    sector2_lb.place_forget()
    sector3_lb.place_forget()
    sector4_lb.place_forget()
    
    root.bind("<B1-Motion>", edit_point_hold_rotate_MWM)
    
    
  
def edit_point_hold_MWM(event):
  global center_point
  global point1
  global point2
  global point3
  global point4
  global out_circle
  global cross1
  global cross2
  global platform_points
  global platform_polygon
  
  for e in will_be_deleted:
    canva.delete(e)
  
  center_point = create_circle(event.x, event.y, 9, canva, delete=True)
  out_circle = create_circle(event.x, event.y, R, canva, no_fill=True)
  center_circle = create_circle(event.x, event.y, center_circle_r, canva, no_fill=True)
  point1 = create_circle(event.x + point1_x_diff, event.y + point1_y_diff, 6, canva, delete=True)
  point2 = create_circle(event.x + point2_x_diff, event.y + point2_y_diff, 6, canva, delete=True)
  point3 = create_circle(event.x + point3_x_diff, event.y + point3_y_diff, 6, canva, delete=True)
  point4 = create_circle(event.x + point4_x_diff, event.y + point4_y_diff, 6, canva, delete=True)
  cross1 = canva.create_line(event.x + point1_x_diff, event.y + point1_y_diff, event.x + point3_x_diff, event.y + point3_y_diff, width=4, fill="green")
  cross2 = canva.create_line(event.x + point2_x_diff, event.y + point2_y_diff, event.x + point4_x_diff, event.y + point4_y_diff, width=4, fill="green")
  will_be_deleted.append(cross1)
  will_be_deleted.append(cross2)
  platform_points = [event.x+pl_p1_dx, event.y+pl_p1_dy, event.x+pl_p2_dx, event.y+pl_p2_dy, event.x+pl_p3_dx, event.y+pl_p3_dy, event.x+pl_p4_dx, event.y+pl_p4_dy]
  platform_polygon = canva.create_polygon(platform_points, fill="", outline="blue", width=3)
  will_be_deleted.append(platform_polygon)
  
  
def edit_point_release_MWM(event):
  global point1_x
  global point1_y
  global point2_x
  global point2_y
  global point3_x
  global point3_y
  global point4_x
  global point4_y
  global center_x
  global center_y
  
  center_x = event.x
  center_y = event.y
  
  point1_x = event.x + point1_x_diff
  point1_y = event.y + point1_y_diff
  
  point2_x = event.x + point2_x_diff
  point2_y = event.y + point2_y_diff

  point3_x = event.x + point3_x_diff
  point3_y = event.y + point3_y_diff
  
  point4_x = event.x + point4_x_diff
  point4_y = event.y + point4_y_diff

  sector_4x = point1_x + 20
  sector_4y = (point1_y + point2_y) / 2 + 30
  sector_3x = point3_x - 100
  sector_3y = (point2_y + point3_y) / 2 + 30
  sector_2x = point3_x - 100
  sector_2y = (point3_y + point4_y) / 2 - 40
  sector_1x = point1_x + 20
  sector_1y = (point4_y + point1_y) / 2 - 40
  
  sector4_lb.place(x=sector_4x, y=sector_4y)
  sector3_lb.place(x=sector_3x, y=sector_3y)
  sector2_lb.place(x=sector_2x, y=sector_2y)
  sector1_lb.place(x=sector_1x, y=sector_1y)
  
  done_release = True
  root.unbind("<B1-Motion>")
  root.unbind("<ButtonRelease-1>")
  
  
def edit_point_hold_rotate_MWM(event):
  global center_point
  global point1
  global point2
  global point3
  global point4
  global out_circle
  global cross1
  global cross2
  global platform_points
  global platform_polygon
  global point2_x
  global point2_y
  global point3_x
  global point3_y
  global point4_x
  global point4_y
  
  def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
  
  for e in will_be_deleted:
    canva.delete(e)
  
  newY_diff = center_y - event.y
  if newY_diff > R:
    newY_diff = R
  newX_diff = math.sqrt((R ** 2 - newY_diff ** 2))
  newX = center_x + newX_diff
  newY = center_y + newY_diff
  point1 = create_circle(newX, newY, 6, canva, delete=True)
  vector_1 = [point1_x_diff, point1_x_diff]
  vector_2 = [newX_diff, newY_diff]
  unit_vector_1 = vector_1 / np. linalg. norm(vector_1)
  unit_vector_2 = vector_2 / np. linalg. norm(vector_2)
  dot_product = np. dot(unit_vector_1, unit_vector_2)
  mwm_angle = np.rad2deg(np.arccos(dot_product))
  new_point2_x, new_point2_y = rotate((center_x, center_y), (point2_x, point2_y), mwm_angle)
  new_point3_x, new_point3_y = rotate((center_x, center_y), (point3_x, point3_y), mwm_angle)
  new_point4_x, new_point4_y = rotate((center_x, center_y), (point4_x, point4_y), mwm_angle)
  # change the points coordinates to new coordinates 
  point1 = create_circle(point1_x, point1_y, 6, canva, delete=True)
  point2 = create_circle(point2_x, point2_y, 6, canva, delete=True)
  point3 = create_circle(point3_x, point3_y, 6, canva, delete=True)
  point4 = create_circle(point4_x, point4_y, 6, canva, delete=True)
  
  
def draw_MWM(event):
  global MWM_click_count
  global text_label4
  global text_label5
  global center_x
  global center_y
  global xdiff
  global ydiff
  global R
  global point1_x
  global point1_y
  global point2_x
  global point2_y
  global point3_x
  global point3_y
  global point4_x
  global point4_y
  global point1_x_diff
  global point1_y_diff
  global point2_x_diff
  global point2_y_diff
  global point3_x_diff
  global point3_y_diff
  global point4_x_diff
  global point4_y_diff
  global center_point
  global point1
  global point2
  global point3
  global point4
  global out_circle
  global cross1
  global cross2
  global color
  global text_label_extra0
  global text_label_extra
  global pl_p1_dx
  global pl_p1_dy
  global pl_p2_dx
  global pl_p2_dy
  global pl_p3_dx
  global pl_p3_dy
  global pl_p4_dx
  global pl_p4_dy
  global sector1_lb
  global sector2_lb
  global sector3_lb
  global sector4_lb
  global center_circle
  global center_circle_r
  global platform_centerX
  global platform_centerY
  
  
  def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
  
  if MWM_click_count == 0: # Selecting center
    center_x = event.x
    center_y = event.y
    text_label3.destroy()
    text_label4 = Label(tab1, text="Select the radius of the maze")
    text_label4.config(font=("Courier", 30))
    text_label4.place(x=500, y=100)
    
    center_point = create_circle(event.x, event.y, 9, canva, delete=True)
  
  elif MWM_click_count == 1: # Selecting radius
    x_diff = abs(center_x - event.x)
    y_diff = abs(center_y - event.y)
    R = math.sqrt((x_diff ** 2 + y_diff ** 2))
    #print(R)
    out_circle = create_circle(center_x, center_y, R, canva, no_fill=True)
    center_circle_r = R * .7
    center_circle = create_circle(center_x, center_y, center_circle_r, canva, no_fill=True) # change_here
    text_label4.destroy()
    text_label5 = Label(tab1, text="Select the Corners of the Platform")
    text_label5.config(font=("Courier", 30))
    text_label5.place(x=450, y=100)
    
  elif MWM_click_count > 1 and MWM_click_count < 5:
    platform_points.append(event.x)
    platform_points.append(event.y)
    create_circle(event.x, event.y, 4, canva, delete=True)
    
  elif MWM_click_count == 5:
    platform_points.append(event.x)
    platform_points.append(event.y)
    create_circle(event.x, event.y, 4, canva, delete=True)
    
    platform_polygon = canva.create_polygon(platform_points, fill="", outline="blue", width=3)
    will_be_deleted.append(platform_polygon)
    color = "green"
    
    platform_centerX = (platform_points[0] + platform_points[2] + platform_points[4] + platform_points[6]) / 4
    platform_centerY = (platform_points[1] + platform_points[3] + platform_points[5] + platform_points[7]) / 4
    p_center_point = create_circle(platform_centerX, platform_centerY, 6, canva, delete=True)
    little_r = math.sqrt((platform_centerX - center_x) ** 2 + (platform_centerY - center_y) ** 2)
    r_ratio = R / little_r
    print("R Ratio is:", r_ratio)
    temp_x = center_x + (platform_centerX - center_x) * r_ratio
    temp_y = center_y + (platform_centerY - center_y) * r_ratio
    point1_x, point1_y = rotate((center_x, center_y), (temp_x, temp_y), math.pi/4)
    point2_x, point2_y = rotate((center_x, center_y), (point1_x, point1_y), math.pi/2)
    point3_x, point3_y = rotate((center_x, center_y), (point1_x, point1_y), math.pi)
    point4_x, point4_y = rotate((center_x, center_y), (point1_x, point1_y), math.pi * 3/2)
    point1 = create_circle(point1_x, point1_y, 6, canva, delete=True)
    point2 = create_circle(point2_x, point2_y, 6, canva, delete=True)
    point3 = create_circle(point3_x, point3_y, 6, canva, delete=True)
    point4 = create_circle(point4_x, point4_y, 6, canva, delete=True)
    cross1 = canva.create_line(point1_x, point1_y, point3_x, point3_y, width=4, fill="green")
    cross2 = canva.create_line(point2_x, point2_y, point4_x, point4_y, width=4, fill="green")
    will_be_deleted.append(cross1)
    will_be_deleted.append(cross2)
    
    text_label5.destroy()
    text_label_extra = Label(tab1, text="Continue or Edit")
    text_label_extra.config(font=("Courier", 30))
    text_label_extra.place(x=820, y=100)
    
    continue_button = Button(tab1, text="Continue", command=complete, width=14)
    continue_button["font"] = myFont
    continue_button.place(x=1620, y=900)
    root.unbind("<Button-1>")
    root.bind("<Button-1>", edit_point_click_MWM)
    
    point1_x_diff = point1_x - center_x
    point1_y_diff = point1_y - center_y
    point2_x_diff = point2_x - center_x
    point2_y_diff = point2_y - center_y
    point3_x_diff = point3_x - center_x
    point3_y_diff = point3_y - center_y
    point4_x_diff = point4_x - center_x
    point4_y_diff = point4_y - center_y
    
    pl_p1_dx = platform_points[0] - center_x
    pl_p1_dy = platform_points[1] - center_y
    pl_p2_dx = platform_points[2] - center_x
    pl_p2_dy = platform_points[3] - center_y
    pl_p3_dx = platform_points[4] - center_x
    pl_p3_dy = platform_points[5] - center_y
    pl_p4_dx = platform_points[6] - center_x
    pl_p4_dy = platform_points[7] - center_y
    
    sector_4x = point1_x + 20
    sector_4y = (point1_y + point2_y) / 2 + 30
    sector_3x = point3_x - 100
    sector_3y = (point2_y + point3_y) / 2 + 30
    sector_2x = point3_x - 100
    sector_2y = (point3_y + point4_y) / 2 - 40
    sector_1x = point1_x + 20
    sector_1y = (point4_y + point1_y) / 2 - 40
    
    sector4_lb = Label(canva, text="IV")
    sector4_lb.config(font=("Courier", 50))
    sector4_lb.place(x=sector_4x, y=sector_4y)
    
    sector3_lb = Label(canva, text="III")
    sector3_lb.config(font=("Courier", 50))
    sector3_lb.place(x=sector_3x, y=sector_3y)
    
    sector2_lb = Label(canva, text="II")
    sector2_lb.config(font=("Courier", 50))
    sector2_lb.place(x=sector_2x, y=sector_2y)
    
    sector1_lb = Label(canva, text="I")
    sector1_lb.config(font=("Courier", 50))
    sector1_lb.place(x=sector_1x, y=sector_1y)
      
  MWM_click_count += 1
    
  
def edit_point_click_TYM(event):
    global closest_point
    global point_index
    global arm_is
    
    total_points = first_arm_points_shapely + right_arm_points_shapely + left_arm_points_shapely
    
    closest_point = total_points[0]
    smallest_distance = 1000000000
    for point in total_points:
      xDiff = (event.x - point[0]) ** 2
      yDiff = (event.y - point[1]) ** 2
      distance = (xDiff + yDiff) ** 1/2
      if distance < smallest_distance:
        smallest_distance = distance
        closest_point = point
        
    point_index = total_points.index(closest_point)
    
    if point_index > 7:
      arm_is = "l"
      point_index -= 8
    elif point_index > 3:
      arm_is = "r"
      point_index -= 4
    elif point_index >= 0:
      arm_is = "1"
      
    root.bind("<B1-Motion>", edit_point_hold_TYM)
    root.bind("<ButtonRelease-1>", edit_point_release_TYM)
    print(closest_point)
    canva.delete(will_be_edited[closest_point])
    
def edit_point_hold_TYM(event):
    global closest_point
    global canva
    global first_arm_polygon
    global right_arm_polygon
    global left_arm_polygon
    
    for e in delete_all:
        canva.delete(e)
        
    new = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
    delete_all.append(new)
    
    ex_x_index = point_index * 2
    ex_y_index = point_index * 2 + 1
    
    if arm_is == "1":
      first_arm_points.insert(ex_x_index, event.x)
      first_arm_points.pop(ex_x_index + 1)
      first_arm_points.insert(ex_y_index, event.y)
      first_arm_points.pop(ex_y_index + 1)
      
      canva.delete(first_arm_polygon)
      first_arm_polygon = canva.create_polygon(first_arm_points, fill="", outline="green", width=3)
      
    elif arm_is == "r":
      right_arm_points.insert(ex_x_index, event.x)
      right_arm_points.pop(ex_x_index + 1)
      right_arm_points.insert(ex_y_index, event.y)
      right_arm_points.pop(ex_y_index + 1)
      
      canva.delete(right_arm_polygon)
      right_arm_polygon = canva.create_polygon(right_arm_points, fill="", outline="green", width=3)
      
    elif arm_is == "l":
      left_arm_points.insert(ex_x_index, event.x)
      left_arm_points.pop(ex_x_index + 1)
      left_arm_points.insert(ex_y_index, event.y)
      left_arm_points.pop(ex_y_index + 1)
      
      canva.delete(left_arm_polygon)
      left_arm_polygon = canva.create_polygon(left_arm_points, fill="", outline="green", width=3)
      
     
def edit_point_release_TYM(event):
    if event.x > 100 and event.y > 100: # ignore error
      will_be_edited[(event.x, event.y)] = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
    
    if arm_is == "1":
      first_arm_points_shapely.clear()
      n = 0
      while n + 1 < len(first_arm_points):
        first_arm_points_shapely.append((first_arm_points[n], first_arm_points[n + 1]))
        n+=2
    
    elif arm_is == "r":
      right_arm_points_shapely.clear()
      n = 0
      while n + 1 < len(right_arm_points):
        right_arm_points_shapely.append((right_arm_points[n], right_arm_points[n + 1]))
        n+=2
          
    elif arm_is == "l":
      left_arm_points_shapely.clear()
      n = 0
      while n + 1 < len(left_arm_points):
        left_arm_points_shapely.append((left_arm_points[n], left_arm_points[n + 1]))
        n+=2
    
def draw_TYM(event):
  global TYM_click_count
  global text_label4
  global text_label5
  global text_label_extra
  global first_arm_polygon
  global right_arm_polygon
  global left_arm_polygon
  
  create_circle(event.x, event.y, 6, canva, edit=True)
  if TYM_click_count < 3:
    first_arm_points.append(event.x)
    first_arm_points.append(event.y)
    first_arm_points_shapely.append((event.x, event.y))
    
  elif TYM_click_count == 3:
    first_arm_points.append(event.x)
    first_arm_points.append(event.y)
    first_arm_points_shapely.append((event.x, event.y))
    first_arm_polygon = canva.create_polygon(first_arm_points, fill="", outline="green", width=3)
    text_label3.destroy()
    text_label4 = Label(tab1, text="Select the corners of the right arm")
    text_label4.config(font=("Courier", 30))
    text_label4.place(x=500, y=100)
    polygons.append(Polygon(first_arm_points_shapely))
    
  elif TYM_click_count < 7:
    right_arm_points.append(event.x)
    right_arm_points.append(event.y)
    right_arm_points_shapely.append((event.x, event.y))
    
  elif TYM_click_count == 7:
    right_arm_points.append(event.x)
    right_arm_points.append(event.y)
    right_arm_points_shapely.append((event.x, event.y))
    polygons.append(Polygon(right_arm_points_shapely))
    right_arm_polygon = canva.create_polygon(right_arm_points, fill="", outline="green", width=3)
    text_label4.destroy()
    text_label5 = Label(tab1, text="Select the corners of the left arm")
    text_label5.config(font=("Courier", 30))
    text_label5.place(x=500, y=100)
    
  elif TYM_click_count < 11:
    left_arm_points.append(event.x)
    left_arm_points.append(event.y)
    left_arm_points_shapely.append((event.x, event.y))
    
  elif TYM_click_count == 11:
    left_arm_points.append(event.x)
    left_arm_points.append(event.y)
    left_arm_points_shapely.append((event.x, event.y))
    polygons.append(Polygon(left_arm_points_shapely))
    left_arm_polygon = canva.create_polygon(left_arm_points, fill="", outline="green", width=3)
    text_label5.destroy()
    text_label_extra = Label(tab1, text="Continue")
    text_label_extra.config(font=("Courier", 30))
    text_label_extra.place(x=820, y=100)
    
    continue_button = Button(tab1, text="Continue", command=complete, width=14)
    continue_button["font"] = myFont
    continue_button.place(x=1620, y=900)
    root.unbind("<Button-1>")
    root.bind("<Button-1>", edit_point_click_TYM)
    
  TYM_click_count += 1
    
  
def edit_point_click_RAM(event):
  global closest_point
  global point_index
  global arm_is
  global total_points
  
  total_points = arm1_points_shapely + arm2_points_shapely + arm3_points_shapely + arm4_points_shapely \
    + arm5_points_shapely + arm6_points_shapely + arm7_points_shapely + arm8_points_shapely
      
  closest_point = total_points[0]
  smallest_distance = 1000000000
  for point in total_points:
    xDiff = (event.x - point[0]) ** 2
    yDiff = (event.y - point[1]) ** 2
    distance = (xDiff + yDiff) ** 1/2
    if distance < smallest_distance:
      smallest_distance = distance
      closest_point = point
      
  point_index = total_points.index(closest_point)
  
  if point_index > 27:
    arm_is = "8"
    point_index -= 28
  elif point_index > 23:
    arm_is = "7"
    point_index -= 24
  elif point_index > 19:
    arm_is = "6"
    point_index -= 20
  elif point_index > 15:
    arm_is = "5"
    point_index -= 16
  elif point_index > 11:
    arm_is = "4"
    point_index -= 12
  elif point_index > 7:
    arm_is = "3"
    point_index -= 8
  elif point_index > 3:
    arm_is = "2"
    point_index -= 4
  elif point_index >= 0:
    arm_is = "1"
    
  root.bind("<B1-Motion>", edit_point_hold_RAM)
  root.bind("<ButtonRelease-1>", edit_point_release_RAM)
  print(closest_point)
  canva.delete(will_be_edited[closest_point])
      
  
def edit_point_hold_RAM(event):
  global closest_point
  global canva
  global arm1
  global arm2
  global arm3
  global arm4
  global arm5
  global arm6
  global arm7
  global arm8
  
  for e in delete_all:
    canva.delete(e)
    
  new = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
  delete_all.append(new)
  
  ex_x_index = point_index * 2
  ex_y_index = point_index * 2 + 1
  
  if arm_is == "1":
    arm1_points.insert(ex_x_index, event.x)
    arm1_points.pop(ex_x_index + 1)
    arm1_points.insert(ex_y_index, event.y)
    arm1_points.pop(ex_y_index + 1)
    
    canva.delete(arm1)
    arm1 = canva.create_polygon(arm1_points, fill="", outline="green", width=3)
    
  elif arm_is == "2":
    arm2_points.insert(ex_x_index, event.x)
    arm2_points.pop(ex_x_index + 1)
    arm2_points.insert(ex_y_index, event.y)
    arm2_points.pop(ex_y_index + 1)
    
    canva.delete(arm2)
    arm2 = canva.create_polygon(arm2_points, fill="", outline="green", width=3)
    
  elif arm_is == "3":
    arm3_points.insert(ex_x_index, event.x)
    arm3_points.pop(ex_x_index + 1)
    arm3_points.insert(ex_y_index, event.y)
    arm3_points.pop(ex_y_index + 1)
    
    canva.delete(arm3)
    arm3 = canva.create_polygon(arm3_points, fill="", outline="green", width=3)
    
  elif arm_is == "4":
    arm4_points.insert(ex_x_index, event.x)
    arm4_points.pop(ex_x_index + 1)
    arm4_points.insert(ex_y_index, event.y)
    arm4_points.pop(ex_y_index + 1)
    
    canva.delete(arm4)
    arm4 = canva.create_polygon(arm4_points, fill="", outline="green", width=3)
    
  elif arm_is == "5":
    arm5_points.insert(ex_x_index, event.x)
    arm5_points.pop(ex_x_index + 1)
    arm5_points.insert(ex_y_index, event.y)
    arm5_points.pop(ex_y_index + 1)
    
    canva.delete(arm5)
    arm5 = canva.create_polygon(arm5_points, fill="", outline="green", width=3)
    
  elif arm_is == "6":
    arm6_points.insert(ex_x_index, event.x)
    arm6_points.pop(ex_x_index + 1)
    arm6_points.insert(ex_y_index, event.y)
    arm6_points.pop(ex_y_index + 1)
    
    canva.delete(arm6)
    arm6 = canva.create_polygon(arm6_points, fill="", outline="green", width=3)
    
  elif arm_is == "7":
    arm7_points.insert(ex_x_index, event.x)
    arm7_points.pop(ex_x_index + 1)
    arm7_points.insert(ex_y_index, event.y)
    arm7_points.pop(ex_y_index + 1)
    
    canva.delete(arm7)
    arm7 = canva.create_polygon(arm7_points, fill="", outline="green", width=3)
    
  elif arm_is == "8":
    arm8_points.insert(ex_x_index, event.x)
    arm8_points.pop(ex_x_index + 1)
    arm8_points.insert(ex_y_index, event.y)
    arm8_points.pop(ex_y_index + 1)
    
    canva.delete(arm8)
    arm8 = canva.create_polygon(arm8_points, fill="", outline="green", width=3)
    
  
def edit_point_release_RAM(event):
  if event.x > 100 and event.y > 100: # ignore error
    will_be_edited[(event.x, event.y)] = canva.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="green", outline="green")
  
  if arm_is == "1":
    arm1_points_shapely.clear()
    n = 0
    while n + 1 < len(arm1_points):
      arm1_points_shapely.append((arm1_points[n], arm1_points[n + 1]))
      n+=2
  
  elif arm_is == "2":
    arm2_points_shapely.clear()
    n = 0
    while n + 1 < len(arm2_points):
      arm2_points_shapely.append((arm2_points[n], arm2_points[n + 1]))
      n+=2
        
  elif arm_is == "3":
    arm3_points_shapely.clear()
    n = 0
    while n + 1 < len(arm3_points):
      arm3_points_shapely.append((arm3_points[n], arm3_points[n + 1]))
      n+=2
  
  elif arm_is == "4":
    arm4_points_shapely.clear()
    n = 0
    while n + 1 < len(arm4_points):
      arm4_points_shapely.append((arm4_points[n], arm4_points[n + 1]))
      n+=2
        
  elif arm_is == "5":
    arm5_points_shapely.clear()
    n = 0
    while n + 1 < len(arm5_points):
      arm5_points_shapely.append((arm5_points[n], arm5_points[n + 1]))
      n+=2
        
  elif arm_is == "6":
    arm6_points_shapely.clear()
    n = 0
    while n + 1 < len(arm6_points):
      arm6_points_shapely.append((arm6_points[n], arm6_points[n + 1]))
      n+=2
        
  elif arm_is == "7":
    arm7_points_shapely.clear()
    n = 0
    while n + 1 < len(arm7_points):
      arm7_points_shapely.append((arm7_points[n], arm7_points[n + 1]))
      n+=2
        
  elif arm_is == "8":
    arm8_points_shapely.clear()
    n = 0
    while n + 1 < len(arm8_points):
      arm8_points_shapely.append((arm8_points[n], arm8_points[n + 1]))
      n+=2
        
  
def draw_RAM(event):
  global RAM_click_count
  global text_label4
  global text_label5
  global center_x
  global center_y
  global arm2_points_shapely
  global arm3_points_shapely
  global arm4_points_shapely
  global arm5_points_shapely
  global arm6_points_shapely
  global arm7_points_shapely
  global arm8_points_shapely
  global arm1
  global arm2
  global arm3
  global arm4
  global arm5
  global arm6
  global arm7
  global arm8
  global center
  global arm2_points
  global arm3_points
  global arm4_points
  global arm5_points
  global arm6_points
  global arm7_points
  global arm8_points
  
  def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
  
  if RAM_click_count == 0:
    center = create_circle(event.x, event.y, 9, canva)
    center_x = event.x
    center_y = event.y
    text_label3.destroy()
    text_label4 = Label(tab1, text="Select the Corners of the Top Arm")
    text_label4.config(font=("Courier", 30))
    text_label4.place(x=500, y=100)
  
  elif RAM_click_count < 4:
    create_circle(event.x, event.y, 6, canva, edit=True)
    arm1_points.append(event.x)
    arm1_points.append(event.y)
    arm1_points_shapely.append((event.x, event.y))
  
  elif RAM_click_count == 4:
    create_circle(event.x, event.y, 6, canva, edit=True)
    canva.delete(center)
    arm1_points.append(event.x)
    arm1_points.append(event.y)
    arm1_points_shapely.append((event.x, event.y))
    arm1 = canva.create_polygon(arm1_points, fill="", outline="green", width=3)
    
    arm2_point1 = rotate((center_x, center_y), (arm1_points[0], arm1_points[1]), math.pi/4)
    arm2_point2 = rotate((center_x, center_y), (arm1_points[2], arm1_points[3]), math.pi/4)
    arm2_point3 = rotate((center_x, center_y), (arm1_points[4], arm1_points[5]), math.pi/4)
    arm2_point4 = rotate((center_x, center_y), (arm1_points[6], arm1_points[7]), math.pi/4)
    arm2_points = [arm2_point1[0], arm2_point1[1], arm2_point2[0], arm2_point2[1], arm2_point3[0], arm2_point3[1], arm2_point4[0], arm2_point4[1]]
    arm2_points_shapely = [arm2_point1, arm2_point2, arm2_point3, arm2_point4]
    arm2 = canva.create_polygon(arm2_points_shapely, fill="", outline="green", width=3)
    
    create_circle(arm2_point1[0], arm2_point1[1], 6, canva, edit=True)
    create_circle(arm2_point2[0], arm2_point2[1], 6, canva, edit=True)
    create_circle(arm2_point3[0], arm2_point3[1], 6, canva, edit=True)
    create_circle(arm2_point4[0], arm2_point4[1], 6, canva, edit=True)
    
    arm3_point1 = rotate((center_x, center_y), (arm1_points[0], arm1_points[1]), math.pi/2)
    arm3_point2 = rotate((center_x, center_y), (arm1_points[2], arm1_points[3]), math.pi/2)
    arm3_point3 = rotate((center_x, center_y), (arm1_points[4], arm1_points[5]), math.pi/2)
    arm3_point4 = rotate((center_x, center_y), (arm1_points[6], arm1_points[7]), math.pi/2)
    arm3_points = [arm3_point1[0], arm3_point1[1], arm3_point2[0], arm3_point2[1], arm3_point3[0], arm3_point3[1], arm3_point4[0], arm3_point4[1]]
    arm3_points_shapely = [arm3_point1, arm3_point2, arm3_point3, arm3_point4]
    arm3 = canva.create_polygon(arm3_points_shapely, fill="", outline="green", width=3)
    
    create_circle(arm3_point1[0], arm3_point1[1], 6, canva, edit=True)
    create_circle(arm3_point2[0], arm3_point2[1], 6, canva, edit=True)
    create_circle(arm3_point3[0], arm3_point3[1], 6, canva, edit=True)
    create_circle(arm3_point4[0], arm3_point4[1], 6, canva, edit=True)
    
    arm4_point1 = rotate((center_x, center_y), (arm1_points[0], arm1_points[1]), math.pi * 3/4)
    arm4_point2 = rotate((center_x, center_y), (arm1_points[2], arm1_points[3]), math.pi * 3/4)
    arm4_point3 = rotate((center_x, center_y), (arm1_points[4], arm1_points[5]), math.pi * 3/4)
    arm4_point4 = rotate((center_x, center_y), (arm1_points[6], arm1_points[7]), math.pi * 3/4)
    arm4_points = [arm4_point1[0], arm4_point1[1], arm4_point2[0], arm4_point2[1], arm4_point3[0], arm4_point3[1], arm4_point4[0], arm4_point4[1]]
    arm4_points_shapely = [arm4_point1, arm4_point2, arm4_point3, arm4_point4]
    arm4 = canva.create_polygon(arm4_points_shapely, fill="", outline="green", width=3)
    
    create_circle(arm4_point1[0], arm4_point1[1], 6, canva, edit=True)
    create_circle(arm4_point2[0], arm4_point2[1], 6, canva, edit=True)
    create_circle(arm4_point3[0], arm4_point3[1], 6, canva, edit=True)
    create_circle(arm4_point4[0], arm4_point4[1], 6, canva, edit=True)
    
    arm5_point1 = rotate((center_x, center_y), (arm1_points[0], arm1_points[1]), math.pi)
    arm5_point2 = rotate((center_x, center_y), (arm1_points[2], arm1_points[3]), math.pi)
    arm5_point3 = rotate((center_x, center_y), (arm1_points[4], arm1_points[5]), math.pi)
    arm5_point4 = rotate((center_x, center_y), (arm1_points[6], arm1_points[7]), math.pi)
    arm5_points = [arm5_point1[0], arm5_point1[1], arm5_point2[0], arm5_point2[1], arm5_point3[0], arm5_point3[1], arm5_point4[0], arm5_point4[1]]
    arm5_points_shapely = [arm5_point1, arm5_point2, arm5_point3, arm5_point4]
    arm5 = canva.create_polygon(arm5_points_shapely, fill="", outline="green", width=3)
    
    create_circle(arm5_point1[0], arm5_point1[1], 6, canva, edit=True)
    create_circle(arm5_point2[0], arm5_point2[1], 6, canva, edit=True)
    create_circle(arm5_point3[0], arm5_point3[1], 6, canva, edit=True)
    create_circle(arm5_point4[0], arm5_point4[1], 6, canva, edit=True)
    
    arm6_point1 = rotate((center_x, center_y), (arm1_points[0], arm1_points[1]), math.pi + math.pi/4)
    arm6_point2 = rotate((center_x, center_y), (arm1_points[2], arm1_points[3]), math.pi + math.pi/4)
    arm6_point3 = rotate((center_x, center_y), (arm1_points[4], arm1_points[5]), math.pi + math.pi/4)
    arm6_point4 = rotate((center_x, center_y), (arm1_points[6], arm1_points[7]), math.pi + math.pi/4)
    arm6_points = [arm6_point1[0], arm6_point1[1], arm6_point2[0], arm6_point2[1], arm6_point3[0], arm6_point3[1], arm6_point4[0], arm6_point4[1]]
    arm6_points_shapely = [arm6_point1, arm6_point2, arm6_point3, arm6_point4]
    arm6 = canva.create_polygon(arm6_points_shapely, fill="", outline="green", width=3)
    
    create_circle(arm6_point1[0], arm6_point1[1], 6, canva, edit=True)
    create_circle(arm6_point2[0], arm6_point2[1], 6, canva, edit=True)
    create_circle(arm6_point3[0], arm6_point3[1], 6, canva, edit=True)
    create_circle(arm6_point4[0], arm6_point4[1], 6, canva, edit=True)
    
    arm7_point1 = rotate((center_x, center_y), (arm1_points[0], arm1_points[1]), math.pi + math.pi/2)
    arm7_point2 = rotate((center_x, center_y), (arm1_points[2], arm1_points[3]), math.pi + math.pi/2)
    arm7_point3 = rotate((center_x, center_y), (arm1_points[4], arm1_points[5]), math.pi + math.pi/2)
    arm7_point4 = rotate((center_x, center_y), (arm1_points[6], arm1_points[7]), math.pi + math.pi/2)
    arm7_points = [arm7_point1[0], arm7_point1[1], arm7_point2[0], arm7_point2[1], arm7_point3[0], arm7_point3[1], arm7_point4[0], arm7_point4[1]]
    arm7_points_shapely = [arm7_point1, arm7_point2, arm7_point3, arm7_point4]
    arm7 = canva.create_polygon(arm7_points_shapely, fill="", outline="green", width=3)
    
    create_circle(arm7_point1[0], arm7_point1[1], 6, canva, edit=True)
    create_circle(arm7_point2[0], arm7_point2[1], 6, canva, edit=True)
    create_circle(arm7_point3[0], arm7_point3[1], 6, canva, edit=True)
    create_circle(arm7_point4[0], arm7_point4[1], 6, canva, edit=True)
    
    arm8_point1 = rotate((center_x, center_y), (arm1_points[0], arm1_points[1]), math.pi + math.pi * 3/4)
    arm8_point2 = rotate((center_x, center_y), (arm1_points[2], arm1_points[3]), math.pi + math.pi * 3/4)
    arm8_point3 = rotate((center_x, center_y), (arm1_points[4], arm1_points[5]), math.pi + math.pi * 3/4)
    arm8_point4 = rotate((center_x, center_y), (arm1_points[6], arm1_points[7]), math.pi + math.pi * 3/4)
    arm8_points = [arm8_point1[0], arm8_point1[1], arm8_point2[0], arm8_point2[1], arm8_point3[0], arm8_point3[1], arm8_point4[0], arm8_point4[1]]
    arm8_points_shapely = [arm8_point1, arm8_point2, arm8_point3, arm8_point4]
    arm8 = canva.create_polygon(arm8_points_shapely, fill="", outline="green", width=3)
    
    create_circle(arm8_point1[0], arm8_point1[1], 6, canva, edit=True)
    create_circle(arm8_point2[0], arm8_point2[1], 6, canva, edit=True)
    create_circle(arm8_point3[0], arm8_point3[1], 6, canva, edit=True)
    create_circle(arm8_point4[0], arm8_point4[1], 6, canva, edit=True)
    
    continue_button = Button(tab1, text="Continue", command=complete, width=14)
    continue_button["font"] = myFont
    continue_button.place(x=1620, y=900)
    
    root.unbind("<Button-1>")
    root.bind("<Button-1>", edit_point_click_RAM)
    
  RAM_click_count += 1
  


def EPM():
  global EPM_click_count
  global open_arm_points
  global closed_arm_points
  global open_arm_points_shapely
  global closed_arm_points_shapely
  global text_label3
  global experiment
  global open_arm_speeds
  global closed_arm_speeds
  global center_speeds
  global open_arm1_list
  global open_arm2_list
  global closed_arm1_list
  global closed_arm2_list
  global center_list
  # global openCloseCross
  # global closeOpenCross
  
  
  """First Variables"""
  EPM_click_count = 0
  experiment = "EPM"
  
  """Destroy buttons, Replace labels"""
  EPM_bt.destroy()
  OFT_bt.destroy()
  MWM_bt.destroy()
  TYM_bt.destroy()
  FST_bt.destroy()
  FH_bt.destroy()
  RAM_bt.destroy()
  text_label2.destroy()
  text_label3 = Label(tab1, text="Select the corners of the open arm")
  text_label3.config(font=("Courier", 30))
  text_label3.place(x=500, y=100)
  
  """Initialize Variables"""
  open_arm_points = []
  open_arm_points_shapely = []
  closed_arm_points = []
  closed_arm_points_shapely = []
  open_arm_speeds = []
  closed_arm_speeds = []
  center_speeds = []
  open_arm1_list = []
  open_arm2_list = []
  closed_arm1_list = []
  closed_arm2_list = []
  center_list = []
  # openCloseCross = 0
  # closeOpenCross = 0
  
  """Binding"""
  root.bind("<Button-1>", draw_EPM)
  

def OFT():
  global OFT_click_count
  global outer_box_points
  global inside_box_points
  global outer_box_points_shapely
  global inside_box_points_shapely
  global text_label23
  global experiment
  global outer_box_speeds
  global inside_box_speeds
  global ratio_cont_bt
  global e_OFT
  
  """First Variables"""
  OFT_click_count = 0
  experiment = "OFT"
  
  """Destroy buttons, Replace labels"""
  EPM_bt.destroy()
  OFT_bt.destroy()
  MWM_bt.destroy()
  TYM_bt.destroy()
  FST_bt.destroy()
  FH_bt.destroy()
  RAM_bt.destroy()
  text_label2.destroy()
  text_label23 = Label(tab1, text="Enter the inner outer box ratio (default is 0.25)")
  text_label23.config(font=("Courier", 30))
  text_label23.place(x=230, y=100)
  
  """Initialize Variables"""
  outer_box_points = []
  outer_box_points_shapely = []
  inside_box_points = []
  inside_box_points_shapely = []
  outer_box_speeds = []
  inside_box_speeds = []
  
  """Getting the Ratio"""  
  e_OFT = Entry(tab1)
  e_OFT.config(font=("Courier", 20), width=9)
  e_OFT.place(x=1620, y=800)
  
  ratio_cont_bt = Button(tab1, text="Continue", command=set_OFT_ratio, width=14, height=3)
  ratio_cont_bt["font"] = myFont
  ratio_cont_bt.place(x=1620, y=850)

    
def MWM():
  global MWM_click_count
  global R
  global platform_points
  global text_label3
  global experiment
  
  """First Variables"""
  MWM_click_count = 0
  experiment = "MWM"
  
  """Destroy buttons, Replace labels"""
  EPM_bt.destroy()
  OFT_bt.destroy()
  MWM_bt.destroy()
  TYM_bt.destroy()
  FST_bt.destroy()
  FH_bt.destroy()
  RAM_bt.destroy()
  text_label2.destroy()
  text_label3 = Label(tab1, text="Select the center of the maze")
  text_label3.config(font=("Courier", 30))
  text_label3.place(x=500, y=100)
  
  """Initialize Variables"""
  platform_points = []
  
  """Binding"""
  root.bind("<Button-1>", draw_MWM)
 

def TYM():
  global TYM_click_count
  global first_arm_points
  global right_arm_points
  global left_arm_points
  global first_arm_points_shapely
  global right_arm_points_shapely
  global left_arm_points_shapely
  global text_label3
  global experiment
  global first_arm_speeds
  global right_arm_speeds
  global left_arm_speeds
  
  """First Variables"""
  TYM_click_count = 0
  experiment = "TYM"
  
  """Destroy buttons, Replace Labels"""
  EPM_bt.destroy()
  OFT_bt.destroy()
  MWM_bt.destroy()
  TYM_bt.destroy()
  FST_bt.destroy()
  FH_bt.destroy()
  RAM_bt.destroy()
  text_label2.destroy()
  text_label3 = Label(tab1, text="Select the corners of the first arm")
  text_label3.config(font=("Courier", 30))
  text_label3.place(x=500, y=100)
  
  """Initialize Variables"""
  first_arm_points = []
  right_arm_points = []
  left_arm_points = []
  first_arm_points_shapely = []
  right_arm_points_shapely = []
  left_arm_points_shapely = []
  first_arm_speeds = []
  right_arm_speeds = []
  left_arm_speeds = []
  
  """Binding"""
  root.bind("<Button-1>", draw_TYM)
  
  
def RAM():
  global RAM_click_count
  global arm1_points
  global arm1_points_shapely
  global text_label3
  global experiment
  
  """First Variables"""
  RAM_click_count = 0
  experiment = "RAM"
  
  """Destroy buttons, Replace Labels"""
  EPM_bt.destroy()
  OFT_bt.destroy()
  MWM_bt.destroy()
  TYM_bt.destroy()
  FST_bt.destroy()
  FH_bt.destroy()
  RAM_bt.destroy()
  text_label2.destroy()
  text_label3 = Label(tab1, text="Select the Center")
  text_label3.config(font=("Courier", 30))
  text_label3.place(x=750, y=100)
  
  """Initialize Variables"""
  arm1_points = []
  arm1_points_shapely = []
  
  """Binding"""
  root.bind("<Button-1>", draw_RAM)
  
  
def assign_ratio():
  global text_label_2
  global ratio
  global from_entry
  global from_label
  global to_entry
  global to_label
  global done_bt
  
  cm = int(e.get())
  lp1_x, lp1_y = point_list_line[0], point_list_line[1]
  lp2_x, lp2_y = point_list_line[2], point_list_line[3]
  
  lx_diff = abs(lp1_x - lp2_x)
  ly_diff = abs(lp1_y - lp2_y)
  
  pixel_distance = math.sqrt((lx_diff ** 2 + ly_diff ** 2))
  
  ratio = cm / pixel_distance
  
  print(ratio)

  """Delete shape, replace text"""
  for event in will_be_deleted:
    canva.delete(event)
  canva.delete(l)
  e.destroy()
  b.destroy()
  text_label1.destroy()
  text_label_2 = Label(tab1, text="Please Select the Time Interval (format: 0.00)")
  text_label_2.config(font=("Courier", 30))
  text_label_2.place(x=440, y=100)
  
  """Creating time input boxes"""
  from_entry = Entry(tab1, width=8)
  from_entry.config(font=("Courier", 20))
  from_entry.place(x=1620, y=700)
  
  from_label = Label(tab1, text="From:")
  from_label.config(font=("Courier", 20))
  from_label.place(x=1527, y=700)
  
  to_entry = Entry(tab1, width=8)
  to_entry.config(font=("Courier", 20))
  to_entry.place(x=1620, y=740)
  
  to_label = Label(tab1, text="To:")
  to_label.config(font=("Courier", 20))
  to_label.place(x=1560, y=740)
  
  done_bt = Button(tab1, text="Done", command=set_time, height=2, width=8)
  done_bt["font"] = myFont
  done_bt.place(x=1760, y = 710)
  
  
def set_time():
  global EPM_bt
  global OFT_bt
  global MWM_bt
  global TYM_bt
  global FST_bt
  global FH_bt
  global experiment
  global from_frame
  global to_frame
  global text_label2
  global from_sec
  global to_sec
  global RAM_bt
  
  """Assigning Variables"""
  experiment = "nothing"
  
  if float(from_entry.get()) < 0:
    from_sec = 0
  else:
    from_sec = float(from_entry.get())
  
  if float(to_entry.get()) > duration:
    to_sec = int(duration)
  else:
    to_sec = float(to_entry.get())  
  
  from_frame = int(from_sec * FPS)
  to_frame = int(to_sec * FPS)
  
  """Deleting Old Buttons"""
  from_entry.destroy()
  from_label.destroy()
  
  to_entry.destroy()
  to_label.destroy()
  done_bt.destroy()
  
  """Replacing the Old Text"""
  text_label_2.destroy()
  text_label2 = Label(tab1, text="Now you can choose the experiment")
  text_label2.config(font=("Courier", 30))
  text_label2.place(x=500, y=100)
  
  """Creating Buttons"""
  # EPM Button
  EPM_bt = Button(tab1, text="EPM", command=EPM, width=14)
  EPM_bt["font"] = myFont
  EPM_bt.place(x=1620, y=200)
  
  # OFT Button
  OFT_bt = Button(tab1, text="OFT", command=OFT, width=14)
  OFT_bt["font"] = myFont
  OFT_bt.place(x=1620, y=240)
  
  # MWM Button
  MWM_bt = Button(tab1, text="MWM", command=MWM, width=14)
  MWM_bt["font"] = myFont
  MWM_bt.place(x=1620, y=280)
  
  # T-Maze, Y-Maze Button
  TYM_bt = Button(tab1, text="T-maze, Y-maze", command=TYM, width=14)
  TYM_bt["font"] = myFont
  TYM_bt.place(x=1620, y=320)
  
  # RAM
  RAM_bt = Button(tab1, text="RAM",command=RAM, width=14)
  RAM_bt["font"] = myFont
  RAM_bt.place(x=1620, y=360)
  
  # FST
  FST_bt = Button(tab1, text="FST", width=14)
  FST_bt["font"] = myFont
  FST_bt.place(x=1620, y=400)
  
  # Free-hand
  FH_bt = Button(tab1, text="Free-hand", command=FH, width=14)
  FH_bt["font"] = myFont
  FH_bt.place(x=1620, y=440)


def set_time_2():
  global from_frame
  global to_frame
    
  from_sec = float(from_entry.get())
  from_frame = int(from_sec * FPS)
  
  to_sec = float(to_entry.get())  
  to_frame = int(to_sec * FPS)
  
  tabControl.select(1)
  

def draw_line(event):
  global click2
  global color
  global point_list_line
  global e
  global b
  global l
  global text_label1
  
  color= "green"
  
  print(event.x, event.y)
  point_list_line.append(event.x)
  point_list_line.append(event.y)
  create_circle(event.x, event.y, 8, canva, delete=True)
  click2 += 1
  
  if click2 == 2:
    l = canva.create_line(point_list_line)
    root.unbind("<Button-1>")
    text_label.destroy()
    text_label1 = Label(tab1, text="How long is the line (in cm)")
    text_label1.config(font=("Courier", 30))
    text_label1.place(x=520, y=100)
    
    e = Entry(canva)
    e.place(x = point_list_line[2] + 20, y= (point_list_line[-1] + point_list_line[1]) / 2)
    b = Button(canva, text="Done", command=assign_ratio)
    b.place(x = point_list_line[2] + 20, y = ((point_list_line[-1] + point_list_line[1]) / 2) + 40)
    
    # while True():
    #     if keyboard.ispressed("enter"):
    #         break
        

  
  

def create_circle(x, y, r, canvasName, delete=False, no_fill=False, edit=False): #center coordinates, radius
  global will_be_edited
  
  x0 = x - r
  y0 = y - r
  x1 = x + r
  y1 = y + r
  
  if edit == True:
    a = canvasName.create_oval(x0, y0, x1, y1, fill=color, outline=color)
    will_be_edited[(x, y)] = a
    #print("nice")
    return a
  
  elif no_fill == True:
    a = canvasName.create_oval(x0, y0, x1, y1, fill="", outline=color, width = 4)
    will_be_deleted.append(a)
    return a
  
  elif delete == False:
   return canvasName.create_oval(x0, y0, x1, y1, fill=color, outline=color)
  else:
   a = canvasName.create_oval(x0, y0, x1, y1, fill=color, outline=color)
   will_be_deleted.append(a)
   
  
  
def FH():
  global experiment
  
  experiment = "Free Draw"
    
  """Destroy buttons, Replace labels"""
  EPM_bt.destroy()
  OFT_bt.destroy()
  MWM_bt.destroy()
  TYM_bt.destroy()
  FST_bt.destroy()
  FH_bt.destroy()
  RAM_bt.destroy()
  text_label2.destroy()
  text_label3 = Label(tab1, text="Select the corners of polygon(s)")
  text_label3.config(font=("Courier", 30))
  text_label3.place(x=500, y=100)
  
  continue_button = Button(tab1, text="Continue", command=complete, width=14)
  continue_button["font"] = myFont
  continue_button.place(x=1620, y=900)
  
  """Initialize Variables"""
  
  """Binding"""
  root.bind("<Button-1>", free_draw)

def free_draw(event):
  global click_count
  global shape_done
  global shape_count
  global color
  global point_list
  
  moe = 8
  
  if shape_count == 0:
    color = "green"
  elif shape_count == 1:
    color = "red"
  elif shape_count == 2:
    color = "blue"
  else:
    color = "yellow"
  
  if any(((event.x <= x + moe) and (event.x >= x - moe)) and ((event.y <= y + moe) and (event.y >= y - moe)) for x, y in polygon_coordinates.values()):
    #print(shape_count)
    shape_done = True
  
  elif shape_done == False:
    click_count += 1
    polygon_coordinates["Point: " + str(click_count)] = [event.x, event.y]
    create_circle(event.x, event.y, 8, canva)
    
  if shape_done:
    points = []
    for lst in polygon_coordinates.values():
      points.append(lst[0])
      points.append(lst[1])
    
    
    canva.create_polygon(points, fill="", outline=color, width=3)
    shape_done = False
    shape_count += 1
    
    globals()["Polygon " + str(shape_count) + " Coordinates"] = polygon_coordinates.copy()
    point_list = []
    for x, y in polygon_coordinates.copy().values():
      point_list.append((x, y))
    #print(point_list)
    
    polygons.append(Polygon(point_list))
    polygon_coordinates.clear()
    
    
def analyze0():
    global yes1_bt
    global no1_bt
    global tempConf_lb
    global mwm_config_bt
    
    yes_bt.destroy()
    no_bt.destroy()
    find_keypoints_lb.destroy()
    
    tempConf_lb = Label(tab1, text="Choose Config File")
    tempConf_lb.config(font=("Courier", 30))
    tempConf_lb.place(x=650, y=100)
    
    yes1_bt = Button(tab1, text="Generic Dry Maze", command=choice1, width=15)
    yes1_bt["font"] = myFont
    yes1_bt.place(x=720, y=500)
    
    no1_bt = Button(tab1, text="Choose New", command=choice2, width=14)
    no1_bt["font"] = myFont
    no1_bt.place(x=950, y=500)
    
    mwm_config_bt = Button(tab1, text="Morris Water Maze", command=choice3, width=15)
    mwm_config_bt["font"] = myFont
    mwm_config_bt.place(x=835, y=550)
    

def choice1():
    global path_config_file
    
    tempConf_lb.destroy()
    yes1_bt.destroy()
    no1_bt.destroy()
    mwm_config_bt.destroy()
    
    path_config_file = "C:/Users/PC/Desktop/GUI/analyses/Analyse-Deniz-2021-10-07/config-Final.yaml"
    analyze_video()
    

def choice2():
    global path_config_file
    
    tempConf_lb.destroy()
    yes1_bt.destroy()
    no1_bt.destroy()
    mwm_config_bt.destroy()
    
    chooseConf_lb = Label(tab1, text="Choose Config File")
    chooseConf_lb.config(font=("Courier", 30))
    chooseConf_lb.place(x=800, y=100)
    
    path_config_file = askopenfilename()
    while ".yaml" not in path_config_file:
        path_config_file = askopenfilename()
        
    chooseConf_lb.destroy()
    
    analyze_video()
    
    
def choice3():
    global path_config_file
    
    tempConf_lb.destroy()
    yes1_bt.destroy()
    no1_bt.destroy()
    mwm_config_bt.destroy()
    
    path_config_file = "C:/Users/PC/Desktop/GUI/analyses/MWM_model-Deniz Kurtaran-2021-12-24/config.yaml"
    analyze_video()


def analyze_video():
  global csv_file
  global choose_csv_bt
  global continue0_bt
  global analyzed_bool
  global path_video_file
  global crop_click_count
  global canva0
  global will_be_deleted
  global temp1_lb
  global temp11_lb
  global cont_analysis_bt
  global frame0
  global latest_config_file
  global delete_all
  global will_be_edited
  global top_left
  global bottom_right
  global color
  global temp12_lb
  global crop_rec
  global top_left_drawing
  global bottom_right_drawning
  global cap0
  global analysis_clip
  
  
  color = "green"
  
  delete_all = []
  will_be_edited = {}
  
  temp01_lb = Label(tab1, text="Choose the Video")
  temp01_lb.config(font=("Courier", 30))
  temp01_lb.place(x=730, y=100)
  
  path_video_file = askopenfilename()
  original = path_video_file # directory creating continue_here
  
  temp01_lb.destroy()
  temp1_lb = Label(tab1, text="Where do you want to crop the video")
  temp11_lb = Label(tab1, text="select top left and bottom right of floor area")
  temp1_lb.config(font=("Courier", 30))
  temp11_lb.config(font=("Courier", 30))
  temp1_lb.place(x=440, y=0)
  temp11_lb.place(x=420, y=80)

  crop_click_count = 0
  analysis_clip = VideoFileClip(path_video_file)
  cap0 = cv2.VideoCapture(path_video_file)
  cap0.set(1, 500) # frame 200
  ret0, frame0 = cap0.read()
  canva0_h = frame0.shape[0]
  canva0_w = frame0.shape[1]
  canva0 = Canvas(root, height = canva0_h, width = canva0_w)
  canva0.place(x=200, y=200)
  
  cont_analysis_bt =  Button(tab1, text="Continue Analysis", command=analyze_video_continue, width=14)
  cont_analysis_bt["font"] = myFont
  cont_analysis_bt.place(x=1620, y=900)
  
  Showimage(frame0, canva0, "fill")
  canva0.update()
  canva0.update()
  will_be_deleted = []
  
  top_left_drawing = create_circle(20, 20, 8, canva0, edit=True)
  top_left = (20, 20)
  bottom_right_drawing = create_circle(frame0.shape[1] - 20, frame0.shape[0] - 20, 8, canva0, edit=True)
  bottom_right = (frame0.shape[1] - 20, frame0.shape[0] - 20)
  crop_rec = canva0.create_rectangle(top_left[0], top_left[1], bottom_right[0], bottom_right[1], fill='', outline="green", width=3)
  
  root.bind("<Button>", edit_point_click_crop)
  
  
def analyze_video_continue():
  global temp3_lb
  global analyzed_bool
  global continue0_bt
  global csv_file
  global df
  global path_video_directory
  
  print("Top Left:", top_left)
  print("Bottom Right:", bottom_right)
  
  """Editing config file for crop points"""
  text_to_search0 = "x1: 0"
  replacement_text0 = "x1: " + str(top_left[0])
  
  text_to_search1 = "x2: 640"
  replacement_text1 = "x2: " + str(bottom_right[0])
  
  text_to_search2 = "y1: 277"
  replacement_text2 = "y1: " + str(top_left[1])
  
  text_to_search3 = "y2: 624"
  replacement_text3 = "y2: " + str(bottom_right[1])
  
  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(text_to_search0, replacement_text0), end='')
      
  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(text_to_search1, replacement_text1), end='')
    
  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(text_to_search2, replacement_text2), end='')
      
  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(text_to_search3, replacement_text3), end='')
  
  canva0.destroy()
  cont_analysis_bt.destroy()
  
  temp1_lb.destroy()
  temp11_lb.destroy()
  temp2_lb = Label(tab1, text="Analysis in Progress, Please Wait...")
  temp2_lb.config(font=("Courier", 30))
  temp2_lb.place(x=560, y=100) 
  tab1.update()

  #Analysis

  deeplabcut.analyze_videos(path_config_file, path_video_file, videotype=".mp4")
  deeplabcut.filterpredictions(path_config_file, path_video_file, videotype=".mp4", filtertype='arima')
  
  #Conversion
  video_path_splitted = path_video_file.split("/")
  video_path_splitted = video_path_splitted[:-1]
  path_video_directory = "/".join(video_path_splitted)
  
  def pick_files(folder, ext="", relative=True):
    """Return the paths of files with extension *ext* present in *folder*."""
    for file in os.listdir(folder):
        if file.endswith(ext) or file.endswith(ext.upper()):
            yield file if relative else os.path.join(folder, file)
  
  h5_files = list(
    pick_files(path_video_directory, "h5", relative=False)
  )
  videos = pick_files(
      path_video_directory, ".mp4", relative=False
  )
  for video in videos:
      if "_labeled" in video:
          continue
      vname = Path(video).stem
      for file in h5_files: # LOOK HERE
          if vname in file:
              scorer = file.split(vname)[1].split(".h5")[0]
              if ("DLC" in scorer or "DeepCut" in scorer) and "_filtered" in scorer:
                  print("Found output file for scorer:", scorer)
                  print(f"Converting {file}...")
                  print("FILE ISSSSS " + file)
                  df = pd.read_hdf((file)) # Changed
                  df.iloc[:, 0] = df.iloc[:, 0] + float(top_left[0])
                  df.iloc[:, 1] = df.iloc[:, 1] + float(top_left[1])
                  df.to_csv(file.replace(".h5", ".csv"))
                  csv_file = file.replace(".h5", ".csv")
  print("Conversion Successful.")
  print("the file is:", csv_file)
  analyzed_bool = True
  
  temp2_lb.destroy()
  temp3_lb = Label(tab1, text="Analysis Complete")
  temp3_lb.config(font=("Courier", 30))
  temp3_lb.place(x=730, y=100)
  
  """Editing config file for crop points"""

  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(replacement_text0, text_to_search0), end='')
      
  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(replacement_text1, text_to_search1), end='')
    
  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(replacement_text2, text_to_search2), end='')
      
  with fileinput.FileInput(path_config_file, inplace=True, backup='.bak') as file:
    for line in file:
      print(line.replace(replacement_text3, text_to_search3), end='')
  
  continue0_bt = Button(tab1, text="Continue", command=draw_or_load, width=14)
  continue0_bt["font"] = myFont
  continue0_bt.place(x=1620, y=900)
  

def edit_point_click_crop(event):
  global closest
  global point_is
  
  crop_frame_points = [top_left, bottom_right]
  closest = crop_frame_points[0]
  smallest_distance = 1000000000
  for point in crop_frame_points:
    xDiff = (event.x - point[0]) ** 2
    yDiff = (event.y - point[1]) ** 2
    distance = (xDiff + yDiff) ** 1/2
    if distance < smallest_distance:
      smallest_distance = distance
      closest_point = point
      
  point_index = crop_frame_points.index(closest_point)
    
  point_is = "top_left"
  if point_index > 0:
    point_is = "bottom_right"
  root.bind("<B1-Motion>", edit_point_hold_crop)
  root.bind("<ButtonRelease-1>", edit_point_release_crop)
  print(closest_point)
  canva0.delete(will_be_edited[closest_point])
  

def edit_point_hold_crop(event):
  global closest
  global canva0
  global crop_rec
  global top_left
  global bottom_right
  global top_left_drawing
  global bottom_right_drawning
  
  for e in delete_all:
    canva0.delete(e)
  
  if point_is == "top_left":
    top_left = (event.x, event.y)
    top_left_drawing = canva0.create_oval(event.x - 8, event.y - 8, event.x + 8, event.y + 8, fill="green", outline="green")
    delete_all.append(top_left_drawing)
  elif point_is == "bottom_right":
    bottom_right = (event.x, event.y)
    bottom_right_drawing = canva0.create_oval(event.x - 8, event.y - 8, event.x + 8, event.y + 8, fill="green", outline="green")
    delete_all.append(bottom_right_drawing)
  
  canva0.delete(crop_rec)
  crop_rec = canva0.create_rectangle(top_left[0], top_left[1], bottom_right[0], bottom_right[1], fill='', outline="green", width=3)


def edit_point_release_crop(event):
  will_be_edited[(event.x, event.y)] = canva0.create_oval(event.x - 8, event.y - 8, event.x + 8, event.y + 8, fill="green", outline="green")
  
  
def draw_or_load():
  global choose_lb
  global choose_video_bt
  global load_polygons_bt
  
  if "analyzed_bool" in globals():
    continue0_bt.destroy()
    temp3_lb.destroy()
  
  yes_bt.destroy()
  no_bt.destroy()
  find_keypoints_lb.destroy()
  
  choose_lb = Label(tab1, text="Draw or Load")
  choose_lb.config(font=("Courier", 30))
  choose_lb.place(x=800, y=100)
  
  choose_video_bt = Button(tab1, text="Draw New Maze \n (for the first time)", command=choose_video, width=16, height=3)
  choose_video_bt["font"] = myFont
  choose_video_bt.place(x=690, y=500)
  
  load_polygons_bt = Button(tab1, text="Load Existing Maze \n (choose this when the maze \nand camera have not moved)", command=load_polygons, width=24, height=3)
  load_polygons_bt["font"] = myFont
  load_polygons_bt.place(x=930, y=500)
  
  
click_count = 0
shape_done = False
shape_count = 0
polygons = []

myFont = font.Font(family='Helvetica')

find_keypoints_lb = Label(tab1, text="Please Make Your Choice")
find_keypoints_lb.config(font=("Courier", 30))
find_keypoints_lb.place(x=700, y=100)

yes_bt = Button(tab1, text="Generate New \n Analysis", command=analyze0, width=18)
yes_bt["font"] = myFont
yes_bt.place(x=690, y=500)

no_bt = Button(tab1, text=" Use Existing Analysis \n (already processed video)", command=draw_or_load, width=21)
no_bt["font"] = myFont
no_bt.place(x=960, y=500)

root.mainloop()  
