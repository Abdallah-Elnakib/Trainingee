import customtkinter as cutk
import Verification
import mysql.connector
import Show_Data
import List
from dotenv import load_dotenv
import os

def search(position, track):
    load_dotenv()
    root_search = cutk.CTk()
    root_search.geometry('750x500')
    root_search.minsize(650, 400)
    root_search.maxsize(650, 400)
    root_search.title('Search')
    cutk.set_appearance_mode('light')
    cutk.set_default_color_theme('blue')


    frame = cutk.CTkFrame(root_search)
    frame.pack(padx=5, pady=5, fill='both', expand=True)

    label = cutk.CTkLabel(frame, text='Search', font=('𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜 𝕋𝕖𝕩𝕥', 24), text_color='black')
    label.pack(padx=10, pady=12)

    def back():
        root_search.destroy()
        List.search_or_add(position, track)




    def search_in_data():
        from mysql.connector import Error
        try:
            mydb = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWORD'), port=os.getenv('PORT'), database=os.getenv('DATABASE'))
            my_cursor = mydb.cursor()
            
        except Error as e:
            import Verification
            Verification.connection_error()
            return

        entry_name = Name.get()
        if entry_name == '':
            Verification.Verification_add_name()
            return
        else:
            sql = f'SELECT * FROM {track} WHERE name LIKE %s OR id = %s'
            data_base = ('%' + entry_name + '%', entry_name)
            my_cursor.execute(sql, data_base)
            result = my_cursor.fetchone()
            if result is None:
                Verification.Verification_search_name()
                return
            else: 
                total = int(result[2]) + int(result[3])
                sql = f'UPDATE {track} SET total = %s WHERE name = %s'
                val = (total, result[1])
                my_cursor.execute(sql, val)
                mydb.commit()
                sql = f'SELECT * FROM {track} WHERE name LIKE %s OR id = %s'
                data_base = ('%' + entry_name + '%', entry_name)
                my_cursor.execute(sql, data_base)
                result_total = my_cursor.fetchone()
                Show_Data.show_data(result_total, position, track)



    Name = cutk.CTkEntry(frame, placeholder_text='Search',  text_color='black',
                                placeholder_text_color='black', font=('Roboto', 15), height=30, width=410, corner_radius=20, border_color='black', border_width=2)
    Name.pack(padx=10, pady=12)

    search_button_name = cutk.CTkButton(frame, text='Search', hover_color='white', text_color='black', command=search_in_data, corner_radius=20, border_color='black', border_width=2)
    search_button_name.pack(pady=15)




    def Close(): 
        root_search.destroy()


    back = cutk.CTkButton(frame, text='Back', hover_color='white', text_color='black', command=back, corner_radius=20, border_color='black', border_width=2)
    back.pack(pady=15)

    Close = cutk.CTkButton(frame, text='Close', hover_color='white', text_color='black', command=Close, corner_radius=20, border_color='black', border_width=2) 
    Close.pack(pady=15)

    root_search.bind('<Return>', lambda e: search_in_data())

    root_search.mainloop()



