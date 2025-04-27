import customtkinter as cutk
import Verification
from pymongo import MongoClient
import List
from dotenv import load_dotenv
import os

def Add_student(position, track):
    import Verification

    load_dotenv()
    root_Add = cutk.CTk()
    root_Add.geometry('420x420')
    root_Add.minsize(380, 370)
    root_Add.maxsize(480, 520)
    root_Add.title('Add Student | Trainingee')
    cutk.set_appearance_mode('system')
    root_Add.configure(bg='#f4f8fb')

    # Header
    header = cutk.CTkFrame(root_Add, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=46)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='Add Student', font=("Segoe UI", 18, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=18, pady=10, sticky='w')
    header.grid_columnconfigure(0, weight=1)

    # Main Frame
    content_frame = cutk.CTkFrame(root_Add, fg_color=("#f4f8fb", "#23272e"), corner_radius=16)
    content_frame.pack(fill='both', expand=True, padx=14, pady=(14,7))
    content_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    def back():
        root_Add.destroy()
        List.search_or_add(position, track)

    def add_data():
        import Verification
        import os
        print("[DEBUG] add_data called")

        try:
            mongo_client = MongoClient(os.getenv('MONGO_URI'))
            db = mongo_client['test']
            print(f"[DEBUG] Connected to DB: test. Will update track: {track}")
        except Exception as e:
            print(f"[ERROR] DB Connection: {e}")
            Verification.connection_error()
            return

        # تأكد من وجود التراك، إذا لم يوجد أنشئه تلقائيًا
        print(f"[DEBUG] Using track: '{track}' from collection 'tracks' in DB '{db.name}'")
        track_doc = db['tracks'].find_one({'track_name': track})
        if not track_doc:
            print(f"[ERROR] Track '{track}' not found في مجموعة tracks. لن يتم إنشاء تراك جديد تلقائيًا!")
            Verification.Verification_wrong_data()
            return

        track_data = track_doc.get('track_data', [])
        print(f"[DEBUG] track_data BEFORE add: {track_data}")
        var0 = 0
        entry_7 = 0
        for i in track_data:
            if i.get('student_id') is not None:
                var0 = i['student_id']
            if i.get('total_degrees') is not None:
                entry_7 = i['total_degrees']

        entry_1 = int(var0) + 1
        name = entry2.get().strip()
        degrees = entry3.get().strip()
        additional = entry4.get().strip()
        comments = "No Comments"  # يمكنك ربطه بعنصر واجهة لاحقًا

        print(f"[DEBUG] name={name}, degrees={degrees}, additional={additional}")
        if name == '':
            Verification.Verification_add_name()
            return
        else:
            # Check uniqueness of name داخل نفس التراك
            if any(s.get('name') == name for s in track_data):
                Verification.Verification_name_Student_used()
                return

        if degrees == '':
            degrees = 0
        elif not str(degrees).isdigit():
            Verification.Verification_wrong_data()
            return
        if additional == '':
            additional = 0
        elif not str(additional).isdigit():
            Verification.Verification_wrong_data()
            return

        basic_total = int(degrees) + int(additional)
        print(f"[DEBUG] basic_total={basic_total}")
        data = {
            'student_id': entry_1,
            'name': name,
            'degrees': int(degrees),
            'additional': int(additional),
            'basic_total': basic_total,
            'total_degrees': entry_7,
            'comments': comments
        }
        print(f"[DEBUG] data to insert: {data}")
        track_data.append(data)
        print(f"[DEBUG] track_data AFTER add: {track_data}")
        try:
            result = db['tracks'].update_one(
                {'track_name': track},
                {'$set': {'track_data': track_data}}
            )
            Verification.add_done()
            print(f"[DEBUG] update_one result: matched={result.matched_count}, modified={result.modified_count}")
            root_Add.destroy()
            List.search_or_add(position, track)
        except Exception as e:
            print(f"[ERROR] Insert: {e}")
            Verification.connection_error()
            return

    def Close(): 
        root_Add.destroy()


    # عناصر الإدخال بتصميم عصري داخل content_frame
    label = cutk.CTkLabel(content_frame, text='Add Student', font=("Segoe UI", 22, "bold"), text_color='#1976d2')
    label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky='ew')

    entry2 = cutk.CTkEntry(content_frame, placeholder_text='Student Name',  text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, border_color='#1976d2', border_width=2)
    entry2.grid(row=1, column=0, padx=18, pady=8, sticky='ew')

    entry3 = cutk.CTkEntry(content_frame, placeholder_text='Degrees', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, border_color='#1976d2', border_width=2)
    entry3.grid(row=2, column=0, padx=18, pady=8, sticky='ew')

    entry4 = cutk.CTkEntry(content_frame, placeholder_text='Additional', text_color='black',
                            placeholder_text_color='gray', font=("Segoe UI", 15), height=34, width=220, border_color='#1976d2', border_width=2)
    entry4.grid(row=3, column=0, padx=18, pady=8, sticky='ew')

    add_btn = cutk.CTkButton(content_frame, text='Add', fg_color=("#43a047", "#388e3c"), hover_color="#388e3c", text_color='#fff', command=add_data, corner_radius=16, border_color='#43a047', border_width=2, font=("Segoe UI", 14, "bold"), height=36)
    add_btn.grid(row=4, column=0, padx=18, pady=(14, 3), sticky='ew')

    back_btn = cutk.CTkButton(content_frame, text='Back', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e', command=back, corner_radius=16, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 13), height=36)
    back_btn.grid(row=5, column=0, padx=18, pady=(3, 3), sticky='ew')

    close_btn = cutk.CTkButton(content_frame, text='Close', fg_color=("#e53935", "#b71c1c"), hover_color="#b71c1c", text_color='#fff', command=Close, corner_radius=16, border_color='#e53935', border_width=2, font=("Segoe UI", 13), height=36)
    close_btn.grid(row=6, column=0, padx=18, pady=(3, 8), sticky='ew')

    footer = cutk.CTkLabel(content_frame, text='Trainingee © 2025', font=("Segoe UI", 10), text_color='#bdbdbd')
    footer.grid(row=7, column=0, pady=(7, 0), sticky='s')

    root_Add.bind('<Return>', lambda e: add_data())
    root_Add.mainloop()




