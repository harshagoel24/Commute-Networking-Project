import Tkinter as tk   # python3
from Tkinter import *
import ttk
import sys, os
import smtplib
#from smtplib import SMTPException  #********EMAIL TO BE SENT FROM SERVER******
import tkMessageBox
from PIL import ImageTk, Image
import socket,pickle,time
#import decoder as dec
from PIL import Image as image
import threading as th
#import gzip,shutil
#from PIL import Image
import subprocess
import threading,select
app=""
fname=""
prnt=0
filename=""
pasv="no"

path="C:/Python27"
genre=-1
s=''
pending="no"
#but=tk.Button(ruv,text="PAUSE!!!",command=prin)

#import Tkinter as tk   # python
TITLE_FONT = ("Helvetica", 18, "bold")
TITLE_FONT1 = ("Helvetica", 18, "bold italic")
TEXT_FONT = ("Times", 12, "bold")
TITLE_FONT2 = ("ALGERIAN", 28, "bold")
TEXT_FONT1 = ("Times", 12, "bold italic")

connected="no"

def ex_pro():
    print("exiting...")
    global s
    s.close()
    sys.exit(0)
    


def send(root,file1,c):
    fpath=os.path.join(root,file1)
    print(fpath)
    size = os.path.getsize(fpath)
    size1 = str(size)
    c.send(size1)
    f = open(fpath,"rb")
    bts= f.read(1024)
    totalSend=len(bts)
    c.send(bts)
    while(bts != ""):
        bts = f.read(1024)
        c.send(bts)
        totalSend += len(bts)
        print totalSend
    return 1
    

def retr(fil,s):
    global connected
    size1 = s.recv(1024)
    size=int(size1)
    print(size)
    with open("new_"+fil, "wb") as f:
  # f = open("new_"+fil, "a")
        data=s.recv(1024)
        
        f.write(data)
        print(data)
        totalRecv = len(data)
        
        while(totalRecv < size):
            
            data = s.recv(1024)
            totalRecv += len(data)
            f.write(data)
            print totalRecv
    connected="no"










def ctoc(choice="",filename="",root=""):
    class Chat_Server(threading.Thread):
            def __init__(self,root,filename):
                print("client server started")
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None
                self.root=root
                self.file1=filename
            def run(self):
                HOST = ''
                PORT = 1776
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                s.listen(1)
                self.conn, self.addr = s.accept()
                while self.running == True:
                    x=0
                    x=send(self.root,self.file1,self.conn)
                    if(x==1):
                        s.close()
                        break
                    
                    '''inputready,outputready,exceptready \
                      = select.select ([self.conn],[self.conn],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.conn.recv(1024)
                        if data:
                            print "Them: " + data
                        else:
                            break
                    time.sleep(0)'''
            def kill(self):
                self.running = 0
                
     
    class Chat_Client(threading.Thread):
            def __init__(self,filename):
                print("client client started")
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1
                self.file1=filename
            def run(self):
                PORT = 6000
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, PORT))
                # Select loop for listen
                
                while self.running == True:
                    retr(self.file1,self.sock)
                    '''inputready,outputready,exceptready \
                      = select.select ([self.sock],[self.sock],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.sock.recv(1024)
                        if data:
                            print "Them: " + data
                        else:
                            break
                    time.sleep(0)'''
            def kill(self):
                self.running = 0
                
    class Text_Input(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
            def run(self):
                while self.running == True:
                  text = raw_input('')
                  try:
                      chat_client.sock.sendall(text)
                  except:
                      Exception
                  try:
                      chat_server.conn.sendall(text)
                  except:
                      Exception
                  time.sleep(0)
            def kill(self):
                self.running = 0

    
    #ip_addr = raw_input('What IP (or type listen)?: ')
    print("hgfghfgf")
    #if ip_addr == 'listen':
    if choice == 'listen':
        chat_server = Chat_Server(root,filename)
        #chat_client = Chat_Client()
        chat_server.start()
        #text_input = Text_Input()
        #text_input.start()
        
    #elif ip_addr == 'Listen':
    elif choice == 'Listen':
        chat_server = Chat_Server(root,filename)
        #chat_client = Chat_Client()
        chat_server.start()
        #text_input = Text_Input()
        #text_input.start()
        
    else:
        #chat_server = Chat_Server()
        chat_client = Chat_Client(filename)
        chat_client.host = choice
        #chat_client.host = ip_addr
        #text_input = Text_Input()
        chat_client.start()
        #text_input.start()




def broad():
    global connected
    class broadcast(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.running = 1
        def run(self):
            global connected
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(('', 5555))
            
            while True:
                root2=""
                file2=""
                found=""
				
                message, address = s.recvfrom(8192)
                print "Got message from %s: %s" % (address, message)
				
                for root, dirs, files in os.walk(path):
                    for file1 in files:
                        if(file1==message):
                            found="found"
                            root2=root
                            file2=file1
                            
                            
                            break
                        else:
                            found="not found"
                    if(found=="found"):
                        break
                    elif(found=="not found"):
                        continue
                    
                if(found=="found"):
                    res="yes"
                    print("file has been found... Sending it to other client")
                    s.sendto(res, address)
                    connect, address = s.recvfrom(8192)
                    print connect
                    if(connect=="no"):
                        print connect
                        if(connected=="no"):
                            connected = "yes"
                            ctoc("listen",file2,root2)
                            
                    
                elif(found=="not found"):
                    print("FILE NOT FOUND!!!!!!")
                    continue

                    
        def kill(self):
            self.running = 0


    x=broadcast()
    x.start()




class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        
        self.frames = {}
        for F in (Welcome, StartPage, Login, Register, Options, Download):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Welcome")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



class Welcome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller

        label = tk.Label(self, text="THE COMMUTE!!", font=TITLE_FONT2, fg="deep sky blue", bg="black")
        label.pack(side="top", fill="x", pady=10)
        l = tk.Label(self, text="The File Transfer Protocol (FTP) is a standard network protocol used to transfer computer files between a client and server on a computer network.  FTP is built on a client-server model architecture and uses separate control and data connections between the client and the server.For secure transmission that protects the username and password, and encrypts the content, FTP is often secured with SSL/TLS (FTPS).", font=('Ariel',10,'bold'))
        
        l.config(wraplength=300)
        l.config(justify=CENTER)
        l.config(foreground='white', background='black')
        mp = PhotoImage(file="last.GIF")
        l.config(image=mp)
        l.image=mp
        l.config(compound="center")
        l.pack()

        #imageee----------------------------
        l = tk.Label(self, text="",  font=('Ariel',10,'bold'))
        
        l.config(wraplength=300)
        l.config(justify=CENTER)
        l.config(foreground='black', background='black')
        mp = PhotoImage(file="logo.GIF")
        l.config(image=mp)
        l.image=mp
        #l.config(compound="center")
        l.place(x=690, y=410)

        '''frame2=Frame(self)
        frame2.pack()

        
        c=Canvas(frame2)
        c.pack(side="top", fill="both", expand=True)
        c.background = PhotoImage(file="key1.gif")
        c.create_image(0,0,image=c.background, anchor='nw')'''
        lblank1 = tk.Label(self, text="", bg="black")
        lblank1.pack()

        lblank2 = tk.Label(self, text="", bg="black")
        lblank2.pack()
        self.button = tk.Button(self, text="Login", font=TEXT_FONT,fg="DeepPink4" ,command=lambda: controller.show_frame("StartPage"))
        self.button.pack()

        lblank = tk.Label(self, text="", bg="black")
        lblank.pack()
        
        self.button2 = tk.Button(self, text="Register Here", fg="blue", font=TEXT_FONT, 
                            command=lambda: controller.show_frame("Register"))
        self.button2.pack()

        
#main page----------------------
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="OliveDrab4")
        self.controller = controller
        label = tk.Label(self, text="Welcome!!", font=TITLE_FONT, bg="OliveDrab4")
        label.pack(side="top", fill="x", pady=10)

        lblank0 = tk.Label(self,text=" ", bg="OliveDrab4")
        lblank0.pack()

        self.luser = tk.Label(self, text="Username:", font=TEXT_FONT1, bg="OliveDrab4")
        self.luser.pack()
        self.euser = tk.Entry(self)
        self.euser.pack()

        self.lpass = tk.Label(self, text="Password:", font=TEXT_FONT1, bg="OliveDrab4")
        self.lpass.pack()
        self.epass = tk.Entry(self)
        self.epass.pack()

        lblank1 = tk.Label(self,text="  ", bg="OliveDrab4")
        lblank1.pack()
        lblank2 = tk.Label(self,text="  ", bg="OliveDrab4")
        lblank2.pack()
        button1 = tk.Button(self, text="Login",fg="green4", font=TEXT_FONT, 
                            command=self.display)
        button1.pack()
        lblank1 = tk.Label(self, bg="OliveDrab4")
        lblank1.pack()

        
        self.button2 = tk.Button(self, text="Register Here", fg="blue", font=TEXT_FONT, 
                            command=lambda: controller.show_frame("Register"))
        self.button2.pack()

        '''self.button3 = tk.Button(self, text="display", command=self.display)
        self.button3.pack()'''

        #imagee------
        l = tk.Label(self, text="",  font=('Ariel',10,'bold'))
        
        l.config(wraplength=300)
        l.config(justify=CENTER)
        l.config(foreground='white', background='black')
        mp = PhotoImage(file="dalja2.GIF")
        l.config(image=mp)
        l.image=mp
        l.config(compound="center")
        l.place(x=40, y=120)

        
        '''canvas = tk.Canvas(self)
        canvas.pack()

        self.photo = tk.PhotoImage(file = './start2.gif')

        canvas.create_image(7,0,image=self.photo)'''

        #function for verifying username and password-------------------
    def display(self):
        global pending
        #getting username nd password from entry fields-----------------
        print("edfdfdddffff")
        s.send("login")
        print("login sent")
        user=self.euser.get()
        print user
        s.send(user)
        time.sleep(1)
        password=self.epass.get()
        print password
        s.send(password)
        print("UV KA ATYACHAR")
        #SEND USERNAME TON SERVER
        
        status=s.recv(1024)
        print status
        print(status)
        
        if(status == "success"):
            print("You are Successfully Logged in")
            lim=s.recv(1024)
            if(lim=="new"):
                self.controller.show_frame("Login")
            elif(lim=="last"):
                pending="yes"
                print("Your Pending file should be downloaded first...")
                self.controller.show_frame("Download")
                
                
        #if(user=="baruni" and password=="bush"):
            #self.controller.show_frame("Login")
        else:
            print("Enter correct username and password")
            if(user!="baruni"):
                #self.errormsg = tk.Label(self, text="Enter correct username")
                #self.errormsg.pack()
                tkMessageBox.showinfo("", "Enter correct username")
            elif(password!="bush"):
                #self.errormsg = tk.Label(self, text="Enter correct password")
                #self.errormsg.pack()
                tkMessageBox.showinfo("", "Enter correct password")
        #clearing text in entry box on button click----------
            self.euser.delete(0, 'end')
            self.epass.delete(0, 'end')
            self.controller.show_frame("StartPage")
        
        
        
            
            
#home page frame-----------------------------------

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="dark turquoise")
        self.controller = controller
        label = tk.Label(self, text="Welcome User", font=TITLE_FONT, bg="dark turquoise")
        label.pack(side="top", fill="x", pady=10)

        self.lfname = tk.Label(self, text="Enter Filename:", font=TEXT_FONT1, bg="dark turquoise")
        self.lfname.pack()
        self.efname = tk.Entry(self)
        self.efname.pack()
        
        lblank0 = tk.Label(self , bg="dark turquoise")
        lblank0.pack()

        lftype = tk.Label(self, text="Select Filetype:", font=TEXT_FONT1, bg="dark turquoise")
        lftype.pack()

        self.v1 = tk.IntVar()

        self.C1 = Radiobutton(self, text="Text", variable=self.v1, value=1, height =2, width = 5 , bg="dark turquoise")
        self.C1.pack()

        self.C2 = Radiobutton(self, text="Image", variable=self.v1, value=2, height =2, width = 5 , bg="dark turquoise")
        self.C2.pack()

        self.C3 = Radiobutton(self, text="Music", variable=self.v1, value=3, height =2, width = 5 , bg="dark turquoise")
        self.C3.pack()

        self.C4 = Radiobutton(self, text="Video", variable=self.v1, value=4, height =2, width = 5 , bg="dark turquoise")
        self.C4.pack()

        lblank1 = tk.Label(self,text="  ", bg="dark turquoise")
        lblank1.pack(side=LEFT)
        lblank2 = tk.Label(self,text="                ", bg="dark turquoise")
        lblank2.pack(side=LEFT)
        lblank3 = tk.Label(self,text="                 ", bg="dark turquoise")
        lblank3.pack(side=LEFT)
        buttonop = tk.Button(self, text="CUSTOMIZE...",font=TEXT_FONT, bg="white",
                           command=self.options)
        buttonop.pack(side=LEFT)

        lblank4 = tk.Label(self,text="            ", bg="dark turquoise")
        lblank4.pack(side=LEFT)
        
        self.button_search = tk.Button(self, text="Search!!",font=TEXT_FONT, bg="white",
                   command=self.srch)
        self.button_search.pack(side=LEFT)
        
        lblank5 = tk.Label(self,text="         ", bg="dark turquoise")
        lblank5.pack(side=LEFT)

        self.button_news = tk.Button(self, text="Get News!!", font=TEXT_FONT, bg="white", command=self.news)
        self.button_news.pack(side=LEFT)
        lblank6 = tk.Label(self,text="              ", bg="dark turquoise")
        lblank6.pack(side=LEFT)
        self.buttondown = tk.Button(self, text="Direct Download",font=TEXT_FONT, bg="white",
                           command=self.dload)
        self.buttondown.pack(side=LEFT)

        lblank6 = tk.Label(self, bg="dark turquoise")
        lblank6.pack(side=BOTTOM)
        

        #imagee------
        l = tk.Label(self, text="",  font=('Ariel',10,'bold'))
        
        l.config(wraplength=300)
        l.config(justify=CENTER)
        l.config(foreground='white', background='dark turquoise')
        mp = PhotoImage(file="dalja3.GIF")
        l.config(image=mp)
        l.image=mp
        l.config(compound="center")
        l.place(x=600, y=100)

        #imagee------
        l = tk.Label(self, text="",  font=('Ariel',10,'bold'))
        
        l.config(wraplength=300)
        l.config(justify=CENTER)
        l.config(foreground='white', background='dark turquoise')
        mp = PhotoImage(file="dalja5.GIF")
        l.config(image=mp)
        l.image=mp
        l.config(compound="center")
        l.place(x=80, y=100)
        # ENTER WHERE SEARCH IS TO BE PUT HERE.......

        
    def options(self):
        global filename
        #s.send("cust")
        filename=self.efname.get()
        check=self.v1.get()
        print filename        
        #self.buttondown.config(state='disabled')
        print check
        self.controller.show_frame("Options")
        self.controller.frames["Options"].disable(check)

    def call_down(self):
        self.controller.show_frame("Download")

    
    def dload(self):
        global filename
        s.send("dload")
        filename=self.efname.get()
        print filename
        #time.sleep(2)
        #self.controller.frames["Download"].call_dload(fname)
        #thh=th.Thread(target=self.call_down)
        global prnt
        print "hello"
        self.controller.show_frame("Download")
        

    

    def news(self):
        global filename
        s.send("news")
        key=self.efname.get()
        s.send(key)
        
        new_lst=pickle.loads(s.recv(5000))
        newsname=key+" LATEST NEWS.txt"
        fileo=open(newsname,"w")
        for ro in new_lst:
            fileo.write(str(ro))
            print(ro)
            print("\n")
        fileo.close()
        print("FILE...DONE!!!")
        self.controller.show_frame("Login")


    def net(self):
        global filename
        s.send("yes")
        filename=s.recv(1024)
        print("net filename"+filename)
        self.efname.delete(0, 'end')
        self.efname.insert(0,filename)
        
    
        
    def srch(self):
        s.send("search") # THIS OPERATES WHILE LOOP AT SERVER..........
        search_key=self.efname.get()
        gen=str(self.v1.get())
        print "KEY: "+search_key
        lis=[]
        lis.append(gen)
        lis.append(search_key)
        s.send(pickle.dumps(lis))
        srch_res=s.recv(1024)
        if (srch_res=="no"):
            print("DOWNLOAD FROM NET!")
            butnet = Button(self, text="DOWNLOAD FROM NET!",font=TEXT_FONT, bg="white", command=self.net)
            butnet.pack(side=LEFT)
        elif(srch_res=="yes"):
            ans_srch=pickle.loads(s.recv(2048))
            j=0
            self.but = Button(self, text="OK", command=self.fn)
            self.but.pack(side=BOTTOM)
            self.var = StringVar(self)
            self.var.set(ans_srch[0])
            self.search = apply(OptionMenu, (self, self.var) + tuple(ans_srch))
            self.search.pack(side=BOTTOM)
            #value=var.get()
            #print(value)
            
            
    def fn(self):
        
        x=self.var.get()
        x=x[2:-3]
        self.efname.delete(0, 'end')
        self.efname.insert(0,x)
        self.search.destroy()
        self.but.destroy()
     
            
        
        
        
        
            
      
#register form--------------
class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="turquoise4")
        self.controller = controller
        label = tk.Label(self, text="Registration form", font=TITLE_FONT, bg="turquoise4", fg="white")
        label.pack(side="top", fill="x", pady=10)

        luser = tk.Label(self, text="Enter Username:", font=TEXT_FONT1,bg="turquoise4" )
        luser.pack()
        self.euser = tk.Entry(self)
        self.euser.pack()
        
        lpass = tk.Label(self, text="Passsword:", font=TEXT_FONT1,bg="turquoise4")
        lpass.pack()
        self.epass = tk.Entry(self)
        self.epass.pack()
        

        lcpass = tk.Label(self, text="Confirm Password:", font=TEXT_FONT1,bg="turquoise4")
        lcpass.pack()
        ecpass = tk.Entry(self)
        ecpass.pack()

        self.lemail = tk.Label(self, text="Enter Email address:", font=TEXT_FONT1,bg="turquoise4")
        self.lemail.pack()
        self.eemail = tk.Entry(self)
        self.eemail.pack()
        

        lblank = tk.Label(self, bg="turquoise4")
        lblank.pack()
        
        button = tk.Button(self, text="Register Me", font=TEXT_FONT,
                           command=self.mail)
        button.pack()
        

#sending mail on registration---------------
    def mail(self):
        s.send("r")
        print("Registration Successful!!")
        usern=self.euser.get()
        passs=self.epass.get()
        s.send
        mailid=self.eemail.get()
        sender = 'pkkb3110@gmail.com'
        #receivers ='barunimalhotra1995@gmail.com'
        password = 'neeti-13102347'
        #sender = raw_input('Username: ')
        #password = raw_input('Password: ')
        #receivers = raw_input('Recipient: ')
        receivers = mailid


        message = """From: From BUSH
        To: To Person 
        Subject: SMTP e-mail test

        HII mail from minor :p
        baruni.
        """

        try:
           smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
           smtpObj.ehlo()
           smtpObj.starttls()
           smtpObj.ehlo()
           smtpObj.login(sender, password)
           smtpObj.sendmail(sender, receivers, message)
           print "Successfully sent email"
           smtpObj.quit()
           
           
        except smtplib.SMTPException:
           print "Error: unable to send email"

        self.controller.show_frame("Login")
        
        

#frame with customization options-----------------
class Options(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="SpringGreen4")
        self.controller = controller

        lblank0 = tk.Label(self, text="                               ", bg="SpringGreen4")
        lblank0.grid(row=0, column=0)
        lblank1 = tk.Label(self, text="                                               ", bg="SpringGreen4")
        lblank1.grid(row=0, column=4)

        label = tk.Label(self, text="You Think We Deliver!!", font=TITLE_FONT1, fg="red", bg="SpringGreen4")
        label.grid(row=0, column=2)

        lblank2 = tk.Label(self, text="                                               ", bg="SpringGreen4")
        lblank2.grid(row=1, column=1)

        #for encryption--------------------
        lencrypt=tk.Label(self, text="Encrypt your data?", font=TEXT_FONT1, bg="SpringGreen4")
        lencrypt.grid(row=2, column=1)
        self.v = IntVar()
        self.rr1 = Radiobutton(self, text="Yes", variable=self.v, value=1, bg="SpringGreen4")
        self.rr1.grid(row=2, column=2)
        self.rr2 = Radiobutton(self, text="No", variable=self.v, value=2,bg="SpringGreen4" )
        self.rr2.grid(row=2, column=3)

        #for compression--------------------
        lblank3 = tk.Label(self, text="", bg="SpringGreen4")
        lblank3.grid(row=3, column=0)
        lcompres=tk.Label(self, text="Compress your data?", font=TEXT_FONT1, bg="SpringGreen4")
        lcompres.grid(row=4, column=1)
        self.v1 = IntVar()
        self.r1 = Radiobutton(self, text="Yes", variable=self.v1, value=1, bg="SpringGreen4")
        self.r1.grid(row=4, column=2)
        self.r2 = Radiobutton(self, text="No", variable=self.v1, value=2, bg="SpringGreen4")
        self.r2.grid(row=4, column=3)

        #quality parameter-----------------------------
        lblank4 = tk.Label(self, text="", bg="SpringGreen4")
        lblank4.grid(row=5, column=0)
        lcompres=tk.Label(self, text="Quality Meter :", font=TEXT_FONT1, bg="SpringGreen4")
        lcompres.grid(row=6, column=1)
        self.v2 = IntVar()
        self.meter = tk.Scale(self, from_=0, to=100, orient=HORIZONTAL,variable=self.v2,length=250, width=20, bg="SpringGreen4")
        self.meter.set(100)
        self.meter.grid(row=6, column=2)

        #duration customization-------------------
        lblank5 = tk.Label(self, text="", bg="SpringGreen4")
        lblank5.grid(row=7, column=0)
        ldur=tk.Label(self, text="Customize Data Duration", font=TEXT_FONT1, bg="SpringGreen4")
        ldur.grid(row=8, column=1)

        lstart = tk.Label(self, text="start time:", bg="SpringGreen4")
        lstart.grid(row=8, column=2)
        self.estart = tk.Entry(self)
        self.estart.grid(row=9, column=2)
        lstart1 = tk.Label(self, text="(hh:mm:ss)", bg="SpringGreen4")
        lstart1.grid(row=10, column=2)
        
        lend = tk.Label(self, text="end time:", bg="SpringGreen4")
        lend.grid(row=8, column=3)
        self.eend = tk.Entry(self)
        self.eend.grid(row=9, column=3)
        lend1 = tk.Label(self, text="(hh:mm:ss)", bg="SpringGreen4")
        lend1.grid(row=10, column=3)

        lblank6 = tk.Label(self, text="", bg="SpringGreen4")
        lblank6.grid(row=11, column=0)
        

        button = tk.Button(self, text="Back to Home Page", font=TEXT_FONT,
                           command=lambda: controller.show_frame("Login"))
        button.grid(row=12, column=2)
        bdown = tk.Button(self, text="Download", font=TEXT_FONT,
                           command=self.exec_opt)
        bdown.grid(row=12, column=3)
    def exec_opt(self):
        global filename,genre
        s.send("cust")
        time.sleep(0.2)
        varr=s.recv(1024)
        time.sleep(0.2)
        if(varr=="incust"):
            
            checklist=["no","no","no","no","","","","","",genre]
            encr=self.v.get()
            compr=self.v1.get()
            qual=self.v2.get()
            start=self.estart.get()
            start=str(start)
            end=self.eend.get()
            end=str(end)
            print start
            print end
            checklist[4]=start
            checklist[5]=end
            checklist[6]=compr
            checklist[7]=qual
            checklist[8]=filename
            if encr==1:
                checklist[0]="yes"
            
            
            if start!="" and end !="":
                checklist[1]="yes"
                #subprocess.call(['C:/ffmpeg/bin/ffmpeg.exe', '-i', fname , '-ss', start, '-t', end , '-async', '1',"cut_"+fname ])
            if compr == 1:
                checklist[2]="yes"
                '''new_filename=fn+".gz"
                with open(fn, 'rb') as f_in, gzip.open(new_filename, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                #NEW FILENAME SEND FROM HERE
                fname=new_filename
                '''
            if qual != 100:
                checklist[3]="yes"
                '''print qual
                image = Image.open(fname)
                image.save("new_"+fname,quality=qual,optimize=True)
                '''
            
            s.send(pickle.dumps(checklist))
            filename=pickle.loads(s.recv(1024))
            print "cust filename: "+filename
            s.send("dload")
            self.controller.show_frame("Download")
            
    def disable(self,x):
        print "hello"
        global genre
        if x == 1:    
            self.r1.config(state='disabled')
            self.r2.config(state='disabled')
            self.meter.config(state='disabled')
            self.estart.config(state='disabled')
            self.eend.config(state='disabled')
            self.rr1.config(state='normal')
            self.rr2.config(state='normal')
            
        elif x == 2:
            self.r1.config(state='disabled')
            self.r2.config(state='disabled')
            self.estart.config(state='disabled')
            self.eend.config(state='disabled')
            self.meter.config(state='normal')
            self.rr1.config(state='normal')
            self.rr2.config(state='normal')
        elif x == 3:
            self.r1.config(state='disabled')
            self.r2.config(state='disabled')
            self.rr1.config(state='disabled')
            self.rr2.config(state='disabled')
            self.meter.config(state='disabled')
            self.estart.config(state='normal')
            self.eend.config(state='normal')
            genre=3
        elif x == 4:
            self.rr1.config(state='disabled')
            self.rr2.config(state='disabled')
            self.r1.config(state='normal')
            self.r2.config(state='normal')
            self.meter.config(state='normal')
            self.estart.config(state='normal')
            self.eend.config(state='normal')
            genre = 4
            
            
            
#download page------------------------
class Download(tk.Frame):

    def __init__(self, parent, controller):
        global thrd
        global pending
        tk.Frame.__init__(self, parent, bg="indian red")
        self.controller = controller
        lblank0 = tk.Label(self, text="                                                                                     ", bg="indian red")
        lblank0.grid(row=0, column=0)
        label = tk.Label(self, text="Downloading...", font=TITLE_FONT1, bg="indian red")
        label.grid(row=0, column=2)
        

        
        
        self.bytes = 0
        self.maxbytes = 0
        
        #progress bar
        lblank1 = tk.Label(self, text="                                          ", bg="indian red")
        lblank1.grid(row=1, column=2)
        lblank2 = tk.Label(self, text="                                            ", bg="indian red")
        lblank2.grid(row=2, column=2)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=3, column=2)
        #thrd=th.Thread(target=self.butts)

        lblank3 = tk.Label(self, text="", bg="indian red")
        lblank3.grid(row=4, column=2)

        sstart = tk.Button(self, text="Start", font=TEXT_FONT,
                           command=self.start)
        sstart.grid(row=5, column=1)
 
            
        
        button = tk.Button(self, text="QUIT!!!", font=TEXT_FONT,
                           command=self.quuit)
        button.grid(row=5, column=4)

        '''button = tk.Button(self, text="QUIT!!!", font=TEXT_FONT,
                           command=self.quuit)
        button.grid(row=9, column=2)'''
        

    def paus(self):
        global pasv
        print "Do you want to pause?"
        while True:
            pasv=str(raw_input())
    def quuit(self):
        app.destroy()
        sys.exit()
        #global app
        #app.quit()
        #ex_pro()

        
    def butts(self):
        bstart = tk.Button(self, text="Resume", font=TEXT_FONT,
                           command=self.paus_no)
        bstart.grid(row=5, column=2)
        bpause = tk.Button(self, text="Pause", font=TEXT_FONT,
                           command=self.paus_yes)
        bpause.grid(row=5, column=3)
            


    def res_pen(self):
        global pending
        print("IN RESUME PENDING..")
        flst=s.recv(1024)
        flist = pickle.loads(flst)
        fnam=flist[0]
        size=flist[1]
        f = open("new_"+fnam,"a")
        totalRecv = os.path.getsize("new_"+fnam)
        data=s.recv(1024)
        
        f.write(data)
        #print(data)
        totalRecv += len(data)
        
        while(totalRecv < size):
            data = s.recv(1024)
            totalRecv += len(data)
            f.write(data)
            print totalRecv
        print("received!!")
        pending="no"
        self.controller.show_frame("Login")
        
        
        
#************DOWNLOADING STARTED********************
    def start(self):
        global filename,prnt,connected,pending,pasv
        
        thrd=threading.Thread(target = self.paus)
        thrd.start()
        if(pending=="yes"):
            self.res_pen()
        else:
            if(filename != 'q'):
                time.sleep(1)
                s.send(filename)
                saved=s.recv(1024)
                time.sleep(1)
                print(saved)
                data = s.recv(1024)
                #data = pickle.loads(data1)
                if(data[:6] == 'Exists'):
                    filesize = int(data[6:])
                    print ("File Exists. " + str(filesize)+ "Bytes,download? ")
                    '''self.progress["value"] = 0
                    self.maxbytes = 50000
                    self.progress["maximum"] = 50000
                    self.read_bytes()
                    '''
                    
                    s.send('OK')
                    
                    start_tym=time.time()
                    data = s.recv(1024)
                    if(data=="exceed"):
                        print("LIMIT EXCEEDED")
                        time.sleep(1)
                        self.quuit()
                    #data = pickle.loads(data1)
                    else:
                        f = open("new_"+filename, "wb")
                        totalRecv = len(data)
                        f.write(data)
                        #thrd.start()
                        while(totalRecv < filesize):
                            if(pasv=="no"):
                                if(prnt==2):
                                    print "Downloading Resumed..."
                                prnt=1
                                data = s.recv(1024)
                                if(data=="exceed"):
                                    print("LIMIT EXCEEDED")
                                    time.sleep(1)
                                    self.quuit()
                                else:
                                    totalRecv += len(data)
                                    f.write(data)
                            elif(pasv=="yes"):
                                if(prnt==1):
                                    print("Downloading Paused...")
                                    prnt=2
                                elif(prnt==2):
                                    continue
                        
                    
                        print("Download Complete")
                        end_tym=time.time()
                        print("Time Taken: ",(end_tym-start_tym))
                        #self.quuit()
                        
                        
                else:
                    print("File does not Exist at SERVER!!")
                    add=s.recv(1024)
                    print(add)
                    if(add==""):
                        s.send("yes")
                        print("sent yes to response")
                    elif(add!=""):
                        s.send("no")
                        connected="yes"
                        ctoc(add,filename,"")
                    
                
        
    

    def Stop(self):
        self.progress.stop()

        


if __name__ == "__main__":
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = "192.168.173.1"
    host=socket.gethostname()
    port = 33333
    s.connect((host,port))
    broad()
    app = SampleApp()
    app.mainloop()
