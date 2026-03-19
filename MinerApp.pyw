import ctypes
import sys
import os
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
import time
import requests
import keyboard
import threading
import webbrowser as wb
from PIL import ImageTk

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class MinerApp:
    def __init__(self):

        self.running = 0
        self.gpurunning = False
        self.xmrigrunning = False

        self.rvnaddress = "RAVEN ADDRESS.NAME" #Ravencoin wallet address with worker name
        self.rvnpool1 = "Pool URL" #Ravencoin pool URL
        self.rvnpass1 = "Pool 1 password" #Ravencoin pool password
        self.rvnpool2 = "Pool URL" #Ravencoin pool URL
        self.rvnpass2 = "Pool 2 password" #Ravencoin pool password
        self.rvntab = "URL for pool dashboard" #URL for pool dashboard to open after starting miner

        self.cfxaddress = "CONFLUX ADDRESS.NAME" #Conflux wallet address with worker name
        self.cfxpool = "Pool URL" #Conflux pool URL
        self.cfxtab = "URL for pool dashboard" #URL for pool dashboard to open after starting miner

        self.xmraddress = "MONERO ADDRESS" #Monero wallet address
        self.xmrpool1 = "Pool URL" #Monero pool URL
        self.xmrpool2 = "Pool URL" #Monero pool URL
        self.xmrtab = "URL for pool dashboard" #URL for pool dashboard to open after starting miner
        self.monerod_path = "path/to/monerod" #Path to monerod.exe (in monero GUI wallet)
        self.xmrblockchainpath = "path/to/blockchain" #Path to monero blockchain (in monero GUI wallet)
        self.p2pool_path = "path/to/p2pool" #Path to p2pool.exe (in monero GUI wallet)

        self.fanprofilemining = "path/to/fanprofile" #Path to mining fan profile (in FanControl)
        self.fanprofiledefault = "path/to/fanprofile" #Path to default fan profile (in FanControl)

        self.root = tk.Tk()
        self.root.title("Miner APP")
        self.root.resizable(0, 0)
        self.root.attributes('-topmost', True)
        self.root.wm_iconbitmap(os.path.join(os.path.dirname(__file__), "data", "icon.ico"))

        s = ttk.Style()
        s.configure("TFrame", background="#202020")
        s.configure("running.TFrame", background="#00FF00")
        s.configure("TLabel", background="#202020", foreground="#FFFFFF", font=("Arial", 12))
        s.configure("TButton", font=("Arial", 12))

        self.individual = ttk.Frame(self.root, style="TFrame")
        self.individual.grid(row=0, column=0)
        self.gpuframe = ttk.Frame(self.individual, style="TFrame")
        self.gpuframe.grid(row=0, column=0)
        self.xmrframe = ttk.Frame(self.individual, style="TFrame")
        self.xmrframe.grid(row=1, column=0)
        self.all = ttk.Frame(self.root, style="TFrame")
        self.all.grid(row=0, column=1)

        scriptdir = os.path.dirname(__file__)
        self.datadir = os.path.join(scriptdir, "data")
        rvnlogopath = os.path.join(self.datadir, "rvn.png")
        self.rvnlogo = ImageTk.PhotoImage(file=rvnlogopath)
        cfxlogopath = os.path.join(self.datadir, "cfx.png")
        self.cfxlogo = ImageTk.PhotoImage(file=cfxlogopath)
        xmrlogopath = os.path.join(self.datadir, "xmr.png")
        self.xmrlogo = ImageTk.PhotoImage(file=xmrlogopath)

        self.gpustartbutton = tk.Button(self.gpuframe, image=self.rvnlogo, text="Start RVN Miner", command=lambda: threading.Thread(target=self.rvn).start(), background="#202020", border=0)
        self.gpustartbutton.grid(row=0, column=0)
        self.gpustopbutton = tk.Button(self.individual, text="Stop GPU", command=lambda: None, width=8, height=3, bg="#720000", fg="#FFFFFF", font=("Arial", 50, "bold"), relief="sunken")
        self.gpustopbutton.grid(row=0, column=1, padx=10, pady=10)
        self.xmrstartbutton = tk.Button(self.xmrframe, image=self.xmrlogo, text="Start XMR Miner", command=lambda: threading.Thread(target=self.xmr).start(), background="#202020", border=0)
        self.xmrstartbutton.grid(row=1, column=0)
        self.xmrstopbutton = tk.Button(self.individual, text="Stop XMR", command=lambda: threading.Thread(target=self.stopxmr).start(), width=8, height=3, bg="#720000", fg="#FFFFFF", font=("Arial", 50, "bold"), relief="flat")
        self.xmrstopbutton.grid(row=1, column=1, padx=10, pady=10)

    def rvn(self):
        self.gpustartbutton.config(command=lambda: None, background="#00FF00")
        self.gpuframe.configure(style="running.TFrame")
        self.gpustopbutton.config(bg="#FF0000", command=lambda: threading.Thread(target=self.stoprvn).start(), relief="raised")
        srbminer_path = os.path.join(self.datadir, "SRBMiner-Multi-3-2-0", "SRBMiner-MULTI.exe")
        keyboard.press_and_release('alt+shift+F10')
        os.system("taskkill /f /im MSIAfterburner.exe")
        self.srbminer = subprocess.Popen([
            srbminer_path,
            "-a", "kawpow",
            "-o", f"{self.rvnpool1}",
            "-u", f"{self.rvnaddress}",
            "-p", f"{self.rvnpass1}",
            "--api-enable",
            "--api-port", "10050",
            #"--gpu-intensity", "24",
            "--gpu-coffset0", "150",
            "--gpu-moffset0", "1000",
            "--gpu-plimit0", "250",
            "--log-file-mode", "2"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE) # Stock 51.72MH/s 150/1000 52.28MH/s 300/2000 52.25MH/s
        time.sleep(1)
        keyboard.press("win+right")
        time.sleep(0.1)
        keyboard.release("right")
        time.sleep(0.1)
        keyboard.press("up")
        time.sleep(0.1)
        keyboard.release("win+up")
        time.sleep(0.1)
        self.fans(0, f"{self.fanprofilemining}")
        self.running += 1
        self.gpurunning = True
        time.sleep(30)
        wb.open_new_tab("http://127.0.0.1:10050/stats")
        time.sleep(1)
        wb.open_new_tab(f"{self.rvntab}")

    def stoprvn(self):
        self.gpustartbutton.config(command=lambda: threading.Thread(target=self.rvn).start(), background="#202020")
        self.gpuframe.configure(style="TFrame")
        self.gpustopbutton.config(command=None, bg="#720000", relief="sunken")
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.srbminer.pid)])
        os.startfile("C:\\Program Files (x86)\\MSI Afterburner\\MSIAfterburner.exe")
        keyboard.press_and_release('alt+shift+F10')
        self.running -= 1
        self.gpurunning = False
        if self.running == 0:
            self.fans(0, f"{self.fanprofiledefault}")

    def cfx(self):
        self.gpustartbutton.config(command=lambda: None, background="#00FF00")
        self.gpuframe.configure(style="running.TFrame")
        self.gpustopbutton.config(bg="#FF0000", command=lambda: threading.Thread(target=self.stopcfx).start(), relief="raised")
        lolminer_path = os.path.join(self.datadir, "lolMiner_v1.98a_Win64", "lolMiner.exe")
        keyboard.press_and_release('alt+shift+F10')
        os.system("taskkill /f /im MSIAfterburner.exe")
        self.lolminer = subprocess.Popen([
            lolminer_path,
            "--algo", "OCTOPUS",
            "--pool", f"{self.cfxpool}",
            "--user", f"{self.cfxaddress}",
            "--coff", "150",
            "--moff", "1000",
            "--pl", "250",
            "--apiport", "10050",
            "--silence", "1"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(1)
        keyboard.press("win+right")
        time.sleep(0.1)
        keyboard.release("right")
        time.sleep(0.1)
        keyboard.press("up")
        time.sleep(0.1)
        keyboard.release("win+up")
        time.sleep(0.1)
        self.fans(0, f"{self.fanprofilemining}")
        self.running += 1
        self.gpurunning = True
        time.sleep(30)
        wb.open_new_tab("http://127.0.0.1:10050/gui")
        time.sleep(1)
        wb.open_new_tab(f"{self.cfxtab}")

    def stopcfx(self):
        self.gpustartbutton.config(command=lambda: threading.Thread(target=self.cfx).start(), background="#202020")
        self.gpuframe.configure(style="TFrame")
        self.gpustopbutton.config(command=None, bg="#720000", relief="sunken")
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.lolminer.pid)])
        os.startfile("C:\\Program Files (x86)\\MSI Afterburner\\MSIAfterburner.exe")
        keyboard.press_and_release('alt+shift+F10')
        self.running -= 1
        self.gpurunning = False
        if self.running == 0:
            self.fans(0, f"{self.fanprofiledefault}")

    def xmr(self):
        self.xmrstartbutton.config(command=lambda: None, background="#00FF00")
        self.xmrframe.configure(style="running.TFrame")
        self.xmrstopbutton.config(command=lambda: threading.Thread(target=self.stopxmr).start(), bg="#FF0000", relief="raised")
        xmrig_path = os.path.join(self.datadir, "xmrig-6.24.0", "xmrig.exe")
        self.monerod = subprocess.Popen([
            self.monerod_path,
            "--prune-blockchain",
            "--zmq-pub", "tcp://127.0.0.1:18083",
            "--out-peers", "32",
            "--in-peers", "64",
            "--add-priority-node=p2pmd.xmrvsbeast.com:18080",
            "--add-priority-node=nodes.hashvault.pro:18080",
            "--enforce-dns-checkpointing",
            "--enable-dns-blocklist",
            "--data-dir", f"{self.xmrblockchainpath}",
            "--non-interactive"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(2)
        keyboard.press("win+left")
        time.sleep(0.1)
        keyboard.release("left")
        time.sleep(0.1)
        keyboard.press("up")
        time.sleep(0.1)
        keyboard.release("win+up")
        time.sleep(2)
        self.p2pool = subprocess.Popen([
            self.p2pool_path,
            "--host", "127.0.0.1",
            "--wallet", f"{self.xmraddress}",
            "--nano"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(2)
        keyboard.press("win+left")
        time.sleep(0.1)
        keyboard.release("left")
        time.sleep(0.1)
        keyboard.press("down")
        time.sleep(0.1)
        keyboard.release("win+down")
        time.sleep(2)
        self.xmrig = subprocess.Popen([
            xmrig_path,
            "-o", "127.0.0.1:3333",
            "-o", f"{self.xmrpool1}",
            "-u", f"{self.xmraddress}",
            "-o", f"{self.xmrpool2}",
            "-u", f"{self.xmraddress}",
            "--cpu-affinity=0xFFFF",
            "-t", "16",
            "--randomx-init=16",
            "-r", "3",
            "--http-host", "127.0.0.1",
            "--http-port", "10051"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(2)
        keyboard.press("win+right")
        time.sleep(0.1)
        keyboard.release("right")
        time.sleep(0.1)
        if self.gpurunning:
            keyboard.press("down")
            time.sleep(0.1)
            keyboard.release("win+down")
        else:
            keyboard.release("win")
        time.sleep(0.1)
        self.fans(0, f"{self.fanprofilemining}")
        self.running += 1
        self.xmrigrunning = True
        time.sleep(30)
        wb.open_new_tab(f"{self.xmrtab}")

    def stopxmr(self):
        self.xmrstartbutton.config(command=lambda: threading.Thread(target=self.xmr).start(), background="#202020")
        self.xmrframe.configure(style="TFrame")
        self.xmrstopbutton.config(command=lambda:None, bg="#720000", relief="sunken")
        self.xmrig.terminate()
        time.sleep(10)
        self.p2pool.terminate()
        time.sleep(10)
        stopurl = "http://127.0.0.1:18081/stop_daemon"
        requests.post(stopurl, timeout=10)
        self.running -= 1
        self.xmrigrunning = False
        if self.running == 0:
            self.fans(300, f"{self.fanprofiledefault}")

    def fans(self, delay, profile):
        time.sleep(delay)
        subprocess.call(["C:\\Program Files (x86)\\FanControl\\FanControl.exe", "-c", f"{profile}"], shell=True)

if not is_admin():
    # Choose pythonw.exe only if the script itself is .pyw
    script_path = sys.argv[0] if sys.argv else __file__
    exe_name = "pythonw.exe" if script_path.lower().endswith(".pyw") else "python.exe"
    
    # Build full path to the correct interpreter
    executable = os.path.join(os.path.dirname(sys.executable), exe_name)
    
    # Properly quoted params (handles spaces, special chars, etc.)
    params = " ".join(f'"{arg}"' for arg in sys.argv)
    
    # Elevate
    ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
    quit()

app = MinerApp()
app.root.mainloop()