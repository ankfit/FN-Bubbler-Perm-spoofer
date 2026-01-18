"""
Fortnite Hardware Spoofer
Permanent hardware ID spoofer for EasyAntiCheat (EAC) bypass
"""
import winreg
import subprocess
import random
import string
import os
import sys
import ctypes
from ctypes import wintypes

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

def generate_random_mac():
    """Generate random MAC address"""
    return ':'.join(['%02x' % random.randint(0, 255) for _ in range(6)])

def generate_random_serial(length=12):
    """Generate random serial number"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def spoof_mac_address():
    """Spoof MAC address via registry"""
    try:
        # Get network adapter registry path
        key_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ) as key:
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey_path = f"{key_path}\\{subkey_name}"
                    
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_WRITE) as subkey:
                            # Check if it's a network adapter
                            try:
                                net_cfg_instance_id = winreg.QueryValueEx(subkey, "NetCfgInstanceId")[0]
                                if "ethernet" in net_cfg_instance_id.lower() or "wireless" in net_cfg_instance_id.lower():
                                    new_mac = generate_random_mac()
                                    winreg.SetValueEx(subkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
                                    print(f"  [OK] MAC Address spoofed: {new_mac}")
                                    return True
                            except:
                                pass
                    except PermissionError:
                        pass
                    i += 1
                except OSError:
                    break
    except Exception as e:
        print(f"  [X] MAC spoofing failed: {e}")
    return False

def spoof_disk_serial():
    """Spoof disk serial numbers via registry"""
    try:
        key_path = r"SYSTEM\CurrentControlSet\Enum\IDE"
        
        # This is complex and may require driver-level spoofing
        # For now, we'll modify what we can in registry
        print("  [!] Disk serial spoofing requires driver-level access")
        print("  [!] Consider using a disk spoofing driver")
        return False
    except Exception as e:
        print(f"  [X] Disk serial spoofing failed: {e}")
    return False

def spoof_motherboard_serial():
    """Spoof motherboard serial via registry"""
    try:
        key_path = r"HARDWARE\DESCRIPTION\System\BIOS"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
            new_serial = generate_random_serial(16)
            try:
                winreg.SetValueEx(key, "SystemSerialNumber", 0, winreg.REG_SZ, new_serial)
                print(f"  [OK] Motherboard Serial spoofed: {new_serial}")
                return True
            except:
                pass
    except Exception as e:
        print(f"  [X] Motherboard serial spoofing failed: {e}")
    return False

def spoof_windows_id():
    """Spoof Windows Installation ID"""
    try:
        key_path = r"SOFTWARE\Microsoft\Cryptography"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
            new_machine_guid = '{' + str(random.uuid4()).upper() + '}'
            winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_machine_guid)
            print(f"  [OK] Windows Machine GUID spoofed: {new_machine_guid}")
            return True
    except Exception as e:
        print(f"  [X] Windows ID spoofing failed: {e}")
    return False

def spoof_cpu_id():
    """Spoof CPU ID via registry"""
    try:
        key_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
            new_processor_id = generate_random_serial(16)
            try:
                winreg.SetValueEx(key, "ProcessorNameString", 0, winreg.REG_SZ, new_processor_id)
                print(f"  [OK] CPU ID modified")
                return True
            except:
                pass
    except Exception as e:
        print(f"  [X] CPU ID spoofing failed: {e}")
    return False

def clear_eac_cache():
    """Clear EasyAntiCheat cache and logs"""
    eac_paths = [
        os.path.expandvars(r"%ProgramData%\EasyAntiCheat"),
        os.path.expandvars(r"%LocalAppData%\EasyAntiCheat"),
        os.path.expandvars(r"%AppData%\EasyAntiCheat"),
    ]
    
    cleared = False
    for path in eac_paths:
        if os.path.exists(path):
            try:
                subprocess.run(['rmdir', '/s', '/q', path], shell=True, check=False)
                print(f"  [OK] Cleared EAC cache: {path}")
                cleared = True
            except:
                pass
    
    return cleared

def delete_fortnite_files():
    """Delete ALL Fortnite-related files and folders"""
    print("\n" + "=" * 60)
    print("Deleting Fortnite files and registry entries...")
    print("=" * 60)
    
    deleted_count = 0
    
    # Common Fortnite installation paths
    fortnite_paths = [
        # Epic Games Launcher
        os.path.expandvars(r"%ProgramFiles%\Epic Games\Fortnite"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Epic Games\Fortnite"),
        os.path.expandvars(r"%LocalAppData%\EpicGamesLauncher"),
        os.path.expandvars(r"%AppData%\Epic"),
        
        # Fortnite specific
        os.path.expandvars(r"%LocalAppData%\FortniteGame"),
        os.path.expandvars(r"%AppData%\Fortnite"),
        os.path.expandvars(r"%ProgramData%\Epic"),
        os.path.expandvars(r"%ProgramData%\EpicGames"),
        
        # EAC
        os.path.expandvars(r"%ProgramData%\EasyAntiCheat"),
        os.path.expandvars(r"%LocalAppData%\EasyAntiCheat"),
        os.path.expandvars(r"%AppData%\EasyAntiCheat"),
        
        # Logs and cache
        os.path.expandvars(r"%LocalAppData%\Fortnite"),
        os.path.expandvars(r"%Temp%\Fortnite*"),
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
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\EpicGames"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\EasyAntiCheat"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\EpicGames"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\EasyAntiCheat"),
    ]
    
    for hkey, path in registry_paths:
        try:
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_ALL_ACCESS) as key:
                winreg.DeleteKey(key, "")
                winreg.DeleteKey(hkey, path)
                print(f"  [OK] Deleted registry: {path}")
                deleted_count += 1
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  [X] Failed to delete registry: {path} - {e}")
    
    # Search and delete Fortnite files in common locations
    search_paths = [
        os.path.expandvars(r"%ProgramFiles%"),
        os.path.expandvars(r"%ProgramFiles(x86)%"),
        os.path.expandvars(r"%LocalAppData%"),
        os.path.expandvars(r"%AppData%"),
    ]
    
    print(f"\n  [OK] Deleted {deleted_count} Fortnite-related items")
    return deleted_count > 0

def main(skip_confirmation=False):
    print("=" * 60)
    print("Fortnite Hardware Spoofer")
    print("=" * 60)
    
    # Check admin rights
    if not is_admin():
        print("\n[!] ERROR: This script requires Administrator privileges!")
        print("Please run as Administrator (Right-click -> Run as Administrator)")
        if not skip_confirmation:
            input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\n[!] WARNING: This will modify your system hardware identifiers!")
    print("[!] Make sure you have a Windows reinstall ready if needed!")
    print("[!] This is PERMANENT and will survive reboots!")
    
    if not skip_confirmation:
        response = input("\nDo you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    
    print("\n" + "=" * 60)
    print("Starting spoofing process...")
    print("=" * 60 + "\n")
    
    # First delete all Fortnite files
    delete_fortnite_files()
    
    # Then spoof hardware
    results = {
        "MAC Address": spoof_mac_address(),
        "Disk Serial": spoof_disk_serial(),
        "Motherboard Serial": spoof_motherboard_serial(),
        "Windows ID": spoof_windows_id(),
        "CPU ID": spoof_cpu_id(),
        "EAC Cache": clear_eac_cache()
    }
    
    print("\n" + "=" * 60)
    print("Spoofing Results:")
    print("=" * 60)
    for item, success in results.items():
        status = "[OK]" if success else "[X]"
        print(f"  {status} {item}")
    
    print("\n" + "=" * 60)
    print("[!] IMPORTANT NEXT STEPS:")
    print("  1. Restart your computer for changes to take effect")
    print("  2. Reinstall Windows for best results (clean slate)")
    print("  3. After Windows reinstall, run this spoofer again")
    print("  4. [!] WICHTIG: Installiere Cuba NEU nach dem Spoofing!")
    print("  5. Then install and test Fortnite")
    print("=" * 60)
    
    if not skip_confirmation:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    # Check if called with --gui flag to skip confirmation
    skip_confirmation = "--gui" in sys.argv
    main(skip_confirmation=skip_confirmation)

