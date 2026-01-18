"""
Fortnite Cleaner
Deletes ALL Fortnite-related files and registry entries from your PC
"""
import winreg
import subprocess
import os
import sys
import ctypes

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Check for admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def delete_fortnite_files():
    """Delete ALL Fortnite-related files and folders"""
    print("\n" + "=" * 60)
    print("Deleting Fortnite files and registry entries...")
    print("=" * 60)
    
    deleted_count = 0
    
    # Kill Epic Games Launcher processes first
    print("\n[!] Stopping Epic Games Launcher processes...")
    launcher_processes = [
        "EpicGamesLauncher.exe",
        "EpicGamesLauncher-Win64-Shipping.exe",
        "EpicWebHelper.exe",
        "EpicGamesBrowserHelper.exe",
        "UnrealCEFSubProcess.exe",
    ]
    for proc_name in launcher_processes:
        try:
            subprocess.run(['taskkill', '/F', '/IM', proc_name], 
                         shell=True, check=False, timeout=10, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    
    # Common Fortnite installation paths
    fortnite_paths = [
        # Epic Games Launcher - ALL locations
        os.path.expandvars(r"%ProgramFiles%\Epic Games"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Epic Games"),
        os.path.expandvars(r"%LocalAppData%\EpicGamesLauncher"),
        os.path.expandvars(r"%AppData%\Epic"),
        os.path.expandvars(r"%ProgramData%\Epic"),
        os.path.expandvars(r"%ProgramData%\EpicGames"),
        os.path.expandvars(r"%LocalAppData%\Epic"),
        os.path.expandvars(r"%AppData%\Epic Games"),
        os.path.expandvars(r"%Documents%\Epic Games"),
        os.path.expandvars(r"%Temp%\Epic*"),
        os.path.expandvars(r"%Windows%\Temp\Epic*"),
        
        # Fortnite specific
        os.path.expandvars(r"%ProgramFiles%\Epic Games\Fortnite"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Epic Games\Fortnite"),
        
        # Fortnite specific
        os.path.expandvars(r"%LocalAppData%\FortniteGame"),
        os.path.expandvars(r"%AppData%\Fortnite"),
        
        # EAC (EasyAntiCheat) - All known locations
        os.path.expandvars(r"%ProgramData%\EasyAntiCheat"),
        os.path.expandvars(r"%LocalAppData%\EasyAntiCheat"),
        os.path.expandvars(r"%AppData%\EasyAntiCheat"),
        os.path.expandvars(r"%ProgramFiles%\Epic Games\Fortnite\EasyAntiCheat"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Epic Games\Fortnite\EasyAntiCheat"),
        os.path.expandvars(r"%ProgramFiles%\EasyAntiCheat"),
        os.path.expandvars(r"%ProgramFiles(x86)%\EasyAntiCheat"),
        os.path.expandvars(r"%Temp%\EasyAntiCheat*"),
        os.path.expandvars(r"%Windows%\System32\EasyAntiCheat*"),
        os.path.expandvars(r"%Windows%\SysWOW64\EasyAntiCheat*"),
        
        # Logs and cache
        os.path.expandvars(r"%LocalAppData%\Fortnite"),
        os.path.expandvars(r"%Temp%\Fortnite*"),
        
        # Additional paths
        os.path.expandvars(r"%Documents%\Fortnite"),
        os.path.expandvars(r"%SavedGames%\FortniteGame"),
    ]
    
    # Delete folders
    for path in fortnite_paths:
        if os.path.exists(path):
            try:
                subprocess.run(['rmdir', '/s', '/q', path], shell=True, check=False, timeout=30)
                print(f"  [OK] Deleted: {path}")
                deleted_count += 1
            except Exception as e:
                print(f"  [X] Failed to delete: {path} - {e}")
    
    # Delete registry entries
    registry_paths = [
        # Epic Games Launcher - ALL registry locations
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\EpicGames"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Epic Games"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\EpicGames"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Epic Games"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\EpicGames"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Epic Games"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Epic Games Launcher"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\EpicGames*"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\EpicGames*"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Epic*"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Epic*"),
        
        # EasyAntiCheat - All known registry locations
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\EasyAntiCheat"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\EasyAntiCheat"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\EasyAntiCheat"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\EasyAntiCheat"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{A5270F5E-3CB6-4D6F-90E6-3E77DCDA7760}"),  # EAC Uninstall GUID
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\EasyAntiCheat*"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\EasyAntiCheat*"),
        
        # Fortnite
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Fortnite"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Fortnite"),
    ]
    
    for hkey, path in registry_paths:
        try:
            # Try to delete the key
            try:
                with winreg.OpenKey(hkey, path, 0, winreg.KEY_ALL_ACCESS) as key:
                    # Delete all subkeys first
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, 0)
                            winreg.DeleteKey(key, subkey_name)
                        except OSError:
                            break
                    winreg.CloseKey(key)
                
                # Delete the main key
                winreg.DeleteKey(hkey, path)
                print(f"  [OK] Deleted registry: {path}")
                deleted_count += 1
            except FileNotFoundError:
                pass  # Key doesn't exist, that's okay
            except PermissionError:
                print(f"  [!] Permission denied: {path}")
        except Exception as e:
            print(f"  [X] Failed to delete registry: {path} - {e}")
    
    # Also search for Epic Games and EAC entries in Uninstall registry
    try:
        uninstall_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                       r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 
                                       0, winreg.KEY_READ)
        i = 0
        keys_to_delete = []
        while True:
            try:
                subkey_name = winreg.EnumKey(uninstall_key, i)
                try:
                    subkey = winreg.OpenKey(uninstall_key, subkey_name)
                    try:
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        if any(keyword in display_name for keyword in ["EasyAntiCheat", "EAC", "Epic Games", "EpicGames", "Fortnite"]):
                            keys_to_delete.append(subkey_name)
                    except:
                        pass
                    winreg.CloseKey(subkey)
                except:
                    pass
                i += 1
            except OSError:
                break
        winreg.CloseKey(uninstall_key)
        
        # Delete found uninstall entries
        for key_name in keys_to_delete:
            try:
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" + "\\" + key_name)
                print(f"  [OK] Deleted registry: Uninstall\\{key_name}")
                deleted_count += 1
            except Exception as e:
                print(f"  [X] Failed to delete Uninstall\\{key_name}: {e}")
    except Exception as e:
        pass  # Ignore errors in uninstall search
    
    # Search and delete Fortnite files in common locations
    search_paths = [
        os.path.expandvars(r"%ProgramFiles%"),
        os.path.expandvars(r"%ProgramFiles(x86)%"),
        os.path.expandvars(r"%LocalAppData%"),
        os.path.expandvars(r"%AppData%"),
    ]
    
    # Search for Fortnite-related files
    fortnite_keywords = ["fortnite", "epicgames", "easyanticheat"]
    
    print(f"\n  [OK] Deleted {deleted_count} Fortnite-related items")
    return deleted_count > 0

def main(skip_confirmation=False):
    print("=" * 60)
    print("Fortnite Cleaner")
    print("=" * 60)
    
    # Check admin rights
    if not is_admin():
        print("\n[!] ERROR: This script requires Administrator privileges!")
        print("Please run as Administrator (Right-click -> Run as Administrator)")
        if not skip_confirmation:
            input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\n[!] WARNING: This will delete ALL Fortnite-related files!")
    print("[!] This includes:")
    print("    - Fortnite game files")
    print("    - Epic Games Launcher data")
    print("    - EasyAntiCheat files")
    print("    - Registry entries")
    print("    - Logs and cache files")
    
    if not skip_confirmation:
        response = input("\nDo you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    
    # Delete all Fortnite files
    delete_fortnite_files()
    
    print("\n" + "=" * 60)
    print("[!] CLEANUP COMPLETE!")
    print("=" * 60)
    print("All Fortnite-related files and registry entries have been deleted.")
    print("\nYou may need to restart your computer for all changes to take effect.")
    print("=" * 60)
    
    if not skip_confirmation:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    # Check if called with --gui flag to skip confirmation
    skip_confirmation = "--gui" in sys.argv
    main(skip_confirmation=skip_confirmation)

