#!/usr/bin/env python3
"""
Test script to debug throttle setting in KSP
"""

import krpc
import time

def test_throttle():
    print("Connecting to KSP...")
    conn = krpc.connect(name="ThrottleTest")
    space_center = conn.space_center
    vessel = space_center.active_vessel
    
    print(f"Vessel: {vessel.name}")
    print(f"Initial throttle: {vessel.control.throttle}")
    print(f"Initial SAS: {vessel.control.sas}")
    
    # Set throttle to 0.3
    print("\nSetting throttle to 0.3...")
    vessel.control.throttle = 0.3
    print(f"Throttle after setting: {vessel.control.throttle}")
    
    # Wait a bit
    print("Waiting 1 second...")
    time.sleep(1)
    print(f"Throttle after 1 second: {vessel.control.throttle}")
    
    # Set SAS
    print("\nSetting SAS to True...")
    vessel.control.sas = True
    print(f"SAS after setting: {vessel.control.sas}")
    
    # Wait a bit more
    print("Waiting 1 second...")
    time.sleep(1)
    print(f"Throttle after 2 seconds: {vessel.control.throttle}")
    print(f"SAS after 2 seconds: {vessel.control.sas}")
    
    # Try setting throttle again
    print("\nSetting throttle to 0.5...")
    vessel.control.throttle = 0.5
    print(f"Throttle after setting 0.5: {vessel.control.throttle}")
    
    # Check if engines are available
    print(f"\nEngine count: {len(vessel.parts.engines)}")
    if vessel.parts.engines:
        print(f"First engine active: {vessel.parts.engines[0].active}")
        print(f"First engine thrust: {vessel.parts.engines[0].thrust}")
    
    conn.close()
    print("Test completed")

if __name__ == "__main__":
    test_throttle()
