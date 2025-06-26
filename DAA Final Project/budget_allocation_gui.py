# this file will handle the gui of the application

# import the necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from collections import defaultdict
import numpy as np

# import the classes from other files (the files should be in the same directory)
from project import Project
from branch_and_bound import BranchAndBound

# gui class of the application
class BudgetAllocationGUI:

    # initialize the gui
    def __init__(self, root):
        self.root = root
        self.projects = []
        self.solution = None
        self.emergency_mode = tk.BooleanVar(master=self.root)
        self.emergency_type = tk.StringVar(master=self.root, value="Typhoon")
        
        self.setup_gui()

    # setup the gui 
    def setup_gui(self):
        """Initialize the GUI components"""
        self.root.title("Group 4 Final Project - Pondong Planado")
        self.root.geometry("1400x900")
        self.root.configure(bg='#4682B4')
        
        # create the main frame
        main_frame = tk.Frame(self.root, bg='#87CEEB')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # title label
        title_label = tk.Label(main_frame, text="Pondong Planado", 
                              font=('Arial', 24, 'bold'), 
                              bg='#87CEEB', fg='white')
        title_label.pack(pady=10)
        
        # subtitle label
        subtitle_label = tk.Label(main_frame, text="A Smart Budgeting System for Barangay Projects", 
                                 font=('Arial', 14, 'italic'), 
                                 bg='#87CEEB', fg='white')
        subtitle_label.pack(pady=(0, 20))
        
        # create a tkinter notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # create tabs
        self.create_main_tab() # main tab where you define a project and allocate the budget
        self.create_chart_tab() # chart tab where you show the chart that visualizes the allocation

    # main tab  
    def create_main_tab(self):
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text="Budget Allocation")
        
        # top frame
        top_frame = tk.LabelFrame(main_tab, text="Budget Configuration & Emergency Mode", 
                                 font=('Arial', 12, 'bold'), bg='#E6F3FF')
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # budget frame 
        budget_frame = tk.Frame(top_frame, bg='#E6F3FF')
        budget_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(budget_frame, text="Total Budget (₱):", bg='#E6F3FF').pack(side=tk.LEFT)
        self.budget_entry = tk.Entry(budget_frame, width=15)
        self.budget_entry.pack(side=tk.LEFT, padx=5)
        
        # emergency mode frame
        emergency_frame = tk.Frame(top_frame, bg='#E6F3FF')
        emergency_frame.pack(side=tk.LEFT, padx=20, pady=5)
        
        # check button
        emergency_check = tk.Checkbutton(emergency_frame, text="Emergency Mode", 
                                       variable=self.emergency_mode,
                                       command=self.toggle_emergency_mode,
                                       bg='#E6F3FF', font=('Arial', 10, 'bold'))
        emergency_check.pack(side=tk.LEFT)
        
        # combo box that contains the emergency types
        self.emergency_combo = ttk.Combobox(emergency_frame, textvariable=self.emergency_type,
                                          values=["Typhoon", "Earthquake", "Flood", "Fire", "Health Crisis"],
                                          state="disabled", width=12)
        self.emergency_combo.pack(side=tk.LEFT, padx=5)
        
        # button frame
        button_frame = tk.Frame(top_frame, bg='#E6F3FF')
        button_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        tk.Button(button_frame, text="Optimize Allocation", command=self.optimize_budget,
                 bg='#32CD32', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Add Project", command=self.show_add_project_dialog,
                 bg='#4169E1', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Remove Selected", command=self.remove_selected_project,
                 bg='#DC143C', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Clear All", command=self.clear_all_projects,
                 bg='#FF6347', fg='white').pack(side=tk.LEFT, padx=2)
        
        # middle frame
        middle_frame = tk.Frame(main_tab)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # projects table
        projects_frame = tk.LabelFrame(middle_frame, text="Available Projects", 
                                     font=('Arial', 12, 'bold'))
        projects_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # projects tree view
        self.projects_tree = ttk.Treeview(projects_frame, 
                                        columns=('Name', 'Cost', 'Benefit', 'Ratio', 'Category', 'Priority'),
                                        show='headings', height=10)
        
        # configure table attributes
        self.projects_tree.heading('Name', text='Name')
        self.projects_tree.heading('Cost', text='Cost (₱)')
        self.projects_tree.heading('Benefit', text='Benefit')
        self.projects_tree.heading('Ratio', text='Ratio')
        self.projects_tree.heading('Category', text='Category')
        self.projects_tree.heading('Priority', text='Priority')
        
        self.projects_tree.column('Name', width=150, anchor='center')
        self.projects_tree.column('Cost', width=100, anchor='center')
        self.projects_tree.column('Benefit', width=80, anchor='center')
        self.projects_tree.column('Ratio', width=80, anchor='center')
        self.projects_tree.column('Category', width=120, anchor='center')
        self.projects_tree.column('Priority', width=100, anchor='center')
    
        projects_scrollbar = ttk.Scrollbar(projects_frame, orient=tk.VERTICAL, command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=projects_scrollbar.set)
        
        self.projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        projects_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # solution table
        solution_frame = tk.LabelFrame(middle_frame, text="Optimal Selection", 
                                     font=('Arial', 12, 'bold'))
        solution_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.solution_tree = ttk.Treeview(solution_frame,
                                        columns=('Name', 'Cost', 'Benefit', 'Category', 'Priority'),
                                        show='headings', height=10)
        
        self.solution_tree.heading('Name', text='Selected Project')
        self.solution_tree.heading('Cost', text='Cost (₱)')
        self.solution_tree.heading('Benefit', text='Benefit')
        self.solution_tree.heading('Category', text='Category')
        self.solution_tree.heading('Priority', text='Priority')
        
        self.solution_tree.column('Name', width=150, anchor='center')
        self.solution_tree.column('Cost', width=100, anchor='center')
        self.solution_tree.column('Benefit', width=80, anchor='center')
        self.solution_tree.column('Category', width=120, anchor='center')
        self.solution_tree.column('Priority', width=100, anchor='center')

        solution_scrollbar = ttk.Scrollbar(solution_frame, orient=tk.VERTICAL, command=self.solution_tree.yview)
        self.solution_tree.configure(yscrollcommand=solution_scrollbar.set)
        
        self.solution_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        solution_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # bottom frame (set the font and the spacing of the text widget)
        bottom_frame = tk.LabelFrame(main_tab, text="Optimization Results", 
                                   font=('Arial', 12, 'bold'))
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(bottom_frame, height=8, wrap=tk.WORD)
        result_scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # status frame
        self.status_label = tk.Label(main_tab, text="Ready to optimize budget allocation", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
        
    # create the chart tab
    def create_chart_tab(self):
        chart_tab = ttk.Frame(self.notebook)
        self.notebook.add(chart_tab, text="Allocation Charts")
        
        # create the charts
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('Budget Allocation Analysis', fontsize=16, fontweight='bold')
        
        # create a canvas that displays the charts
        self.canvas = FigureCanvasTkAgg(self.fig, chart_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize empty charts
        self.update_charts()
        
    # emergency mode toggle function
    def toggle_emergency_mode(self):
        is_emergency = self.emergency_mode.get()
        self.emergency_combo.config(state="readonly" if is_emergency else "disabled")
        
        # update all projects once the emergency mode is enabled
        for project in self.projects:
            project.set_emergency_priority(is_emergency)
        
        self.update_projects_table()
        
        # emergency mode conditions
        if is_emergency:
            self.status_label.config(text=" Emergency mode enabled - Priority given to critical sectors")
        else:
            self.status_label.config(text="Normal mode - Standard optimization")
    
    # add projects using dialog
    def show_add_project_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Project")
        dialog.geometry("400x300")
        dialog.configure(bg='#F0F8FF')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # center the dialog on the screen
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # create fields that can be filled in
        fields = {}
        
        # name field
        tk.Label(dialog, text="Project Name:", bg='#F0F8FF').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        fields['name'] = tk.Entry(dialog, width=30)
        fields['name'].grid(row=0, column=1, padx=10, pady=5)
        
        # cost field
        tk.Label(dialog, text="Cost (₱):", bg='#F0F8FF').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        fields['cost'] = tk.Entry(dialog, width=30)
        fields['cost'].grid(row=1, column=1, padx=10, pady=5)
        
        # benefit score field
        tk.Label(dialog, text="Benefit Score (0-10):", bg='#F0F8FF').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        fields['benefit'] = tk.Entry(dialog, width=30)
        fields['benefit'].grid(row=2, column=1, padx=10, pady=5)
        
        # benefit score conditions
        warning_label = tk.Label(dialog, text="Benefit score must be between 0 and 10", 
                               fg='red', bg='#F0F8FF', font=('Arial', 9, 'italic', 'bold'))
        warning_label.grid(row=3, column=1, padx=10, pady=2)
        
        # category selection
        tk.Label(dialog, text="Category:", bg='#F0F8FF').grid(row=4, column=0, sticky='w', padx=10, pady=5)
        fields['category'] = ttk.Combobox(dialog, width=27,
                                        values=["Infrastructure", "Health", "Education", 
                                               "Environment", "Social Services", "Economic Development"])
        fields['category'].grid(row=4, column=1, padx=10, pady=5)
        
        # description field
        tk.Label(dialog, text="Description:", bg='#F0F8FF').grid(row=5, column=0, sticky='nw', padx=10, pady=5)
        fields['description'] = tk.Text(dialog, width=30, height=5)
        fields['description'].grid(row=5, column=1, padx=10, pady=5)
        
        # buttons
        button_frame = tk.Frame(dialog, bg='#F0F8FF')
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # add the project 
        def add_project():
            try:
                name = fields['name'].get().strip()
                cost = float(fields['cost'].get())
                benefit = float(fields['benefit'].get())
                category = fields['category'].get()
                description = fields['description'].get(1.0, tk.END).strip()
                
                # checks the conditions and also the required fields
                if not name:
                    messagebox.showerror("Error", "Please enter a project name.")
                    return
                
                if cost <= 0:
                    messagebox.showerror("Error", "Cost must be a positive number.")
                    return
                
                if not category:
                    messagebox.showerror("Error", "Please select a category.")
                    return
                
                # this will raise an error if the benefit score is not between 0 and 10
                project = Project(name, cost, benefit, category, description)
                
                # set the priorities if emergency mode is enabled
                if self.emergency_mode.get():
                    project.set_emergency_priority(True)
                
                # add the project to the list
                self.projects.append(project)
                self.update_projects_table()
                dialog.destroy() # close the dialog
                self.status_label.config(text=f"Project added successfully. Total projects: {len(self.projects)}")

            # shows the errors   
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Please enter valid numbers for cost and benefit.\n{str(e)}")
        
        # setting up the add project button
        tk.Button(button_frame, text="Add Project", command=add_project,
                 bg='#4169E1', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        # setting up the cancel button
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#DC143C', fg='white').pack(side=tk.LEFT, padx=5)
    
    # optimize the budget allocation
    def optimize_budget(self):
        # check the projects and budget amount if valid
        try:
            budget = float(self.budget_entry.get())
            
            if not self.projects:
                messagebox.showerror("Error", "Please add some projects first.")
                return
            
            if budget <= 0:
                messagebox.showerror("Error", "Please enter a valid positive budget amount.")
                return
            
            self.status_label.config(text="Optimizing budget allocation...")
            self.root.update()
            
            # optimization with emergency situation consideration
            self.solution = BranchAndBound.solve_knapsack(self.projects, budget, self.emergency_mode.get())
            self.display_solution(budget)
            self.update_charts()
            self.status_label.config(text="Optimization completed successfully.")

        # handle the errors  
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget amount.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during optimization: {str(e)}")
            self.status_label.config(text="Optimization failed.")
    
    # display the solutions
    def display_solution(self, budget):
        # if there's no solution
        if not self.solution:
            return
        
        # update the solution table
        for item in self.solution_tree.get_children():
            self.solution_tree.delete(item)
        
        for project in self.solution.selected_projects:
            priority_text = f"Emergency P{project.emergency_priority_level}" if project.is_emergency_priority else "Normal"
            self.solution_tree.insert('', 'end', values=(
                project.name,
                f"₱{project.cost:,.2f}",
                f"{project.benefit:.2f}",
                project.category,
                priority_text
            ))
        
        # Update the bottom text area
        result_text = "=== BUDGET ALLOCATION OPTIMIZATION RESULTS ===\n\n"
        
        if self.emergency_mode.get():
            result_text += f"EMERGENCY MODE: {self.emergency_type.get()}\n"
            result_text += "Priority given to critical infrastructure and services\n\n"
        
        result_text += f"Total Budget: ₱{budget:,.2f}\n"
        result_text += f"Allocated Amount: ₱{self.solution.total_cost:,.2f} ({(self.solution.total_cost / budget) * 100:.1f}%)\n"
        result_text += f"Remaining Budget: ₱{budget - self.solution.total_cost:,.2f}\n"
        result_text += f"Total Benefit Score: {self.solution.total_benefit:.2f}\n"
        result_text += f"Efficiency Ratio: {self.solution.efficiency:.3f}\n\n"
        
        result_text += "Selected Projects (Priority Order):\n"
        result_text += "─" * 60 + "\n"
        
        for project in self.solution.selected_projects:
            priority_indicator = f" P{project.emergency_priority_level}" if project.is_emergency_priority else ""
            result_text += f"• {project.name}{priority_indicator}\n"
            result_text += f"  Cost: ₱{project.cost:,.2f} | Benefit: {project.benefit:.2f} | Category: {project.category}\n"
        
        # breakdown the categories
        result_text += "\nCategory Breakdown:\n"
        category_totals = defaultdict(lambda: {'count': 0, 'cost': 0})
        for project in self.solution.selected_projects:
            category_totals[project.category]['count'] += 1
            category_totals[project.category]['cost'] += project.cost
        
        for category, data in category_totals.items():
            result_text += f"• {category}: {data['count']} projects, ₱{data['cost']:,.2f}\n"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result_text)
    
    # update the charts
    def update_charts(self):
        # clear all the axes
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
        
        if not self.solution or not self.solution.selected_projects:
            # show empty state if there's no solution
            self.ax1.text(0.5, 0.5, 'No data available\nRun optimization first', 
                         ha='center', va='center', transform=self.ax1.transAxes, fontsize=12)
            self.ax2.text(0.5, 0.5, 'No data available\nRun optimization first', 
                         ha='center', va='center', transform=self.ax2.transAxes, fontsize=12)
            self.ax3.text(0.5, 0.5, 'No data available\nRun optimization first', 
                         ha='center', va='center', transform=self.ax3.transAxes, fontsize=12)
            self.ax4.text(0.5, 0.5, 'No data available\nRun optimization first', 
                         ha='center', va='center', transform=self.ax4.transAxes, fontsize=12)
        else:
            self._create_budget_utilization_chart()
            self._create_category_breakdown_chart()
            self._create_project_comparison_chart()
            self._create_priority_distribution_chart()
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    # create the budget utilization pie chart
    def _create_budget_utilization_chart(self):
        budget = float(self.budget_entry.get()) if self.budget_entry.get() else 0
        if budget <= 0:
            return
        
        # calculate the allocated and remaining budget
        allocated = self.solution.total_cost
        remaining = budget - allocated
        
        # define the sizes, labels, and colors for the pie chart
        sizes = [allocated, remaining]
        labels = ['Allocated', 'Remaining']
        colors = ['#32CD32', '#FF6347']
        
        # plot the pie chart
        self.ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.ax1.set_title('Budget Utilization')
    
    # create the category breakdown pie chart
    def _create_category_breakdown_chart(self):
        # calculate the total cost per category
        category_totals = defaultdict(float)
        for project in self.solution.selected_projects:
            category_totals[project.category] += project.cost
        
        if category_totals:
            categories = list(category_totals.keys())
            costs = list(category_totals.values())
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            # plot the pie chart
            self.ax2.pie(costs, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
            self.ax2.set_title('Allocation by Category')
    
    # create the project comparison bar chart
    def _create_project_comparison_chart(self):
        # show top 10 projects by cost if there are more than 10 projects
        if len(self.solution.selected_projects) > 10:
            projects = sorted(self.solution.selected_projects, key=lambda x: x.cost, reverse=True)[:10]
        else:
            projects = self.solution.selected_projects
        
        # define the names, cost, and benefits for the bar chart
        names = [p.name[:15] + '...' if len(p.name) > 15 else p.name for p in projects]
        costs = [p.cost for p in projects]
        benefits = [p.benefit for p in projects]
        
        # define the bar chart
        x = np.arange(len(names))
        width = 0.15
        
        # create the bar chart for costs and benefits
        bars1 = self.ax3.bar(x - width/2, costs, width, label='Cost (₱)', color='#4169E1', alpha=0.7)
        bars2 = self.ax3.bar(x + width/2, [b * 1000 for b in benefits], width, label='Benefit (×1000)', color='#32CD32', alpha=0.7)
        
        # add labels and title
        self.ax3.set_xlabel('Projects')
        self.ax3.set_ylabel('Amount')
        self.ax3.set_title('Selected Projects - Cost vs Benefit')
        self.ax3.set_xticks(x)
        self.ax3.set_xticklabels(names, rotation=90, ha='right')
        self.ax3.legend()
    
    # create the emergency priority distribution chart
    def _create_priority_distribution_chart(self):
        # check if emergency mode is enabled and if there are projects selected
        if self.emergency_mode.get():
            priority_counts = defaultdict(int)
            for project in self.solution.selected_projects:
                if project.is_emergency_priority:
                    priority_counts[f"Priority {project.emergency_priority_level}"] += 1
                else:
                    priority_counts["Normal"] += 1 # normal priority projects
            
            # if there are emergency priority projects
            if priority_counts:
                priorities = list(priority_counts.keys())
                counts = list(priority_counts.values())
                colors = ['#FF4500', '#FF6347', '#FFA500', '#FFD700', '#90EE90', '#87CEEB']
                
                # plot the bar chart
                bars = self.ax4.bar(priorities, counts, color=colors[:len(priorities)])
                self.ax4.set_title('Emergency Priority Distribution')
                self.ax4.set_ylabel('Number of Projects')
                
                # edit the bars of the bar chart
                for bar in bars:
                    height = bar.get_height()
                    self.ax4.text(bar.get_x() + bar.get_width()/2., height,
                                f'{int(height)}', ha='center', va='bottom')
        else: # if emergency mode is not enabled
            self.ax4.text(0.5, 0.5, 'Emergency mode not enabled',
                         ha='center', va='center', transform=self.ax4.transAxes, fontsize=12)
            self.ax4.set_title('Emergency Priority Distribution')
    
    # update projects table
    def update_projects_table(self):

        # clear the existing projects in the table
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        #  return project values to the table
        for project in self.projects:
            priority_text = f"Emergency P{project.emergency_priority_level}" if project.is_emergency_priority else "Normal"
            self.projects_tree.insert('', 'end', values=(
                project.name,
                f"₱{project.cost:,.2f}",
                f"{project.benefit:.2f}",
                f"{project.benefit_cost_ratio:.3f}",
                project.category,
                priority_text
            ))
    # remove selected project from the projects table
    def remove_selected_project(self):
        selection = self.projects_tree.selection()
        if not selection: # if there's no selected projects
            messagebox.showwarning("Warning", "Please select a project to remove.")
            return
        
        # store the project in a list and get the index of the selected project
        item = selection[0]
        index = self.projects_tree.index(item)
        project_name = self.projects[index].name
        
        # confirm the removal
        result = messagebox.askyesno("Confirm Removal", 
                                   f"Are you sure you want to remove project: {project_name}?")
        # if the user picked yes
        if result:
            del self.projects[index]
            self.update_projects_table()
            
            # clear the solution if the removed project was part of it
            for item in self.solution_tree.get_children():
                self.solution_tree.delete(item)
            self.result_text.delete(1.0, tk.END)
            self.solution = None
            self.update_charts()
            
            self.status_label.config(text=f"Project removed. Total projects: {len(self.projects)}")
    
    # clear all projects from the projects table
    def clear_all_projects(self):
        # if there are no projects to clear
        if not self.projects:
            return
        
        # confirm the clearing operation
        result = messagebox.askyesno("Confirm Clear", 
                                   "Are you sure you want to clear all projects?")
        
        # if the user picked yes
        if result:
            self.projects.clear()
            self.update_projects_table()
            
            # clear the solution and result text
            for item in self.solution_tree.get_children():
                self.solution_tree.delete(item)
            self.result_text.delete(1.0, tk.END)
            self.solution = None
            self.update_charts()
            
            self.status_label.config(text="All projects cleared.")

# main function
def main():
    root = tk.Tk()
    app = BudgetAllocationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()