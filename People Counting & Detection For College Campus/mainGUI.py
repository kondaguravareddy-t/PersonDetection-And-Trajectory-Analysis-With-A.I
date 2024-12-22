import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True
import mainGUI_support
import os.path


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    root = tk.Tk()
    top = Toplevel1(root)
    mainGUI_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    rt = root
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    mainGUI_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


    
import cv2
import custom_counter

class Toplevel1:
    def __init__(self, top=None):



        def before_930(event):            
            Thread(target=custom_counter.start,args=("Person came before 9:30 AM"," came before 9:30 AM")).start()

        def after_930_and_before_1100(event):
            Thread(target=custom_counter.start,args=("Person came after 9:30 AM and before 11 AM"," came after 9:30 AM and before 11")).start()

        def after_1300_and_before_1400(event):
            Thread(target=custom_counter.start,args=("Person leaving after 1 PM and before 2 PM"," leaving after 1 PM and before 2 PM")).start()

        def after_1530(event):
            Thread(target=custom_counter.start,args=("Person leaving after 3:30 PM"," leaving after 3:30 PM")).start()


        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font16 = "-family Constantia -size 40 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font18 = "-family {Sitka Small} -size 15 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        w = 1000
        h = 650
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        top.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # top.geometry("1016x635")
        top.title("Smart People Counter")
        top.configure(background="#ffffff")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.33, rely=0.01, height=250, width=350)
        self.Label1.configure(background="#ffffff")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        photo_location = os.path.join(prog_location, "Images/yologo_2.png")
        self._img0 = tk.PhotoImage(file=photo_location)
        self.Label1.configure(image=self._img0)
        self.Label1.configure(text='''Label''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.03, rely=0.3, height=88, width=1000)
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font16)
        self.Label2.configure(foreground="#2365e8")
        self.Label2.configure(text='''Smart People Counting''')
        self.Label2.configure(width=659)

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.03, rely=0.535, relheight=0.402, relwidth=0.94)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="7")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(width=955)

        self.btnWebcam = tk.Label(self.Frame1)
        self.btnWebcam.place(relx=0.580, rely=0.157, height=154, width=154)
        self.btnWebcam.configure(background="#ffffff")
        self.btnWebcam.configure(disabledforeground="#a3a3a3")
        self.btnWebcam.configure(foreground="#000000")
        photo_location = os.path.join(prog_location, "Images/after_130_before_200.png")
        self._img1 = tk.PhotoImage(file=photo_location)
        self.btnWebcam.configure(image=self._img1)
        self.btnWebcam.configure(text='''Label''')
        self.btnWebcam.bind('<Button-1>', after_1300_and_before_1400)


        self.btnImage = tk.Label(self.Frame1)
        self.btnImage.place(relx=0.300, rely=0.1, height=200, width=200)
        self.btnImage.configure(activebackground="#f9f9f9")
        self.btnImage.configure(activeforeground="black")
        self.btnImage.configure(background="#ffffff")
        self.btnImage.configure(disabledforeground="#a3a3a3")
        self.btnImage.configure(foreground="#000000")
        self.btnImage.configure(highlightbackground="#d9d9d9")
        self.btnImage.configure(highlightcolor="black")
        photo_location = os.path.join(prog_location, "Images/after_930_before_1100.png")
        self._img2 = tk.PhotoImage(file=photo_location)
        self.btnImage.configure(image=self._img2)
        self.btnImage.configure(text='''Label''')
        self.btnImage.configure(width=172)
        self.btnImage.bind('<Button-1>', after_930_and_before_1100)

        self.btnVideo = tk.Label(self.Frame1)
        self.btnVideo.place(relx=0.042, rely=0.090, height=186, width=162)
        self.btnVideo.configure(activebackground="#f9f9f9")
        self.btnVideo.configure(activeforeground="black")
        self.btnVideo.configure(background="#ffffff")
        self.btnVideo.configure(disabledforeground="#a3a3a3")
        self.btnVideo.configure(foreground="#000000")
        self.btnVideo.configure(highlightbackground="#d9d9d9")
        self.btnVideo.configure(highlightcolor="black")
        photo_location = os.path.join(prog_location, "Images/before_930.png")
        self._img3 = tk.PhotoImage(file=photo_location)
        self.btnVideo.configure(image=self._img3)
        self.btnVideo.configure(width=162)
        self.btnVideo.bind('<Button-1>', before_930)

        self.Label3_5 = tk.Label(self.Frame1)
        self.Label3_5.place(relx=0.590, rely=0.784, height=26, width=142)
        self.Label3_5.configure(activebackground="#f9f9f9")
        self.Label3_5.configure(activeforeground="black")
        self.Label3_5.configure(background="#ffffff")
        self.Label3_5.configure(disabledforeground="#a3a3a3")
        self.Label3_5.configure(font=font18)
        self.Label3_5.configure(foreground="#061104")
        self.Label3_5.configure(highlightbackground="#d9d9d9")
        self.Label3_5.configure(highlightcolor="#000000")
        self.Label3_5.configure(width=142)

        self.Label3_6 = tk.Label(self.Frame1)
        self.Label3_6.place(relx=0.34, rely=0.784, height=36, width=142)
        self.Label3_6.configure(activebackground="#f9f9f9")
        self.Label3_6.configure(activeforeground="black")
        self.Label3_6.configure(background="#ffffff")
        self.Label3_6.configure(disabledforeground="#a3a3a3")
        self.Label3_6.configure(font=font18)
        self.Label3_6.configure(foreground="#061104")
        self.Label3_6.configure(highlightbackground="#d9d9d9")
        self.Label3_6.configure(highlightcolor="#000000")
        self.Label3_6.configure(width=142)

        self.Label3_6 = tk.Label(self.Frame1)
        self.Label3_6.place(relx=0.07, rely=0.784, height=36, width=142)
        self.Label3_6.configure(activebackground="#f9f9f9")
        self.Label3_6.configure(activeforeground="black")
        self.Label3_6.configure(background="#ffffff")
        self.Label3_6.configure(disabledforeground="#a3a3a3")
        self.Label3_6.configure(font=font18)
        self.Label3_6.configure(foreground="#061104")
        self.Label3_6.configure(highlightbackground="#d9d9d9")
        self.Label3_6.configure(highlightcolor="#000000")
        self.Label3_6.configure(width=142)

        self.btnExit = tk.Label(self.Frame1)
        self.btnExit.place(relx=0.822, rely=0.100, height=186, width=150)
        self.btnExit.configure(activebackground="#f9f9f9")
        self.btnExit.configure(activeforeground="black")
        self.btnExit.configure(background="#ffffff")
        self.btnExit.configure(disabledforeground="#a3a3a3")
        self.btnExit.configure(foreground="#000000")
        self.btnExit.configure(highlightbackground="#d9d9d9")
        self.btnExit.configure(highlightcolor="black")
        photo_location = os.path.join(prog_location, "Images/after_1530.png")
        self._img4 = tk.PhotoImage(file=photo_location)
        self.btnExit.configure(image=self._img4)
        self.btnExit.configure(text='''Label''')
        self.btnExit.configure(width=162)
        self.btnExit.bind('<Button-1>', after_1530)

        self.Label3_6 = tk.Label(self.Frame1)
        self.Label3_6.place(relx=0.832, rely=0.784, height=26, width=130)
        self.Label3_6.configure(activebackground="#f9f9f9")
        self.Label3_6.configure(activeforeground="black")
        self.Label3_6.configure(background="#ffffff")
        self.Label3_6.configure(disabledforeground="#a3a3a3")
        self.Label3_6.configure(font=font18)
        self.Label3_6.configure(foreground="#061104")
        self.Label3_6.configure(highlightbackground="#d9d9d9")
        self.Label3_6.configure(highlightcolor="#000000")
        self.Label3_6.configure(width=142)


