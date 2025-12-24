"""
Diagnostic script to identify why the server connection fails
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("DIAGNOSTIC: Environment Check")
print("=" * 60)

# Check Python info
print(f"\n1. Python executable: {sys.executable}")
print(f"2. Python version: {sys.version}")
print(f"3. Current working directory: {os.getcwd()}")

# Check project structure
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
print(f"4. Project root: {PROJECT_ROOT}")
print(f"5. .env file exists: {(PROJECT_ROOT / '.env').exists()}")

# Try to load dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
    print("6. dotenv loaded: SUCCESS")
except Exception as e:
    print(f"6. dotenv loaded: FAILED - {e}")

# Check GITHUB_TOKEN
token = os.getenv("GITHUB_TOKEN")
if token:
    print(f"7. GITHUB_TOKEN: SET (length={len(token)}, starts with: {token[:4]}...)")
else:
    print("7. GITHUB_TOKEN: NOT SET <-- THIS IS THE PROBLEM!")

# Check if server module is importable
print("\n" + "=" * 60)
print("DIAGNOSTIC: Server Module Check")
print("=" * 60)

try:
    # Add project to path
    sys.path.insert(0, str(PROJECT_ROOT / "src"))
    from github_mcp import server
    print("8. github_mcp.server: IMPORTABLE")
except Exception as e:
    print(f"8. github_mcp.server: FAILED - {e}")

# Try to run server directly to see error
print("\n" + "=" * 60)
print("DIAGNOSTIC: Direct Server Test")
print("=" * 60)

import subprocess
result = subprocess.run(
    [sys.executable, "-c", 
     f"import sys; sys.path.insert(0, r'{PROJECT_ROOT / 'src'}'); "
     f"from dotenv import load_dotenv; load_dotenv(r'{PROJECT_ROOT / '.env'}'); "
     f"import os; "
     f"print('Token set:', bool(os.getenv('GITHUB_TOKEN'))); "
     f"from github_mcp.server import get_github_client; "
     f"client = get_github_client(); "
     f"print('GitHub client created successfully!')"],
    capture_output=True,
    text=True,
    cwd=str(PROJECT_ROOT)
)

print(f"Stdout: {result.stdout}")
if result.stderr:
    print(f"Stderr: {result.stderr}")
print(f"Return code: {result.returncode}")

print("\n" + "=" * 60)
print("END DIAGNOSTIC")
print("=" * 60)
