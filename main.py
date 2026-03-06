import tkinter as tk

root = tk.Tk()
root.title("DSA Project Workspace")
root.geometry("400x300")

label = tk.Label(root, text="System Ready!", font=("Helvetica", 18))
label.pack(pady=50)

root.mainloop()