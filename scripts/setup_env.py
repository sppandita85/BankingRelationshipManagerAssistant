#!/usr/bin/env python3
"""
Environment Setup Script for Banking RM Agent
Helps you set up environment variables securely.
"""

import os
import secrets
import sys
from pathlib import Path

def generate_jwt_secret():
    """Generate a secure JWT secret key."""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file from template."""
    env_file = Path(".env")
    template_file = Path("env_template.txt")
    
    if env_file.exists():
        response = input(".env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env file creation.")
            return False
    
    if not template_file.exists():
        print("Error: env_template.txt not found!")
        return False
    
    # Read template
    with open(template_file, 'r') as f:
        content = f.read()
    
    # Generate JWT secret
    jwt_secret = generate_jwt_secret()
    content = content.replace('your_super_secret_jwt_key_here', jwt_secret)
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ .env file created successfully!")
    print(f"🔐 JWT Secret generated: {jwt_secret[:8]}...")
    return True

def validate_env_file():
    """Validate that required environment variables are set."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "OPENAI_API_KEY",
        "DB_PASSWORD", 
        "JWT_SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or placeholder values for: {', '.join(missing_vars)}")
        print("Please update your .env file with actual values.")
        return False
    
    print("✅ All required environment variables are set!")
    return True

def check_gitignore():
    """Check if .env is in .gitignore."""
    gitignore_file = Path(".gitignore")
    
    if not gitignore_file.exists():
        print("❌ .gitignore file not found!")
        return False
    
    with open(gitignore_file, 'r') as f:
        content = f.read()
    
    if '.env' in content:
        print("✅ .env is properly ignored by Git!")
        return True
    else:
        print("❌ .env is NOT in .gitignore!")
        print("Please add '.env' to your .gitignore file.")
        return False

def main():
    """Main setup function."""
    print("🔐 Banking RM Agent - Environment Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("src/banking_rm_agent").exists():
        print("❌ Please run this script from the project root directory!")
        sys.exit(1)
    
    # Step 1: Create .env file
    print("\n1. Creating .env file...")
    if create_env_file():
        print("   ✅ .env file created")
    else:
        print("   ⚠️  .env file creation skipped")
    
    # Step 2: Check .gitignore
    print("\n2. Checking .gitignore...")
    check_gitignore()
    
    # Step 3: Validate environment
    print("\n3. Validating environment variables...")
    validate_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 Environment setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your actual API keys and passwords")
    print("2. Test your configuration: python -c 'from src.banking_rm_agent import BankingRMAgent'")
    print("3. Run the application: streamlit run src/banking_rm_agent/interfaces/streamlit_app.py")

if __name__ == "__main__":
    main()
