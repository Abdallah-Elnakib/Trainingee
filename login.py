import customtkinter as cutk
from models.models_user import User
from config.ConnDB import get_db
import First_Page
from dotenv import load_dotenv
import os
from pymongo import MongoClient

def login():
    global show_password, check_to_destroy
    check_to_destroy = 0

    load_dotenv()
    mongo_client = MongoClient(os.getenv('MONGO_URI'))
    db = mongo_client['test']
    root_login = cutk.CTk()
    root_login.geometry('600x400')
    root_login.minsize(500, 350)
    root_login.maxsize(700, 500)
    cutk.set_appearance_mode('system')
    cutk.set_default_color_theme('blue')
    root_login.title('Trainingee | Login')



    def show_password_check():
        global show_password
        if entry2.cget('show') == '*':
            entry2.configure(show='')
        else:
            entry2.configure(show='*')


    def check():
        import Verification
        global user_name, result
        entry_1 = entry1.get().lower()
        entry_2 = entry2.get()
        get_db()
        user = User.objects(username=entry_1).first()
        if entry_1 == '':
            Verification.Verification_name()
        elif entry_2 == '':
            Verification.Verification_password()
        else:
            if user is None:
                Verification.Verification_name_found()
                return
            user_name = user.username
            password = user.password
            if user is not None:
                if entry_2 != password:
                    Verification.Verification_wrong_password()
                elif entry_2 == password:
                    root_login.destroy()
                    First_Page.first_page(user.role)



    frame = cutk.CTkFrame(root_login, corner_radius=25, fg_color=("#f7fafd", "#23272e"))
    frame.pack(padx=25, pady=25, fill='both', expand=True)

    # Main Title
    title_label = cutk.CTkLabel(frame, text='👋 Welcome to Trainingee', font=("Segoe UI", 24, "bold"), text_color=("#1a237e", "#90caf9"))
    title_label.pack(pady=(20, 5))

    # Subtitle
    subtitle_label = cutk.CTkLabel(frame, text='Sign in to manage courses and trainees', font=("Segoe UI", 15), text_color=("#374151", "#b0bec5"))
    subtitle_label.pack(pady=(0, 20))

    # Username Entry
    entry1 = cutk.CTkEntry(frame, placeholder_text='Username', text_color=("#212121","#e3f2fd"),
            placeholder_text_color=("#607d8b","#b0bec5"), font=("Segoe UI", 15), height=38, width=270, corner_radius=15, border_color=("#1565c0","#90caf9"), border_width=2)
    entry1.pack(pady=8)
    # Password Entry
    entry2 = cutk.CTkEntry(frame, placeholder_text='Password', show='*',  text_color=("#212121","#e3f2fd"),
            placeholder_text_color=("#607d8b","#b0bec5"), font=("Segoe UI", 15), height=38, width=270, corner_radius=15, border_color=("#1565c0","#90caf9"), border_width=2)
    entry2.pack(pady=8)
    # Show Password
    show_password = cutk.CTkCheckBox(frame, text='Show Password', command=show_password_check,
        font=("Segoe UI", 12), text_color=("#1a237e", "#90caf9"))
    show_password.pack(pady=5)
    # Login Button
    button_login = cutk.CTkButton(frame, text='Sign In', hover_color=("#1565c0","#3949ab"), text_color=("#fff","#23272e"),
        fg_color=("#1976d2","#90caf9"), font=("Segoe UI", 15, "bold"), command=check, corner_radius=18, border_color=("#1565c0","#90caf9"), border_width=2)
    button_login.pack(pady=18)

    # Footer
    footer = cutk.CTkLabel(frame, text='All rights reserved © 2025', font=("Segoe UI", 10), text_color=("#90a4ae","#b0bec5"))
    footer.pack(side="bottom", pady=(0,8))



    root_login.bind('<Return>', lambda e: check())

    root_login.mainloop()

login()