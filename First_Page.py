import customtkinter as ctk
from PIL import Image, ImageTk
import Settings
from models.models_track import Track
import List
import search_in_all_track
import os
from dotenv import load_dotenv
from tkinter import messagebox

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
    def check_track(track_name):
        track = track_name[0]
        root_home.destroy()
        import Show_All_Data
        Show_All_Data.show_all_data(user.role, track)

    def settings_page():
        if messagebox.askyesno("Confirm", "Are you sure you want to open settings?"):
            root_home.destroy()
            Settings.settings_call(user.role)

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

    def change_pass_call():
        if messagebox.askyesno("Confirm", "Are you sure you want to change password?"):
            import change_pass
            root_home.destroy()
            change_pass.to_change_password(user.role)

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
    label_pad = {'padx': 10, 'pady': (20, 5)}
    icon_size = (22, 22)

    # --- Sidebar Navigation Labels with Icons ---
    label_font = ("Segoe UI", 16, "bold")
    label_fg = "white"
    icon_size = (22, 22)
    label_pad = {'padx': 10, 'pady': (20, 5)}
    label_kwargs = {'anchor': 'w', 'justify': 'left'}

    # Settings label with icon and spacing
    settings_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    settings_frame.pack(fill="x", padx=(18,10), pady=(20, 5))
    ctk.CTkLabel(settings_frame, image=settings_icon, text="", width=22).pack(side="left")
    settings_text = ctk.CTkLabel(settings_frame, text="Settings", font=label_font, text_color=label_fg, cursor="hand2", **label_kwargs)
    settings_text.pack(side="left", padx=(12,0))
    settings_frame.bind("<Button-1>", lambda e: settings_page())
    settings_text.bind("<Button-1>", lambda e: settings_page())

    # Password label with icon and spacing
    pass_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    pass_frame.pack(fill="x", padx=(18,10), pady=5)
    ctk.CTkLabel(pass_frame, image=pass_icon, text="", width=22).pack(side="left")
    pass_text = ctk.CTkLabel(pass_frame, text="Password", font=label_font, text_color=label_fg, cursor="hand2", **label_kwargs)
    pass_text.pack(side="left", padx=(12,0))
    pass_frame.bind("<Button-1>", lambda e: change_pass_call())
    pass_text.bind("<Button-1>", lambda e: change_pass_call())

    # Logout label with icon and spacing
    logout_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    logout_frame.pack(fill="x", padx=(18,10), pady=(5, 20))
    ctk.CTkLabel(logout_frame, image=logout_icon, text="", width=22).pack(side="left")
    logout_text = ctk.CTkLabel(logout_frame, text="Logout", font=label_font, text_color=label_fg, cursor="hand2", **label_kwargs)
    logout_text.pack(side="left", padx=(12,0))
    logout_frame.bind("<Button-1>", lambda e: logout())
    logout_text.bind("<Button-1>", lambda e: logout())
    
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

    main_content = ctk.CTkFrame(root_home, corner_radius=0, fg_color=(LIGHT_BG, DARK_BG))
    main_content.grid(row=0, column=1, sticky="nswe")
    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_rowconfigure(1, weight=1)
    
    # Top bar
    top_bar = ctk.CTkFrame(main_content, height=60, corner_radius=0, fg_color="transparent")
    top_bar.grid(row=0, column=0, sticky="nwe", padx=20, pady=10)
    top_bar.grid_columnconfigure(1, weight=1)
    
    # Page title
    page_title = ctk.CTkLabel(top_bar, 
                            text="Tracks Dashboard",
                            font=("Segoe UI", 22, "bold"),
                            text_color=(TEXT_COLOR_LIGHT, TEXT_COLOR_DARK))
    page_title.grid(row=0, column=0, sticky="w", padx=10)
    
    # Search bar
    search_frame = ctk.CTkFrame(top_bar, height=40, fg_color="transparent")
    search_frame.grid(row=0, column=1, sticky="e", padx=10)
    
    search_entry = ctk.CTkEntry(search_frame,
                              placeholder_text="Search tracks...",
                              width=250,
                              height=36,
                              corner_radius=20,
                              border_width=1,
                              font=("Segoe UI", 14))
    search_entry.pack(side="left", padx=(0, 5))
    
    try:
        search_icon = ctk.CTkImage(light_image=Image.open("search.png"), size=(20, 20))
        search_btn = ctk.CTkButton(search_frame,
                                 text="",
                                 image=search_icon,
                                 width=36,
                                 height=36,
                                 corner_radius=18,
                                 fg_color=PRIMARY_COLOR,
                                 hover_color="#1565c0",
                                 command=lambda: search(None))
        search_btn.pack(side="left")
    except:
        search_btn = ctk.CTkButton(search_frame,
                                 text="Search",
                                 width=80,
                                 height=36,
                                 corner_radius=18,
                                 fg_color=PRIMARY_COLOR,
                                 hover_color="#1565c0",
                                 command=lambda: search(None))
        search_btn.pack(side="left")
    
    # ========== Content Area ========== #
    content_frame = ctk.CTkScrollableFrame(main_content, 
                                         fg_color="transparent",
                                         corner_radius=10)
    content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    content_frame.grid_columnconfigure(0, weight=1)
    
    # Stats cards row
    stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    stats_frame.grid(row=0, column=0, sticky="nwe", pady=(0, 20))
    
    stats = [
        {"title": "Total Tracks", "value": "12", "icon": "book", "color": PRIMARY_COLOR},
        {"title": "Active Trainees", "value": "84", "icon": "people", "color": "#4caf50"},
        {"title": "Completed", "value": "36", "icon": "check", "color": "#ff9800"},
        {"title": "In Progress", "value": "48", "icon": "clock", "color": "#9c27b0"},
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
    
    # Center the window
    root_home.update_idletasks()
    width = root_home.winfo_width()
    height = root_home.winfo_height()
    x = (root_home.winfo_screenwidth() // 2) - (width // 2)
    y = (root_home.winfo_screenheight() // 2) - (height // 2)
    root_home.geometry(f'+{x}+{y}')

    root_home.mainloop()