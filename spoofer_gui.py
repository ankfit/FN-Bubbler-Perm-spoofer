"""
Fortnite Spoofer GUI
Simple GUI for hardware spoofing
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

class SpooferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fortnite Hardware Spoofer")
        self.root.geometry("500x400")
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
        style.configure('TButton', font=('Arial', 11, 'bold'))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#1e1e1e', foreground='#ff6b00')
        
        # Title
        title = ttk.Label(self.root, text="🎮 Fortnite Hardware Spoofer", style='Title.TLabel')
        title.pack(pady=20)
        
        # Warning Frame
        warning_frame = tk.Frame(self.root, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        warning_frame.pack(pady=10, padx=20, fill=tk.X)
        
        warning_text = tk.Label(warning_frame, 
                               text="[!] WARNING: This will PERMANENTLY modify your hardware IDs!\n"
                                    "[!] Restart required after spoofing!\n"
                                    "[!] Consider Windows reinstall for best results!",
                               bg='#2d2d2d', fg='#ffaa00', font=('Arial', 9, 'bold'),
                               justify=tk.LEFT)
        warning_text.pack(pady=10, padx=10)
        
        # Info Frame
        info_frame = tk.Frame(self.root, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        info_text = tk.Label(info_frame,
                            text="This tool will spoof:\n"
                                 "• MAC Address\n"
                                 "• Windows Machine GUID\n"
                                 "• Motherboard Serial\n"
                                 "• Clear EAC Cache",
                            bg='#2d2d2d', fg='white', font=('Arial', 9),
                            justify=tk.LEFT)
        info_text.pack(pady=10, padx=10)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg='#1e1e1e')
        button_frame.pack(pady=20)
        
        self.spoof_btn = tk.Button(button_frame, text="SPOOF HARDWARE", 
                                   command=self.run_spoof,
                                   bg='#ff6b00', fg='white', font=('Arial', 14, 'bold'),
                                   relief=tk.RAISED, padx=30, pady=15, width=20)
        self.spoof_btn.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Ready", bg='#1e1e1e', fg='#00ff00',
                                    font=('Arial', 10, 'bold'))
        self.status_label.pack(pady=10)
        
    def run_spoof(self):
        """Run the spoofing script"""
        response = messagebox.askyesno(
            "Confirm Spoofing",
            "Are you SURE you want to spoof your hardware?\n\n"
            "This is PERMANENT and will survive reboots!\n"
            "You will need to restart your computer!\n\n"
            "Continue?")
        
        if not response:
            return
        
        self.status_label.config(text="Spoofing in progress...", fg='#ffaa00')
        self.spoof_btn.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Run the spoofer script with --gui flag to skip confirmation
            script_path = os.path.join(os.path.dirname(__file__), 'fortnite_spoofer.py')
            result = subprocess.run([sys.executable, script_path, '--gui'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.status_label.config(text="[OK] Spoofing Complete! Restart required!", fg='#00ff00')
                messagebox.showinfo("Success", 
                                   "Hardware spoofing completed!\n\n"
                                   "[!] IMPORTANT: Restart your computer now!\n"
                                   "[!] WICHTIG: Installiere Cuba NEU nach dem Spoofing!\n"
                                   "[!] Consider Windows reinstall for best results!")
            else:
                self.status_label.config(text="[X] Spoofing failed", fg='#ff0000')
                messagebox.showerror("Error", f"Spoofing failed:\n{result.stderr}")
        except Exception as e:
            self.status_label.config(text="[X] Error occurred", fg='#ff0000')
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.spoof_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = SpooferGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

