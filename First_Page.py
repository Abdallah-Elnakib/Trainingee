import customtkinter as ctk
from PIL import Image, ImageTk
import Settings
from models.models_track import Track
import List
import search_in_all_track
import os
from dotenv import load_dotenv
from tkinter import messagebox
import bcrypt
import Add_users
import add_or_delete_track
import show_all_users

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def first_page(user):
    load_dotenv()   

    # ========== Functions ========== #
    showing_change_pass = [False]
    def show_change_pass_form():
        showing_change_pass[0] = True
        content_frame.grid_remove()
        change_pass_card.grid(row=0, column=1, sticky="nsew", padx=120, pady=60)
        dashboard_frame.configure(fg_color="transparent")
        pass_frame.configure(fg_color="#e3f2fd")
    def hide_change_pass_form():
        showing_change_pass[0] = False
        change_pass_card.grid_remove()
        content_frame.grid()
        dashboard_frame.configure(fg_color="#e3f2fd")
        pass_frame.configure(fg_color="transparent")
    def check_track(track_name):
        track = track_name[0]
        root_home.destroy()
        import Show_All_Data
        Show_All_Data.show_all_data(user.role, track)
    def settings_page():
        content_frame.grid_remove()
        change_pass_card.grid_remove()
        settings_card.grid(row=0, column=1, sticky="nsew", padx=120, pady=60)
        dashboard_text.configure(text_color=label_fg)
        pass_text.configure(text_color=label_fg)
        settings_text.configure(text_color=label_active_fg)
        logout_text.configure(text_color=label_fg)
    def search(event=None):
        entry_name = search_entry.get()
        if entry_name:
            search_in_all_track.search(entry_name)
        else:
            messagebox.showwarning("Search", "Please enter a search term")
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            root_home.destroy()
            import link
            link.Logout()

    # Create main window
    root_home = ctk.CTk()
    root_home.minsize(1100, 700)
    root_home.title('Trainingee | Dashboard')
    ctk.set_appearance_mode('system')
    root_home.configure(bg='#f5f7fa')
    # ... بعد بناء كل عناصر الواجهة ...
    root_home.after(0, lambda: center_window(root_home, 1200, 800))
    
    try:
        root_home.iconbitmap('Logo.ico')
    except:
        pass

    # ========== Styles & Colors ========== #
    PRIMARY_COLOR = "#1976d2"
    SECONDARY_COLOR = "#ff5722"
    DARK_BG = "#1e293b"
    LIGHT_BG = "#f5f7fa"
    CARD_COLOR_LIGHT = "#ffffff"
    CARD_COLOR_DARK = "#334155"
    TEXT_COLOR_LIGHT = "#263238"
    TEXT_COLOR_DARK = "#e2e8f0"
    
    def get_theme_colors():
        mode = ctk.get_appearance_mode()
        return {
            'bg': LIGHT_BG if mode == "Light" else DARK_BG,
            'card': CARD_COLOR_LIGHT if mode == "Light" else CARD_COLOR_DARK,
            'text': TEXT_COLOR_LIGHT if mode == "Light" else TEXT_COLOR_DARK,
            'primary': PRIMARY_COLOR,
            'secondary': SECONDARY_COLOR
        }

    # ========== Main Layout ========== #
    root_home.grid_rowconfigure(0, weight=1)
    root_home.grid_columnconfigure(1, weight=1)
    
    # ========== Sidebar ========== #
    sidebar = ctk.CTkFrame(root_home, corner_radius=0, fg_color=(PRIMARY_COLOR, "#1e293b"), width=220)
    sidebar.grid(row=0, column=0, sticky="nswe")
    sidebar.grid_propagate(False)
    
    # Logo and app name
    logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    logo_frame.pack(pady=(20, 30), padx=10, fill="x")
    
    try:
        logo_img = ctk.CTkImage(light_image=Image.open("assets/logo_light.png"), 
                              dark_image=Image.open("assets/logo_dark.png"),
                              size=(40, 40))
        logo_label = ctk.CTkLabel(logo_frame, image=logo_img, text="")
        logo_label.pack(side="left", padx=(10, 5))
    except:
        logo_img = None

    # --- Sidebar icons ---
    global settings_icon, pass_icon, logout_icon
    try:
        settings_icon = ctk.CTkImage(light_image=Image.open("settings.png"),
                                     dark_image=Image.open("settings.png"),
                                     size=(22, 22))
        print("settings_icon loaded")
    except Exception as e:
        print("settings_icon failed:", e)
        settings_icon = None
    try:
        pass_icon = ctk.CTkImage(light_image=Image.open("password.png"),
                                 dark_image=Image.open("password.png"),
                                 size=(22, 22))
        print("pass_icon loaded")
    except Exception as e:
        print("pass_icon failed:", e)
        pass_icon = None
    try:
        logout_icon = ctk.CTkImage(light_image=Image.open("logout.png"),
                                   dark_image=Image.open("logout.png"),
                                   size=(22, 22))
        print("logout_icon loaded")
    except Exception as e:
        print("logout_icon failed:", e)
        logout_icon = None

    
    app_name = ctk.CTkLabel(logo_frame, 
                            text="Trainingee", 
                            font=("Segoe UI", 18, "bold"),
                            text_color="white")
    app_name.pack(side="left", fill="x", expand=True)
    
    # --- Sidebar Navigation Labels with Icons ---
    label_font = ("Segoe UI", 16, "bold")
    label_fg = "white"
    label_active_fg = "white"
    icon_size = (22, 22)
    label_kwargs = {'anchor': 'w', 'justify': 'left'}

    # Dashboard (Always first)
    dashboard_frame = ctk.CTkFrame(sidebar, fg_color="transparent", corner_radius=8)
    dashboard_frame.pack(fill="x", padx=(18,10), pady=(30, 5))
    try:
        layout_icon = ctk.CTkImage(light_image=Image.open("layout.png"), size=(22, 22))
    except:
        layout_icon = None
    dashboard_icon_label = ctk.CTkLabel(dashboard_frame, image=layout_icon, text="", width=32)
    dashboard_icon_label.pack(side="left")
    dashboard_text = ctk.CTkLabel(
        dashboard_frame,
        text="Dashboard",
        font=label_font,
        text_color=label_active_fg,
        cursor="hand2",
        **label_kwargs
    )
    dashboard_text.pack(side="left", padx=(22,0))

    # Settings
    settings_frame = ctk.CTkFrame(sidebar, fg_color="transparent", corner_radius=8)
    settings_frame.pack(fill="x", padx=(18,10), pady=(5, 5))
    settings_icon_label = ctk.CTkLabel(settings_frame, image=settings_icon, text="", width=32)
    settings_icon_label.pack(side="left")
    settings_text = ctk.CTkLabel(settings_frame, text="Settings", font=label_font, text_color=label_fg, cursor="hand2", **label_kwargs)
    settings_text.pack(side="left", padx=(22,0))
    settings_frame.bind("<Button-1>", lambda e: settings_page())
    settings_text.bind("<Button-1>", lambda e: settings_page())
    settings_icon_label.bind("<Button-1>", lambda e: settings_page())

    # Password
    pass_frame = ctk.CTkFrame(sidebar, fg_color="transparent", corner_radius=8)
    pass_frame.pack(fill="x", padx=(18,10), pady=5)
    pass_icon_label = ctk.CTkLabel(pass_frame, image=pass_icon, text="", width=32)
    pass_icon_label.pack(side="left")
    pass_text = ctk.CTkLabel(pass_frame, text="Password", font=label_font, text_color=label_fg, cursor="hand2", anchor='w', justify='left')
    pass_text.pack(side="left", padx=(22,0))

    # Logout
    logout_frame = ctk.CTkFrame(sidebar, fg_color="transparent", corner_radius=8)
    logout_frame.pack(fill="x", padx=(18,10), pady=(5, 20))
    logout_icon_label = ctk.CTkLabel(logout_frame, image=logout_icon, text="", width=32)
    logout_icon_label.pack(side="left")
    logout_text = ctk.CTkLabel(logout_frame, text="Logout", font=label_font, text_color=label_fg, cursor="hand2", **label_kwargs)
    logout_text.pack(side="left", padx=(22,0))
    logout_frame.bind("<Button-1>", lambda e: logout())
    logout_text.bind("<Button-1>", lambda e: logout())

    def show_dashboard():
        change_pass_card.grid_remove()
        settings_card.grid_remove()
        content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=(0, 20))
        dashboard_text.configure(text_color=label_active_fg)
        pass_text.configure(text_color=label_fg)
        settings_text.configure(text_color=label_fg)
        logout_text.configure(text_color=label_fg)
    def show_change_pass_form():
        content_frame.grid_remove()
        change_pass_card.grid(row=0, column=1, sticky="nsew", padx=120, pady=60)
        dashboard_text.configure(text_color=label_fg)
        pass_text.configure(text_color=label_active_fg)
        settings_text.configure(text_color=label_fg)
        logout_text.configure(text_color=label_fg)
    dashboard_frame.bind("<Button-1>", lambda e: show_dashboard())
    dashboard_text.bind("<Button-1>", lambda e: show_dashboard())
    pass_frame.bind("<Button-1>", lambda e: show_change_pass_form())
    pass_text.bind("<Button-1>", lambda e: show_change_pass_form())

    # User section at bottom
    user_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    user_frame.pack(side="bottom", fill="x", padx=10, pady=20)
    
    try:
        user_img = ctk.CTkImage(light_image=Image.open("user.png"), size=(24, 24))
        ctk.CTkLabel(user_frame, image=user_img, text="").pack(side="left", padx=(0, 8))
    except:
        pass
    
    user_info = ctk.CTkFrame(user_frame, fg_color="transparent")
    user_info.pack(side="left", fill="x", expand=True)
    first_name = getattr(user, "first_name", "User")
    ctk.CTkLabel(user_info, 
                text=f"Welcome, {first_name}",
                font=("Segoe UI", 14, "bold"),
                text_color="white").pack(anchor="w")

    # ========== Content Area ========== #
    content_frame = ctk.CTkScrollableFrame(root_home, 
                                         fg_color="transparent",
                                         corner_radius=10)
    content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=(0, 20))
    content_frame.grid_columnconfigure(0, weight=1)
    
    # Stats cards row
    stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    stats_frame.grid(row=0, column=0, sticky="nwe", pady=(0, 20))
    
    # Get real statistics from database
    from models.models_user import User
    from models.models_track import Track
    from config.ConnDB import get_db
    get_db()
    
    # Count total tracks
    total_tracks = Track.objects().count()
    
    # Count active trainees (users with role 'trainee')
    active_trainees = User.objects(role='trainee').count()
    
    # For completed and in-progress, we'll use a simple calculation
    # Assuming 30% completion rate for demonstration
    completed = int(active_trainees * 0.3)
    in_progress = active_trainees - completed
    
    stats = [
        {"title": "Total Tracks", "value": str(total_tracks), "icon": "book", "color": PRIMARY_COLOR},
        {"title": "Active Trainees", "value": str(active_trainees), "icon": "people", "color": "#4caf50"},
        {"title": "Completed", "value": str(completed), "icon": "check", "color": "#ff9800"},
        {"title": "In Progress", "value": str(in_progress), "icon": "clock", "color": "#9c27b0"},
    ]
    
    for i, stat in enumerate(stats):
        try:
            icon_img = ctk.CTkImage(light_image=Image.open(f"{stat['icon']}.png"), size=(30, 30))
        except:
            icon_img = None
            
        card = ctk.CTkFrame(stats_frame,
                           height=100,
                           corner_radius=12,
                           border_width=1,
                           border_color=("#e0e0e0", "#374151"),
                           fg_color=(CARD_COLOR_LIGHT, CARD_COLOR_DARK))
        card.grid(row=0, column=i, padx=10, sticky="nsew")
        card.grid_propagate(False)
        
        if icon_img:
            ctk.CTkLabel(card, image=icon_img, text="").place(relx=0.8, rely=0.3, anchor="center")
        
        ctk.CTkLabel(card,
                    text=stat["value"],
                    font=("Segoe UI", 24, "bold"),
                    text_color=stat["color"]).place(relx=0.2, rely=0.3, anchor="w")
        
        ctk.CTkLabel(card,
                    text=stat["title"],
                    font=("Segoe UI", 12),
                    text_color=(TEXT_COLOR_LIGHT, TEXT_COLOR_DARK)).place(relx=0.2, rely=0.6, anchor="w")
    
    # Tracks section
    tracks_header = ctk.CTkFrame(content_frame, fg_color="transparent")
    tracks_header.grid(row=1, column=0, sticky="nwe", pady=(10, 5))
    
    ctk.CTkLabel(tracks_header,
                text="Available Tracks",
                font=("Segoe UI", 18, "bold"),
                text_color=(TEXT_COLOR_LIGHT, TEXT_COLOR_DARK)).grid(row=0, column=0, sticky="w")
    
    # Tracks grid
    tracks_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
    tracks_grid.grid(row=2, column=0, sticky="nsew")
    tracks_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="columns")
    
    from config.ConnDB import get_db
    get_db()
    
    # Modern cards for tracks (3 columns)
    for i, track in enumerate(Track.objects()):
        row = i // 3
        col = i % 3
        
        card = ctk.CTkFrame(tracks_grid,
                           corner_radius=12,
                           border_width=1,
                           border_color=("#e0e0e0", "#374151"),
                           fg_color=(CARD_COLOR_LIGHT, CARD_COLOR_DARK))
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Card content
        try:
            track_icon = ctk.CTkImage(light_image=Image.open(f"assets/icons/track_{col+1}.png"), size=(60, 60))
            ctk.CTkLabel(card, image=track_icon, text="").pack(pady=(15, 5))
        except:
            pass
        
        ctk.CTkLabel(card,
                    text=track.track_name,
                    font=("Segoe UI", 16, "bold"),
                    text_color=(TEXT_COLOR_LIGHT, TEXT_COLOR_DARK)).pack(pady=(0, 5))
        
        ctk.CTkLabel(card,
                    text=f"{len(track.track_data)} Trainees",
                    font=("Segoe UI", 12),
                    text_color=("#757575", "#9ca3af")).pack(pady=(0, 15))
        
        ctk.CTkButton(card,
                     text="View Details",
                     width=120,
                     height=32,
                     corner_radius=16,
                     fg_color=PRIMARY_COLOR,
                     hover_color="#1565c0",
                     command=lambda t=track.track_name: check_track((t,))).pack(pady=(0, 15))
    
    # Bind Enter key to search
    root_home.bind('<Return>', search)
    
    # ========== نموذج تغيير كلمة السر ========== #
    change_pass_card = ctk.CTkFrame(root_home, corner_radius=18, fg_color="#fff", border_width=1, border_color="#e0e0e0")
    change_pass_card.grid_remove()
    ctk.CTkLabel(change_pass_card, text="Change Password", font=("Segoe UI", 26, "bold"), text_color="#1976d2").pack(pady=(30, 18))
    
    # ========== نموذج الإعدادات ========== #
    settings_card = ctk.CTkFrame(root_home, corner_radius=24, fg_color=(CARD_COLOR_LIGHT, CARD_COLOR_DARK), border_width=1, border_color=("#e0e0e0", "#374151"))
    settings_card.grid_remove()
    
    # Header with gradient effect
    header_frame = ctk.CTkFrame(settings_card, corner_radius=12, fg_color=PRIMARY_COLOR, height=80)
    header_frame.pack(fill="x", padx=20, pady=(20, 30))
    header_frame.pack_propagate(False)
    
    # Header content with icon
    header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
    header_content.pack(fill="both", expand=True, padx=20)
    
    try:
        settings_header_icon = ctk.CTkImage(light_image=Image.open("settings.png"), size=(32, 32))
        ctk.CTkLabel(header_content, image=settings_header_icon, text="").pack(side="left", padx=(0, 15))
    except:
        pass
        
    ctk.CTkLabel(header_content, 
                text="Settings", 
                font=("Segoe UI", 28, "bold"), 
                text_color="white").pack(side="left")
    
    # Main content container with two columns
    main_container = ctk.CTkFrame(settings_card, fg_color="transparent")
    main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)
    
    # Settings functions
    def add_users_func():
        Add_users.add_users_call()
    
    def delete_user_func():
        root_home.destroy()
        Add_users.delete_user(user.role)
    
    def add_track_func():
        root_home.destroy()
        add_or_delete_track.add_track(user.role)
    
    def delete_track_func():
        root_home.destroy()
        add_or_delete_track.delete_track_in_data_base(user.role)
    
    def show_users_func():
        root_home.destroy()
        show_all_users.show_users(user.role)
    
    # Left column - User Management
    user_section = ctk.CTkFrame(main_container, fg_color=("#f8f9fa", "#2d3748"), corner_radius=16)
    user_section.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
    
    # Section header
    user_header = ctk.CTkFrame(user_section, fg_color="transparent", height=50)
    user_header.pack(fill="x", padx=15, pady=(15, 5))
    
    try:
        user_icon = ctk.CTkImage(light_image=Image.open("user.png"), size=(24, 24))
        ctk.CTkLabel(user_header, image=user_icon, text="").pack(side="left", padx=(0, 10))
    except:
        pass
        
    ctk.CTkLabel(user_header, 
                text="User Management", 
                font=("Segoe UI", 18, "bold"), 
                text_color=(TEXT_COLOR_LIGHT, TEXT_COLOR_DARK)).pack(side="left")
    
    # User management buttons
    user_buttons = ctk.CTkFrame(user_section, fg_color="transparent")
    user_buttons.pack(fill="both", expand=True, padx=15, pady=(5, 15))
    
    # Modern button style
    btn_style = dict(height=50, corner_radius=12, font=("Segoe UI", 14, "bold"))
    
    # Add User button with hover effect and icon
    add_user_btn = ctk.CTkButton(user_buttons, 
                              text="Add User", 
                              command=add_users_func,
                              fg_color=("#4caf50", "#2e7d32"), 
                              hover_color=("#43a047", "#388e3c"), 
                              border_width=0,
                              text_color='#fff', 
                              **btn_style)
    add_user_btn.pack(fill='x', pady=8)
    
    # Delete User button
    delete_user_btn = ctk.CTkButton(user_buttons, 
                                 text='Delete User', 
                                 command=delete_user_func,
                                 fg_color=("#f44336", "#c62828"), 
                                 hover_color=("#e53935", "#b71c1c"), 
                                 border_width=0,
                                 text_color='#fff', 
                                 **btn_style)
    delete_user_btn.pack(fill='x', pady=8)
    
    # Show All Users button
    show_users_btn = ctk.CTkButton(user_buttons, 
                                text='Show All Users', 
                                command=show_users_func,
                                fg_color=("#2196f3", "#1565c0"), 
                                hover_color=("#1e88e5", "#0d47a1"), 
                                border_width=0,
                                text_color='#fff', 
                                **btn_style)
    show_users_btn.pack(fill='x', pady=8)
    
    # Right column - Track Management
    track_section = ctk.CTkFrame(main_container, fg_color=("#f8f9fa", "#2d3748"), corner_radius=16)
    track_section.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
    
    # Section header
    track_header = ctk.CTkFrame(track_section, fg_color="transparent", height=50)
    track_header.pack(fill="x", padx=15, pady=(15, 5))
    
    try:
        track_icon = ctk.CTkImage(light_image=Image.open("book.png"), size=(24, 24))
        ctk.CTkLabel(track_header, image=track_icon, text="").pack(side="left", padx=(0, 10))
    except:
        pass
        
    ctk.CTkLabel(track_header, 
                text="Track Management", 
                font=("Segoe UI", 18, "bold"), 
                text_color=(TEXT_COLOR_LIGHT, TEXT_COLOR_DARK)).pack(side="left")
    
    # Track management buttons
    track_buttons = ctk.CTkFrame(track_section, fg_color="transparent")
    track_buttons.pack(fill="both", expand=True, padx=15, pady=(5, 15))
    
    # Add Track button
    add_track_btn = ctk.CTkButton(track_buttons, 
                               text='Add Track', 
                               command=add_track_func,
                               fg_color=("#03a9f4", "#0277bd"), 
                               hover_color=("#039be5", "#01579b"), 
                               border_width=0,
                               text_color='#fff', 
                               **btn_style)
    add_track_btn.pack(fill='x', pady=8)
    
    # Delete Track button
    delete_track_btn = ctk.CTkButton(track_buttons, 
                                  text='Delete Track', 
                                  command=delete_track_func,
                                  fg_color=("#f44336", "#c62828"), 
                                  hover_color=("#e53935", "#b71c1c"), 
                                  border_width=0,
                                  text_color='#fff', 
                                  **btn_style)
    delete_track_btn.pack(fill='x', pady=8)
    
    # Bottom section with back button
    bottom_section = ctk.CTkFrame(settings_card, fg_color="transparent")
    bottom_section.pack(fill="x", padx=20, pady=(0, 20))
    
    # Back button with modern design
    back_btn = ctk.CTkButton(bottom_section, 
                          text='← Back to Dashboard', 
                          command=show_dashboard,
                          fg_color=("#9e9e9e", "#616161"), 
                          hover_color=("#757575", "#424242"), 
                          border_width=0,
                          text_color='#fff', 
                          height=44,
                          corner_radius=22,
                          font=("Segoe UI", 14, "bold"))
    back_btn.pack(fill='x')
    
    # Footer with subtle design
    footer_frame = ctk.CTkFrame(settings_card, fg_color="transparent", height=30)
    footer_frame.pack(fill="x", side="bottom")
    footer_frame.pack_propagate(False)
    
    ctk.CTkLabel(footer_frame, 
                text='Trainingee © 2025 | All rights reserved', 
                font=("Segoe UI", 10), 
                text_color=("#90a4ae", "#b0bec5")).pack(side="right", padx=20)
    fields_frame = ctk.CTkFrame(change_pass_card, fg_color="transparent")
    fields_frame.pack(pady=(0, 10))
    old_pass = ctk.CTkEntry(fields_frame, placeholder_text="Old Password", show="*", width=320, height=44, corner_radius=12)
    old_pass.pack(pady=8)
    new_pass = ctk.CTkEntry(fields_frame, placeholder_text="New Password", show="*", width=320, height=44, corner_radius=12)
    new_pass.pack(pady=8)
    confirm_pass = ctk.CTkEntry(fields_frame, placeholder_text="Confirm New Password", show="*", width=320, height=44, corner_radius=12)
    confirm_pass.pack(pady=8)
    # عرف الدالة أولاً
    def toggle_password_visibility():
        show = old_pass.cget('show') == '*'
        old_pass.configure(show='' if show else '*')
        new_pass.configure(show='' if show else '*')
        confirm_pass.configure(show='' if show else '*')
    # ثم أنشئ الزر
    show_pass_btn = ctk.CTkButton(fields_frame, text="👁 Show/Hide Passwords", command=toggle_password_visibility, width=180, height=32, fg_color="#e3eafc", text_color="#1976d2", font=("Segoe UI", 12, "bold"))
    show_pass_btn.pack(pady=(0, 10))
    msg_label = ctk.CTkLabel(change_pass_card, text="", font=("Segoe UI", 13), text_color="#e53935")
    msg_label.pack(pady=4)
    # عرف دالة تغيير كلمة السر أولاً
    def submit_change_pass():
        from models.models_user import User
        from config.ConnDB import get_db
        import bcrypt
        get_db()
        if not old_pass.get() or not new_pass.get() or not confirm_pass.get():
            msg_label.configure(text="Please fill all fields", text_color="#e53935")
            return
        if new_pass.get() != confirm_pass.get():
            msg_label.configure(text="Passwords do not match", text_color="#e53935")
            return
        # تحقق من المستخدم وكلمة السر القديمة
        username = user.username
        user_obj = User.objects(username=username).first()
        if user_obj is None:
            msg_label.configure(text="User not found", text_color="#e53935")
            return
        # تحقق من كلمة السر القديمة (مشفرة أو نصية)
        if user_obj.password.startswith("$2"):
            if not bcrypt.checkpw(old_pass.get().encode(), user_obj.password.encode()):
                msg_label.configure(text="Old password is incorrect", text_color="#e53935")
                return
        else:
            if user_obj.password != old_pass.get():
                msg_label.configure(text="Old password is incorrect", text_color="#e53935")
                return
        # تشفير كلمة السر الجديدة وتحديثها فقط
        hashed_new_pass = bcrypt.hashpw(new_pass.get().encode(), bcrypt.gensalt()).decode()
        User.objects(id=user_obj.id).update(set__password=hashed_new_pass)
        msg_label.configure(text="Password changed successfully!", text_color="#43a047")
        change_pass_card.after(1200, hide_change_pass_form)
    # ثم أنشئ الزر
    ctk.CTkButton(change_pass_card, text="Change Password", fg_color="#1976d2", hover_color="#1565c0", corner_radius=12, width=200, height=44, font=("Segoe UI", 15, "bold"), command=submit_change_pass).pack(pady=(18, 30))

    # Center the window
    root_home.update_idletasks()
    width = root_home.winfo_width()
    height = root_home.winfo_height()
    x = (root_home.winfo_screenwidth() // 2) - (width // 2)
    y = (root_home.winfo_screenheight() // 2) - (height // 2)
    root_home.geometry(f'+{x}+{y}')

    root_home.mainloop()