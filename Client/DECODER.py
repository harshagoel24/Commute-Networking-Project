import sys
def decoder(enc):
    leng=len(enc)-1
    msg_f=[]
    msg_s=[]
    msg_t=[]
    ans=[]
    dep=4
    q=leng/dep
    q=int(q)+1
    ind=0
    for i in range(q):
        msg_f.append(enc[i])
        ind+=1
    var=2
    c=0
    while (var<=leng):
        var=var+dep
        c+=1
    last=leng-c
    for i in range(last+1,leng+1):
        msg_t.append(enc[i])    

    for i in range(q,last+1):
        msg_s.append(enc[i])
    f=0
    s=0
    t=0
    for i in range(leng+1):
        if(i%4==0):
            ans.append(msg_f[f])
            f+=1
        elif((i%2)>0):
            ans.append(msg_s[s])
            s+=1
        else:
            ans.append(msg_t[t])
            t+=1
    return(ans)

name=raw_input("Enter File to be DECODED!!!")
fname=str(name)
filo=open(fname,"r")
enc=filo.readlines()

varr="decryp_"+fname
fil=open(varr,"w")
for i in range(len(enc)):
    enc[i]=enc[i][:-1]
    neww=decoder(str(enc[i]))
    for k in range(len(neww)):
        fil.write(str(neww[k]))
    fil.write("\n")
fil.close()


print("FILE DECRYPTED!!...BYE")

sys.exit("TATA!!")
