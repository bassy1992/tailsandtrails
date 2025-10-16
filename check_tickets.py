#!/usr/bin/env python3

import requests

def check_available_tickets():
    """Check what tickets are available in the database"""
    try:
        url = "https://tailsandtrails-production.up.railway.app/api/tickets/"
        response = requests.get(url)
        
        if response.status_code == 200:
            tickets = response.json()
            print(f"✅ Found {len(tickets)} tickets:")
            for ticket in tickets:
                print(f"   ID: {ticket['id']}, Title: {ticket['title']}")
            return tickets
        else:
            print(f"❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    check_available_tickets()