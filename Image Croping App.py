"""
A) Visual Description:
-------------------
This youtube video explains how to use this application: https://www.youtube.com/watch?v=hvrOhBz8DJE
"""
#### Imports #### Imports #### Imports #### Imports #### Imports #### Imports #### Imports #### Imports #### Imports ####
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
########################################### My Classes ##################################################
#####Custom Widget Classes
class Imagedisplay(Frame):
    def __init__(self, master, wmax = 1000, hmax = 600):
        '''
        MASTER is the master window/widget to which the Imagedisplay's object is associated
        IMPATH is the path to the image to be displayed
        WMAX and HMAX are the maximum width and maximum height allowed, in pixels, for the displayed image, respectively.
        '''
        #The class "Imagedisplay" is a child/sub-class of the class "Frame". However, the attributes making "Imagedisplay" instances behave as widgets are not inherited yet.
        #Such properties could be inherited if 3 conditions are satisfied:
            #Condition 1: Run the __init__ method of the class "Frame".
            #Condition 2: To make Imagedisplay integrable with a master widget/window, we should pass the argument "master" to the __init__ method of the class "Frame"
            #Condition 3: To make "Imagedisplay" instances behave as widgets, we should pass the argument "self", which represents the "Imagedisplay" instance, to the __ini__ method of the class "Frame"

        #This command satisfies the aforementioned 3 conditions
        super(Imagedisplay, self).__init__(master)
        self.patch_dst = ""#Defining the attribute patch destination
        self.patch_prefix = ""#Defining a prefix to filenames of stored patches
        #Before conversion from pil image to tkinter image, we make sure that its size fits the frame. If not, we resize it to fit the frame
        #Defining the maximum value of width and height (wmax, hmax) of the image to display
        self.wmax = wmax
        self.hmax = hmax

        #Defining the width and height of the patch to save
        self.patch_h = 32
        self.patch_w = 32

        #Creating a tkinter image "image_as_tk" that can be displayed on a Label widget
        self.im_as_np = np.multiply(np.ones((self.hmax, self.wmax), dtype = np.uint8),100)
        self.im_as_pil = Image.fromarray(self.im_as_np)
        self.im_as_tk = ImageTk.PhotoImage(self.im_as_pil)
        #Creating elements/sub-widgets of the custom widget as attributes of the class Imagedisplay.
        #The custom widget, to which we refer as "self", is the master/parent of the sub-widget "LabelFrame"

        self.frame = LabelFrame(self, text = "Image Display")
        #The sub-widget "LabelFrame" is the master of the sub-widget Button
        self.imagelabel = Label(self.frame, image = self.im_as_tk)
        self.coord_label = Label(self.frame, text = "Current position (x,y): Load an image/images and hover the mouse on")

        #Packing the subwidgets of the Imagedisplay
        self.frame.pack()
        self.imagelabel.grid(row = 0, column =0)#Note: subwidgets of frame must be packed with the same geometry manager. In my case, I used the .grid() manager
        self.coord_label.grid(row = 1, column = 0, sticky = W)

    def update_image(self, impath):
        """
        Description: This function updates the displayed image and prints on a text label the cursor's coordinates (x,y) when hovered on the image
        Parameters:
            IMPATH: the path to the image to display
        """
        #To update the image, we pass from 3 steps:
            #Step1: delete the previous image label using .gridforget() method
            #Step2: assign the new imagelabel to your label variable
            #Step3: re-define the position of that label using the .grid() method

        #########################################Updating the displayed image#########################################
        #######Step1: delete the previous image label using .gridforget() method
        self.imagelabel.grid_forget()

        #Step2:assign the new imagelabel to your label variable
        self.im_as_pil = Image.open(impath)
        #self.im_as_pil may be resized to make it fit in the GUI.
        ##self.im_as_pil_org won't be resized. It'll be used to slice the patch from.
        self.im_as_pil_org = self.im_as_pil
        #Before conversion from pil image to tkinter image, we make sure that its size fits the frame. If not, we resize it to fit the frame
        #Defining the maximum value of width and height (wmax, hmax) of the image to display
        #Getting the original width and height of the image to display
        self.org_w , self.org_h = self.im_as_pil.size


        ###Downscale the image while keeping the aspect ratio. To this end, both w and h are downscaled with the same factor "scaling_factor"###
        #Initialization of the scaling_factor to 1
        scaling_factor = w_scaled = h_scaled = int(1)
        if self.org_w<=self.wmax and self.org_h<=self.hmax:#If the image doesn't exceed the expected dimensions (wmax,hmax), then transform the pil image into a tkinter image. Otherwise, the image is downscaled while keeping the aspect ratio
            self.im_as_tk = ImageTk.PhotoImage(self.im_as_pil)
        elif self.org_w>self.wmax and self.org_h>self.hmax:#True if both w and h exceed the threshold wmax,hmax
            #This factor is either (wmax/w) or (hmax/h). Choosing the minimum, i.e., min(wmax/w,hmax/h) esures that the width and height of the downscaled image do not exceed the threshold (wmax,hmax)
            scaling_factor = min(self.wmax/self.org_w,self.hmax/self.org_h)
            w_scaled = int(self.org_w*scaling_factor)
            h_scaled = int(self.org_h*scaling_factor)
            self.im_as_pil = self.im_as_pil.resize((w_scaled,h_scaled))
            self.im_as_tk = ImageTk.PhotoImage(self.im_as_pil)
        elif self.org_w>self.wmax and self.org_h<self.hmax:#True if only w exceeds the threshold wmax
            scaling_factor = wmax/self.org_w
            w_scaled = int(self.org_w*scaling_factor)
            h_scaled = int(self.org_h*scaling_factor)
            self.im_as_pil = self.im_as_pil.resize((w_scaled,h_scaled))
            self.im_as_tk = ImageTk.PhotoImage(self.im_as_pil)
        elif self.org_w<self.wmax and self.org_h>self.hmax:#True if only h exceeds the threshold hmax ###Problem here
            scaling_factor = self.hmax/self.org_h
            w_scaled = int(self.org_w*scaling_factor)
            h_scaled = int(self.org_h*scaling_factor)
            self.im_as_pil = self.im_as_pil.resize((w_scaled,h_scaled))
            self.im_as_tk = ImageTk.PhotoImage(self.im_as_pil)

        #Updating the new image to display
        self.imagelabel = Label(self.frame, image = self.im_as_tk)
        ###End of downscaling###################################################################################################################

        #Step3: re-define the position of that label using the .grid() method
        self.imagelabel.grid(row = 0, column =0)
        #########################################END of: Updating the displayed image#########################################


        #########################################Printing on a text label the cursor's coordinates (x,y)#########################################
        ###Defining event's callout###
        def Mouse_motion(event):
            #######################Scaling the image if its dimesions exceed the thresholds wmax and hmax################
            if w_scaled != 1 and h_scaled != 1:#True if the image has been scaled
                x = int((event.x)*(self.org_w/w_scaled))
                y = int((event.y)*(self.org_h/h_scaled))
            else:#Executed if the image isn't scaled
                x = event.x
                y = event.y
            ##############################################################################################################

            #######################Solving the padding issue of the widget label##########################################
            #Description of the issue:
                #The coordinates of the mouse position on the image label are not quite correct.
                #There is an error of 2 pixels
                #This error is explained by the observation that tkinter pads any given image with 2 pixels from all sides (top, bottom, right, left)
                #This section solves this issue and makes sure that the printed coordinate image are accurate.
            x = x - 2
            y = y - 2
            if x<self.org_w and y<self.org_h:
                ######Making sure that the smallest value of x and y is 0############
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                ######################################################################
                ######################Print the text label displaying the coordinates of the current mouse####################
                #self.coord_label = Label(self.frame, text = "Current position (x,y): "+"("+str(x)+","+ str(y)+")              ")#Extra space added at the end to over-ride the remaining parenthesis
                self.coord_label.config(text = "Current position (x,y): "+"("+str(x)+","+ str(y)+")              ")
                self.real_x = x #This attribute is used to specify the x coordinate of the patch to store
                self.real_y = y #This attribute is used to specify the y coordinate of the patch to store
        def savepatch(event):
            if os.path.isdir(self.patch_dst):#True if the user has selected a destination folder where the patches are to be stored
                x_coord = self.real_x
                y_coord = self.real_y
                #convert PIL image object (with the original size) to numpy.ndarray object, whose channels are respectively B, G and R
                im_np = np.asarray(self.im_as_pil_org)
                #convert from BGR to RGB.
                im_np = cv.cvtColor(im_np, cv.COLOR_BGR2RGB)

                ################Slicing the image <==> Get the patch################
                step = 1
                half_w = int(self.patch_w/2)
                half_h = int(self.patch_h/2)
                self.starting_row = x_coord - half_w
                self.ending_row = x_coord + half_w
                self.starting_col = y_coord - half_h
                self.ending_col = y_coord + half_h
                rows_slice = slice(self.starting_row,self.ending_row,step)
                cols_slice = slice(self.starting_col,self.ending_col,step)
                #Slicing from the original image with the original size : "im_np"
                im_patch = im_np[cols_slice,rows_slice,:]
                selectedPatch_height = im_patch.shape[0]
                selectedPatch_width = im_patch.shape[1]

                ######################################################################

                ########################Patch Saving Mechanism#############################
                """
                Description of the Patch Saving Mechanism:
                    Any stored patch is suffixed by the tkinter variable patch_number
                    When a destination folder is selected, patch_number is set to be equal to the number of files + 1
                    When a patch is stored, patch_number gets incremented
                    Storage conditions; The pach is stored only if:
                        1) its size is not higher than that of the image
                        2) the entire patch area is included in the image
                """
                patch_order = patch_number.get()
                patch_path = self.patch_dst +"/"+self.patch_prefix + str(patch_order)+ ".png"
                #######The patch is stored only if it is not out of the image frame######
                if self.org_w <= self.patch_w or self.org_h <= self.patch_h:
                    messagebox.showerror("Patch size error", "The patch size is higher or equal than the image size!!\nThe patch size should smaller than the image size")
                elif selectedPatch_height<self.patch_h or selectedPatch_width < self.patch_w:#True if the patch has a portion that' out of the frame/image
                    messagebox.showerror("Patch position error", "The patch you selected has a portion that's out of the frame\nTry avoiding near frame's border regions when selecting your patches")
                else:
                    #The attribute .last_patch is used to show on the user interface the last patch stored
                    #We convert the patch to BGR. We do this conversion because tkinter images are RGB images only if the image before conversion to the tkinter image was a BGR image.
                    im_patch_bgr = cv.cvtColor(im_patch, cv.COLOR_RGB2BGR)
                    self.last_patch = Image.fromarray(im_patch_bgr)#convert to a PIL image
                    self.last_patch = ImageTk.PhotoImage(self.last_patch)#Convert to a tk image

                    cv.imwrite(patch_path,im_patch)
                    patch_number.set(patch_order + 1)
                    number_of_patches.set(number_of_patches.get() + 1)

                ##########################################################################
            else:
                messagebox.showwarning(title = "Warning", message = "You can't store patches until a destination folder is selected")
        ##############################################################################################################
        def Overlay_Patches(event):
            ################Overlaying selected patches##########################
            start_point = (int(self.starting_row*scaling_factor), int(self.starting_col*scaling_factor))
            end_point = (int(self.ending_row*scaling_factor), int(self.ending_col*scaling_factor))
            color = (255,0,0)#Red Color
            thikness = 2
            self.img_ov = np.asarray(self.im_as_pil)
            cv.rectangle(self.img_ov, start_point, end_point, color = color, thickness = thikness)
            self.im_as_pil = Image.fromarray(self.img_ov)
            self.im_as_tk = ImageTk.PhotoImage(self.im_as_pil)
            self.imagelabel.config(image = self.im_as_tk)
        ###Binding events###
        self.imagelabel.bind("<Motion>",Mouse_motion)
        self.imagelabel.bind("<Double-1>",savepatch, add = '+')
        self.imagelabel.bind("<Double-1>",Overlay_Patches, add = '+')
        #########################################END of:Printing on a text label the cursor's coordinates (x,y)#########################################


#################### Main Code: Callback functions##############################

def Load_imgs_paths(event):
    """
    This function loads all paths of loaded images and stores them in a tuple of strings "impaths"
    If impaths is not an empty string, i.e., " ", then the image that corresponds to the first path is displayed on the Imagedisplay instance
    """
    initialdir = os.getcwd()
    #initialdir = r"C:\Users\Dell\Desktop"
    title = "Select one or more images to load"
    filetypes = (("png files","*.png"),("jpeg files","*.jpeg"),("All files","*.*"))
    #impaths is a tuple of paths of selected files (or a void string '' if no file is selected)
    #impaths should probably be a global variable
    global impaths
    impaths = filedialog.askopenfilenames(initialdir = initialdir, title = title, filetypes = filetypes)
    if impaths != '': #True if at least one image is loaded
        #Set the current image index to zero
        current_image_index.set(0)
        Back_button.config(state = "disabled")#When a least one image is loaded, always disable the back button (because we are in the first image)
        display.update_image(impaths[0])
        impaths_len.set(len(impaths)) #if an image/images are loaded, get their number and store it in the tkinter variable impaths_len
        Browsing_status_text = "Image 1/" + str(impaths_len.get())
        Browsing_status.config(text = Browsing_status_text)
        if impaths_len.get()> 1: #If more than one image is loaded, enable the next button
            Next_button.config(state = "active")
        elif impaths_len.get() == 1:#If only one image is loaded, disable the next button
            Next_button.config(state = "disabled")

def Browse_next(event):
    def Execute_next():
        """
        This function performs processes of going next. It's called if conditions of going next are satisfied.
        Execution Conditions:
            If the Next button is not disabled, there are 2 possibilites:
                1) the calling event is "ButtonPress": In this case, call Execute_next()
                2) the calling event is "MouseWheel": In this case, check if the mousewheel is scrolled up <==> delta.event >0
                   If it's scrolled up, call Execute_next() and do not otherwise.
        """
        Back_button.config(state = "active")#Going next implies there is a previous image. Thus, the back button is enabled
        indx = current_image_index.get() + 1
        display.update_image(impaths[indx])
        current_image_index.set(indx)
        if (indx+1) == impaths_len.get():#True if the current image is the last one
            Next_button.config(state = "disabled")#Disable the next button if there is no next image
        ################Updating the Browsing Status Label################
        Browsing_status_text = "Image "+ str(indx + 1) + "/" + str(impaths_len.get())
        Browsing_status.config(text = Browsing_status_text)
    Next_button_state =  Next_button.state()
    Next_button_state = Next_button_state[0]#The first element of the tuple Next_button_state is the state. Thus, it's indexed by 0.
    if Next_button_state != "disabled":#Go to the next image only if the button is enabled
        if str(event.type) == "ButtonPress":
            Execute_next()
        elif str(event.type) == "MouseWheel" and event.delta>0:
            Execute_next()

def Browse_back(event):
    def Execute_back():
        """
        This function performs processes of going back. It's called if conditions of going back are satisfied.
        Execution Conditions:
            If the Back button is not disabled, there are 2 possibilites:
                1) the calling event is "ButtonPress": In this case, call Execute_back()
                2) the calling event is "MouseWheel": In this case, check if the mousewheel is scrolled down <==> event.delta < 0.
                   If it's scrolled down, call Execute_next() and do not otherwise.
        """
        Next_button.config(state = "active")#Going back implies there is a next image. Thus, the next button is enabled
        indx = current_image_index.get() - 1
        display.update_image(impaths[indx])
        current_image_index.set(indx)
        if indx == 0:
            Back_button.config(state = "disabled")
        ################Updating the Browsing Status Label################
        Browsing_status_text = "Image "+ str(indx + 1) + "/" + str(impaths_len.get())
        Browsing_status.config(text = Browsing_status_text)
        ########################################################

    Back_button_state = Back_button.state()
    Back_button_state = Back_button_state[0]

    if Back_button_state != "disabled":#Go to the back image only if the button is enabled
        if str(event.type) == "ButtonPress":
            Execute_back()
        elif str(event.type) == "MouseWheel" and event.delta<0:
            Execute_back()

def Update_patchDst(event):
    """
    This callback function updates the destination folder where patches are to be stored.
    This destination is an attribute of the ImageDisplay object: display.patch_dst
    """
    title = "Choose a folder destination to store the patches"
    initialdir = os.getcwd()#directroy initialized at current working directory
    dir = filedialog.askdirectory(initialdir = initialdir,title = title)
    if os.path.isdir(dir):
        display.patch_dst = dir
        Selected_Folder.delete(0,len(Selected_Folder.get()))#Deletes the previous text of the entry
        Selected_Folder.insert(0,"Current Patch destination: " + dir)
        #The number/order of the next patch should be equal to the number of files in the destination directory + 1
        #This number of files is assumed to be the number of patches stored
        patch_number.set(len(os.listdir(dir)) + 1)
        #this method .schedule() tells the Observer object 2 things:
            #(1) what events to monitor (defined in the object newpatch_event; an object of a subclass FileSystemEventHandler)
            #(2) what's the path of the folder to monitor (defined in "path")
        observer.schedule(newpatch_event, path = display.patch_dst)


def Update_patch_size(event):
    ################Entry Text Processing: to get the width and height#########################
    patch_size_txt = Patch_size_entry.get()
    processed_txt = patch_size_txt.replace(" ","")#Remove all white spaces
    processed_txt = processed_txt.split(",")#Split the string at the first comma "," to get the width and height as the first and second element of the returned list
    ################End of Entry Text Processing###############################################
    ################Updating the patch width and height attributes of the ImageDisplay Instance############
    try:
        extracted_width = int(processed_txt[0])
        extracted_height = int(processed_txt[1])
        #No_error indicates if the "except" code is executed
        No_error = True
    except:
        messagebox.showwarning("Invalid patch size format", "Invalid patch size; Type-in patch size as : width, height. The width and height must be integers")
        #No_error indicates if the "except" code is executed
        No_error = False
    if No_error:#We update the patch width and height only of no error is raised
        display.patch_w = extracted_width
        display.patch_h = extracted_height
        infMsg = "The patch size has been updated:\n Patch width = "+ str(display.patch_w)+"\n Patch height = "+ str(display.patch_h)
        messagebox.showinfo("Patch size info", infMsg)

def Update_patch_prefix(event):
    display.patch_prefix = patch_prefix_entry.get()
    display.patch_prefix.replace(" ","")#Delete all spaces
    messagebox.showinfo("patches filenames", "Next stored patches are prefixed by ''"+display.patch_prefix+"'" )

def On_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        observer.stop()#Stop the event handler monitoring the modification of destination folder
        root.destroy()#Destroy the window
################################################################################

####################################################Creating Widgets######################################
#Create a root window
root = Tk()
#root.geometry("1000x680+0+0")

frame1 = Frame(root)
frame2 = Frame(root)
display = Imagedisplay(frame1)
Browsing_frame = LabelFrame(frame1, text = "Browse")
Back_button = ttk.Button(Browsing_frame, text = "<<Back", state = "disabled")
Next_button = ttk.Button(Browsing_frame, text = "Next>>", state = "disabled")
Browsing_status = ttk.Label(Browsing_frame, text = "Browsing Status")

loadsave_frame = LabelFrame(frame2, text = "Load & Save")
Load_button = ttk.Button(loadsave_frame, text = "Load", width = 20)
Destination_button = ttk.Button(loadsave_frame, text = "Patches Destination", width = 20)
Selected_Folder = Entry(loadsave_frame, width = 45)
Selected_Folder.insert(0, "Patches destination: 'Choose pathes destination'")





Patch_frame = LabelFrame(frame2, text = "Patch")
stored_patch_frame = LabelFrame(Patch_frame, text = "Last Patch stored")
last_saved_patch = Label(stored_patch_frame)
patch_prefix_label = Label(Patch_frame, text = "Type-in filenames prefix, followed by enter")
patch_prefix_entry = Entry(Patch_frame, borderwidth = 3,relief = "ridge")
psl_text = "Enter the patch width and height,\nseparated by a comma ',', then type 'Enter'/'Return'.\n For example: 32,16"
Patch_size_label = Label(Patch_frame, text = psl_text)
Patch_size_entry = Entry(Patch_frame, borderwidth = 3,relief = "ridge")
Patch_size_entry.insert(0,"32,32")
Number_of_Patches_label = Label(Patch_frame, text = "Number of saved patches")
Number_of_Patches = Entry(Patch_frame, width = 45)
############################################################################################################

###########################################################################################################################




####### Binding Events Section ####### Binding Events Section ####### Binding Events Section ####### Binding Events Section ###
Load_button.bind("<Button-1>", Load_imgs_paths)
Destination_button.bind("<Button-1>", Update_patchDst)

Next_button.bind("<Button-1>", Browse_next)
Back_button.bind("<Button-1>", Browse_back)
Patch_size_entry.bind("<Return>", Update_patch_size)
patch_prefix_entry.bind("<Return>", Update_patch_prefix)

root.bind("<MouseWheel>",Browse_next)
root.bind("<MouseWheel>",Browse_back, add = '+')
root.protocol("WM_DELETE_WINDOW", On_closing)



#This variable enables the callback functions "Browse_next" and "Browse_back" to get the order of the current image
current_image_index = IntVar(0)
#This variable specifies the order of the next patch to be stored. This allows giving the stored patches different names
patch_number = IntVar(0)
#Number of saved patches
number_of_patches = IntVar(0)
#the number of loaded images
impaths_len = IntVar(0)
###########################################################################################################################




############################################### Managing Geometry Section #################################################
root.geometry("+0+0")
root.maxsize()#Autmoatically scales to the content of the window
##Frame 1##
frame1.grid(row = 0, column = 0)

display.grid(row = 0, column = 0, padx = 5)
Browsing_frame.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 5)

Back_button.grid(row = 0, column = 0, sticky = W)
Browsing_status.grid(row = 0, column = 1)
Next_button.grid(row = 0, column = 2, sticky = E)
###########

##Frame 2##
frame2.grid(row = 0, column = 1,sticky = N)

Patch_frame.grid(row = 0, column = 0, ipady = 4)
stored_patch_frame.grid(row = 0, column = 0,sticky = W)
last_saved_patch.pack()
patch_prefix_label.grid(row = 1, column = 0,sticky = W)
patch_prefix_entry.grid(row = 2, column = 0,sticky = W)
Patch_size_label.grid(row = 3, column = 0,sticky = W)
Patch_size_entry.grid(row = 4, column = 0,sticky = W)
Number_of_Patches_label.grid(row = 5, column = 0,sticky = W)
Number_of_Patches.grid(row = 6, column = 0,sticky = W)

loadsave_frame.grid(row = 1, column = 0, sticky = NW)
Load_button.grid(row = 0, column = 0, ipady = 8, padx = 10, pady = 10)
Destination_button.grid(row = 0, column = 1, ipady = 8, padx = 10, pady = 10)
Selected_Folder.grid(row = 1, column = 0, columnspan = 2, pady = 5)
###########



###########################################################################################################################


###### Main Code Section ##### Main Code Section ##### Main Code Section ##### Main Code Section ##### Main Code Section


#####################Creating an event to monitor if a new patch has been stored###############
"""
This section creates an event to monitor if a new patch is stored.
If such event is triggered, we diplay on the user interface (preciselyn on the image label "last_saved_patch") the last
patch stored.
"""
#Creating an instance of Observer class.
#The observer observes if an event or a set of events occur.
#This/these events are defined by overridding methods of the class "FileSystemEventHandler" in a subclass we shall define as "Newpatch_event(FileSystemEventHandler)"
#Possible events defined in the class FileSystemEventHandler as methods, which can be overridden in the subclass we shall define
#To tell the observer object what event(s) it should monitor, we invoke the method .schedule(), which takes as arguments an instance of the defined subclass and the path of the file or folder to monitor
#Finally, to start monitoring for the events (defined in the subclass of FileSystemEventHandler), the method .start() is invoked
observer = Observer()
class Newpatch_event(FileSystemEventHandler):
    def on_modified(self, event):#overridding the on_modified method
        """
        The argument "event" has 3 attributes: event_type, is_directory and src_path:
        """
        #This method would get executed if the path of the file/folder specified in the .schedule() method gets on_modified
        #My assumption is that thi modification corresponds to storage of a new patch
        #In that case, the image of the last patch stored is displayed on the user interface
        last_saved_patch.config(image = display.last_patch)
        #Delete the previous content of the entry displaying the number of patches saved since launching the app
        Number_of_Patches.delete(0,(len(Number_of_Patches.get())))
        #If a the desination folder has changed, show the number of patches saved since launching the app
        Number_of_Patches.insert(0,number_of_patches.get())

newpatch_event = Newpatch_event()
#Starting the observer.
#Note:
    #the observer must be told with the method ".schedule()" the path of the folder where programmed events are monitored
    #This path changes when the user changes the desination folder, i.e., folder where patches are to be stored_patch_frame
    #The observer is told which path to observe in the callback "Update_patchDst".
    #The reson why the ".schedule()" is invoked inside the callback "Update_patchDst" is the possibility of accessing the updated desination folder
observer.start()
###############################################################################################
root.mainloop()
###########################################################################################################################
