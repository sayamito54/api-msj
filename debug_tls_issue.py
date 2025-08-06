#!/usr/bin/env python3
"""
Debug TLS Connection Issue
Diagnoses the "Connection already using TLS" error
"""

import asyncio
import aiosmtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

async def debug_tls_connection():
    """Debug TLS connection step by step."""
    print("🔍 Debugging TLS Connection Issue")
    print("=" * 50)
    
    # Get configuration
    smtp_host = os.getenv("SMTP_HOST", "smtp-relay.sendinblue.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "test@example.com")
    smtp_pass = os.getenv("SMTP_PASS", "test-password")
    email_from = os.getenv("EMAIL_FROM", "test@example.com")
    
    print(f"Configuration:")
    print(f"  Host: {smtp_host}")
    print(f"  Port: {smtp_port}")
    print(f"  User: {smtp_user}")
    print(f"  From: {email_from}")
    
    # Test different configurations
    configs = [
        {
            "name": "Port 587 with STARTTLS (Correct)",
            "host": smtp_host,
            "port": 587,
            "use_tls": False,
            "use_starttls": True
        },
        {
            "name": "Port 465 with TLS (Alternative)",
            "host": smtp_host,
            "port": 465,
            "use_tls": True,
            "use_starttls": False
        },
        {
            "name": "Port 587 with TLS (Incorrect - This causes the error)",
            "host": smtp_host,
            "port": 587,
            "use_tls": True,
            "use_starttls": False
        }
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n🧪 Test {i}: {config['name']}")
        print(f"   Port: {config['port']}")
        print(f"   use_tls: {config['use_tls']}")
        print(f"   use_starttls: {config['use_starttls']}")
        
        try:
            # Create test message
            message = MIMEMultipart()
            message["From"] = email_from
            message["To"] = smtp_user
            message["Subject"] = f"Test {i}: {config['name']}"
            message.attach(MIMEText("Test email", "plain"))
            
            # Create SMTP client
            smtp = aiosmtplib.SMTP(
                hostname=config['host'],
                port=config['port'],
                use_tls=config['use_tls'],
                username=smtp_user,
                password=smtp_pass,
                validate_certs=False
            )
            
            print("   1. Connecting...")
            await smtp.connect()
            print("   ✅ Connected")
            
            if config['use_starttls']:
                print("   2. Starting STARTTLS...")
                await smtp.starttls()
                print("   ✅ STARTTLS successful")
                
                print("   3. Authenticating after STARTTLS...")
                await smtp.login(smtp_user, smtp_pass)
                print("   ✅ Authentication successful")
            else:
                print("   2. Authenticating...")
                await smtp.login(smtp_user, smtp_pass)
                print("   ✅ Authentication successful")
            
            print("   4. Sending test email...")
            await smtp.send_message(message, recipients=[smtp_user])
            print("   ✅ Email sent successfully")
            
            await smtp.quit()
            print(f"   🎉 Test {i} PASSED")
            
        except Exception as e:
            print(f"   ❌ Test {i} FAILED: {e}")
            if "Connection already using TLS" in str(e):
                print("   💡 This is the exact error you're experiencing!")
                print("   🔧 Solution: Use use_tls=False for port 587")

async def test_current_config():
    """Test the current configuration from the service."""
    print("\n🔍 Testing Current Service Configuration")
    print("=" * 50)
    
    # Simulate the exact logic from email_service.py
    smtp_port = 587
    use_tls = smtp_port == 465  # This should be False for port 587
    use_starttls = smtp_port == 587  # This should be True for port 587
    
    print(f"Current logic:")
    print(f"  Port: {smtp_port}")
    print(f"  use_tls = smtp_port == 465: {use_tls}")
    print(f"  use_starttls = smtp_port == 587: {use_starttls}")
    
    if use_tls and use_starttls:
        print("❌ PROBLEM: Both use_tls and use_starttls are True!")
        print("   This causes 'Connection already using TLS' error")
        print("   Solution: use_tls should be False for port 587")
    elif use_starttls:
        print("✅ CORRECT: use_starttls=True, use_tls=False for port 587")
    elif use_tls:
        print("✅ CORRECT: use_tls=True for port 465")
    else:
        print("⚠️  WARNING: Neither TLS nor STARTTLS configured")

async def main():
    """Run diagnostics."""
    await debug_tls_connection()
    await test_current_config()
    
    print("\n📋 Summary:")
    print("The error 'Connection already using TLS' occurs when:")
    print("1. You set use_tls=True for port 587")
    print("2. Then try to call starttls() on an already-TLS connection")
    print("\n✅ Correct configuration for port 587:")
    print("   - use_tls=False")
    print("   - use_starttls=True")
    print("   - Call starttls() after connect()")
    print("   - Then authenticate")

if __name__ == "__main__":
    asyncio.run(main()) 