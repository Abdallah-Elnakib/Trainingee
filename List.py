import customtkinter as cutk
import Add_Student
import Search
import Show_All_Data


def search_or_add(position, track):
    root_search_or_add = cutk.CTk()
    root_search_or_add.geometry('600x420')
    root_search_or_add.minsize(500, 350)
    root_search_or_add.maxsize(700, 500)
    root_search_or_add.title('Search or Add | Trainingee')
    cutk.set_appearance_mode('system')
    cutk.set_default_color_theme('blue')
    root_search_or_add.configure(bg='#f4f8fb')

    def search():
        root_search_or_add.destroy()
        Search.search(position, track)


    def add_student():
        root_search_or_add.destroy()
        Add_Student.Add_student(position , track)

    def all_student():
        root_search_or_add.destroy()
        Show_All_Data.show_all_data(position, track)

    def back_to_first_page():
        from First_Page import first_page
        root_search_or_add.destroy()
        first_page(position)


    def Close(): 
        root_search_or_add.destroy()

    frame = cutk.CTkFrame(root_search_or_add, corner_radius=25, fg_color=("#fff", "#23272e"))
    frame.pack(padx=30, pady=30, fill='both', expand=True)

    # Main title
    label = cutk.CTkLabel(frame, text='What would you like to do?', font=("Segoe UI", 22, "bold"), text_color=("#1976d2", "#90caf9"))
    label.pack(pady=(18, 5))

    # Subtitle
    subtitle = cutk.CTkLabel(frame, text='Add a new student, search for a student, or view all students.', font=("Segoe UI", 14), text_color=("#374151", "#b0bec5"))
    subtitle.pack(pady=(0, 25))

    # Buttons area
    btns_frame = cutk.CTkFrame(frame, fg_color=("#f4f8fb", "#23272e"), corner_radius=15)
    btns_frame.pack(pady=10)

    # Search Button
    search_btn = cutk.CTkButton(btns_frame, text='Search', width=180, height=45, fg_color=("#1976d2","#90caf9"), text_color="#fff", hover_color="#1565c0", font=("Segoe UI", 15, "bold"), command=search, corner_radius=18)
    search_btn.grid(row=0, column=0, padx=18, pady=12)

    # Add Button (for editors and managers)
    if position == 'editor' or position == 'manager':
        add_btn = cutk.CTkButton(btns_frame, text='Add Student', width=180, height=45, fg_color=("#43a047","#388e3c"), text_color="#fff", hover_color="#388e3c", font=("Segoe UI", 15, "bold"), command=add_student, corner_radius=18)
        add_btn.grid(row=0, column=1, padx=18, pady=12)

    # All Students Button
    all_data_btn = cutk.CTkButton(btns_frame, text='All Students', width=180, height=45, fg_color=("#0288d1","#81d4fa"), text_color="#fff", hover_color="#0277bd", font=("Segoe UI", 15, "bold"), command=all_student, corner_radius=18)
    all_data_btn.grid(row=1, column=0, padx=18, pady=12)

    # Back Button
    back_btn = cutk.CTkButton(btns_frame, text='Back', width=180, height=45, fg_color=("#757575","#bdbdbd"), text_color="#fff", hover_color="#616161", font=("Segoe UI", 15, "bold"), command=back_to_first_page, corner_radius=18)
    back_btn.grid(row=1, column=1, padx=18, pady=12)

    # Close Button (separated at bottom)
    close_btn = cutk.CTkButton(frame, text='Close', width=140, height=38, fg_color=("#e53935","#b71c1c"), text_color="#fff", hover_color="#c62828", font=("Segoe UI", 13), command=Close, corner_radius=16)
    close_btn.pack(pady=(24, 4))

    # Footer
    footer = cutk.CTkLabel(frame, text='All rights reserved  2025', font=("Segoe UI", 10), text_color=("#90a4ae","#b0bec5"))
    footer.pack(side="bottom", pady=(0,6))

    root_search_or_add.mainloop()
