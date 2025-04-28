import customtkinter as ctk
from models.models_user import User

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

from config.ConnDB import get_db
from First_Page import first_page
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import ui_colors
from tkinter import PhotoImage

def login():
    global show_password, check_to_destroy
    check_to_destroy = 0

    load_dotenv()
    mongo_client = MongoClient(os.getenv('MONGO_URI'))
    db = mongo_client['test']
    
    # Create main window
    root_login = ctk.CTk()
    # root_login.minsize(800, 600)
    # root_login.maxsize(1200, 900)
    ctk.set_appearance_mode('system')
    root_login.title('Trainingee | Login')
    # ... بعد بناء كل عناصر الواجهة ...
    root_login.after(0, lambda: center_window(root_login, 1000, 700))
    
    # Set window icon (replace with your actual icon path)
    try:
        root_login.iconbitmap('Logo.ico')
    except:
        pass
    
    # Configure window background
    root_login.configure(bg=ui_colors.get_bg_color())
    
    # Load images (replace with your actual image paths)
    try:
        logo_img = PhotoImage(file='Logo.ico').subsample(2, 2)
        bg_img = PhotoImage(file='Logo.ico')
        bg_label = ctk.CTkLabel(root_login, image=bg_img, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        logo_img = None
        bg_img = None

    def toggle_mode():
        mode = ctk.get_appearance_mode()
        if mode == 'Dark':
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')
        update_colors()
        
    def update_colors():
        """Update all widget colors dynamically"""
        root_login.configure(bg=ui_colors.get_bg_color())
        card_frame.configure(fg_color=ui_colors.get_card_color())
        logo.configure(text_color=ui_colors.PRIMARY_COLOR)
        title_label.configure(text_color=ui_colors.PRIMARY_COLOR)
        subtitle_label.configure(text_color=ui_colors.get_label_color())
        entry1.configure(
            text_color=ui_colors.get_text_color(), 
            placeholder_text_color=ui_colors.get_placeholder_color(), 
            border_color=ui_colors.get_button_color(),
            fg_color=ui_colors.get_input_bg_color()
        )
        entry2.configure(
            text_color=ui_colors.get_text_color(), 
            placeholder_text_color=ui_colors.get_placeholder_color(), 
            border_color=ui_colors.get_button_color(),
            fg_color=ui_colors.get_input_bg_color()
        )
        show_password.configure(
            text_color=ui_colors.get_label_color(),
            fg_color=ui_colors.get_button_color(),
            hover_color=ui_colors.get_hover_primary()
        )
        button_login.configure(
            fg_color=ui_colors.get_button_color(), 
            hover_color=ui_colors.get_hover_primary(),
            text_color=ui_colors.get_button_text_color()
        )
        footer.configure(text_color=ui_colors.get_footer_color())
        mode_btn.configure(
            fg_color=ui_colors.get_button_color(),
            hover_color=ui_colors.get_hover_primary()
        )
        forgot_label.configure(text_color=ui_colors.get_label_color())
        helper.configure(text_color=ui_colors.get_footer_color())
        
        # Update card shadow based on theme
        if ctk.get_appearance_mode() == 'Dark':
            card_shadow.configure(fg_color='#000000')
        else:
            card_shadow.configure(fg_color='#dde7f3')

    def show_password_check():
        if entry2.cget('show') == '*':
            entry2.configure(show='')
        else:
            entry2.configure(show='*')

    def animate_button():
        """Button press animation"""
        orig_width = button_login.cget('width')
        button_login.configure(width=orig_width-5)
        root_login.after(100, lambda: button_login.configure(width=orig_width))
        check()

    def check():
        import Verification
        global user_name, result
        entry_1 = entry1.get().lower()
        entry_2 = entry2.get()
        get_db()
        user = User.objects(username=entry_1).first()
        
        if entry_1 == '':
            Verification.Verification_name()
            shake_animation(entry1)
        elif entry_2 == '':
            Verification.Verification_password()
            shake_animation(entry2)
        else:
            if user is None:
                Verification.Verification_name_found()
                shake_animation(entry1)
                return
            user_name = user.username
            password = user.password
            if user is not None:
                if entry_2 != password:
                    Verification.Verification_wrong_password()
                    shake_animation(entry2)
                elif entry_2 == password:
                    # Success animation before destroying window
                    button_login.configure(fg_color='#4CAF50', text='✓ Login Successful')
                    def go_to_home():
                        root_login.destroy()
                        first_page(user)
                    root_login.after(500, go_to_home)

    def shake_animation(widget):
        """Shake effect for invalid inputs"""
        try:
            x = widget.winfo_x()
            for _ in range(3):
                try:
                    widget.place(x=x+8)
                    widget.update()
                    widget.place(x=x-8)
                    widget.update()
                except Exception:
                    break
            try:
                widget.place(x=x)
            except Exception:
                pass
        except Exception:
            pass

    def on_enter(e):
        try:
            e.widget.configure(fg_color="#e3eafc")
        except Exception:
            pass

    def on_leave(e):
        try:
            e.widget.configure(fg_color=ui_colors.get_input_bg_color())
        except Exception:
            pass

    # ========== UI Elements ========== #
    
    # Card shadow (modern effect)
    card_shadow = ctk.CTkFrame(
        root_login,
        corner_radius=28,
        fg_color='#e3eafc' if ctk.get_appearance_mode() == 'Light' else '#23272e',
        width=370,
        height=510
    )
    card_shadow.place(relx=0.5, rely=0.5, anchor='center', x=7, y=9)

    # Main card frame
    card_frame = ctk.CTkFrame(
        root_login,
        corner_radius=22,
        fg_color=ui_colors.get_card_color(),
        border_color='#b0bec5',
        border_width=1,
        width=360,
        height=500
    )
    card_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Theme toggle button (top-right)
    def update_theme_icon():
        if ctk.get_appearance_mode() == 'Light':
            mode_btn.configure(text='🌙', fg_color='#1976d2', hover_color='#1565c0')
            mode_btn.tooltip_text = 'تفعيل الوضع الليلي'
        else:
            mode_btn.configure(text='☀️', fg_color='#ffd54f', hover_color='#ffb300')
            mode_btn.tooltip_text = 'تفعيل الوضع النهاري'

    mode_btn = ctk.CTkButton(
        root_login,
        text='🌙' if ctk.get_appearance_mode() == 'Light' else '☀️',
        width=36,
        height=36,
        font=("Segoe UI", 18),
        fg_color='#1976d2' if ctk.get_appearance_mode() == 'Light' else '#ffd54f',
        hover_color='#1565c0' if ctk.get_appearance_mode() == 'Light' else '#ffb300',
        corner_radius=18,
        command=lambda: [toggle_mode(), update_theme_icon()],
        border_width=0
    )
    mode_btn.place(relx=0.97, rely=0.045, anchor='ne')
    mode_btn.tooltip_text = 'تفعيل الوضع الليلي' if ctk.get_appearance_mode() == 'Light' else 'تفعيل الوضع النهاري'

    update_theme_icon()
    
    # Logo and header
    if logo_img:
        logo = ctk.CTkLabel(card_frame, image=logo_img, text="")
    else:
        logo = ctk.CTkLabel(
            card_frame, 
            text='👨‍💻', 
            font=("Segoe UI", 64), 
            text_color=ui_colors.PRIMARY_COLOR
        )
    logo.pack(pady=(40, 10))
    
    title_label = ctk.CTkLabel(
        card_frame, 
        text='Trainingee', 
        font=("Segoe UI", 24, "bold"), 
        text_color=ui_colors.PRIMARY_COLOR
    )
    title_label.pack(pady=(0, 5))
    
    subtitle_label = ctk.CTkLabel(
        card_frame, 
        text='Sign in to your account', 
        font=("Segoe UI", 14), 
        text_color=ui_colors.get_label_color()
    )
    subtitle_label.pack(pady=(0, 30))
    
    # Form elements
    form_frame = ctk.CTkFrame(card_frame, fg_color='transparent')
    form_frame.pack(pady=(0, 20), padx=20, fill='both')
    
    # Username field
    username_label = ctk.CTkLabel(
        form_frame, 
        text='Username', 
        font=("Segoe UI", 12),
        text_color=ui_colors.get_label_color(),
        anchor='w'
    )
    username_label.pack(fill='x', pady=(0, 5))
    
    entry1 = ctk.CTkEntry(
        form_frame, 
        placeholder_text='Enter your username',
        font=("Segoe UI", 14), 
        height=48, 
        width=320,
        corner_radius=12, 
        border_width=1,
        border_color=ui_colors.get_placeholder_color(),
        fg_color=ui_colors.get_input_bg_color(),
        text_color=ui_colors.get_text_color(),
        placeholder_text_color=ui_colors.get_placeholder_color()
    )
    entry1.pack(pady=(0, 15))
    entry1.bind('<FocusIn>', on_enter)
    entry1.bind('<FocusOut>', on_leave)
    
    # Password field
    password_label = ctk.CTkLabel(
        form_frame, 
        text='Password', 
        font=("Segoe UI", 12),
        text_color=ui_colors.get_label_color(),
        anchor='w'
    )
    password_label.pack(fill='x', pady=(0, 5))
    
    entry2 = ctk.CTkEntry(
        form_frame, 
        placeholder_text='Enter your password', 
        show='*',
        font=("Segoe UI", 14), 
        height=48, 
        width=320,
        corner_radius=12, 
        border_width=1,
        border_color=ui_colors.get_placeholder_color(),
        fg_color=ui_colors.get_input_bg_color(),
        text_color=ui_colors.get_text_color(),
        placeholder_text_color=ui_colors.get_placeholder_color()
    )
    entry2.pack(pady=(0, 10))
    entry2.bind('<FocusIn>', on_enter)
    entry2.bind('<FocusOut>', on_leave)
    
    # Show password and forgot password row
    options_frame = ctk.CTkFrame(form_frame, fg_color='transparent')
    options_frame.pack(fill='x', pady=(0, 20))

    show_password = ctk.CTkCheckBox(
        options_frame,
        text='Show password',
        font=("Segoe UI", 12),
        text_color=ui_colors.get_label_color(),
        fg_color=ui_colors.get_button_color(),
        hover_color=ui_colors.get_hover_primary(),
        command=show_password_check
    )
    show_password.pack(side='left')

    # Forgot password as clickable label
    def forgot_password_action(event=None):
        print('Password reset requested')
        # هنا يمكنك فتح نافذة أو تنفيذ إجراء حقيقي

    forgot_label = ctk.CTkLabel(
        options_frame,
        text='Forgot password?',
        font=("Segoe UI", 12, 'underline'),
        text_color='#1976d2',
        cursor='hand2'
    )
    forgot_label.pack(side='right')
    forgot_label.bind('<Button-1>', forgot_password_action)
    
    # Login button
    button_login = ctk.CTkButton(
        card_frame, 
        text='Sign In', 
        font=("Segoe UI", 16, "bold"), 
        height=52,
        corner_radius=12,
        fg_color=ui_colors.get_button_color(),
        hover_color=ui_colors.get_hover_primary(),
        text_color=ui_colors.get_button_text_color(),
        command=animate_button
    )
    button_login.pack(fill='x', padx=40, pady=(10, 20))
    
    # Footer
    footer = ctk.CTkLabel(
        card_frame, 
        text='© 2025 Trainingee. All rights reserved', 
        font=("Segoe UI", 10), 
        text_color=ui_colors.get_footer_color()
    )
    footer.pack(side="bottom", pady=(0, 15))
    
    # Helper text
    helper = ctk.CTkLabel(
        card_frame, 
        text='Need help? Contact support@trainingee.com', 
        font=("Segoe UI", 11), 
        text_color=ui_colors.get_footer_color()
    )
    helper.pack(side="bottom", pady=(0, 5))
    
    # Bind Enter key to login
    root_login.bind('<Return>', lambda e: animate_button())
    
    # Initial color update
    update_colors()
    
    # Center the window on screen
    root_login.update_idletasks()
    width = root_login.winfo_width()
    height = root_login.winfo_height()
    x = (root_login.winfo_screenwidth() // 2) - (width // 2)
    y = (root_login.winfo_screenheight() // 2) - (height // 2)
    root_login.geometry(f'+{x}+{y}')
    
    root_login.mainloop()

login()