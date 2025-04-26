import customtkinter as cutk
import Add_users
import First_Page
import show_all_users
from PIL import Image, ImageTk
import add_or_delete_track

def settings_call(position):
    root_settings = cutk.CTk()
    root_settings.geometry('520x520')
    root_settings.minsize(480, 420)
    root_settings.maxsize(520, 620)
    root_settings.title('Settings | Trainingee')
    cutk.set_appearance_mode('system')
    cutk.set_default_color_theme('blue')
    root_settings.configure(bg='#f4f8fb')

    # Header Bar
    header = cutk.CTkFrame(root_settings, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=60)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='Settings', font=("Segoe UI", 22, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=25, pady=18, sticky='w')
    header.grid_columnconfigure(0, weight=1)

    # Main Content Frame
    content_frame = cutk.CTkFrame(root_settings, fg_color=("#f4f8fb", "#23272e"), corner_radius=20)
    content_frame.pack(fill='both', expand=True, padx=18, pady=(18,8))

    # زر/أيقونة المستخدم (أعلى الصفحة)
    try:
        image = Image.open("user.png")
        image = image.resize((22, 22))
        photo = ImageTk.PhotoImage(image)
    except:
        photo = None


    def add_users():
        Add_users.add_users_call()


    def delete_user():
        root_settings.destroy()
        Add_users.delete_user(position)


    def add_track_call():
        root_settings.destroy()
        add_or_delete_track.add_track(position)


    def delete_track_call():
        root_settings.destroy()
        add_or_delete_track.delete_track_in_data_base(position)
        


    def show_users():
        root_settings.destroy()
        show_all_users.show_users(position)


    def back():
        root_settings.destroy()
        First_Page.first_page(position)


    # أزرار الإعدادات بتوزيع عصري وألوان مميزة
    btn_style = dict(height=44, corner_radius=16, font=("Segoe UI", 14, "bold"))
    pady_btn = 8
    padx_btn = 12

    button = cutk.CTkButton(content_frame, text="Add User", command=add_users,
                            fg_color=("#43a047", "#388e3c"), hover_color="#388e3c", border_color='#43a047', border_width=2,
                            image=photo, compound="left", text_color='#fff', **btn_style)
    button.pack(padx=padx_btn, pady=(18, pady_btn), fill='x')

    delete_user_btn = cutk.CTkButton(content_frame, text='Delete User', command=delete_user,
                            fg_color=("#e53935","#b71c1c"), hover_color="#c62828", border_color='#e53935', border_width=2,
                            text_color='#fff', **btn_style)
    delete_user_btn.pack(padx=padx_btn, pady=pady_btn, fill='x')

    show_users_btn = cutk.CTkButton(content_frame, text='Show All Users', command=show_users,
                            fg_color=("#1976d2","#90caf9"), hover_color="#1565c0", border_color='#1976d2', border_width=2,
                            text_color='#fff', **btn_style)
    show_users_btn.pack(padx=padx_btn, pady=pady_btn, fill='x')

    add_track_btn = cutk.CTkButton(content_frame, text='Add Track', command=add_track_call,
                            fg_color=("#0288d1","#81d4fa"), hover_color="#0277bd", border_color='#0288d1', border_width=2,
                            text_color='#fff', **btn_style)
    add_track_btn.pack(padx=padx_btn, pady=(pady_btn, 0), fill='x')

    delete_track_btn = cutk.CTkButton(content_frame, text='Delete Track', command=delete_track_call,
                            fg_color=("#e53935","#b71c1c"), hover_color="#c62828", border_color='#e53935', border_width=2,
                            text_color='#fff', **btn_style)
    delete_track_btn.pack(padx=padx_btn, pady=pady_btn, fill='x')

    back_btn = cutk.CTkButton(content_frame, text='Back', command=back,
                            fg_color=("#757575","#bdbdbd"), hover_color="#616161", border_color='#757575', border_width=2,
                            text_color='#fff', **btn_style)
    back_btn.pack(padx=padx_btn, pady=(pady_btn, 12), fill='x')

    # Footer
    footer = cutk.CTkLabel(root_settings, text='All rights reserved © 2025', font=("Segoe UI", 10), text_color=("#90a4ae","#b0bec5"))
    footer.pack(side='bottom', pady=(0, 4))

    root_settings.mainloop()


