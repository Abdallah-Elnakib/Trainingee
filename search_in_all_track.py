import customtkinter as cutk
import mysql.connector
from tkinter import *
from  tkinter import ttk
from dotenv import load_dotenv
import os

def search(name_or_id):
    load_dotenv()
    from mysql.connector import Error
    try:
        mydb = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWORD'), port=os.getenv('PORT'), database=os.getenv('DATABASE'))
        my_cursor = mydb.cursor()
    except Error as e:
        import Verification
        Verification.connection_error()
        return

    # Unified program colors (customtkinter-like)
    BG_COLOR = "#f0f0f0"
    FRAME_COLOR = "#e5e9f2"
    ACCENT_COLOR = "#3578e5"
    HEADER_COLOR = "#dde6f7"
    TEXT_COLOR = "#222"

    root_search_in_tracks = cutk.CTk()
    root_search_in_tracks.geometry('900x650')
    root_search_in_tracks.minsize(900, 650)
    root_search_in_tracks.maxsize(900, 650)
    root_search_in_tracks.title('Show All Tracks Search')
    root_search_in_tracks.configure(bg=BG_COLOR)

    # Header
    header = cutk.CTkFrame(root_search_in_tracks, fg_color=HEADER_COLOR, corner_radius=18, height=65)
    header.pack(fill='x', padx=0, pady=(0, 10))
    header_label = cutk.CTkLabel(header, text="Search Results In All Tracks", font=("Segoe UI", 24, "bold"), text_color=ACCENT_COLOR)
    header_label.pack(side='left', padx=28, pady=12)

    # Table frame
    table_frame = cutk.CTkFrame(root_search_in_tracks, fg_color=FRAME_COLOR, corner_radius=16)
    table_frame.pack(fill='both', expand=True, padx=28, pady=(0, 18))

    # Custom Treeview Style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview',
                    background=FRAME_COLOR,
                    fieldbackground=FRAME_COLOR,
                    foreground=TEXT_COLOR,
                    rowheight=38,
                    font=("Segoe UI", 14))
    style.configure('Treeview.Heading',
                    background=ACCENT_COLOR,
                    foreground=BG_COLOR,
                    font=("Segoe UI", 15, "bold"),
                    relief="flat")
    style.map('Treeview', background=[('selected', ACCENT_COLOR)])

    my_data = ttk.Treeview(table_frame, height=12, show='headings', selectmode='browse')
    my_data.pack(fill='both', expand=True, padx=12, pady=12)

    columns = ('Track', 'ID', 'Name', 'Degrees', 'Additional_degrees', 'Total', 'Commintent', 'Total degrees')
    my_data['columns'] = columns
    for col, w in zip(columns, [140, 60, 180, 90, 110, 90, 110, 120]):
        my_data.column(col, anchor=CENTER, width=w, minwidth=60)
        my_data.heading(col, text=col, anchor=CENTER)

    # Scrollbar
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=my_data.yview)
    vsb.pack(side='right', fill='y')
    my_data.configure(yscrollcommand=vsb.set)

    # Query DB
    my_cursor.execute('SHOW TABLES')
    result_track = my_cursor.fetchall()
    found_any = False
    for i in result_track:
        if i[0] != 'data_users_login' and i[0] != 'tracks_name':
            my_cursor.execute(f"SHOW COLUMNS FROM {i[0]}")
            table_columns = [row[0] for row in my_cursor.fetchall()]
            if 'name' in table_columns and 'id' in table_columns:
                sql = f'SELECT * FROM {i[0]} WHERE name LIKE %s OR id = %s'
                data_base = ('%' + name_or_id + '%', name_or_id)
                my_cursor.execute(sql, data_base)
                result = my_cursor.fetchone()
                if result is not None:
                    found_any = True
                    # Get real track name from tracks_name table
                    my_cursor.execute('SELECT name_in_database FROM tracks_name WHERE name = %s', (i[0],))
                    track_name_row = my_cursor.fetchone()
                    track_name = track_name_row[0] if track_name_row else i[0]
                    row_data = [track_name] + list(result[0:])
                    my_data.insert('', 'end', values=row_data)

    if not found_any:
        import Verification
        Verification.Verification_search_name()
        return

    root_search_in_tracks.mainloop()

    