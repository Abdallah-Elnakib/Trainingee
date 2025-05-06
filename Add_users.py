import customtkinter as cutk
from models.models_user import User
from config.ConnDB import get_db
import Verification
import Settings
from dotenv import load_dotenv
import os

check_pos = '_select_'


def add_users_call():
    global check
    load_dotenv()
    root_add_users = cutk.CTk()
    root_add_users.geometry('420x370')
    root_add_users.minsize(370, 320)
    root_add_users.maxsize(480, 420)
    root_add_users.title('Add User | Trainingee')
    cutk.set_appearance_mode('system')
    root_add_users.configure(bg='#f4f8fb')
    # Header
    header = cutk.CTkFrame(root_add_users, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=46)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='Add User', font=("Segoe UI", 18, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=18, pady=10, sticky='w')
    header.grid_columnconfigure(0, weight=1)
    # Main Frame
    content_frame = cutk.CTkFrame(root_add_users, fg_color=("#f4f8fb", "#23272e"), corner_radius=16)
    content_frame.pack(fill='both', expand=True, padx=14, pady=(14,7))
    content_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    
    def add():
        import Verification
        get_db()
        User_Name = entry1.get().strip().lower()
        Password = entry2.get()
        Position = check_pos
        Gender = entry3.get()
        # الحقول الجديدة
        First_Name = User_Name.capitalize()
        Last_Name = ""
        Email = ""
        # تحقق من صحة البيانات
        if User_Name == '':
            Verification.Verification_name()
            return
        elif Password == '':
            Verification.Verification_password()
            return
        elif Position == '_select_':
            Verification.add_Position()
            return
        elif len(Password) < 8:
            Verification.Password_Low()
            return
        # تحقق من عدم وجود المستخدم
        if User.objects(username=User_Name).first():
            Verification.Verification_name_used()
            return
        # أضف المستخدم
        # جلب القيم من الحقول الجديدة
        first_name = entry_first_name.get().strip()
        last_name = entry_last_name.get().strip()
        email = entry_email.get().strip()
        # تحقق من صحة جميع الحقول
        if not first_name:
            Verification.Verification_wrong_data()
            return
        if not last_name:
            Verification.Verification_wrong_data()
            return
        if not email or '@' not in email:
            Verification.Verification_wrong_data()
            return
        User(
            first_name=first_name,
            last_name=last_name,
            username=User_Name,
            email=email,
            password=Password,
            gender=Gender,
            role=Position
        ).save()
        Verification.add_user_done()

    entry_first_name = cutk.CTkEntry(content_frame, placeholder_text='First Name', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry_first_name.grid(row=0, column=0, padx=18, pady=(12, 4), sticky='ew')

    entry_last_name = cutk.CTkEntry(content_frame, placeholder_text='Last Name', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry_last_name.grid(row=1, column=0, padx=18, pady=4, sticky='ew')

    entry_email = cutk.CTkEntry(content_frame, placeholder_text='Email', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry_email.grid(row=2, column=0, padx=18, pady=4, sticky='ew')

    entry1 = cutk.CTkEntry(content_frame, placeholder_text='Username', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry1.grid(row=3, column=0, padx=18, pady=4, sticky='ew')

    entry2 = cutk.CTkEntry(content_frame, placeholder_text='Password', show='*', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry2.grid(row=4, column=0, padx=18, pady=4, sticky='ew')

    entry3 = cutk.CTkEntry(content_frame, placeholder_text='Gender', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry3.grid(row=5, column=0, padx=18, pady=4, sticky='ew')

    def checkbox(values):
        global check_pos
        check_pos = values

    checkbox_manager = cutk.CTkOptionMenu(content_frame, values=[ '_select_' , 'user' , 'editor' , 'manager'] , command=checkbox, fg_color='#e3eafc', button_color='#1976d2', font=("Segoe UI", 13))
    checkbox_manager.grid(row=5, column=0, padx=18, pady=8, sticky='ew')

    create_btn = cutk.CTkButton(content_frame, text='Create', fg_color=("#43a047", "#388e3c"), hover_color="#388e3c", text_color='#fff', command=add, corner_radius=16, border_color='#43a047', border_width=2, font=("Segoe UI", 14, "bold"), height=36)
    create_btn.grid(row=6, column=0, padx=18, pady=(12, 6), sticky='ew')

    footer = cutk.CTkLabel(content_frame, text='Trainingee © 2025', font=("Segoe UI", 10), text_color='#bdbdbd')
    footer.grid(row=7, column=0, pady=(7, 0), sticky='s')

    root_add_users.bind('<Return>', lambda e: add())
    root_add_users.mainloop()

def delete_user(position):
    import Verification
    get_db()
    root_delete_user = cutk.CTk()
    root_delete_user.geometry('420x300')
    root_delete_user.minsize(370, 260)
    root_delete_user.maxsize(480, 360)
    root_delete_user.title('Delete User | Trainingee')
    cutk.set_appearance_mode('system')
    root_delete_user.configure(bg='#f4f8fb')
    # Header
    header = cutk.CTkFrame(root_delete_user, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=46)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='Delete User', font=("Segoe UI", 18, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=18, pady=10, sticky='w')
    header.grid_columnconfigure(0, weight=1)
    # Main Frame
    content_frame = cutk.CTkFrame(root_delete_user, fg_color=("#f4f8fb", "#23272e"), corner_radius=16)
    content_frame.pack(fill='both', expand=True, padx=14, pady=(14,7))
    content_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    entry1 = cutk.CTkEntry(content_frame, placeholder_text='Username', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry1.grid(row=0, column=0, padx=18, pady=(28, 8), sticky='ew')

    def delete_user_in_data_base():
        username = entry1.get().strip().lower()
        if not username:
            Verification.Verification_wrong_data()
            return
        user = User.objects(username=username).first()
        if not user:
            Verification.Verification_name_not_found()  # رسالة مناسبة للمستخدم غير الموجود
            return
        user.delete()
        Verification.delete_user_done()  # رسالة مناسبة للحذف الناجح

    delete_btn = cutk.CTkButton(content_frame, text='Delete', fg_color=("#e53935", "#b71c1c"), hover_color="#b71c1c", text_color='#fff', corner_radius=16, command=delete_user_in_data_base, border_color='#e53935', border_width=2, font=("Segoe UI", 14, "bold"), height=36)
    delete_btn.grid(row=1, column=0, padx=18, pady=(12, 6), sticky='ew')

    def back():
        root_delete_user.destroy()

    back_btn = cutk.CTkButton(content_frame, text='Back', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e', command=back, corner_radius=16, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 13), height=36)
    back_btn.grid(row=2, column=0, padx=18, pady=(6, 10), sticky='ew')

    footer = cutk.CTkLabel(content_frame, text='Trainingee © 2025', font=("Segoe UI", 10), text_color='#bdbdbd')
    footer.grid(row=4, column=0, pady=(7, 0), sticky='s')

    root_delete_user.bind('<Return>', lambda e: delete_user_in_data_base())
    root_delete_user.mainloop()


