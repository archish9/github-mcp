"""Test script to debug server startup issues"""
import sys
import os
import asyncio
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("1. Importing server module...")
    from github_mcp import server
    print("   ✓ Import successful")
    
    print("\n2. Testing get_github_client (should fail gracefully if no token)...")
    try:
        client = server.get_github_client()
        print("   ✓ GitHub client created")
    except ValueError as e:
        print(f"   ⚠ Expected error (no token): {e}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        traceback.print_exc()
    
    print("\n3. Testing server.run with a simple test...")
    print("   (This will wait for stdin, so it may hang - that's normal)")
    print("   Press Ctrl+C to stop")
    
    # Try to run the server
    try:
        asyncio.run(server.main())
    except KeyboardInterrupt:
        print("\n   ✓ Server stopped by user")
    except Exception as e:
        print(f"   ✗ Error running server: {e}")
        traceback.print_exc()
        
except Exception as e:
    print(f"✗ Fatal error: {e}")
    traceback.print_exc()
    sys.exit(1)

