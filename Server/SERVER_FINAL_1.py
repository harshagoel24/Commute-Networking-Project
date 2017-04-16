#from __future__ import unicode_literals
import os,threading,socket,pickle
import subprocess
import gzip,shutil
import psycopg2,time,random
from PIL import Image
import urllib
import youtube_dl
import encoder
#set client_encoding to 'latin1'
parind=0
def new(chunk,pin):
    ind_fin=chunk.find(pin)
    ind_fin += len(pin) + 4 
    last=chunk.find("\"",ind_fin)
    headline=chunk[ind_fin:last]
    return headline

def para(chunk,ind):
    global parind
    ind_fin=chunk.find("<p>",ind)
    
    ind_fin += 3
    parind = ind_fin
    last=chunk.find("</p>",ind_fin)
    headline=chunk[ind_fin:last]
    return headline
path="C:/FTP"     ###### path of shared forder of serevr
currdate=time.strftime('%Y/%m/%d')
try:
    conn=psycopg2.connect(database="commute",user="postgres",password="harsha",host="localhost",port="8000")
except:
    print "Unable to connect to the database..."
checklist=list()
curs=conn.cursor()
curs.execute("select * from lastupdate")
row=curs.fetchone()
lastmodify=row[0]
fid=1

for root, dirs, files in os.walk(path):
    for file in files:
        filename = os.path.join(root,file)
        nameoffile = file
        temp=file
        size = os.path.getsize(filename)
        ex=temp.split('.')
        extension=ex[-1]
        modifydate=os.path.getmtime(filename)
        curs.execute("select * from files where fname= %s",(nameoffile,))
        if(curs.rowcount==1):
            if(modifydate>=lastmodify):
                curs.execute("update files set size= %s,address = %s where fname=%s",(size,filename,nameoffile,))

        else:
            curs.execute("select * from files order by fid desc limit 1")
            if(curs.rowcount>0):
                
                rowss=curs.fetchone()
                fid=rowss[0]+1
                #print nameoffile,' ',size,' ',extension,' ',filename
            curs.execute("Insert into files(fid,fname,ext,size,address) values (%s, %s, %s, %s, %s)",(fid,nameoffile,extension,size,filename,))

curs.execute("update lastupdate set lastupdate=%s where lid=1",(currdate,))        

conn.commit()


def broad(msg):
    connect="no"
    dest = ('<broadcast>', 5000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(msg,dest)
    address1=""
    flag=0
    tm=time.time()
    cnt=0
    
    while True:

        (buf, address) = s.recvfrom(2048)
        print "Received from %s: %s" % (address, buf)
        s.sendto(connect,address)
        if(buf=="yes" and flag==0):
            address1=address
            connect="yes"
            flag=1
            break

    return address1

############update files#######

def update(filename):
        nameoffile = filename
        temp=filename
        size = os.path.getsize(filename)
        ex=temp.split('.')
        extension=ex[-1]
        add=os.getcwd()+'/'+filename
        curs.execute("select * from files order by fid desc limit 1")
        if(curs.rowcount>0):
            rowss=curs.fetchone()
            fid=rowss[0]+1
            curs.execute("Insert into files(fid,fname,ext,size,address) values (%s, %s, %s, %s, %s)",(fid,nameoffile,extension,size,add,))
            conn.commit()





############LOGIN##########

def login(sock):
    print("********")
    
    username=sock.recv(1024)
    print "usern: "+username
    time.sleep(1)
    password=sock.recv(1024)
    print "pass: "+password
    #print username
    print("HARSHA KA ATYACHAR!!")
    
    
    curs.execute("select * from users where name= %s and password= %s", (username,password))
            
    #to check the if the user is in the database
    #try:
    
    #except:
        #print("not able to run")
    if(curs.rowcount==1):
        sock.send("success")
        print("success")
        row=curs.fetchone()
        uid=row[0]
        #datalimit = row[]
        
        print("LOGIN SUCCESSFUL")
        
        return uid
    else:
        sock.send("Register Yourself")
        
        
        x=sock.recv(1024)
        if(x=="login"):
            login(name,sock)
        elif(x=="register"):
            register(name,sock)
        
    


############ REGISTER##########

def register(name,sock):
    print "IN register function.."
    username = sock.recv(1024)
    try:
        curs.execute("select * from users where name= %s", (username,))
    except:
        print("not executed")
    if(curs.rowcount>0):
        sock.send("username already exist")
        register(name,sock)
    else:
        sock.send("Approved")
        pas= "notmatch"
        while(pas=="notmatch"):
            password = sock.recv(1024)
            confirmpass = sock.recv(1024)
            if(password != confirmpass):
                sock.send("notmatch")
                pas="notmatch"
            else:
                pas="match"
                sock.send("Password Confirmed")
                uid=1
                try:
                    curs.execute("select * from users order by id desc limit 1")
                except:
                    print("unable to execute desc query")
                if(curs.rowcount>0):
                    row=curs.fetchone()
                    uid=row[0]+1
                key=random.randrange(10000,99999)
                curs.execute("insert into users values(%s,%s,%s,0,500000000,%s)",(uid,username,password,key,))
                sock.send("You Are Successfully Registered..!! \n")
                sock.send(str(key))# PLEASE ENTER REGISTRATRYKON KEY.....
                conn.commit()
        uid=login(name,sock)
        return uid

############ SENTF DATABASE##########
####### every time u send the file call function as
##########sentf(uid,fid)

def sentf(uid,fid):
    senddate= time.strftime("%x")
    curs.execute("insert into sentf values (%s,%s,%s)",(uid,fid,senddate,))
    conn.commit()
        

############ CHECKING DATA LIMIT##########
######### to call the function
####### allowlimit = checklimit(uid,filesize1)
###### and condition on allowlimit if 1 allow sending else pause

def checklimit(uid,size):
    usage=0
    currdate= time.strftime("%x")
    curs.execute("select * from sentf where uid=%s and sendingdate=%s",(uid,currdate,))
    rows=curs.fetchall()
    for row in rows:
        fidd=row[1]
        curs.execute("select * from files where fid=%s",(fidd,))
        filerow=curs.fetchone()
        usage=usage+filerow[3]
    allow=50000-usage      ##!@#$^%$#@@#$  DECREASE LIMIT WHEN WANTED
    if(allow>size):
        return 1
    else:
        return allow



def internet(sock,genr,skey):
    print genr
    ret_link=""
    red=""
    
    print "Youtube"
    link="https://www.youtube.com/results?search_query="
    key=skey
    key.replace(" ","+")
    back="https://www.youtube.com"
    tot=link+key
    handle = urllib.urlopen(tot)
    html_gunk = handle.read()
    fin="/watch?v="
    res="\""
    ind=html_gunk.find(fin)
    las=html_gunk.find(res,ind)
    id_vid=html_gunk[ind:las]
    ret_link=back+id_vid
    print(ret_link)
    red=str(ret_link)
    print(red)
    #namee=id_vid+"webm"
    #print(namee)
    if genr=='4':

        
        ydl = youtube_dl.YoutubeDL({'preferredcodec': 'mp4'})

        with ydl:
            result = ydl.extract_info(
                red,
                download=True # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        #print(video)
        video_url = video['title']
        print(video_url)
        print(video['ext'])
        namee=""
        namee=str(video_url)+"-"+str(id_vid[9:])+"."+str(video['ext'])
        
        nm=namee.replace("|","_")
        print(nm)
        newname=str(skey)+".mp4"
        os.rename(nm,newname)
        update(newname)
        sock.send(newname)
        
        
    elif genr=='3':
        ydl = youtube_dl.YoutubeDL({'format': 'bestaudio/best', # choice of quality
        'extractaudio' : True,      # only keep the audio
        'audioformat' : "mp3"})

        with ydl:
            result = ydl.extract_info(
                red,
                download=True # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        #print(video)
        video_url = video['title']
        print(video_url)
        print(video['ext'])
        namee=""
        namee=str(video_url)+"-"+str(id_vid[9:])+"."+str(video['ext'])
        print(namee)
        nm=namee.replace("|","_")
        print(nm)
        newname=str(skey)+".webm"
        os.rename(nm,newname)
        update(newname)
        sock.send(newname)

    
    








def search(sock):
    extt=''
    gen=pickle.loads(sock.recv(1024))
    if gen[0]==1:
        extt='txt'
    elif gen[0]==2:
        extt='jpg'
    elif gen[0]==3:
        extt='mp3'
    elif gen[0]==4:
        extt='mp4'
    exx='%'+gen[1]+'%'
    curs.execute("select distinct fname from files where ext= %s or fname like %s", (extt,exx))
    if(curs.rowcount>0):
        sock.send("yes")
        row_s=curs.fetchall()
        for rr in row_s:
            print rr
        sock.send(pickle.dumps(row_s))
        print "GENRE: "+gen[0]+gen[1]
    else:
        print("CLIENT m bhi yahi h...")
        sock.send("no")
        net=sock.recv(1024)
        if (net=="yes"):
            internet(sock,gen[0],gen[1])
            
        


def news(sock):
    key=sock.recv(1024)
    print(key)
    new_list=list()
    global parind
    link="http://news.google.com/news/section?q="
    fil=str(key)
    key.replace(" ","+")


    tot=link+key
    handle = urllib.urlopen(tot)
    html_gunk = handle.read()
    fin="http://indiatoday.intoday.in"
    res="\""
    ind=html_gunk.find(fin)
    las=html_gunk.find(res,ind)
    id_vid=html_gunk[ind:las]
    ret_link=id_vid


    ret_news = urllib.urlopen(ret_link)
    html_chunk = ret_news.read()
    #print(html_chunk)
    sen=str(html_chunk)
    hd=new(sen,"headline")
    dat=new(sen,"datePublished")
    nl="\n"
    parlst=list()
    parlst.append(para(sen,0))
    for i in range(10):
        parlst.append(para(sen,parind))
    heads="HEADLINES: "+hd
    new_list.append(heads+str(nl))
    dated="DATE: "+dat
    new_list.append(dated+str(nl))
    for pad in parlst:
        if(('<a' in pad)or('http' in pad)or('<b' in pad)):
            continue
        else:
            parag="  -->  "+pad
            new_list.append(parag+str(nl))
    print(new_list)
            
    sock.send(pickle.dumps(new_list))
    

def get_addr(keyfile):
    curs.execute("select address from files where fname= %s", (keyfile,))
    if(curs.rowcount>0):
        row_s=curs.fetchone()
        return row_s[0]
    
    
    

def cust(sock):
    global checklist
    time.sleep(0.2)
    sock.send("incust")
    time.sleep(0.2)
    checklist=pickle.loads(sock.recv(1024))
    print checklist
    add_file=get_addr(checklist[8])
    if checklist[0]=="yes":
        print("NOW ENCRYPTING...")
        f=open(add_file,"r")
        mg=f.readlines()
        f.close()
        var1="new_enc_"+checklist[8]
        f=open(var1,"w")
        for i in range(len(mg)):
            print(mg[i],i)
            rr=encoder.encoder(mg[i])
            for k in range(len(rr)):
                if rr[k]!="\n":
                    f.write(rr[k])
            f.write("\n")
        print("done encoding text")
        f.close()
        checklist[8]=var1
        update(var1)

        
    
    if checklist[1]=="yes":
        subprocess.call(['C:/ffmpeg/bin/ffmpeg.exe', '-i', checklist[8] , '-ss', checklist[4], '-t', checklist[5] , '-async', '1',"cut_"+checklist[8] ])
        checklist[8]="cut_"+checklist[8]
        
    if checklist[3]=="yes":
        if checklist[9] == 3 or checklist[9]==4:
            subprocess.call(['C:/ffmpeg/bin/ffmpeg.exe', '-i', checklist[8], '-c:v', 'libx264', '-crf', '24', '-b:v', '1M', '-c:a', 'aac', 'low_'+checklist[8]])
        else:
            image = Image.open(checklist[8])
            image.save("low_"+checklist[8],quality=checklist[7],optimize=True)
        checklist[8]="low_"+checklist[8]
        
    if checklist[2]=="yes":
        new_filename=checklist[8]+".gz"
        with open(checklist[8], 'rb') as f_in, gzip.open(new_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        #NEW FILENAME SEND FROM HERE
        checklist[8]=new_filename
    update(checklist[8])
    sock.send(pickle.dumps(checklist[8]))


def after_sent(uid,fid):
    curs.execute("delete from pending where uid = %s and fid = %s",(uid,fid,))
    conn.commit()
    

def up_sent(uid,fid,packetsent):
    curs.execute("select * from files where fid=%s",(fid,))
    filerow=curs.fetchone()
    size=filerow[3]
    z=0
    curs.execute("Insert into pending(uid,fid,packetleft,packetsent) values (%s, %s, %s, %s)",(uid,fid,z,packetsent,))
    conn.commit()


def send_pending(uid,sock,fidd,pax):
    lst=list()
    curs.execute("select * from files where fid=%s",(fidd,))
    rr=curs.fetchone()
    fnam=rr[1]
    fad=rr[5]
    lst.append(fnam)
    
    fsize=os.path.getsize(fad)
    lst.append(fsize)
    
    sock.send(pickle.dumps(lst))
    with open(fad, "rb") as f:
        bytesent=1024*(pax-1)
        bytesToSend = f.read(bytesent)
        while(bytesToSend != ""):
            bytesToSend = f.read(1024)
            sock.send(bytesToSend)
    after_sent(uid,fidd)
    sentf(uid,fidd)
    
    



def Retrfile(name,sock):
    global checklist
    sign=sock.recv(1024)
    print(sign+"received..")
    
    if (sign=="login"):
        print("rec LLL")
        
        uid=login(sock)
        print("uid recv: "+str(uid))
        
        print("successfully logged in!! UID: "+str(uid))
        
        curs.execute("select * from pending where uid=%s",(uid,))
        if(curs.rowcount>0):
            sock.send("last")
            row=curs.fetchone()
            fidd=row[1]
            pacs=row[3]
            print(fidd)
            send_pending(uid,sock,fidd,pacs)
        else:
            sock.send("new")
            
    elif (sign=="r"):
        uid=register(name,sock)
    while(True):
        check=sock.recv(1024)
        if check=="search":
            search(sock)
        elif check=="cust":
            cust(sock)
        elif check=="news":
            news(sock)
        elif check=="internet":
            internet(sock)
            
        elif check=="dload":
            print(check)
            break
            
    
    time.sleep(1)
    filename = sock.recv(1024)
    time.sleep(1)
    #filename = pickle.loads(filename1)
    print("file: "+filename)
    curs.execute("select * from files where fname=%s",(filename,))
    if(curs.rowcount>0):
        row=curs.fetchone()
        size=row[3]
        fid=row[0]
        f_add=row[5]
        x="Exists"+str(size)
        sock.send(x)
        userResponse=sock.recv(1024)
        pac_sent=0
        #userResponse=pickle.loads(userResponse1)
        print(userResponse)
        if(userResponse[:2] == 'OK'):
            allowlimit=checklimit(uid,size)  #if allowlimit==1 then send whole file
            print(allowlimit)
            if(allowlimit==1):
                with open(f_add, "rb") as f:
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
                    while(bytesToSend != ""):
                        #print(bytesToSend)
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)
                    print "FILE SENT..."
                    sentf(uid,fid)
                    
            else:
                print(allowlimit)
                print("IN ELSE OF CHECK LIMIT")
                with open(f_add, "rb") as f:
                    bytesToSend = f.read(1024)
                    if(allowlimit>0):
                        sock.send(bytesToSend)
                        pac_sent+=1
                        while(bytesToSend != ""):
                            allowlimit-=1024
                            #print(bytesToSend)
                            bytesToSend = f.read(1024)
                            if(allowlimit>1024):
                                sock.send(bytesToSend)
                                pac_sent+=1
                                print("pac sent..."+str(pac_sent))
                            else:
                                print("FILE STOPPED SINCE LIMIT EXCEEDED pac sen: "+str(pac_sent))
                                up_sent(uid,fid,pac_sent)
                                break;
                    else:
                        print("FILE STOPPED SINCE LIMIT EXCEEDED pac sen: "+str(pac_sent))
                        up_sent(uid,fid,pac_sent)
                    sock.send("exceed")
                        
                
            
    else:
        print "SERVER DOESNT HAVE IT!!!"
        sock.send("server doesn't have it")
        addressrecv,port=broad(filename)
        print("addres recv: "+addressrecv)
        sock.send(addressrecv)

        resp=sock.recv(1024)

        if resp=="yes":
            print("response yes...")
            

        

    sock.close()
    return
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 33333

s.bind((host,port))
s.listen(5)
print("Server Started")
while(True):
    c,addr = s.accept()
    print("Client Connected :",addr)
    t=threading.Thread(target = Retrfile, args=("retrThread",c))
    t.start()
s.close()
