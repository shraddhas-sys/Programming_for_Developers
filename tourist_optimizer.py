import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import math
import matplotlib.pyplot as plt
import itertools
import time

def load_data():
    try:
        with open('tourist_spots.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "JSON file 'tourist_spots.json' not found!")
        return []

def heuristic_optimization(data, budget, available_time, interest):
    start_time = time.time()
    selected = []
    total_cost = 0
    total_time = 0

    # Sort locations 
    sorted_spots = sorted(data, key=lambda x: (interest in x['tags']), reverse=True)
    
    for spot in sorted_spots:
        if (interest in spot['tags']) or (interest == ""):
            if (total_cost + spot['entry_fee'] <= budget) and \
               (total_time + spot['visit_time'] <= available_time):
                selected.append(spot)
                total_cost += spot['entry_fee']
                total_time += spot['visit_time']
                
    execution_time = time.time() - start_time
    return selected, total_cost, total_time, execution_time

def brute_force_optimization(data, budget, available_time, interest):
    start_time = time.time()
    best_combination = []
    max_spots = 0
    
    # Possible combination
    for i in range(1, len(data) + 1):
        for combo in itertools.combinations(data, i):
            c_cost = sum(s['entry_fee'] for s in combo)
            c_time = sum(s['visit_time'] for s in combo)
            c_match = any(interest in s['tags'] for s in combo) if interest else True
            
            if c_cost <= budget and c_time <= available_time and c_match:
                if len(combo) > max_spots:
                    max_spots = len(combo)
                    best_combination = combo
                    
    execution_time = time.time() - start_time
    return list(best_combination), execution_time

def run_planner():
    data = load_data()
    if not data: return
    
    try:
        u_budget = float(entry_budget.get())
        u_time = float(entry_time.get())
        u_interest = entry_interest.get().lower()
        
        h_res, h_cost, h_duration, h_exec = heuristic_optimization(data, u_budget, u_time, u_interest)
        b_res, b_exec = brute_force_optimization(data, u_budget, u_time, u_interest)
        
        display_results(h_res, h_cost, h_duration, h_exec, b_res, b_exec)
        
        if h_res:
            show_path_map(h_res)
            
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for Budget and Time.")

def display_results(h_res, h_cost, h_duration, h_exec, b_res, b_exec):
    result_box.delete(1.0, tk.END)
    report = f"--- SUGGESTED ITINERARY (HEURISTIC) ---\n"
    if not h_res:
        report += "No spots found matching your criteria.\n"
    else:
        for i, s in enumerate(h_res):
            report += f"{i+1}. {s['name']} (Fee: Rs.{s['entry_fee']}, Time: {s['visit_time']}h)\n"
        
        report += f"\nTotal Estimated Cost: Rs.{h_cost}\n"
        report += f"Total Time Required: {h_duration} hours\n"
        
    report += f"\n--- ALGORITHM COMPARISON ---\n"
    report += f"Heuristic Spots: {len(h_res)} (Time: {h_exec:.6f}s)\n"
    report += f"Brute-Force Spots: {len(b_res)} (Time: {b_exec:.6f}s)\n"
    
    result_box.insert(tk.END, report)

def show_path_map(spots):
    names = [s['name'] for s in spots]
    lats = [s['lat'] for s in spots]
    longs = [s['long'] for s in spots]
    
    plt.figure(figsize=(9, 6))
    plt.plot(longs, lats, marker='o', linestyle='-', color='#556b2f', linewidth=2, markersize=8)
    for i, name in enumerate(names):
        plt.annotate(f"{i+1}. {name}", (longs[i], lats[i]), xytext=(8,8), textcoords='offset points', fontsize=9)
    
    plt.title("Optimized Tourist Path (Kathmandu)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

# Setting up the main window 
BG_COLOR = "#FFFDD0"      
HEADER_COLOR = "#6F4E37"  
BTN_COLOR = "#E6E6FA"     
TXT_COLOR = "#333333"     

root = tk.Tk()
root.title("Kathmandu Tourist Path Optimizer")
root.geometry("550x800")
root.configure(bg=BG_COLOR)

tk.Label(root, text="TOURIST OPTIMIZER", font=("Verdana", 22, "bold"), 
         fg=HEADER_COLOR, bg=BG_COLOR).pack(pady=40)

form = tk.Frame(root, bg=BG_COLOR)
form.pack(pady=10)

def create_field(label_text):
    tk.Label(form, text=label_text, font=("Verdana", 10, "bold"), 
             bg=BG_COLOR, fg=TXT_COLOR).pack(anchor="w")
    entry = tk.Entry(form, width=40, font=("Verdana", 11), bd=0, 
                     highlightthickness=1, highlightbackground="#cccccc")
    entry.pack(pady=(5, 15), ipady=8)
    return entry

entry_time = create_field("Available Time (Hours):")
entry_budget = create_field("Maximum Budget (Rs):")
entry_interest = create_field("Interest (nature, culture, history):")

btn_plan = tk.Button(root, text="GENERATE ITINERARY", command=run_planner, 
                     bg=BTN_COLOR, fg="#556b2f", font=("Verdana", 12, "bold"), 
                     width=25, pady=12, relief="flat", cursor="hand2")
btn_plan.pack(pady=20)

result_box = scrolledtext.ScrolledText(root, width=60, height=15, 
                                       font=("Courier New", 10), bd=0, 
                                       bg="#ffffff", fg=TXT_COLOR)
result_box.pack(pady=20, padx=40)

root.mainloop()