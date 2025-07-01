import customtkinter as cutk
import Verification

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

from First_Page import first_page
from dotenv import load_dotenv

def to_change_password(position):
    load_dotenv()
    root_chacge_pass = cutk.CTk()
    root_chacge_pass.minsize(380, 440)
    root_chacge_pass.maxsize(410, 520)
    root_chacge_pass.title('Change Password | Trainingee')

    root_chacge_pass.after(0, lambda: center_window(root_chacge_pass, 410, 480))
    cutk.set_appearance_mode('system')
    root_chacge_pass.configure(bg='#f4f8fb')

    # Header Bar
    header = cutk.CTkFrame(root_chacge_pass, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=56)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='Change Password', font=("Segoe UI", 20, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=22, pady=16, sticky='w')
    header.grid_columnconfigure(0, weight=1)

    # Main Content Frame
    content_frame = cutk.CTkFrame(root_chacge_pass, fg_color=("#f4f8fb", "#23272e"), corner_radius=20)
    content_frame.pack(fill='both', expand=True, padx=18, pady=(18,8))

    def show_password_check():
        global show_password
        if entry2.cget('show') == '*':
            entry2.configure(show='')
        else:
            entry2.configure(show='*')

        if entry3.cget('show') == '*':
            entry3.configure(show='')
        else:
            entry3.configure(show='*')
        
        if entry4.cget('show') == '*':
            entry4.configure(show='')
        else:
            entry4.configure(show='*')

    def back():
        root_chacge_pass.destroy()
        first_page(position)

    def check_and_change_pass():
        from models.models_user import User
        from config.ConnDB import get_db
        get_db()
        username = entry1.get().strip().lower()
        old_pass = entry2.get()
        new_pass = entry3.get()
        confirm_pass = entry4.get()

        user = User.objects(username=username).first()

        if username == '':
            Verification.Verification_name()
            return
        elif old_pass == '':
            Verification.Verification_password()
            return
        elif new_pass == '':
            Verification.new_pass()
            return
        elif confirm_pass == '':
            Verification.confirm_pass()
            return
        elif new_pass != confirm_pass:
            Verification.not_match()
            return
        elif user is None:
            Verification.Verification_name_found()
            return
        elif user.password != old_pass:
            Verification.Verification_wrong_password()
            return
        else:
            def go_home():
                root_chacge_pass.destroy()
                first_page(position)
            user.password = new_pass
            user.save()
            Verification.password_changed_successfully(callback=go_home)


    # عناصر الإدخال بتصميم عصري داخل content_frame
    content_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    entry1 = cutk.CTkEntry(content_frame, placeholder_text='Username', text_color='black',
                           placeholder_text_color='gray', font=('Segoe UI', 15), height=36, width=260, corner_radius=16, border_color='#1976d2', border_width=2)
    entry1.grid(row=0, column=0, padx=18, pady=(18,8), sticky='ew')

    entry2 = cutk.CTkEntry(content_frame, placeholder_text='Old Password', show='*',  text_color='black',
                           placeholder_text_color='gray', font=('Segoe UI', 15), height=36, width=260, corner_radius=16, border_color='#1976d2', border_width=2)
    entry2.grid(row=1, column=0, padx=18, pady=8, sticky='ew')

    entry3 = cutk.CTkEntry(content_frame, placeholder_text='New Password', show='*',  text_color='black',
                           placeholder_text_color='gray', font=('Segoe UI', 15), height=36, width=260, corner_radius=16, border_color='#1976d2', border_width=2)
    entry3.grid(row=2, column=0, padx=18, pady=8, sticky='ew')

    entry4 = cutk.CTkEntry(content_frame, placeholder_text='Confirm password', show='*',  text_color='black',
                           placeholder_text_color='gray', font=('Segoe UI', 15), height=36, width=260, corner_radius=16, border_color='#1976d2', border_width=2)
    entry4.grid(row=3, column=0, padx=18, pady=8, sticky='ew')

    show_password = cutk.CTkCheckBox(content_frame, text='Show Password', command=show_password_check,
                                     font=('Segoe UI', 13), text_color='#1976d2', fg_color='#fff', border_color='#1976d2', hover_color='#e3eafc')
    show_password.grid(row=4, column=0, pady=(8, 14), sticky='w', padx=18)

    entry5 = cutk.CTkButton(content_frame, text='Change', fg_color=("#43a047", "#388e3c"), hover_color="#388e3c", text_color='#fff', command=check_and_change_pass, corner_radius=18, border_color='#43a047', border_width=2, font=("Segoe UI", 15, "bold"), height=38)
    entry5.grid(row=5, column=0, padx=18, pady=(8, 4), sticky='ew')

    entry6 = cutk.CTkButton(content_frame, text='Back', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e', command=back, corner_radius=18, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 14), height=38)
    entry6.grid(row=6, column=0, padx=18, pady=(4, 10), sticky='ew')

    # Footer (اختياري)
    footer = cutk.CTkLabel(content_frame, text='Trainingee © 2025', font=("Segoe UI", 11), text_color='#bdbdbd')
    footer.grid(row=7, column=0, pady=(10, 0), sticky='s')

    root_chacge_pass.bind('<Return>', lambda e: check_and_change_pass())

    root_chacge_pass.mainloop()