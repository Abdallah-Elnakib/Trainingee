import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
import customtkinter as ctk
from customtkinter import CTkImage
from models.models_track import Track
from config.ConnDB import get_db
from dotenv import load_dotenv
import ui_colors
import os
import List
from PIL import Image, ImageTk

class StudentManager:
    def __init__(self, position, track):
        self.position = position
        self.track = track
        self.root = None
        self.tree = None
        self.search_entry = None
        self.pending_new_row = None
        self.pending_new_entry = None
        self.result_after_add_ranking = []
        self.columns = ['ID', 'Name', 'Degrees', 'Additional', 'Total', 'Comments', 'Total Degrees', 'Ranking', '']
        
        load_dotenv()
        self.setup_database()
        self.create_ui()
        
    def setup_database(self):
        try:
            self.mongo_client = MongoClient(os.getenv('MONGO_URI'))
            self.db = self.mongo_client['test']
            self.collection = self.db['test']
        except Exception as e:
            self.show_connection_error()
            
    def show_connection_error(self):
        import Verification
        Verification.connection_error()
        List.search_or_add(self.position, self.track)
        
    def create_ui(self):
        self.root = ctk.CTk()
        self.setup_window()
        self.create_header()
        self.create_main_content()
        self.setup_treeview()
        self.load_students()
        self.center_window()
        self.root.mainloop()
        
    def setup_window(self):
        self.root.title(f'Trainingee | {self.track} Students')
        self.root.geometry('1280x800')
        self.root.minsize(1150, 720)
        ctk.set_appearance_mode('system')
        self.root.configure(fg_color="#f4f6fb")
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_header(self):
        header = ctk.CTkFrame(self.root, fg_color=ui_colors.get_header_color(), corner_radius=0, height=90)
        header.grid(row=0, column=0, sticky="nsew", columnspan=10)
        header.grid_columnconfigure(1, weight=1)

        # شعار أو أيقونة (يمكنك استبدال المسار بصورة شعارك)
        try:
            logo_img = CTkImage(Image.open('Logo.ico'), size=(38, 38))
            logo_label = ctk.CTkLabel(header, image=logo_img, text="", width=38)
            logo_label.image = logo_img
            logo_label.grid(row=0, column=0, padx=(18, 8), pady=8, sticky="w")
        except Exception:
            pass

        # زر العودة
        back_btn = ctk.CTkButton(header, text="←", width=40, height=40, fg_color="transparent", hover_color=ui_colors.get_hover_primary(), font=("Segoe UI", 20, "bold"), command=self.go_back)
        back_btn.grid(row=0, column=0, padx=(60, 10), sticky="w")

        # العنوان
        title = ctk.CTkLabel(header, text=f"Students Management - {self.track}", font=("Segoe UI", 26, "bold"), text_color=ui_colors.get_text_color())
        title.grid(row=0, column=1, sticky="n", pady=10)

        self.create_action_buttons(header)
        
    def create_action_buttons(self, header):
        actions_frame = ctk.CTkFrame(header, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e", padx=20)
        try:
            add_icon = CTkImage(Image.open('add_icon.png'), size=(22, 22))
            task_icon = CTkImage(Image.open('task_icon.png'), size=(22, 22))
            refresh_icon = CTkImage(Image.open('refresh_icon.png'), size=(22, 22))
            logout_icon = CTkImage(Image.open('logout_icon.png'), size=(22, 22))
        except Exception:
            add_icon = task_icon = refresh_icon = logout_icon = None
        if self.position in ['manager', 'editor']:
            ctk.CTkButton(actions_frame,
                         text="Add Student",
                         image=add_icon,
                         compound="left",
                         width=140,
                         height=48,
                         fg_color="#43a047",
                         hover_color="#388e3c",
                         font=("Segoe UI", 15, "bold"),
                         corner_radius=24,
                         command=self.add_student_dialog).pack(side="left", padx=8, pady=8)
            ctk.CTkButton(actions_frame,
                         text="Add Task",
                         image=task_icon,
                         compound="left",
                         width=130,
                         height=48,
                         fg_color="#ffa726",
                         hover_color="#ff9800",
                         font=("Segoe UI", 15, "bold"),
                         corner_radius=24,
                         command=self.add_task_dialog).pack(side="left", padx=8, pady=8)
        ctk.CTkButton(actions_frame,
                     text="Refresh",
                     image=refresh_icon,
                     compound="left",
                     width=120,
                     height=48,
                     fg_color="#1976d2",
                     hover_color="#1565c0",
                     font=("Segoe UI", 15, "bold"),
                     corner_radius=24,
                     command=self.refresh_data).pack(side="left", padx=8, pady=8)
        ctk.CTkButton(actions_frame,
                     text="Logout",
                     image=logout_icon,
                     compound="left",
                     width=120,
                     height=48,
                     fg_color="#e53935",
                     hover_color="#b71c1c",
                     font=("Segoe UI", 15, "bold"),
                     corner_radius=24,
                     command=self.logout).pack(side="left", padx=8, pady=8)
    
    def create_main_content(self):
        # إطار حول الجدول مع ظل خفيف
        main_content = ctk.CTkFrame(self.root, fg_color="#e3eafc", corner_radius=18)
        main_content.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 30))
        main_content.grid_rowconfigure(1, weight=1)
        main_content.grid_columnconfigure(0, weight=1)
        self.create_search_bar(main_content)
        self.tree_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        self.tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_search_bar(self, parent):
        search_frame = ctk.CTkFrame(parent, height=64, fg_color="#f4f8fb", corner_radius=32)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 14), padx=0)
        search_frame.grid_columnconfigure(1, weight=1)
        # أيقونة العدسة
        try:
            search_icon = CTkImage(Image.open('search.png'), size=(20, 20))
        except Exception:
            search_icon = None
        icon_label = ctk.CTkLabel(search_frame, image=search_icon, text="", width=32)
        icon_label.image = search_icon
        icon_label.grid(row=0, column=0, padx=(18, 0))
        self.search_entry = ctk.CTkEntry(search_frame,
                                      placeholder_text="Search by student name or ID...",
                                      width=420,
                                      height=44,
                                      corner_radius=22,
                                      border_width=2,
                                      font=("Segoe UI", 15),
                                      text_color=ui_colors.get_text_color(),
                                      placeholder_text_color=ui_colors.get_placeholder_color())
        self.search_entry.grid(row=0, column=1, padx=(8, 8), pady=10, sticky="ew")
        self.search_entry.bind('<Return>', lambda e: self.search_student())
        search_btn = ctk.CTkButton(search_frame,
                                 text="Search",
                                 width=100,
                                 height=44,
                                 fg_color=ui_colors.PRIMARY_COLOR,
                                 hover_color=ui_colors.get_hover_primary(),
                                 font=("Segoe UI", 15, "bold"),
                                 corner_radius=22,
                                 command=self.search_student)
        search_btn.grid(row=0, column=2, padx=(0, 18))
        self.results_label = ctk.CTkLabel(search_frame,
                                        text="0 students",
                                        font=("Segoe UI", 14),
                                        text_color=ui_colors.get_text_color())
        self.results_label.grid(row=0, column=3, padx=(10, 18))
    
    def setup_treeview(self):
        ROW_COLOR_1 = "#ffffff"
        ROW_COLOR_2 = "#f0f4fa"
        HEADER_COLOR = "#1976d2"
        SELECTED_COLOR = "#e3f2fd"
        TEXT_COLOR = "#23272e"
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', 
            background=ROW_COLOR_1,
            foreground=TEXT_COLOR,
            fieldbackground=ROW_COLOR_1,
            rowheight=48,
            font=('Segoe UI', 14),
            borderwidth=0)
        style.configure('Treeview.Heading', 
            background=HEADER_COLOR,
            foreground='white',
            font=('Segoe UI', 15, 'bold'),
            padding=14)
        style.map('Treeview', 
            background=[('selected', SELECTED_COLOR)],
            foreground=[('selected', HEADER_COLOR)])
        columns = self.columns
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', style='Treeview', selectmode='browse')
        self.tree.column("ID", width=80, anchor='center')
        self.tree.column("Name", width=300, anchor='w')
        self.tree.column("Degrees", width=120, anchor='center')
        self.tree.column("Additional", width=120, anchor='center')
        self.tree.column("Total", width=120, anchor='center')
        self.tree.column("Comments", width=250, anchor='w') 
        self.tree.column("Total Degrees", width=150, anchor='center')
        self.tree.column("Ranking", width=100, anchor='center')
        self.tree.column("", width=80, anchor='center')
        for col in columns:
            self.tree.heading(col, text=col)
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.tree.tag_configure('excellent', background='#e8f5e9')  
        self.tree.tag_configure('good', background='#fff8e1')      
        self.tree.tag_configure('poor', background='#ffebee')      
        self.tree.tag_configure('new', background='#e3f2fd')       
        if self.position != 'user':
            self.tree.bind("<Double-1>", self.edit_cell)
            self.tree.bind("<ButtonRelease-1>", self.on_delete_click)

    def load_students(self, filter_query=None):
        self.tree.delete(*self.tree.get_children())
        self.result_after_add_ranking = []
        track_doc = self.db['tracks'].find_one({'track_name': self.track})
        students = []
        if track_doc and 'track_data' in track_doc:
            students = track_doc['track_data']
        students.sort(key=lambda x: (x.get('degrees', 0) + x.get('additional', 0)), reverse=True)
        if filter_query:
            students = [s for s in students if filter_query in str(s.get('student_id', '')).lower() or filter_query in str(s.get('name', '')).lower()]
        for idx, student in enumerate(students, 1):
            student_id = student.get('student_id', '')
            name = student.get('name', '')
            degrees = student.get('degrees', 0)
            additional = student.get('additional', 0)
            total = degrees + additional
            comments = student.get('comments', '')
            total_degrees = student.get('total_degrees', 0)
            tags = self.get_performance_tags(degrees, total_degrees)
            values = [student_id, name, degrees, additional, total, comments, total_degrees, idx, '🗑️']
            self.result_after_add_ranking.append(values)
            row_tag = 'alt' if idx % 2 == 0 else ''
            self.tree.insert('', 'end', values=values, tags=tags + (row_tag,))
            self.tree.tag_configure('alt', background="#f0f4fa")
        self.results_label.configure(text=f"{len(students)} students")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f'+{x}+{y}')

    def go_back(self):
        if self.root and self.root.winfo_exists():
            self.root.destroy()
        List.search_or_add(self.position, self.track)

    def add_student_dialog(self):
        self.pending_new_row = None
        self.pending_new_entry = None
        self.add_student()

    def add_task_dialog(self):
        self.get_degrees()

    def refresh_data(self):
        self.root.destroy()
        self.show_all_data()

    def logout(self):
        import link
        self.root.destroy()

    def search_student(self):
        query = self.search_entry.get().strip().lower()
        self.load_students(filter_query=query)

    def edit_cell(self, event):
        global entry
        import Verification
        selected_item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)
        x, y, width, height = self.tree.bbox(selected_item, column)
        if x == 2:
            Verification.error_id_chaged()
            return

        x_tree, y_tree, width, height = self.tree.bbox(selected_item, column)
        tree_abs_x = self.tree.winfo_rootx()
        tree_abs_y = self.tree.winfo_rooty()
        root_abs_x = self.root.winfo_rootx()
        root_abs_y = self.root.winfo_rooty()
        x_abs = x_tree + tree_abs_x - root_abs_x
        y_abs = y_tree + tree_abs_y - root_abs_y
        entry = tk.Entry(self.root)
        entry.place(x=x_abs, y=y_abs, width=width, height=height)
        entry.insert(0, self.tree.set(selected_item, column))

        def update_database_and_treeviwe(new_value):
            self.tree.set(selected_item, column, new_value)
            values = self.tree.item(selected_item, "values")
            self.update_treeviwe(values, selected_item)
            self.update_database(values)

        def update_database(values):
            student_id = values[0]
            try:
                student_id_db = int(student_id)
            except ValueError:
                student_id_db = student_id
            new_data = {
                'name': values[1],
                'degrees': int(values[2]),
                'additional': int(values[3]),
                'comments': values[5]
            }
            self.db['tracks'].update_one(
                {'track_name': self.track, 'track_data.student_id': student_id_db},
                {'$set': {
                    'track_data.$.name': new_data['name'],
                    'track_data.$.degrees': new_data['degrees'],
                    'track_data.$.additional': new_data['additional'],
                    'track_data.$.comments': new_data['comments']
                }}
            )

        def save_edit(event):
            global entry
            new_value = entry.get()
            entry.destroy()
            update_database_and_treeviwe(new_value)

        entry.bind("<Return>", save_edit)
        entry.focus()

    def update_treeviwe(self, values, selected_item):
        self.result_after_add_ranking[int(values[7])-1][1] = values[1]
        self.result_after_add_ranking[int(values[7])-1][2] = values[2] 
        self.result_after_add_ranking[int(values[7])-1][3] = values[3] 
        self.result_after_add_ranking[int(values[7])-1][4] = int(values[2]) + int(values[3])
        self.result_after_add_ranking[int(values[7])-1][5] = values[5]      
        self.tree.item(selected_item, values=self.result_after_add_ranking[int(values[7])-1])

        data = [(self.tree.item(child)["values"], child) for child in self.tree.get_children()]
        data.sort(key=lambda x: x[0][4], reverse=True)
        self.result_after_add_ranking.sort(key=lambda x: x[4], reverse=True)
        new_rank = 0
        for index, (_, item_id) in enumerate(data):
            self.tree.move(item_id, '', index)

        for child in self.tree.get_children():
            self.result_after_add_ranking[new_rank][7] = new_rank + 1
            item = self.tree.item(child)['values']
            if item[4] != None and item[2] != None and item[3] != None:
                if int(item[4]) == 0 and int(item[6]) != 0: 
                    self.tree.item(child, tags = ('= 0',), values=self.result_after_add_ranking[new_rank]) 
                    self.tree.tag_configure('= 0', background='red')
                # If degrees to student > 85% set color 
                elif int(item[2]) < int(item[6]) * 0.85 and int(item[2]) > int(item[6]) * 0.75:
                    self.tree.item(child, tags = ('< 0.85 > 0.75',), values=self.result_after_add_ranking[new_rank]) 
                    self.tree.tag_configure('< 0.85 > 0.75', background='#aacc00')
                # if degees to student < 85% and deegree > 75% set color
                elif int(item[2]) < int(item[6]) *0.75 :
                    self.tree.item(child, tags = ('< 0.75',), values=self.result_after_add_ranking[new_rank]) 
                    self.tree.tag_configure('< 0.75', background='#e9e04f')

                else : 
                    self.tree.item(child, tags = ('> 0.85',), values=self.result_after_add_ranking[new_rank])
                    self.tree.tag_configure('> 0.85', background='#57e94f')

            new_rank += 1

    def on_delete_click(self, event):
        column = self.tree.identify_column(event.x)
        if column != f'#{len(self.columns)}':  # عمود الحذف
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return
        values = self.tree.item(item)['values']
        student_id = values[0]
        student_name = values[1]
        confirm_dialog = ctk.CTkToplevel(self.root)
        confirm_dialog.title("Confirm Deletion")
        confirm_dialog.geometry("400x200")
        confirm_dialog.resizable(False, False)
        confirm_dialog.transient(self.root)
        confirm_dialog.grab_set()
        frame = ctk.CTkFrame(confirm_dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        msg = ctk.CTkLabel(frame,
                          text=f"Delete student {student_name} (ID: {student_id})?",
                          font=("Segoe UI", 14),
                          text_color=ui_colors.get_text_color())
        msg.pack(pady=10)
        warning = ctk.CTkLabel(frame,
                             text="This action cannot be undone!",
                             font=("Segoe UI", 12),
                             text_color=ui_colors.get_danger_color())
        warning.pack(pady=5)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        def do_delete():
            self.db['tracks'].update_one(
                {'track_name': self.track},
                {'$pull': {'track_data': {'student_id': student_id}}}
            )
            self.tree.delete(item)
            self.recalculate_rankings()
            confirm_dialog.destroy()
        cancel_btn = ctk.CTkButton(btn_frame,
                                  text="Cancel",
                                  width=100,
                                  fg_color=ui_colors.SECONDARY_COLOR,
                                  hover_color=ui_colors.get_hover_secondary(),
                                  command=confirm_dialog.destroy)
        cancel_btn.pack(side="left", padx=10)
        delete_btn = ctk.CTkButton(btn_frame,
                                  text="Delete",
                                  width=100,
                                  fg_color=ui_colors.ERROR_COLOR,
                                  hover_color=ui_colors.get_hover_error(),
                                  command=do_delete)
        delete_btn.pack(side="right", padx=10)

    def get_degrees(self):
        add_task = ctk.CTk()
        add_task.geometry('750x600')
        add_task.minsize(450, 200)
        add_task.maxsize(450, 200)
        add_task.title('Error')



        def Cancel(): 
            add_task.destroy()
        
        def ok():
            global total
            degrees_ = Degrees.get()
            students = list(self.collection.find())
            for i in students:
                if i.get('degrees') is not None and i.get('additional') is not None:
                    degrees = int(i.get('total_degrees', 0)) + int(degrees_)
                    self.collection.update_one({'name': i['name']}, {'$set': {'total_degrees': degrees}})
            add_task.destroy()
            self.refresh_data()
        
            

        frame = ctk.CTkFrame(add_task)
        frame.pack(padx=1, pady=1, fill='both', expand=True)

        label_text = ctk.CTkLabel(frame, font=('Roboto', 16), text='Add Task',
                                               text_color='green')
        label_text.pack()

        Degrees = ctk.CTkEntry(frame, placeholder_text='Degrees',  text_color='black',
                            placeholder_text_color='black', font=('Roboto', 15), height=30, width=250, border_color='black', border_width=2)
        Degrees.pack(padx=10, pady=12)

        button_cansel = ctk.CTkButton(frame, text='Cancel', hover_color='white', text_color='black', command=Cancel, corner_radius=20, border_color='black', border_width=2)
        button_cansel.pack(pady=15)

        button = ctk.CTkButton(frame, text='OK', hover_color='white', text_color='black', command=ok, corner_radius=20, border_color='black', border_width=2)
        button.pack(pady=15)

        add_task.mainloop()

    def add_student(self):
        global pending_new_row, pending_new_entry

        try:
            if pending_new_entry and pending_new_row:
                if pending_new_entry.get().strip() == '':
                    self.tree.delete(pending_new_row)
                    pending_new_entry.destroy()
        except Exception:
            pass
        pending_new_row = None
        pending_new_entry = None
        # 1. جلب كل الـ student_id الحاليين في كل التراكات
        all_tracks = list(self.db['tracks'].find({}))
        max_id = 0
        for tr in all_tracks:
            for s in tr.get('track_data', []):
                if s.get('student_id') is not None:
                    try:
                        max_id = max(max_id, int(s.get('student_id')))
                    except Exception:
                        pass

        new_id = max_id + 1
        default_row = [new_id, '', 0, 0, 0, 'No Comments', 0, len(self.result_after_add_ranking)+1, '🗑️']
        item_id = self.tree.insert(parent='', index='end', text='', values=default_row)
        self.tree.see(item_id)
        self.tree.selection_set(item_id)

        col_name = '#2'  
        x, y, width, height = self.tree.bbox(item_id, col_name)
        tree_abs_x = self.tree.winfo_rootx()
        tree_abs_y = self.tree.winfo_rooty()
        root_abs_x = self.root.winfo_rootx()
        root_abs_y = self.root.winfo_rooty()
        x_abs = x + tree_abs_x - root_abs_x
        y_abs = y + tree_abs_y - root_abs_y
        entry = ctk.CTkEntry(self.root, text_color=ui_colors.get_text_color(), placeholder_text_color=ui_colors.get_placeholder_color())
        entry.place(x=x_abs, y=y_abs, width=width, height=height)
        entry.focus()
        pending_new_row = item_id
        pending_new_entry = entry
        def save_new_student(event=None):
            name = entry.get().strip()

            if len(name.split()) != 4:
                import Verification
                Verification.Verification_wrong_data()
                return

            track_doc = self.db['tracks'].find_one({'track_name': self.track})
            track_data = track_doc.get('track_data', []) if track_doc else []
            if any(s.get('name') == name for s in track_data):
                import Verification
                Verification.Verification_name_Student_used()
                return

            existing_id = None
            for tr in all_tracks:
                for s in tr.get('track_data', []):
                    if s.get('name') == name:
                        existing_id = s.get('student_id')
            student_id = existing_id if existing_id is not None else new_id


            degrees = 0
            additional = 0
            basic_total = 0
            total_degrees = 0
            comments = 'No Comments'
            data = {
                'student_id': student_id,
                'name': name,
                'degrees': degrees,
                'additional': additional,
                'basic_total': basic_total,
                'total_degrees': total_degrees,
                'comments': comments
            }
            # أضف الطالب إلى قاعدة البيانات
            if not track_doc:
                self.db['tracks'].insert_one({'track_name': self.track, 'track_data': [data]})
                track_data = [data]
            else:
                track_data.append(data)
                self.db['tracks'].update_one({'track_name': self.track}, {'$set': {'track_data': track_data}})


            new_ranking = len(self.result_after_add_ranking) + 1
            values = [student_id, name, degrees, additional, basic_total, comments, total_degrees, new_ranking, '🗑️']

            self.result_after_add_ranking.append([student_id, name, degrees, additional, basic_total, comments, total_degrees, new_ranking, '🗑️'])

            tags = None
            if basic_total != None and degrees != None and additional != None:
                if int(basic_total) == 0 and int(total_degrees) != 0:
                    tags = ('= 0',)
                    self.tree.tag_configure('= 0', background='red')
                elif int(degrees) < int(total_degrees) * 0.85 and int(degrees) > int(total_degrees) * 0.75:
                    tags = ('< 0.85 > 0.75',)
                    self.tree.tag_configure('< 0.85 > 0.75', background='#aacc00')
                elif int(degrees) < int(total_degrees) * 0.75:
                    tags = ('< 0.75',)
                    self.tree.tag_configure('< 0.75', background='#e9e04f')
                else:
                    tags = ('> 0.85',)
                    self.tree.tag_configure('> 0.85', background='#57e94f')
            self.tree.item(item_id, values=values, tags=tags)
            entry.destroy()
            pending_new_row = None
            pending_new_entry = None

            self.root.unbind('<Button-1>')
        def cancel_new_row_anywhere(event=None):
            global pending_new_row, pending_new_entry
            # لا تحذف الصف إذا كان الضغط داخل الـ Entry نفسه
            if event and hasattr(event, 'widget') and pending_new_entry:
                if event.widget == pending_new_entry:
                    return
            if pending_new_entry and pending_new_row:
                self.tree.delete(pending_new_row)
                pending_new_entry.destroy()
                pending_new_row = None
                pending_new_entry = None
                self.root.unbind('<Button-1>')
        entry.bind('<Return>', save_new_student)
        self.root.bind('<Button-1>', cancel_new_row_anywhere, add='+')

    def show_all_data(self):
        self.root.destroy()
        show_all_data(self.position, self.track)

    def get_performance_tags(self, degrees, total_degrees):
        if total_degrees > 0:
            percentage = (degrees / total_degrees) * 100
            if percentage >= 85:
                return ('excellent',)
            elif percentage >= 75:
                return ('good',)
            else:
                return ('poor',)
        return ('new',)

def show_all_data(position, track):
    app = StudentManager(position, track)

if __name__ == "__main__":
    load_dotenv()
    show_all_data("manager", "Test Track")