import customtkinter as cutk
import mysql.connector
import Verification
from dotenv import load_dotenv
import os

def show_data(result, position, track):
    load_dotenv()
    root_data_show = cutk.CTk()
    root_data_show.geometry('750x500')
    root_data_show.minsize(500, 600)
    root_data_show.maxsize(500, 600)
    root_data_show.title('Data')


    from mysql.connector import Error
    try:
        mydb = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWORD'), port=os.getenv('PORT'), database=os.getenv('DATABASE'))
        my_cursor = mydb.cursor()
            
    except Error as e:
        import Verification
        Verification.connection_error()
        return


    frame = cutk.CTkFrame(root_data_show)
    frame.pack(padx=5, pady=5, fill='both', expand=True)


    def Close(): 
        root_data_show.destroy()


    def Edit_and_add():

        def add_in_Degrees():
            global new_number_Degrees
            add_number = int(Degrees.get())
            new_number_Degrees = int(result[2]) + add_number
            sql = f'UPDATE {track} SET degrees = %s WHERE name = %s'
            val = (new_number_Degrees, result[1])
            my_cursor.execute(sql, val)
            mydb.commit()


        def add_in_Additional_Degrees():
            global new_number_Additional_Degrees
            add_number = int(Additional_Degrees.get())
            new_number_Additional_Degrees = int(result[3]) + add_number
            sql = f'UPDATE {track} SET additional_degrees = %s WHERE name = %s'
            val = (new_number_Additional_Degrees, result[1])
            my_cursor.execute(sql, val)
            mydb.commit()


        def add_in_Commintent():
            now_commintent = Commintent.get()
            sql = f'UPDATE {track} SET commintent = %s WHERE name = %s'
            val = (now_commintent, result[1])
            my_cursor.execute(sql, val)
            mydb.commit()

        

        if Degrees.get() != '':
            add_in_Degrees()
        if Additional_Degrees.get() != '':
            add_in_Additional_Degrees()
        if Commintent.get() != '':
            add_in_Commintent()

        Verification.add_done()



    label = cutk.CTkButton(frame, text='ID : ' + result[0], font=('𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜 𝕋𝕖𝕩𝕥', 20), text_color='black', corner_radius=20)
    label.pack(padx=10, pady=12)
    

    labe2 = cutk.CTkButton(frame, text='Name : ' + result[1], font=('𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜 𝕋𝕖𝕩𝕥', 20), text_color='black', corner_radius=20)
    labe2.pack(padx=10, pady=12)


    labe3 = cutk.CTkButton(frame, text='Degrees  : ' + result[2], font=('𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜 𝕋𝕖𝕩𝕥', 20), text_color='black', corner_radius=20)
    labe3.pack(padx=10, pady=12)




    if position == 'editor' or position == 'manager':
        Degrees = cutk.CTkEntry(frame, placeholder_text='Degrees', text_color='black',
                                    placeholder_text_color='black', font=('Roboto', 15), height=30, width=300, corner_radius=20)
        Degrees.pack(padx=10, pady=12)


    labe4 = cutk.CTkButton(frame, text='Additional Degrees : ' + result[3], font=('𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜 𝕋𝕖𝕩𝕥', 20), text_color='black', corner_radius=20)
    labe4.pack(padx=10, pady=12)

    if position == 'editor' or position == 'manager':
        Additional_Degrees = cutk.CTkEntry(frame, placeholder_text='Additional Degrees', text_color='black',
                                    placeholder_text_color='black', font=('Roboto', 15), height=30, width=300, corner_radius=20)
        Additional_Degrees.pack(padx=10, pady=12)



    labe5 = cutk.CTkButton(frame, text='Total  : ' + result[4], font=('𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜 𝕋𝕖𝕩𝕥', 20), text_color='black', corner_radius=20)
    labe5.pack(padx=10, pady=12)


    labe6 = cutk.CTkLabel(frame, text='Commintent : ' + result[5], font=('𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜 𝕋𝕖𝕩𝕥', 20), text_color='black', corner_radius=20)
    labe6.pack(padx=10, pady=12)

    if position == 'editor' or position == 'manager':
        Commintent = cutk.CTkEntry(frame, placeholder_text='Commintent', text_color='black',
                                    placeholder_text_color='black', font=('Roboto', 15), height=30, width=300, corner_radius=20)
        Commintent.pack(padx=10, pady=12)


    if position == 'editor' or position == 'manager':
        add = cutk.CTkButton(frame, text='Add', hover_color='black', text_color='black', command=Edit_and_add, corner_radius=20)
        add.pack(pady=15)

    ok = cutk.CTkButton(frame, text='Ok', hover_color='black', text_color='black', command=Close, corner_radius=20)
    ok.pack(pady=15)

    
    root_data_show.mainloop()






