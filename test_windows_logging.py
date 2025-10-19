#!/usr/bin/env python3

"""
Test script to verify Windows logging works correctly
"""

import sys
import os
import platform
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_logging_setup():
    """Test the logging setup for Windows"""
    print("Testing Windows Logging Setup")
    print("=" * 40)
    
    # Simulate the logging setup from the HTTP service
    if platform.system() == 'Windows':
        log_file = os.path.join(os.getcwd(), 'alphasign-http.log')
        print(f"Windows detected - using log file: {log_file}")
    else:
        log_file = '/var/log/alphasign-http.log'
        print(f"Unix detected - using log file: {log_file}")
    
    # Test logging setup
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger('AlphaSignHTTP')
        
        # Test logging
        logger.info("Test log message from Windows logging setup")
        logger.warning("Test warning message")
        logger.error("Test error message")
        
        print("[OK] Logging setup successful")
        print(f"[OK] Log file created: {log_file}")
        
        # Check if log file exists and has content
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                content = f.read()
                if content:
                    print(f"[OK] Log file contains {len(content)} characters")
                    print("[OK] Logging is working correctly")
                    return True
                else:
                    print("[ERROR] Log file is empty")
                    return False
        else:
            print("[ERROR] Log file was not created")
            return False
            
    except Exception as e:
        print(f"[ERROR] Logging setup failed: {e}")
        return False

def test_http_service_logging():
    """Test the HTTP service logging specifically"""
    print("\nTesting HTTP Service Logging")
    print("=" * 40)
    
    try:
        from alphasign_http_service import AlphaSignHTTPService
        
        # Create service instance (don't start it)
        service = AlphaSignHTTPService(host='127.0.0.1', port=8889)  # Use different port for test
        
        # Test logging
        service.logger.info("HTTP service logging test")
        service.logger.warning("HTTP service warning test")
        
        print("[OK] HTTP service logging works")
        return True
        
    except Exception as e:
        print(f"[ERROR] HTTP service logging test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Alpha Sign HTTP Service - Windows Logging Test")
    print("=" * 50)
    
    # Test basic logging setup
    if not test_logging_setup():
        print("\n[ERROR] Basic logging test failed!")
        return False
    
    # Test HTTP service logging
    if not test_http_service_logging():
        print("\n[ERROR] HTTP service logging test failed!")
        return False
    
    print("\n[SUCCESS] All logging tests passed!")
    print("\nThe HTTP service will log to the current directory on Windows.")
    print("Log file: alphasign-http.log")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
