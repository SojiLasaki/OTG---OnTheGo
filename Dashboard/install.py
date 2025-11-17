import subprocess
import sys

# install packages
# List of packages to install
packages = [
    "dash",
    "dash-bootstrap-components",
    "pandas",
    "requests"
]

for package in packages:
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("All packages are installed.")