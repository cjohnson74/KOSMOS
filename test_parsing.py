#!/usr/bin/env python3
"""
Test script to verify the FlightAgent parsing fix
"""

import sys
sys.path.insert(0, '/Users/carsonjohnson/Documents/KOSMOS')

from kosmos.agents.flight import FlightAgent
from langchain_core.messages import AIMessage

def test_parsing():
    """Test parsing regular functions instead of async"""
    print("🧪 Testing FlightAgent parsing with regular functions")
    
    # Test code with regular function (what LLM actually generates)
    test_code = '''
```python
def launch_to_orbit():
    """Launch the vessel to orbit"""
    # Use conn and vessel directly from execution context
    vessel = conn.space_center.active_vessel
    
    # Set throttle to full
    vessel.control.throttle = 1.0
    
    # Enable SAS
    vessel.control.sas = True
    vessel.control.sas_mode = conn.space_center.SASMode.stability_assist
    
    print("Launching to orbit...")
    return True
```
'''
    
    # Create FlightAgent instance
    flight_agent = FlightAgent()
    
    # Test parsing
    mock_message = AIMessage(content=test_code)
    result = flight_agent.process_ai_message(mock_message)
    
    print(f"✅ Parsing result: {type(result)}")
    if isinstance(result, dict):
        print(f"✅ Program name: {result['program_name']}")
        print(f"✅ Exec code: {result['exec_code']}")
        print(f"✅ Program code length: {len(result['program_code'])} chars")
        print("\n📝 Generated code:")
        print(result['program_code'])
        print(f"\n🚀 Execution code: {result['exec_code']}")
    else:
        print(f"❌ Parsing failed: {result}")

if __name__ == "__main__":
    test_parsing()
