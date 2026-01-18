"""
Fortnite Cleaner GUI
Simple GUI for cleaning all Fortnite files and registry entries
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import ctypes

def is_admin():
    """Check if running as administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Restart script as administrator"""
    if is_admin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False

class FortniteCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fortnite Cleaner")
        self.root.geometry("600x500")
        self.root.configure(bg='#1e1e1e')
        
        # Check admin
        if not is_admin():
            messagebox.showwarning("Admin Required", 
                                 "This tool requires Administrator privileges!\n\n"
                                 "The window will close and reopen with admin rights.")
            if run_as_admin():
                self.root.destroy()
                return
            else:
                self.root.after(1000, self.root.destroy)
                return
        
        self.create_widgets()
    
    def create_widgets(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title
        title = tk.Label(self.root, text="Fortnite Cleaner", 
                        bg='#1e1e1e', fg='#ff6b00', font=('Arial', 18, 'bold'))
        title.pack(pady=15)
        
        # Warning Frame
        warning_frame = tk.Frame(self.root, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        warning_frame.pack(pady=10, padx=20, fill=tk.X)
        
        warning_text = tk.Label(warning_frame, 
                               text="[!] WARNING: This will delete ALL Fortnite-related files!\n"
                                    "[!] Including:\n"
                                    "    • Fortnite game files\n"
                                    "    • Epic Games Launcher data\n"
                                    "    • EasyAntiCheat files\n"
                                    "    • Registry entries\n"
                                    "    • Logs and cache files",
                               bg='#2d2d2d', fg='#ffaa00', font=('Arial', 9, 'bold'),
                               justify=tk.LEFT)
        warning_text.pack(pady=10, padx=10)
        
        # Info Frame
        info_frame = tk.Frame(self.root, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        info_text = tk.Label(info_frame,
                            text="This tool will completely remove Fortnite from your PC.\n"
                                 "Use this before reinstalling or after uninstalling.",
                            bg='#2d2d2d', fg='white', font=('Arial', 9),
                            justify=tk.LEFT)
        info_text.pack(pady=10, padx=10)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg='#1e1e1e')
        button_frame.pack(pady=20)
        
        self.clean_btn = tk.Button(button_frame, text="CLEAN FORTNITE", 
                                   command=self.run_clean,
                                   bg='#ff6b00', fg='white', font=('Arial', 14, 'bold'),
                                   relief=tk.RAISED, padx=30, pady=15, width=20)
        self.clean_btn.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Ready", bg='#1e1e1e', fg='#00ff00',
                                    font=('Arial', 10, 'bold'))
        self.status_label.pack(pady=10)
    
    def run_clean(self):
        """Run the cleaning script"""
        response = messagebox.askyesno(
            "Confirm Cleaning",
            "Are you SURE you want to delete ALL Fortnite files?\n\n"
            "This will delete:\n"
            "• All game files\n"
            "• Epic Games Launcher data\n"
            "• EasyAntiCheat files\n"
            "• Registry entries\n"
            "• Logs and cache\n\n"
            "This action CANNOT be undone!\n\n"
            "Continue?")
        
        if not response:
            return
        
        self.status_label.config(text="Cleaning in progress...", fg='#ffaa00')
        self.clean_btn.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Run the cleaner script
            script_path = os.path.join(os.path.dirname(__file__), 'fortnite_cleaner.py')
            result = subprocess.run([sys.executable, script_path, '--gui'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.status_label.config(text="[OK] Cleaning Complete!", fg='#00ff00')
                messagebox.showinfo("Success", 
                                   "Fortnite files cleaned successfully!\n\n"
                                   "All Fortnite-related files and registry entries have been deleted.\n"
                                   "You may need to restart your computer.")
            else:
                self.status_label.config(text="[X] Cleaning failed", fg='#ff0000')
                messagebox.showerror("Error", f"Cleaning failed:\n{result.stderr}")
        except Exception as e:
            self.status_label.config(text="[X] Error occurred", fg='#ff0000')
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.clean_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = FortniteCleanerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

