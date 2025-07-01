import customtkinter as cutk
import ui_colors
from models.models_track import Track
from config.ConnDB import get_db
import First_Page
from dotenv import load_dotenv


def add_track(position):
    
    load_dotenv()
    root_add_trak = cutk.CTk()
    root_add_trak.geometry('370x300')
    root_add_trak.minsize(340, 260)
    root_add_trak.maxsize(400, 340)
    root_add_trak.title('Add Track | Trainingee')
    cutk.set_appearance_mode('system')
    root_add_trak.configure(bg='#f4f8fb')

    # Header
    header = cutk.CTkFrame(root_add_trak, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=46)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='Add Track', font=("Segoe UI", 17, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=18, pady=10, sticky='w')
    header.grid_columnconfigure(0, weight=1)

    # Main Frame
    content_frame = cutk.CTkFrame(root_add_trak, fg_color=("#f4f8fb", "#23272e"), corner_radius=16)
    content_frame.pack(fill='both', expand=True, padx=14, pady=(14,7))
    content_frame.grid_rowconfigure((0,1,2,3), weight=1)
    content_frame.grid_columnconfigure(0, weight=1)


    def add_track_in_data_base():
        import Verification
        get_db()
        track_name = entry1.get().strip()
        if not track_name:
            Verification.Verification_wrong_data()
            return
        # تحقق من عدم وجود تراك بنفس الاسم
        if Track.objects(track_name=track_name).first():
            Verification.Track_Already_Token()
            return
        # أضف التراك
        Track(track_name=track_name, track_data=[]).save()
        root_add_trak.destroy()
        First_Page.first_page(position)

    def back():
        root_add_trak.destroy()
        First_Page.first_page(position)


    entry1 = cutk.CTkEntry(content_frame, placeholder_text='Track Name', text_color='black',
                            placeholder_text_color='gray', font=('Segoe UI', 15), height=34, width=220, corner_radius=14, border_color='#1976d2', border_width=2)
    entry1.grid(row=0, column=0, padx=18, pady=(22, 8), sticky='ew')

    add = cutk.CTkButton(content_frame, text='Add Track', fg_color=("#43a047", "#388e3c"), hover_color="#388e3c", text_color='#fff', command=add_track_in_data_base, corner_radius=16, border_color='#43a047', border_width=2, font=("Segoe UI", 14, "bold"), height=36)
    add.grid(row=1, column=0, padx=18, pady=(10, 4), sticky='ew')

    back_btn = cutk.CTkButton(content_frame, text='Back', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e', command=back, corner_radius=16, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 13), height=36)
    back_btn.grid(row=2, column=0, padx=18, pady=(4, 10), sticky='ew')

    footer = cutk.CTkLabel(content_frame, text='Trainingee © 2025', font=("Segoe UI", 10), text_color='#bdbdbd')
    footer.grid(row=3, column=0, pady=(7, 0), sticky='s')

    root_add_trak.bind('<Return>', lambda e: add_track_in_data_base())
    root_add_trak.mainloop()



def delete_track_in_data_base(position):
    import Verification
    get_db()
    root_delete_track = cutk.CTk()
    root_delete_track.geometry('370x300')
    root_delete_track.minsize(340, 260)
    root_delete_track.maxsize(400, 340)
    root_delete_track.title('Delete Track | Trainingee')
    cutk.set_appearance_mode('system')
    root_delete_track.configure(bg='#f4f8fb')

    # Header
    header = cutk.CTkFrame(root_delete_track, fg_color=("#1976d2", "#23272e"), corner_radius=0, height=46)
    header.pack(fill='x', side='top')
    header.grid_propagate(False)
    header_title = cutk.CTkLabel(header, text='Delete Track', font=("Segoe UI", 17, "bold"), text_color=("#fff", "#90caf9"))
    header_title.grid(row=0, column=0, padx=18, pady=10, sticky='w')
    header.grid_columnconfigure(0, weight=1)

    # Main Frame
    content_frame = cutk.CTkFrame(root_delete_track, fg_color=("#f4f8fb", "#23272e"), corner_radius=16)
    content_frame.pack(fill='both', expand=True, padx=14, pady=(14,7))
    content_frame.grid_rowconfigure((0,1,2,3), weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    def delete_track_in_database():
        import Verification
        track_name = track_name_to_delete.get().strip()
        if not track_name:
            Verification.Verification_wrong_data()
            return
        track = Track.objects(track_name=track_name).first()
        if not track:
            Verification.Track_Not_Found()
            return
        track.delete()
        root_delete_track.destroy()
        First_Page.first_page(position)

    def delete_track():
        delete_data = cutk.CTk()
        delete_data.geometry('410x220')
        delete_data.minsize(350, 180)
        delete_data.maxsize(500, 260)
        delete_data.title('Delete Confirmation')
        cutk.set_appearance_mode('system')
        delete_data.configure(bg='#f4f8fb')
        # Header
        header = cutk.CTkFrame(delete_data, fg_color=("#e53935", "#b71c1c"), corner_radius=0, height=38)
        header.pack(fill='x', side='top')
        header.grid_propagate(False)
        header_title = cutk.CTkLabel(header, text='Delete Track', font=("Segoe UI", 14, "bold"), text_color=("#fff", "#fff"))
        header_title.grid(row=0, column=0, padx=14, pady=7, sticky='w')
        header.grid_columnconfigure(0, weight=1)
        # Main Frame
        frame = cutk.CTkFrame(delete_data, fg_color=("#f4f8fb", "#23272e"), corner_radius=14)
        frame.pack(fill='both', expand=True, padx=8, pady=8)
        label_text = cutk.CTkLabel(frame, font=("Segoe UI", 13), text='Warning: This action will delete all data in this Track and will not be retrieved again.\nAre you sure about this decision?', text_color='#e53935', wraplength=370, justify='center')
        label_text.pack(pady=(18, 10))
        btns_frame = cutk.CTkFrame(frame, fg_color='transparent')
        btns_frame.pack(pady=5)
        def Cancel():
            delete_data.destroy()
        button_cansel = cutk.CTkButton(btns_frame, text='Cancel', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e', command=Cancel, corner_radius=14, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 13), width=90, height=34)
        button_cansel.grid(row=0, column=0, padx=(0, 16))
        def ok():
            # حذف التراك من قاعدة البيانات
            db = get_db()
            db['tracks'].delete_one({'track_name': track})
            delete_data.destroy()
            # يمكنك هنا إعادة تحميل الصفحة أو تحديث القائمة إذا لزم الأمر
        # زر OK الآن يعمل بشكل صحيح
        button = cutk.CTkButton(btns_frame, text='OK', fg_color=("#e53935", "#b71c1c"), hover_color="#b71c1c", text_color='#fff', command=ok, corner_radius=14, border_color='#e53935', border_width=2, font=("Segoe UI", 13, "bold"), width=90, height=34)
        button.grid(row=0, column=1)
        delete_data.mainloop()

    def back():
        root_delete_track.destroy()
        First_Page.first_page(position)       


    # جلب جميع أسماء التراكات من قاعدة البيانات
    all_tracks = [track.track_name for track in Track.objects()]
    selected_track = cutk.StringVar(value=all_tracks[0] if all_tracks else "")
    option_menu = cutk.CTkOptionMenu(content_frame, values=all_tracks, variable=selected_track, fg_color='#fff', button_color='#1976d2', font=("Segoe UI", 15))
    option_menu.grid(row=0, column=0, padx=18, pady=(22, 8), sticky='ew')

    def delete_track():
        track_name = selected_track.get()
        delete_data = cutk.CTk()
        delete_data.geometry('410x220')
        delete_data.minsize(350, 180)
        delete_data.maxsize(500, 260)
        delete_data.title('Delete Confirmation')
        cutk.set_appearance_mode('system')
        delete_data.configure(bg='#23272e')
        # Header
        header = cutk.CTkFrame(delete_data, fg_color=("#e53935", "#b71c1c"), corner_radius=0, height=46)
        header.pack(fill='x', side='top')
        header.grid_propagate(False)
        header_title = cutk.CTkLabel(header, text='Delete Track', font=("Segoe UI", 17, "bold"), text_color="#fff")
        header_title.grid(row=0, column=0, padx=18, pady=10, sticky='w')
        header.grid_columnconfigure(0, weight=1)
        # Main
        content_frame2 = cutk.CTkFrame(delete_data, fg_color=("#23272e"), corner_radius=16)
        content_frame2.pack(fill='both', expand=True, padx=14, pady=(14,7))
        label = cutk.CTkLabel(content_frame2, text=f"Warning: This action will delete all data in this Track and will not be retrieved again.\nAre you sure about this decision?", font=("Segoe UI", 14), text_color="#e57373", wraplength=350, justify='center')
        label.pack(pady=(18, 8))
        # أزرار التأكيد والإلغاء
        btns_frame = cutk.CTkFrame(content_frame2, fg_color="transparent")
        btns_frame.pack(pady=10)
        def ok():
            import Verification
            track = Track.objects(track_name=track_name).first()
            if not track:
                Verification.Track_Not_Found()
                return
            track.delete()
            delete_data.destroy()
            root_delete_track.destroy()
            First_Page.first_page(position)
        def cancel():
            delete_data.destroy()
        ok_btn = cutk.CTkButton(btns_frame, text='OK', fg_color=("#e53935", "#b71c1c"), hover_color="#b71c1c", text_color='#fff', command=ok, corner_radius=16, border_color='#e53935', border_width=2, font=("Segoe UI", 14, "bold"), height=36, width=120)
        ok_btn.grid(row=0, column=0, padx=12)
        cancel_btn = cutk.CTkButton(btns_frame, text='Cancel', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e', command=cancel, corner_radius=16, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 14), height=36, width=120)
        cancel_btn.grid(row=0, column=1, padx=12)
        delete_data.mainloop()

    delete_track_btn = cutk.CTkButton(content_frame, text='Delete Track', fg_color=("#e53935", "#b71c1c"), hover_color="#b71c1c", text_color='#fff', corner_radius=16, command=delete_track, border_color='#e53935', border_width=2, font=("Segoe UI", 14, "bold"), height=36)
    delete_track_btn.grid(row=1, column=0, padx=18, pady=(10, 4), sticky='ew')

    back_btn = cutk.CTkButton(content_frame, text='Back', fg_color=("#bdbdbd", "#23272e"), hover_color="#757575", text_color='#23272e', command=back, corner_radius=16, border_color='#bdbdbd', border_width=2, font=("Segoe UI", 13), height=36)
    back_btn.grid(row=2, column=0, padx=18, pady=(4, 10), sticky='ew')

    footer = cutk.CTkLabel(content_frame, text='Trainingee © 2025', font=("Segoe UI", 10), text_color='#bdbdbd')
    footer.grid(row=3, column=0, pady=(7, 0), sticky='s')

    root_delete_track.bind('<Return>', lambda e: delete_track_in_database())
    root_delete_track.mainloop()

