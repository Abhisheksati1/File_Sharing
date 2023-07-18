from tkinter import *
import socket
from tkinter import filedialog
from tkinter import messagebox
import os

root=Tk()
root.title("Shareit")
root.geometry("450x576+500+100")
root.configure(bg="#f4fdfe")
root.resizable(False,False)

def Send():
    window=Toplevel(root)
    window.title("send")
    window.geometry('450x560+500+100')
    window.configure(bg="#f4fdfe")
    window.resizable(False,False)

    filename = str()

    def select_file():
        '''askopenfilename function is from the filedialog module of the tkinter
           initialdir=os.getcwd(): This sets the initial directory that is displayed when the file dialog box opens to the current working directory. os.getcwd() retrieves the current working directory.
           title='Select Image File': This sets the title of the file dialog box to "Select Image File".
           filetype=(('file_type','*.txt'),('all files','*.*')): This sets the file types that are displayed in the file dialog box. The first element in each tuple is the file type description, and the second element is the file extension.'''
        nonlocal filename
        filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Select Image File',
                                            filetype=(('file_type','*.txt'),('all files','*.*')))           
    def Sender():
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(host)
        print('Waiting for any incoming connections....')

        while True:
            try:
                conn, addr = s.accept()
                break
            except ConnectionResetError:
                print('Connection reset. Retrying...')

        with open(filename, 'rb') as file:
            while True:
                try:
                    file_data = file.read(4096)
                    if not file_data:
                        break

                    conn.sendall(file_data)
                except ConnectionResetError:
                    print('Connection reset. Retrying...')
                    conn.close()
                    while True:
                        try:
                            conn, addr = s.accept()
                            break
                        except ConnectionResetError:
                            print('Connection reset. Retrying...')

        conn.close()
        print("Data has been transmitted successfully")


    #icon
    image_icon1=PhotoImage(file="image/share-icon.png")
    window.iconphoto(False,image_icon1)

    sbackground=PhotoImage(file="image/sender.png")
    Label(window,image=sbackground).place(x=-2,y=0)

    Mbackground=PhotoImage(file="image/id.png")
    Label(window,image=Mbackground,bg="#f4fdfe").place(x=100,y=260)

    host=socket.gethostname()
    Label(window,text=f'ID: {host}',bg='white',fg='black').place(x=140,y=290)
    

    Button(window,text="+ select file",width=10,height=1,font="arial 14 bold",bg="#fff",fg="#000",command=select_file).place(x=160,y=150)    
    Button(window,text="SEND",width=8,height=1,font='arial 14 bold',bg='#000',fg="#fff",command=Sender).place(x=300,y=150)

    window.mainloop()

def Receive():
    main=Toplevel(root)
    main.title("Receive")
    main.geometry('450x560+500+100')
    main.configure(bg="#f4fdfe")
    main.resizable(False,False)

    def receiver():
        ID = SenderID.get()
        filename1 = incoming_file.get()

        s = socket.socket()
        port = 8080

        while True:
            try:
                s.connect((ID, port))
                break
            except ConnectionResetError:
                print('Connection reset. Retrying...')

        with open(filename1, 'wb') as file:
            while True:
                try:
                    file_data = s.recv(4096)
                    if not file_data:
                        break

                    file.write(file_data)
                except ConnectionResetError:
                    print('Connection reset. Retrying...')
                    s.close()
                    while True:
                        try:
                            s = socket.socket()
                            s.connect((ID, port))
                            break
                        except ConnectionResetError:
                            print('Connection reset. Retrying...')

        s.close()
        print("File has been received successfully")


    #icon
    image_icon1=PhotoImage(file="image/recieve.png")
    main.iconphoto(False,image_icon1)

    Hbackground=PhotoImage(file="image/receiver.png")
    Label(main,image=Hbackground).place(x=2,y=0)
    
    logo=PhotoImage(file="image/pofile.png")
    Label(main,image=logo,bg="#f4fdfe").place(x=100,y=280)

    Label(main,text="Recieve",font=('arial',20),bg='#f4fdfe').place(x=100,y=250)

    Label(main,text="Input Sender ID",font=('arial',10,'bold'),bg='#f4fdfe').place(x=20,y=340)
    SenderID=Entry(main,width=25,fg="black",border=2,bg='white',font=('arial',15))
    SenderID.place(x=20,y=370)
    SenderID.focus()

    Label(main,text="Filename for incoming file:",font=('arial',10,'bold'),bg='#f4fdfe').place(x=20,y=420)
    incoming_file=Entry(main,width=25,fg="black",border=2,bg='white',font=('arial',15))
    incoming_file.place(x=20,y=450)

    imageicon=PhotoImage(file="image/done.png")
    rr=Button(main,text="Receive",compound=LEFT,image=imageicon,width=130,bg='#39c790',font="arial 14 bold",command=receiver).place(x=20,y=500)
           
    main.mainloop()


#icon
image_icon=PhotoImage(file="image/icon.png")
root.iconphoto(False,image_icon)

Label(root,text="File Transfer",font=('Acumin Variable Concept',20,'bold'),bg="#f4fdfe").place(x=20,y=30)

Frame(root,width=400,height=2,bg="#f3f5f6").place(x=25,y=80)

send_image=PhotoImage(file="image/send.png")
send=Button(root,image=send_image,bg="#f4fdfe",bd=0,command=Send)
send.place(x=50,y=100)


receive_image=PhotoImage(file="image/recieve.png")
receive=Button(root,image=receive_image,bg="#f4fdfe",bd=0,command=Receive)
receive.place(x=300,y=100)

#label
Label(root,text="Send",font=('Acumin Varible Concept', 17, 'bold'),bg="#f4fdfe").place(x=65,y=200)
Label(root,text="Recieve",font=('Acumin Varible Concept', 17, 'bold'),bg="#f4fdfe").place(x=300,y=200)


background=PhotoImage(file="image/background.png")
Label(root,image=background).place(x=-2,y=323)

    

root.mainloop()
