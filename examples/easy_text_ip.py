#!/usr/bin/env python3

## Simple hello world message over IP
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphasign import AlphaSign, Easy

# Connect to sign via IP (serial over IP converter)
# Format: 'ip:port' or just 'ip' (uses default port 10001)
sign = AlphaSign(port='192.168.133.54:10001')
Easy.Text.show('Hello World over IP!')
