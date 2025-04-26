import customtkinter as cutk



def show_message(title, message, kind='error', button_text='OK', width=340, height=170, font_size=16):
    root = cutk.CTk()
    root.geometry(f'{width}x{height}')
    root.minsize(width, height)
    root.maxsize(width, height)
    root.title(title)
    cutk.set_appearance_mode('system')
    root.configure(bg='#f4f8fb')

    # ألوان حسب نوع الرسالة
    if kind == 'error':
        header_color = ("#e53935", "#b71c1c")
        text_color = ("#e53935", "#ef9a9a")
        btn_color = ("#e53935", "#b71c1c")
        btn_hover = "#c62828"
    elif kind == 'success':
        header_color = ("#43a047", "#388e3c")
        text_color = ("#43a047", "#a5d6a7")
        btn_color = ("#43a047", "#388e3c")
        btn_hover = "#388e3c"
    else:
        header_color = ("#1976d2", "#23272e")
        text_color = ("#1976d2", "#90caf9")
        btn_color = ("#1976d2", "#23272e")
        btn_hover = "#1565c0"

    # Header
    header = cutk.CTkFrame(root, fg_color=header_color, corner_radius=0, height=38)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text=title, font=("Segoe UI", 15, "bold"), text_color=("#fff", "#fff"))
    header_title.grid(row=0, column=0, padx=15, pady=7, sticky='w')
    header.grid_columnconfigure(0, weight=1)

    # Main Frame
    frame = cutk.CTkFrame(root, fg_color=("#f4f8fb", "#23272e"), corner_radius=18)
    frame.pack(fill='both', expand=True, padx=10, pady=(10,8))

    # الرسالة
    label_text = cutk.CTkLabel(frame, font=("Segoe UI", font_size), text=message, text_color=text_color, wraplength=width-40, justify='center')
    label_text.pack(pady=(18, 8))

    # زر الموافقة
    button = cutk.CTkButton(frame, text=button_text, fg_color=btn_color, hover_color=btn_hover, text_color='#fff', command=root.destroy, corner_radius=16, border_color=btn_color, border_width=2, font=("Segoe UI", 13, "bold"), height=38)
    button.pack(pady=(0, 10), ipadx=10, ipady=2)

    root.bind('<Return>', lambda e: root.destroy())
    root.mainloop()

# الدوال القديمة الآن تستخدم show_message بشكل عصري

def password_changed_successfully(callback=None):
    def on_ok():
        if callback:
            callback()
        root.destroy()
    root = cutk.CTk()
    root.geometry('340x170')
    root.minsize(340, 170)
    root.maxsize(340, 170)
    root.title("Password Changed")
    cutk.set_appearance_mode('system')
    root.configure(bg='#f4f8fb')
    header = cutk.CTkFrame(root, fg_color=("#43a047", "#388e3c"), corner_radius=0, height=38)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text="Password Changed", font=("Segoe UI", 15, "bold"), text_color=("#fff", "#fff"))
    header_title.grid(row=0, column=0, padx=15, pady=7, sticky='w')
    header.grid_columnconfigure(0, weight=1)
    frame = cutk.CTkFrame(root, fg_color=("#f4f8fb", "#23272e"), corner_radius=18)
    frame.pack(fill='both', expand=True, padx=10, pady=(10,8))
    message_label = cutk.CTkLabel(frame, text="Your password has been changed successfully.", font=("Segoe UI", 14), text_color="#23272e")
    message_label.pack(pady=(20, 10))
    ok_btn = cutk.CTkButton(frame, text="OK", fg_color=("#43a047", "#388e3c"), hover_color="#388e3c", text_color='#fff', command=on_ok, corner_radius=16, border_color='#43a047', border_width=2, font=("Segoe UI", 13, "bold"), height=32)
    ok_btn.pack(pady=(5, 10))
    root.mainloop()

def delete_user_done():
    show_message("User Deleted", "The user has been deleted successfully.", kind='success')

def Verification_name_found():
    show_message('Username Error', 'Username does not match', kind='error')

def Verification_name():
    show_message('Username Required', 'Please Enter Your Username', kind='error')

def Verification_password():
    show_message('Password Required', 'Please Enter Your Password', kind='error')

def Password_Low():
    show_message('Password Error', 'Low Password', kind='error', width=360)

def add_Position():
    show_message('Position Required', 'Please Select Position', kind='error', width=370)

def add_user_done():
    show_message('Success', 'Done', kind='success', width=300, font_size=17)

def Verification_wrong_password():
    show_message('Password Error', 'Incorrect password', kind='error', font_size=14)

def Verification_name_used():
    show_message('Username Error', 'Username is Already Taken', kind='error', font_size=14)

def Verification_name_Student_used():
    show_message('Student Name Error', 'Student Name is Already Taken', kind='error', font_size=14)

def Verification_wrong_data():
    show_message('Invalid Data', 'Incorrect Data. Please Enter Valid Data', kind='error', width=370)

def Verification_add_name():
    show_message('Student Name Required', 'Please Enter Your Student Name', kind='error')

def Verification_search_id():
    show_message('ID Error', 'ID does Not Match', kind='error')


def Verification_search_name():
    root_Verification_search_name = cutk.CTk()
    root_Verification_search_name.geometry('750x500')
    root_Verification_search_name.minsize(250, 150)
    root_Verification_search_name.maxsize(250, 150)
    root_Verification_search_name.title('Error')


    def Close(): 
        root_Verification_search_name.destroy()

    frame = cutk.CTkFrame(root_Verification_search_name)
    frame.pack(padx=1, pady=1, fill='both', expand=True)

    label_text = cutk.CTkLabel(frame, font=('Roboto', 16), text='Name Is Not Found',
                                               text_color='red')
    label_text.pack()

    button = cutk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=Close, corner_radius=20, border_color='black', border_width=2)
    button.pack(pady=15)

    root_Verification_search_name.bind('<Return>', lambda e: Close())

    root_Verification_search_name.mainloop()


def add_done():
    root_add_done = cutk.CTk()
    root_add_done.geometry('750x500')
    root_add_done.minsize(250, 150)
    root_add_done.maxsize(250, 150)
    root_add_done.title('Error')


    def Close(): 
        root_add_done.destroy()

    frame = cutk.CTkFrame(root_add_done)
    frame.pack(padx=1, pady=1, fill='both', expand=True)

    label_text = cutk.CTkLabel(frame, font=('Roboto', 16), text='Data Save',
                                               text_color='green')
    label_text.pack()

    button = cutk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=Close, corner_radius=20, border_color='black', border_width=2)
    button.pack(pady=15)
def not_match():
    show_message('Password Error', "Password Doesn't Match", kind='error')

def new_pass():
    show_message('Password Required', 'Please Enter New Password', kind='error')

def confirm_pass():
    show_message('Password Required', 'Please Confirm Password', kind='error')

def connection_error():
    connection_error = cutk.CTk()
    connection_error.geometry('750x500')
    connection_error.minsize(650, 150)
    connection_error.maxsize(650, 150)
    connection_error.title('Error')


    def Close(): 
        connection_error.destroy()

    frame = cutk.CTkFrame(connection_error)
    frame.pack(padx=1, pady=1, fill='both', expand=True)

    label_text = cutk.CTkLabel(frame, font=('Roboto', 16), text="No internet connection please check your connection and try again",
                                               text_color='red')
    label_text.pack()

    button = cutk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=Close, corner_radius=20, border_color='black', border_width=2)
    button.pack(pady=15)

    connection_error.bind('<Return>', lambda e: Close())

    connection_error.mainloop()


def Track_Already_Token():
    Track_Already_Token = cutk.CTk()
    Track_Already_Token.geometry('750x500')
    Track_Already_Token.minsize(650, 150)
    Track_Already_Token.maxsize(650, 150)
    Track_Already_Token.title('Error')


    def Close(): 
        Track_Already_Token.destroy()

    frame = cutk.CTkFrame(Track_Already_Token)
    frame.pack(padx=1, pady=1, fill='both', expand=True)

    label_text = cutk.CTkLabel(frame, font=('Roboto', 16), text="Track Name is Already Token",
                                               text_color='red')
    label_text.pack()

    button = cutk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=Close, corner_radius=20, border_color='black', border_width=2)
    button.pack(pady=15)

    Track_Already_Token.bind('<Return>', lambda e: Close())

    Track_Already_Token.mainloop()


def Track_Not_Found():
    Track_Not_Found = cutk.CTk()
    Track_Not_Found.geometry('750x500')
    Track_Not_Found.minsize(650, 150)
    Track_Not_Found.maxsize(650, 150)
    Track_Not_Found.title('Error')


    def Close(): 
        Track_Not_Found.destroy()

    frame = cutk.CTkFrame(Track_Not_Found)
    frame.pack(padx=1, pady=1, fill='both', expand=True)

    label_text = cutk.CTkLabel(frame, font=('Roboto', 16), text="Track Name is Not Found",
                                               text_color='red')
    label_text.pack()

    button = cutk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=Close, corner_radius=20, border_color='black', border_width=2)
    button.pack(pady=15)

    Track_Not_Found.bind('<Return>', lambda e: Close())

    Track_Not_Found.mainloop()
