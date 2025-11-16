#!/usr/bin/env python3
"""
Utility to create an admin user and print credentials.

Usage:
  python create_admin.py --email admin@example.com

This script uses the existing `register_user` function in `streamlit_auth.py` so
passwords are hashed consistently with the app.
"""
from __future__ import annotations

import argparse
import secrets
import string
from typing import Optional

from streamlit_auth import register_user


def generate_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an admin user for the Streamlit app")
    parser.add_argument("--email", "-e", required=False, default="admin@example.com", help="Email address for the admin account")
    parser.add_argument("--password", "-p", required=False, help="Optional: provide a password. If omitted a secure one will be generated.")
    args = parser.parse_args()

    password: Optional[str] = args.password or generate_password(12)
    success, message = register_user(args.email.strip().lower(), password, is_admin=True)
    if success:
        print("✅ Admin account created successfully.")
        print(f"Email: {args.email.strip().lower()}")
        print(f"Password: {password}")
        print("\nPlease log in to the Streamlit app and change this password immediately.")
    else:
        print(f"❌ Failed to create admin: {message}")
        if "already exists" in message:
            print("If the user already exists but is not an admin, you can either promote them in the app's Admin Panel or delete them from app/credentials.json and re-run this script.")


if __name__ == "__main__":
    main()
