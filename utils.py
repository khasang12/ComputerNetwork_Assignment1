import csv
import tkinter.messagebox

#### SIGNIN - SIGNUP
user_data_csv = "accounts.csv"
def sign_in(user_name, password):
    try:
        # check if appears
        check = False
        with open(user_data_csv, "rt") as f:
            csvreader = csv.reader(f, delimiter=",")
            for row in csvreader:
                if row == []:
                    break
                elif user_name in row[0]:
                    check = True
                    if password != row[2]:
                        tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Nhập sai mật khẩu !!")
                        return
                    else:
                        tkinter.messagebox.showinfo(title="Chuyển hướng",message="Đăng nhập thành công !!")
                        return
            if not check:
                tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Tài khoản không tồn tại !!")
    except IOError:
        print("I/O error")

def sign_up(user_name, full_name, password):
    try:
        # check if appears
        with open(user_data_csv, "rt") as f:
            csvreader = csv.reader(f, delimiter=",")
            for row in csvreader:
                if row == []:
                    break
                elif user_name in row[0]:
                    tkinter.messagebox.showerror(title="Lỗi đăng kí",message="Tài khoản đã được đăng kí")
                    return
        # append
        with open(user_data_csv, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow((user_name, full_name, password))
        tkinter.messagebox.showinfo(title="Chuyển hướng",message="Đăng kí tài khoản thành công !!")
    except IOError:
        print("I/O error")