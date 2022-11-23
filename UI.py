from tkinter import *
from tkinter import font
import re
import tkinter.messagebox
from utils2.server import *
from PIL import ImageTk, Image

class FirstPage(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.geometry("480x480")
        self.title('P2P ChatApp')
        
        # Homepage - logo
        img = ImageTk.PhotoImage(Image.open("logo.png").resize((560,420)))
        self.background = Label(self, image = img)
        self.background.pack()
        
        self.login = RegistryFrame(self, bground="white",fname="login")
        self.register = RegistryFrame(self, bground="white",fname="register")
        
        # buttons
        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")

        button1=Button(buttonframe,border=0, width=20, pady=5, bg='#57a1f8', fg='white', text="Login", command=lambda: self.change_frame("login"))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button1.grid_rowconfigure(0, weight=1)
        button2=Button(buttonframe,border=0, width=20, pady=5, bg='#57a1f8', fg='white', text="Register", command=lambda: self.change_frame("register"))
        button2.grid(row=0, column=1, padx=5, pady=5)
        self.mainloop()
        
    def change_frame(self,frame_name):
        # delete background
        self.background.pack_forget()
        # controller
        if frame_name == "login":
            self.login.pack(fill='both', expand=1)
            self.register.pack_forget()
        elif frame_name == "register":
            self.register.pack(fill='both', expand=1)
            self.login.pack_forget()
        else:
            print("Ahuhu :((")
            
class RegistryFrame(Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(bg=kwargs["bground"])
        self.fname = kwargs["fname"]
        self.render()
    def render(self):
        if self.fname == "login":
            label_0 = Label(self, fg="#57a1f8", bg="#fff", text="Login form", font=("Microsoft YaHei UI Light",25,"bold"))
            label_0.place(x=150,y=20)
            
            user = Entry(self, width=30, border=0)
            user.place(x=100,y=100)
            user.insert(0,'Username')
            user.bind('<FocusIn>', lambda event: on_enter(event, "user"))
            user.bind('<FocusOut>', lambda event: on_leave(event, "user"))
            Frame(self, width=295, height=2,bg='black').place(x=95,y=120)

            passwd = Entry(self, width=30, border=0)
            passwd.place(x=100,y=150)
            passwd.insert(0,'Password')
            passwd.bind('<FocusIn>', lambda event: on_enter(event, "passwd"))
            passwd.bind('<FocusOut>', lambda event: on_leave(event, "passwd"))
            Frame(self, width=295, height=2,bg='black').place(x=95,y=170)

            submit = Button(self, text="Login", border=0, width=40, pady=5, bg='#57a1f8', fg='white', command=lambda: login_redirect())
            submit.place(x=100,y=220)
            
            def on_enter(_,name):
                if name == "user":
                    user.delete(0,END)
                elif name == "passwd":
                    passwd.delete(0,END)
                else:
                    pass
            def on_leave(_, name):
                if name == "user":
                    if user.get() == "":
                        user.insert(0,'Username')
                elif name == "passwd":
                    if passwd.get() == "":
                        passwd.insert(0,'Password')
                else:
                    pass
            
            def login_redirect():
                # Validate results
                if user.get() == "" or user.get() == "Username":
                    tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Nhập tên tài khoản giúp em ạ :((")
                elif passwd.get() == "" or passwd.get() == "Password":
                    tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Nhập mật khẩu giúp em ạ :((")
                else:
                    sign_in(user.get(),passwd.get())
                
        elif self.fname == "register":    
            label_0 = Label(self, fg="#57a1f8", bg="#fff", text="Registration form", font=("Microsoft YaHei UI Light",25,"bold"))
            label_0.place(x=100,y=20)
            
            full_name = Entry(self, width=30, border=0)
            full_name.place(x=100,y=100)
            full_name.insert(0,'Full name')
            full_name.bind('<FocusIn>', lambda event: on_enter(event, "full_name"))
            full_name.bind('<FocusOut>', lambda event: on_leave(event, "full_name"))
            Frame(self, width=295, height=2,bg='black').place(x=95,y=120)
            
            user_name = Entry(self, width=30, border=0)
            user_name.place(x=100,y=150)
            user_name.insert(0,'Username')
            user_name.bind('<FocusIn>', lambda event: on_enter(event, "user_name"))
            user_name.bind('<FocusOut>', lambda event: on_leave(event, "user_name"))
            Frame(self, width=295, height=2,bg='black').place(x=95,y=170)

            password = Entry(self, width=30, border=0)
            password.place(x=100,y=200)
            password.insert(0,'Password')
            password.bind('<FocusIn>', lambda event: on_enter(event, "password"))
            password.bind('<FocusOut>', lambda event: on_leave(event, "password"))
            Frame(self, width=295, height=2,bg='black').place(x=95,y=220)
            
            re_password = Entry(self, width=30, border=0)
            re_password.place(x=100,y=250)
            re_password.insert(0,'Retype Password')
            re_password.bind('<FocusIn>', lambda event: on_enter(event, "re_password"))
            re_password.bind('<FocusOut>', lambda event: on_leave(event, "re_password"))
            Frame(self, width=295, height=2,bg='black').place(x=95,y=270)

            submit = Button(self, text="Register", border=0, width=40, pady=5, bg='#57a1f8', fg='white', command=lambda: register_redirect())
            submit.place(x=100,y=320)
            
            def on_enter(_,name):
                if name == "full_name":
                    full_name.delete(0,END)
                elif name == "user_name":
                    user_name.delete(0,END)
                elif name == "password":
                    password.delete(0,END)
                elif name == "re_password":
                    re_password.delete(0,END)
                else:
                    pass
            def on_leave(_, name):
                if name == "full_name" and full_name.get() == "":
                    full_name.insert(0,'Full name')
                elif name == "user_name" and user_name.get() == "":
                    user_name.insert(0,'User name')
                elif name == "password" and password.get() == "":
                    password.insert(0,'Password')
                elif name == "re_password" and re_password.get() == "":
                    re_password.insert(0,'Retype Password')
                else:
                    pass
            def register_redirect():
                # Validate results
                if full_name.get() == "" or full_name.get() == "Full name":
                    tkinter.messagebox.showerror(title="Lỗi đăng kí",message="Vui lòng nhập họ tên !!")
                elif user_name.get() == "" or user_name.get() == "Username":
                    tkinter.messagebox.showerror(title="Lỗi đăng kí",message="Vui lòng nhập tên tài khoản !!")
                elif password.get() == "" or password.get() == "Password":
                    tkinter.messagebox.showerror(title="Lỗi đăng kí",message="Vui lòng nhập mật khẩu !!")
                elif not re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$", password.get()):
                    tkinter.messagebox.showerror(title="Lỗi đăng kí",message="Mật khẩu có độ dài tối thiểu là 6, bao gồm ít nhất 1 kí tự hoa, 1 kí tự thường, 1 chữ số và 1 kí tự đặc biệt (trừ khoảng trắng)")
                elif re_password.get() != password.get():
                    tkinter.messagebox.showerror(title="Lỗi đăng kí",message="Mật khẩu nhập lại không trùng khớp !!")
                else: 
                    sign_up(user_name.get(),full_name.get(),password.get())
if __name__ == "__main__":
    FirstPage()
