# this file will handle the title card of the application

# import the necessary libraries
import tkinter as tk
from tkinter import messagebox

# title card class
class TitleCard:
    # initialize the gui
    def __init__(self):
        self.root = tk.Tk()
        self.setup_gui()
    
    # setup the gui
    def setup_gui(self):
        self.root.title("Design and Analysis of Algorithms - Final Project")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # gradient background
        self.root.configure(bg='#4682B4')
        
        # center window where the title and button will be displayed
        self.root.geometry("+%d+%d" % ((self.root.winfo_screenwidth() / 2) - 250, 
                                      (self.root.winfo_screenheight() / 2) - 200))
        
        # main frame
        main_frame = tk.Frame(self.root, bg='#87CEEB', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # title
        title_label = tk.Label(main_frame, text="Pondong Planado", 
                              font=('Roboto', 28, 'bold'), 
                              bg='#87CEEB', fg='white',
                              relief=tk.FLAT)
        title_label.pack(pady=(40, 10))
        
        # subtitle
        subtitle_label = tk.Label(main_frame, text="A Smart Budgeting System for Barangay Projects", 
                                 font=('Roboto', 16, 'italic'), 
                                 bg='#87CEEB', fg='white')
        subtitle_label.pack(pady=(0, 40))
        
        # button frame
        button_frame = tk.Frame(main_frame, bg='#87CEEB')
        button_frame.pack(pady=20)
        
        # start button
        start_button = tk.Button(button_frame, text="START", 
                               font=('Arial', 16, 'bold'),
                               width=12, height=3,
                               bg='#228B22', fg='white',
                               relief=tk.RAISED, bd=3,
                               cursor='hand2',
                               command=self.start_application)
        start_button.pack(side=tk.LEFT, padx=10)
        
        # start button hover effects
        def on_start_enter(e):
            start_button.config(bg='#008000')
        
        def on_start_leave(e):
            start_button.config(bg='#228B22')
        
        start_button.bind("<Enter>", on_start_enter)
        start_button.bind("<Leave>", on_start_leave)
        
        # exit button
        exit_button = tk.Button(button_frame, text="EXIT", 
                              font=('Arial', 16, 'bold'),
                              width=12, height=3,
                              bg='#DC143C', fg='white',
                              relief=tk.RAISED, bd=3,
                              cursor='hand2',
                              command=self.exit_application)
        exit_button.pack(side=tk.LEFT, padx=10)
        
        # exit button hover effects
        def on_exit_enter(e):
            exit_button.config(bg='#B22222')
        
        def on_exit_leave(e):
            exit_button.config(bg='#DC143C')
        
        exit_button.bind("<Enter>", on_exit_enter)
        exit_button.bind("<Leave>", on_exit_leave)
        
        # footer
        footer_label = tk.Label(main_frame, text="Final Requirement for Design and Analysis of Algorithms", 
                               font=('Arial', 12), 
                               bg='#87CEEB', fg='white')
        footer_label.pack(side=tk.BOTTOM, pady=(40, 20))
        
        # closing the application
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
    
    # start the application
    def start_application(self):
        try:
            self.root.withdraw()  # hide the title card
            
            # import the gui file (the gui file must be in the same directory)
            from budget_allocation_gui import BudgetAllocationGUI
            
            # create the root window
            main_root = tk.Tk()
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