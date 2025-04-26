import customtkinter as cutk
from PIL import Image, ImageTk
import Settings
from models.models_track import Track
import List
import search_in_all_track
import os
from dotenv import load_dotenv



def first_page(position):
    load_dotenv()   
    root_home = cutk.CTk()
    root_home.geometry('1085x700')
    root_home.minsize(1085, 670)
    root_home.maxsize(1085, 670)
    root_home.title('Trainingee | Home')
    cutk.set_appearance_mode('system')
    cutk.set_default_color_theme('blue')
    root_home.configure(bg='#f4f8fb')

    # Header Bar
    header = cutk.CTkFrame(root_home, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=60)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)

    header_title = cutk.CTkLabel(header, text='Trainingee Dashboard', font=("Segoe UI", 22, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=30, pady=18, sticky='w')

    # Logout Button
    logout_btn = cutk.CTkButton(header, text='Logout', width=110, height=36, fg_color=("#e53935","#b71c1c"), text_color="#fff", hover_color="#c62828", corner_radius=15, command=lambda: logout())
    logout_btn.grid(row=0, column=2, padx=15, pady=12, sticky='e')

    # Change Password Button
    change_pass_btn = cutk.CTkButton(header, text='Change Password', width=140, height=36, fg_color=("#1565c0","#3949ab"), text_color="#fff", hover_color="#1976d2", corner_radius=15, command=lambda: change_pass_call())
    change_pass_btn.grid(row=0, column=1, padx=5, pady=12, sticky='e')
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)
    header.grid_columnconfigure(2, weight=0)

    # Main Content Frame
    frame = cutk.CTkScrollableFrame(root_home, width=1000, height=600, fg_color=("#f4f8fb", "#23272e"))
    frame.pack(padx=20, pady=(10, 20), fill='both', expand=True)



    def check_track(track_name):
        track = track_name[0]
        root_home.destroy()
        List.search_or_add(position, track)

    def settings_page():
        root_home.destroy()
        Settings.settings_call(position)

    
    def search(event):
        entry_name = Name.get()
        search_in_all_track.search(entry_name)


    def logout():
        root_home.destroy()
        import link
        link.Logout()


    def change_pass_call():
        import change_pass
        root_home.destroy()
        change_pass.to_change_password(position)


    # حذف أزرار logout/change_pass من الإطار الرئيسي لأنها أصبحت في الهيدر

    # Settings button for manager
    if position == 'manager':
        image = Image.open("setti.png")
        image = image.resize((18, 18))
        photo = ImageTk.PhotoImage(image)
        settings_btn = cutk.CTkButton(header, text="Settings", command=settings_page, width=120, height=36, corner_radius=15,
                                      fg_color=("#43a047","#388e3c"), text_color="#fff", hover_color="#388e3c", image=photo, compound="left")
        settings_btn.grid(row=0, column=3, padx=15, pady=12, sticky='e')
        header.grid_columnconfigure(3, weight=0)

    # Search Entry with icon
    search_icon = cutk.CTkImage(light_image=Image.open('search.png').resize((22,22)), size=(22,22)) if os.path.exists('search.png') else None
    search_frame = cutk.CTkFrame(frame, fg_color=("#e3eafc", "#23272e"), corner_radius=14)
    search_frame.grid(row=0, column=0, columnspan=2, pady=(10, 30), padx=(0,0), sticky='w')
    Name = cutk.CTkEntry(search_frame, placeholder_text='Search for track...',  text_color='#23272e', placeholder_text_color='#90a4ae',
                         font=("Segoe UI", 15), height=38, width=370, corner_radius=14, border_color='#1976d2', border_width=2)
    Name.pack(side='left', padx=(8,5), pady=6)
    if search_icon:
        search_icon_label = cutk.CTkLabel(search_frame, image=search_icon, text='')
        search_icon_label.pack(side='left', padx=(0,8))
    
    from config.ConnDB import get_db
    get_db()
    row = 2
    column = 0
    # Modern cards for tracks (2 columns per row)
    for track in Track.objects():
        Track_name = track.track_name
        card_btn = cutk.CTkButton(frame, corner_radius=25, fg_color=("#fff", "#263238"),
                            text_color=("#1976d2","#90caf9"), hover_color=("#e3eafc","#37474f"), font=("Segoe UI", 20, "bold"), 
                            text=Track_name, width=400, height=110, border_color=("#1976d2","#90caf9"), border_width=2)
        card_btn.configure(command=lambda button=track.track_name: check_track((button,)))
        card_btn.grid(row=row, column=column, padx=18, pady=28)
        if column == 1:
            column = 0
            row += 1 
        else:
            column += 1

    
    root_home.bind('<Return>', search)

    root_home.mainloop()

