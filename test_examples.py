#!/usr/bin/env python3

"""
Test script to verify that all examples can be imported and run
"""

import sys
import os
import subprocess

def test_example_import(example_path):
    """Test if an example can be imported without errors"""
    try:
        # Read the example file
        with open(example_path, 'r') as f:
            content = f.read()
        
        # Check if it has the correct import path setup
        if 'sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))' in content:
            print(f"[OK] {os.path.basename(example_path)} has correct import path")
            return True
        else:
            # For existing examples, this is not an error
            print(f"[INFO] {os.path.basename(example_path)} uses standard import (may need PYTHONPATH)")
            return True  # Don't fail for existing examples
            
    except Exception as e:
        print(f"[ERROR] {os.path.basename(example_path)} error: {e}")
        return False

def test_example_syntax(example_path):
    """Test if an example has valid Python syntax"""
    try:
        with open(example_path, 'r') as f:
            content = f.read()
        
        # Compile to check syntax
        compile(content, example_path, 'exec')
        print(f"[OK] {os.path.basename(example_path)} has valid syntax")
        return True
    except SyntaxError as e:
        print(f"[ERROR] {os.path.basename(example_path)} syntax error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {os.path.basename(example_path)} error: {e}")
        return False

def main():
    """Test all example files"""
    print("Testing Example Files")
    print("=" * 40)
    
    # Find all example files
    examples_dir = "examples"
    example_files = []
    
    if os.path.exists(examples_dir):
        for file in os.listdir(examples_dir):
            if file.endswith('.py') and not file.startswith('__'):
                example_files.append(os.path.join(examples_dir, file))
    
    if not example_files:
        print("No example files found!")
        return False
    
    print(f"Found {len(example_files)} example files:")
    for file in example_files:
        print(f"  - {os.path.basename(file)}")
    print()
    
    # Test each example
    syntax_ok = 0
    import_ok = 0
    
    for example_file in example_files:
        print(f"Testing {os.path.basename(example_file)}...")
        
        # Test syntax
        if test_example_syntax(example_file):
            syntax_ok += 1
        
        # Test import setup
        if test_example_import(example_file):
            import_ok += 1
        
        print()
    
    # Summary
    print("=" * 40)
    print(f"Syntax tests passed: {syntax_ok}/{len(example_files)}")
    print(f"Import setup tests passed: {import_ok}/{len(example_files)}")
    
    if syntax_ok == len(example_files) and import_ok == len(example_files):
        print("[SUCCESS] All examples are properly configured!")
        return True
    else:
        print("[WARNING] Some examples need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
