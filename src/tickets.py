from datetime import datetime
from enum import Enum
import random
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class TriageSLA(Enum):
    SIX_HOURS = "6hrs"
    ONE_DAY = "1day"
    THREE_DAYS = "3day"


class Ticket:
    def __init__(self, description, required_capabilities, proficiency_level, triage_sla):
        if triage_sla not in TriageSLA:
            raise ValueError("Invalid triage SLA value. Must be one of: 6hrs, 1day, 3day.")
        
        self.created_timestamp = datetime.now()
        self.description = description
        self.required_capabilities = required_capabilities
        self.proficiency_level = proficiency_level
        self.triage_sla = triage_sla

    def __repr__(self):
        return (f"Ticket(created_timestamp={self.created_timestamp}, "
                f"description={self.description}, "
                f"required_capabilities={self.required_capabilities}, "
                f"proficiency_level={self.proficiency_level}, "
                f"triage_sla={self.triage_sla.value})")
    
    def generate_tickets(n):
        capabilities_pool = ["Python", "Java", "SQL", "AWS", "Docker", "Kubernetes", "React", "Node.js"]
        proficiency_levels = ["Beginner", "Intermediate", "Advanced"]
        triage_sla_values = list(TriageSLA)

        tickets = []
        for _ in range(n):
            # Generate a right-skewed distribution for capabilities
            capabilities_count = random.choices(range(1, 4), weights=[70, 20, 10], k=1)[0]
            required_capabilities = random.choices(capabilities_pool, k=capabilities_count)
            
            # Assign proficiency levels with a right-skewed distribution
            proficiency_level = {
                cap: random.choices(
                    proficiency_levels, 
                    weights=[80, 15, 5],  # Skewed weights: more "Beginner", fewer "Advanced"
                    k=1
                )[0] 
                for cap in required_capabilities
            }
            
            # Randomly select a triage SLA with a right-skewed distribution
            triage_sla = random.choices(
                triage_sla_values, 
                weights=[80, 15, 5],  # Skewed weights: more "6hrs", fewer "3day"
                k=1
            )[0]
            
            # Create a ticket
            ticket = Ticket(
                description=f"Ticket for {', '.join(required_capabilities)}",
                required_capabilities=required_capabilities,
                proficiency_level=proficiency_level,
                triage_sla=triage_sla
            )
            tickets.append(ticket)
        
        return tickets
    

    


# Example usage
if __name__ == "__main__":
    # Generate 10 tickets
    tickets = Ticket.generate_tickets(50)
    
    # Print the generated tickets
    for ticket in tickets:
        print(ticket)   
    
    # Prepare data for visualization
    data = []
    for ticket in tickets:
        for capability, proficiency in ticket.proficiency_level.items():
            data.append({
                "Capability": capability,
                "Proficiency": proficiency,
                "SLA": ticket.triage_sla.value
            })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Count combinations of (Capability, Proficiency, SLA)
    combination_counts = df.groupby(["Capability", "Proficiency", "SLA"]).size().reset_index(name="Count")

    # Plot the data
    plt.figure(figsize=(12, 8))
    sns.barplot(
        data=combination_counts,
        x="Capability",
        y="Count",
        hue="Proficiency",
        dodge=True
    )
    plt.title("Count of (Capability, Proficiency, SLA) Combinations")
    plt.xlabel("Capability")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.legend(title="Proficiency")
    plt.tight_layout()
    plt.show()