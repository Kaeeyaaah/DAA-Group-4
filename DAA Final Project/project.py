# this file will handle everything there is to handle in a project

# project class
class Project:
    
    # initialize a project's information
    def __init__(self, name, cost, benefit, category, description=""):
        self.name = name
        self.cost = cost
        self.set_benefit(benefit)  # this is used to validate the benefit score
        self.category = category
        self.description = description
        self.benefit_cost_ratio = cost > 0 and benefit / cost or 0
        self.is_emergency_priority = False
        self.emergency_priority_level = 5  # default lowest priority
    
    def set_benefit(self, benefit):

        # benefit score conditions
        if benefit > 10:
            raise ValueError(f"Benefit score cannot exceed 10. Current value: {benefit}")
        if benefit < 0:
            raise ValueError(f"Benefit score cannot be negative. Current value: {benefit}")
        
        self.benefit = benefit
        self.benefit_cost_ratio = self.cost > 0 and benefit / self.cost or 0
    
    # handling emergency situations
    def set_emergency_priority(self, is_emergency):
        self.is_emergency_priority = is_emergency
        if is_emergency:
            # Set priority levels based on category during emergencies
            category_lower = self.category.lower()
            if category_lower == "infrastructure":
                self.emergency_priority_level = 1  # infrastructure have the highest priority
            elif category_lower == "health":
                self.emergency_priority_level = 2
            elif category_lower == "social services":
                self.emergency_priority_level = 3
            elif category_lower == "environment":
                self.emergency_priority_level = 4
            else:
                self.emergency_priority_level = 5  # lowest priority for other project categories
        else:
            self.emergency_priority_level = 5 # priority level if there's no emergency

    # end of set_emergency_priority
    def __str__(self):
        emergency_status = f" [EMERGENCY PRIORITY: {self.emergency_priority_level}]" if self.is_emergency_priority else ""
        return f"Project: {self.name} | Cost: ₱{self.cost:.2f} | Benefit: {self.benefit:.2f} | Ratio: {self.benefit_cost_ratio:.3f} | Category: {self.category}{emergency_status}"
