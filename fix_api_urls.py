#!/usr/bin/env python3
"""
Script to replace hardcoded localhost URLs with environment variables in frontend files
"""
import os
import re

def replace_in_file(file_path, pattern, replacement):
    """Replace pattern with replacement in file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count matches before replacement
        matches = len(re.findall(pattern, content))
        if matches > 0:
            new_content = re.sub(pattern, replacement, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ {file_path}: Replaced {matches} occurrences")
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def find_and_replace_urls():
    """Find and replace all hardcoded localhost URLs"""
    
    # Pattern to match localhost URLs
    pattern = r'http://localhost:8000/api'
    replacement = '${import.meta.env.VITE_API_URL || \'http://localhost:8000/api\'}'
    
    # Files to process
    frontend_dir = 'Tfront'
    
    # Find all TypeScript/JavaScript files
    files_to_process = []
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith(('.tsx', '.ts', '.js', '.jsx')):
                files_to_process.append(os.path.join(root, file))
    
    print(f"Found {len(files_to_process)} files to process...")
    
    updated_files = 0
    for file_path in files_to_process:
        if replace_in_file(file_path, pattern, replacement):
            updated_files += 1
    
    print(f"\n🎉 Updated {updated_files} files successfully!")
    
    # Also update template literal usage
    pattern2 = r'\$\{import\.meta\.env\.VITE_API_URL \|\| \'http://localhost:8000/api\'\}/([^\'"`\s\)]+)'
    replacement2 = r'`${import.meta.env.VITE_API_URL || \'http://localhost:8000/api\'}/\1`'
    
    print("\nFixing template literal syntax...")
    for file_path in files_to_process:
        replace_in_file(file_path, pattern2, replacement2)

if __name__ == "__main__":
    find_and_replace_urls()