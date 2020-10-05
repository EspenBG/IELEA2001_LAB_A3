import subprocess

if __name__ == '__main__':
    try:
        subprocess.run(["C:\\Program Files (x86)\\Nmap\\ncat.exe", "-l", "8001"], shell=True)
    except Exception:
        pass