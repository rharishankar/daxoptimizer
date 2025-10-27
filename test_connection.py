#!/usr/bin/env python3
"""
Simple test to diagnose GitHub Models API connection
"""

import os
from openai import OpenAI

print("=" * 60)
print("GitHub Models API Connection Test")
print("=" * 60)

# Check if token is set
token = os.environ.get("GITHUB_TOKEN")
if not token:
    print("\n❌ GITHUB_TOKEN is not set!")
    print("\nSet it with:")
    print("  export GITHUB_TOKEN='your_token_here'")
    exit(1)
else:
    print(f"\n✅ Token found: {token[:10]}...{token[-4:]}")

# Try to connect to API
print("\n📡 Testing connection to GitHub Models API...")

try:
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token
    )
    
    print("✅ Client created successfully")
    
    # Try a simple API call
    print("\n🔄 Sending test request...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Say 'Hello, this is a test!' and nothing else."}
        ],
        max_tokens=50,
        temperature=0.1
    )
    
    result = response.choices[0].message.content
    
    print(f"✅ Success! API Response: {result}")
    print("\n🎉 Your connection is working!")
    print("\nYour dax_optimizer.py should work now.")
    
except Exception as e:
    print(f"\n❌ Connection Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Token doesn't have access to GitHub Models API")
    print("2. Network/firewall blocking the connection")
    print("3. GitHub Models API endpoint changed")
    print("4. You need GitHub Copilot subscription")
    print("\nTroubleshooting:")
    print("- Check your token at: https://github.com/settings/tokens")
    print("- Verify you have GitHub Copilot access")
    print("- Try regenerating your token with 'repo' scope")
    print("- Check if your network blocks Azure endpoints")

print("\n" + "=" * 60)
