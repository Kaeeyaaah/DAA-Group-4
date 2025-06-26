# this file will handle the title card of the application

# import the necessary libraries
import customtkinter as ctk
from tkinter import messagebox

# title card class
class TitleCard:
    # initialize the gui
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_gui()
    
    # setup the gui
    def setup_gui(self):
        self.root.title("Design and Analysis of Algorithms - Final Project")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # gradient background
        self.root.configure(fg_color='#4682B4')
        
        # center window where the title and button will be displayed
        self.root.geometry("+%d+%d" % ((self.root.winfo_screenwidth() / 2) - 250, 
                                      (self.root.winfo_screenheight() / 2) - 200))
        
        # main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="#9DCCDE", corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # title
        title_label = ctk.CTkLabel(main_frame, text="Pondong Planado", 
                                   font=('Roboto', 28, 'bold'), 
                                   fg_color="transparent", text_color='black')
        title_label.pack(pady=(40, 10))
        
        # subtitle
        subtitle_label = ctk.CTkLabel(main_frame, text="A Smart Budgeting System for Barangay Projects", 
                                      font=('Roboto', 16, 'italic'), 
                                      fg_color="transparent", text_color='black')
        subtitle_label.pack(pady=(0, 40))
        
        # button frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # start button
        start_button = ctk.CTkButton(
            button_frame, text="START", 
            font=('Arial', 16, 'bold'),
            width=120, height=40,
            fg_color="#2C4E2C", text_color='white',
            hover_color="#3e6b3e",
            corner_radius=20,
            border_width=3,
            border_color="#1e3320",
            command=self.start_application
        )
        start_button.pack(side="left", padx=10)
        
        # exit button
        exit_button = ctk.CTkButton(
            button_frame, text="EXIT", 
            font=('Arial', 16, 'bold'),
            width=120, height=40,
            fg_color="#2C4E2C", text_color='white',
            hover_color="#6b2e2e",
            corner_radius=20,
            border_width=3,
            border_color="#33201e",
            command=self.exit_application
        )
        exit_button.pack(side="left", padx=10)
        
        # footer
        footer_label = ctk.CTkLabel(main_frame, text="Final Requirement for Design and Analysis of Algorithms", 
                                    font=('Arial', 12), 
                                    fg_color="transparent", text_color='black')
        footer_label.pack(side="bottom", pady=(40, 20))
        
        # closing the application
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
    
    # start the application
    def start_application(self):
        try:
            self.root.withdraw()  # hide the title card
            
            # import the gui file (the gui file must be in the same directory)
            from budget_allocation_gui import BudgetAllocationGUI
            
            # create the root window
            main_root = ctk.CTk()
            app = BudgetAllocationGUI(main_root)
            
            # show title card again when the main window is closed
            def on_main_close():
                main_root.destroy()
                self.root.deiconify()
            
            main_root.protocol("WM_DELETE_WINDOW", on_main_close)
            main_root.mainloop()
            
        # import error handling
        except ImportError as e:
            messagebox.showerror("Error", f"Could not start main application: {str(e)}")
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.root.deiconify()
    
    # exit the application
    def exit_application(self):
        result = messagebox.askyesno("Confirm Exit", 
                                   "Are you sure you want to exit the application?",
                                   icon='question')
        
        if result:
            self.root.quit()
            self.root.destroy()
    
    # run the title card
    def run(self):
        self.root.mainloop()

# main function
def main():
    # create the title card and run it
    title_card = TitleCard()
    title_card.run()

if __name__ == "__main__":
    main()
