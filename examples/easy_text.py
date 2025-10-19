#!/usr/bin/env python3

## Simple hello world message
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphasign import AlphaSign, Easy

sign = AlphaSign(port='/dev/ttyUSB0')
Easy.Text.show('Hello World!')

