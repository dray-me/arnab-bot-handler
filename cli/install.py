import subprocess
import sys

def install():
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Installation complete.")

if __name__ == "__main__":
    install()
