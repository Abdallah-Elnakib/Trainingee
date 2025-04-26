import tkinter as tk
from  tkinter import ttk
from pymongo import MongoClient
import customtkinter as cutk
import Add_Student
import List
# import pyarabic.araby as araby
from dotenv import load_dotenv
import os


def show_all_data(position, track):
    load_dotenv()
    global my_data, columns
    import Verification
    try:
        mongo_client = MongoClient(os.getenv('MONGO_URI'))
        db = mongo_client[os.getenv('DATABASE')]
        collection = db[track]
    except Exception as e:
        import Verification
        Verification.connection_error()
        List.search_or_add(position, track)
        return


    def delete_student_in_database():
        def delete():
            collection.delete_one({"id": item_id})

        selected_item = my_data.selection()[0]
        item_values = my_data.item(selected_item, 'values')  # Get values of the selected item
        item_id = str(item_values[0])
        my_data.delete(selected_item)
        delete()

    # this function useing to delete row in database and delete in treeviwe
    def delete_record():
        delete_student = cutk.CTk()
        delete_student.geometry('750x600')
        delete_student.minsize(850, 200)
        delete_student.maxsize(850, 200)
        delete_student.title('Error')



        def Cancel(): 
            delete_student.destroy()
        
        def ok():
            delete_student.destroy()
            delete_student_in_database()
            

        frame = cutk.CTkFrame(delete_student)
        frame.pack(padx=1, pady=1, fill='both', expand=True)

        label_text = cutk.CTkLabel(frame, font=('Roboto', 16), text='Warning This action will result in the student being permanently deleted from the database. Are you sure?',
                                               text_color='red')
        label_text.pack()

        button_cansel = cutk.CTkButton(frame, text='Cancel', hover_color='white', text_color='black', command=Cancel, corner_radius=20, border_color='black', border_width=2)
        button_cansel.pack(pady=15)

        button = cutk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=ok, corner_radius=20, border_color='black', border_width=2)
        button.pack(pady=15)

        delete_student.mainloop()
        

    

    # this function to get all days in start dat to today and chech degrees 
    def get_degrees():
        add_task = cutk.CTk()
        add_task.geometry('750x600')
        add_task.minsize(450, 200)
        add_task.maxsize(450, 200)
        add_task.title('Error')



        def Cancel(): 
            add_task.destroy()
        
        def ok():
            global total
            degrees_ = Degrees.get()
            students = list(collection.find())
            for i in students:
                if i.get('degrees') is not None and i.get('additional') is not None:
                    degrees = int(i.get('total_degrees', 0)) + int(degrees_)
                    collection.update_one({'name': i['name']}, {'$set': {'total_degrees': degrees}})
            add_task.destroy()
            refrash()
        
            

        frame = cutk.CTkFrame(add_task)
        frame.pack(padx=1, pady=1, fill='both', expand=True)

        label_text = cutk.CTkLabel(frame, font=('Roboto', 16), text='Add Task',
                                               text_color='green')
        label_text.pack()

        Degrees = cutk.CTkEntry(frame, placeholder_text='Degrees',  text_color='black',
                            placeholder_text_color='black', font=('Roboto', 15), height=30, width=250, border_color='black', border_width=2)
        Degrees.pack(padx=10, pady=12)

        button_cansel = cutk.CTkButton(frame, text='Cancel', hover_color='white', text_color='black', command=Cancel, corner_radius=20, border_color='black', border_width=2)
        button_cansel.pack(pady=15)

        button = cutk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=ok, corner_radius=20, border_color='black', border_width=2)
        button.pack(pady=15)

        add_task.mainloop()

    def update_treeviwe(values,selected_item):
        global result_after_add_ranking
        result_after_add_ranking[int(values[7])-1][1] = values[1]
        result_after_add_ranking[int(values[7])-1][2] = values[2] 
        result_after_add_ranking[int(values[7])-1][3] = values[3] 
        result_after_add_ranking[int(values[7])-1][4] = int(values[2]) + int(values[3])
        result_after_add_ranking[int(values[7])-1][5] = values[5]      
        my_data.item(selected_item, values=result_after_add_ranking[int(values[7])-1])

        data = [(my_data.item(child)["values"], child) for child in my_data.get_children()]
        data.sort(key=lambda x: x[0][4], reverse=True)
        result_after_add_ranking.sort(key=lambda x: x[4], reverse=True)
        new_rank = 0
        for index, (_, item_id) in enumerate(data):
            my_data.move(item_id, '', index)

        for child in my_data.get_children():
            result_after_add_ranking[new_rank][7] = new_rank + 1
            item = my_data.item(child)['values']
            if item[4] != None and item[2] != None and item[3] != None:
                if int(item[4]) == 0 and int(item[6]) != 0: 
                    my_data.item(child, tags = ('= 0',), values=result_after_add_ranking[new_rank]) 
                    my_data.tag_configure('= 0', background='red')
                # If degrees to student > 85% set color 
                elif int(item[2]) < int(item[6]) * 0.85 and int(item[2]) > int(item[6]) * 0.75:
                    my_data.item(child, tags = ('< 0.85 > 0.75',), values=result_after_add_ranking[new_rank]) 
                    my_data.tag_configure('< 0.85 > 0.75', background='#aacc00')
                # if degees to student < 85% and deegree > 75% set color
                elif int(item[2]) < int(item[6]) *0.75 :
                    my_data.item(child, tags = ('< 0.75',), values=result_after_add_ranking[new_rank]) 
                    my_data.tag_configure('< 0.75', background='#e9e04f')

                else : 
                    my_data.item(child, tags = ('> 0.85',), values=result_after_add_ranking[new_rank])
                    my_data.tag_configure('> 0.85', background='#57e94f')

            new_rank += 1



    def edit_cell(event):
        global entry
        import Verification
        selected_item = my_data.selection()[0]
        column = my_data.identify_column(event.x)
        row = my_data.identify_row(event.y)
        x, y, width, height = my_data.bbox(selected_item, column)
        if x == 2:
            Verification.error_id_chaged()
            return

        x_tree, y_tree, width, height = my_data.bbox(selected_item, column)
        tree_abs_x = my_data.winfo_rootx()
        tree_abs_y = my_data.winfo_rooty()
        root_abs_x = root_all_data.winfo_rootx()
        root_abs_y = root_all_data.winfo_rooty()
        x_abs = x_tree + tree_abs_x - root_abs_x
        y_abs = y_tree + tree_abs_y - root_abs_y
        entry = tk.Entry(root_all_data)
        entry.place(x=x_abs, y=y_abs, width=width, height=height)
        entry.insert(0, my_data.set(selected_item, column))

        def update_database_and_treeviwe(new_value):
            my_data.set(selected_item, column, new_value)
            values = my_data.item(selected_item, "values")
            update_treeviwe(values,selected_item)
            update_database(values)

        def save_edit(event):
            global entry
            new_value = entry.get()
            entry.destroy()
            update_database_and_treeviwe(new_value)

        entry.bind("<Return>", save_edit)
        entry.focus()

    def add_to_treeviwe():
        global result_after_add_ranking

        students = list(collection.find())
        for i in students:
            if i.get('degrees') is not None and (i.get('additional') is not None and i.get('additional') != ''):
                total = int(i['degrees']) + int(i['additional'])
                collection.update_one({'name': i['name']}, {'$set': {'total': total}})

        ranking = 1
        sorted_students = list(collection.find().sort('total', -1))
        result_after_add_ranking = []
        for i in sorted_students:
            row = [i.get('id'), i.get('name'), i.get('degrees'), i.get('additional'), i.get('total'), i.get('commintent'), i.get('total_degrees'), ranking]
            result_after_add_ranking.append(row)
            ranking += 1

        for i in result_after_add_ranking:
            # If degrees to student =  0 set color 
            

            if i[4] != None and i[2] != None and i[3] != None:
                if int(i[4]) == 0 and int(i[6]) != 0:
                    my_data.insert(tags = ('= 0',), parent='', index='end',  text='', values=i) 
                    my_data.tag_configure('= 0', background='red')

            # If degrees to student > 85% set color 
            
                elif int(i[2]) < int(i[6]) * 0.85 and int(i[2]) > int(i[6]) * 0.75:
                    my_data.insert(tags = ('< 0.85 > 0.75',), parent='', index='end',  text='', values=i) 
                    my_data.tag_configure('< 0.85 > 0.75', background='#aacc00')
                # if degees to student < 85% and deegree > 75% set color
                elif int(i[2]) < int(i[6]) *0.75 :
                    my_data.insert(tags = ('< 0.75',), parent='', index='end',  text='', values=i) 
                    my_data.tag_configure('< 0.75', background='#e9e04f')

                else : 
                    my_data.insert(tags = ('> 0.85',), parent='', index='end',  text='', values=i)
                    my_data.tag_configure('> 0.85', background='#57e94f')




    def Add_student_call():
        Add_Student.Add_student(position, track)

    # this function Used to return to the previous page.
    def back(): 
        root_all_data.destroy()
        List.search_or_add(position, track)

    # this function used to Refrash page and get all data in database
    def refrash():
        root_all_data.destroy()
        show_all_data(position, track)

    # this function used to search in database to get data and show is data
    def logout():
        import link
        root_all_data.destroy()


    def check():
        query = str(search_entry.get()).strip().lower()
        for i in my_data.get_children():
            item = my_data.item(i)['values']
            student_id = str(item[0]).strip().lower()
            student_name = str(item[1]).strip().lower()
            if query in student_id or query in student_name:
                my_data.selection_set(i)
                my_data.see(i)
                break


    root_all_data = cutk.CTk()  
    root_all_data.title('All Students | Trainingee')
    root_all_data.minsize(1150, 720)
    root_all_data.maxsize(1300, 900)
    cutk.set_appearance_mode('system')
    cutk.set_default_color_theme('blue')
    root_all_data.configure(bg='#f4f8fb')

    # Header Bar
    header = cutk.CTkFrame(root_all_data, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=60)
    header.grid(row=0, column=0, columnspan=10, sticky='ew')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='All Students', font=("Segoe UI", 22, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=30, pady=18, sticky='w')
    logout_btn = cutk.CTkButton(header, text='Logout', width=110, height=36, fg_color=("#e53935","#b71c1c"), text_color="#fff", hover_color="#c62828", corner_radius=15, command=logout)
    logout_btn.grid(row=0, column=2, padx=15, pady=12, sticky='e')
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)
    header.grid_columnconfigure(2, weight=0)

    # Main Content Frame
    content_frame = cutk.CTkFrame(root_all_data, fg_color=("#f4f8fb", "#23272e"), corner_radius=20)
    content_frame.grid(row=1, column=0, padx=20, pady=(10, 10), sticky='nsew', columnspan=10)
    root_all_data.rowconfigure(1, weight=1)
    root_all_data.columnconfigure(0, weight=1)

    # Custom style for Treeview
    style = ttk.Style(root_all_data)
    style.theme_use('clam')
    style.configure('Treeview', background ='#f7fafd', fieldbackground = '#f7fafd', foreground = '#222', rowheight=38, font=('Segoe UI', 13), borderwidth=0)
    style.configure('Treeview.Heading', background = '#1976d2', foreground = 'white', font=('Segoe UI', 14, 'bold'))
    style.map('Treeview', background=[('selected', '#bbdefb')])

    
    columns = ['ID', 'Name', 'Degrees', 'Additional', 'Total', 'Commintent', 'Total degrees', 'Ranking']
    my_data = ttk.Treeview(content_frame, height=17, columns=columns, show='headings', style='Treeview')
    my_data.column("#0", width=0)
    my_data.column("ID", width=40, anchor='center')
    my_data.column("Name", width=250)
    my_data.column("Degrees", width=80, anchor='center')
    my_data.column("Additional", width=80, anchor='center')
    my_data.column("Total", width=80, anchor='center')
    my_data.column("Commintent" , width=160)
    my_data.column("Total degrees" , width=80, anchor='center')
    my_data.column("Ranking" , width=80, anchor='center')
    for col in columns:
        my_data.heading(col, text=col)
    my_data.grid(column=0, row=2, columnspan=10, pady=(15,10), padx=10, sticky='nsew')
    content_frame.rowconfigure(2, weight=1)
    content_frame.columnconfigure(0, weight=1)

    # Search bar and action buttons
    top_btns_frame = cutk.CTkFrame(content_frame, fg_color=("#f4f8fb", "#23272e"), corner_radius=12)
    top_btns_frame.grid(row=1, column=0, pady=(10,0), padx=10, sticky='ew')
    # Search Entry
    search_entry = cutk.CTkEntry(top_btns_frame, placeholder_text='Search by ID or Name...', text_color='#23272e', placeholder_text_color='#90a4ae', font=("Segoe UI", 15), height=38, width=350, corner_radius=14, border_color='#1976d2', border_width=2)
    search_entry.pack(side='left', padx=(8,5), pady=8)
    search_entry.bind('<Return>', lambda e: check())
    # Action Buttons
    btns = []
    if position == 'manager' or position == 'editor':
        btns.append(cutk.CTkButton(top_btns_frame, text='Add Student', width=120, height=38, fg_color=("#43a047","#388e3c"), text_color="#fff", hover_color="#388e3c", font=("Segoe UI", 13, "bold"), command=Add_student_call, corner_radius=14))
        btns.append(cutk.CTkButton(top_btns_frame, text='Delete Student', width=120, height=38, fg_color=("#e53935","#b71c1c"), text_color="#fff", hover_color="#c62828", font=("Segoe UI", 13, "bold"), command=delete_record, corner_radius=14))
        btns.append(cutk.CTkButton(top_btns_frame, text='Add Task', width=110, height=38, fg_color=("#0288d1","#81d4fa"), text_color="#fff", hover_color="#0277bd", font=("Segoe UI", 13, "bold"), command=get_degrees, corner_radius=14))
    btns.append(cutk.CTkButton(top_btns_frame, text='Refresh', width=110, height=38, fg_color=("#1976d2","#90caf9"), text_color="#fff", hover_color="#1565c0", font=("Segoe UI", 13, "bold"), command=refrash, corner_radius=14))
    btns.append(cutk.CTkButton(top_btns_frame, text='Back', width=90, height=38, fg_color=("#757575","#bdbdbd"), text_color="#fff", hover_color="#616161", font=("Segoe UI", 13, "bold"), command=back, corner_radius=14))
    for b in btns:
        b.pack(side='left', padx=6, pady=8)

    # Bind edit on double click
    if position != 'user':
        my_data.bind("<Double-1>", edit_cell)

    add_to_treeviwe()

    # Footer
    footer = cutk.CTkLabel(root_all_data, text='All rights reserved © 2025', font=("Segoe UI", 10), text_color=("#90a4ae","#b0bec5"))
    footer.grid(row=3, column=0, columnspan=10, pady=(0,8), sticky='sew')

    root_all_data.mainloop()

