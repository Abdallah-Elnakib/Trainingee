from tkinter import *
from  tkinter import ttk
import mysql.connector
import customtkinter as cutk
import Add_users
from dotenv import load_dotenv
import os
def show_users(position):
    load_dotenv()
    from mysql.connector import Error
    try:
        mydb = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWORD'), port=os.getenv('PORT'), database=os.getenv('DATABASE'))
        my_cursor = mydb.cursor()
            
    except Error as e:
        import Verification
        Verification.connection_error()
        return

    root_all_users = cutk.CTk()  
    root_all_users.title('All Users | Trainingee')
    root_all_users.geometry('700x540')
    root_all_users.minsize(600, 480)
    root_all_users.maxsize(900, 700)
    cutk.set_appearance_mode('system')
    root_all_users.configure(bg='#f4f8fb')
    # Header
    header = cutk.CTkFrame(root_all_users, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=46)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='All Users', font=("Segoe UI", 18, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=18, pady=10, sticky='w')
    header.grid_columnconfigure(0, weight=1)
    # Main Frame
    content_frame = cutk.CTkFrame(root_all_users, fg_color=("#f4f8fb", "#23272e"), corner_radius=16)
    content_frame.pack(fill='both', expand=True, padx=14, pady=(14,7))
    content_frame.grid_rowconfigure((0,1,2,3), weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    def call_delete_user():
        Add_users.delete_user(position)

    style = ttk.Style(root_all_users)
    style.theme_use('clam')
    style.configure('Treeview', background='#f4f8fb', fieldbackground='#f4f8fb', foreground='black', rowheight=32, borderwidth=0, font=("Segoe UI", 12))
    style.configure('Treeview.Heading', background='#1976d2', foreground='white', font=("Segoe UI", 13, "bold"))
    style.map('Treeview', background=[('selected', '#90caf9')])

    def back_settigs():
        import Settings
        root_all_users.destroy()
        Settings.settings_call(position)

    # أزرار حديثة
    btns_frame = cutk.CTkFrame(content_frame, fg_color='transparent')
    btns_frame.grid(row=0, column=0, sticky='ew', pady=(10, 0))
    btns_frame.grid_columnconfigure((0,1), weight=1)

    back_to_settings = cutk.CTkButton(btns_frame, text='Back', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e',
                        command=back_settigs, corner_radius=16, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 12), height=36)
    back_to_settings.grid(row=0, column=0, padx=(0, 10), pady=3, sticky='ew')

    delete_user = cutk.CTkButton(btns_frame, text='Delete User', fg_color=("#e53935", "#b71c1c"), hover_color="#b71c1c", text_color='#fff',
                        command=call_delete_user, corner_radius=16, border_color='#e53935', border_width=2, font=("Segoe UI", 12, "bold"), height=36)
    delete_user.grid(row=0, column=1, padx=(10, 0), pady=3, sticky='ew')

    # جدول المستخدمين
    table_frame = cutk.CTkFrame(content_frame, fg_color='transparent')
    table_frame.grid(row=1, column=0, pady=(10, 0), sticky='nsew')
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    my_data = ttk.Treeview(table_frame, height=12, show='headings', selectmode='browse')
    my_data.grid(row=0, column=0, sticky='nsew')
    my_data['columns'] = ('User_name', 'Password', 'Position')
    my_data.column("User_name", anchor=CENTER, width=170)
    my_data.column("Password", anchor=CENTER, width=170)
    my_data.column("Position", anchor=CENTER, width=120)
    my_data.heading("User_name", text="User Name", anchor=CENTER)
    my_data.heading("Password", text="Password", anchor=CENTER)
    my_data.heading("Position", text="Position", anchor=CENTER)

    my_cursor.execute('SELECT * FROM data_users_login')
    result = my_cursor.fetchall()
    for i in result:
        my_data.insert('', 'end', values=i)

    # Scrollbar
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=my_data.yview)
    my_data.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=1, sticky='ns')

    # Footer
    footer = cutk.CTkLabel(content_frame, text='Trainingee © 2025', font=("Segoe UI", 10), text_color='#bdbdbd')
    footer.grid(row=3, column=0, pady=(7, 0), sticky='s')

    root_all_users.mainloop()

