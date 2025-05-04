import customtkinter as cutk
import ui_colors

# صفحات وهمية كنموذج
class HomePage(cutk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color=ui_colors.get_card_color(), corner_radius=16)
        label = cutk.CTkLabel(self, text="الرئيسية | Dashboard", font=ui_colors.FONT_TITLE, text_color=ui_colors.get_text_color())
        label.pack(pady=30)
        desc = cutk.CTkLabel(self, text="مرحبا بك في برنامج Trainingee بنسخته الحديثة!\nجرب التنقل من القائمة الجانبية.", font=ui_colors.FONT_LABEL, text_color=ui_colors.get_label_color(), justify='center')
        desc.pack(pady=10)

class StudentsPage(cutk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color=ui_colors.get_card_color(), corner_radius=16)
        label = cutk.CTkLabel(self, text="عرض الطلاب | Students", font=ui_colors.FONT_TITLE, text_color=ui_colors.get_text_color())
        label.pack(pady=30)
        # ... هنا يمكنك إضافة جدول الطلاب لاحقًا ...
        desc = cutk.CTkLabel(self, text="هنا سيتم عرض بيانات الطلاب بشكل عصري.", font=ui_colors.FONT_LABEL, text_color=ui_colors.get_label_color())
        desc.pack(pady=10)

class MainWindow(cutk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Trainingee | Modern UI")
        self.geometry('900x600')
        self.minsize(700, 500)
        cutk.set_appearance_mode('system')
        self.configure(bg=ui_colors.get_bg_color())

        # Sidebar
        sidebar = cutk.CTkFrame(self, fg_color=ui_colors.get_header_color(), width=180, corner_radius=0)
        sidebar.pack(side='left', fill='y')
        sidebar.grid_propagate(False)
        logo = cutk.CTkLabel(sidebar, text="Trainingee", font=ui_colors.FONT_HEADER, text_color='#fff')
        logo.pack(pady=(30, 16))
        btn_home = cutk.CTkButton(sidebar, text="الرئيسية", font=ui_colors.FONT_BUTTON, fg_color=ui_colors.get_button_color(), hover_color=ui_colors.get_hover_primary(), text_color='#fff', command=self.show_home, corner_radius=12, height=38)
        btn_home.pack(pady=10, padx=18, fill='x')
        btn_students = cutk.CTkButton(sidebar, text="الطلاب", font=ui_colors.FONT_BUTTON, fg_color=ui_colors.get_button_color(), hover_color=ui_colors.get_hover_primary(), text_color='#fff', command=self.show_students, corner_radius=12, height=38)
        btn_students.pack(pady=10, padx=18, fill='x')
        # ... أضف باقي الصفحات هنا ...
        # Footer
        footer = cutk.CTkLabel(sidebar, text='© 2025 Trainingee', font=ui_colors.FONT_FOOTER, text_color=ui_colors.get_footer_color())
        footer.pack(side='bottom', pady=18)

        # Main Content Area
        self.container = cutk.CTkFrame(self, fg_color=ui_colors.get_bg_color())
        self.container.pack(side='left', fill='both', expand=True)
        self.pages = {}
        self.show_home()

    def show_home(self):
        self._show_page('home', HomePage)
    def show_students(self):
        self._show_page('students', StudentsPage)
    def _show_page(self, page_name, page_class):
        for widget in self.container.winfo_children():
            widget.destroy()
        if page_name not in self.pages:
            self.pages[page_name] = page_class(self.container)
        self.pages[page_name].pack(fill='both', expand=True)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
