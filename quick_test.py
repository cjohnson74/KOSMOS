#!/usr/bin/env python3
"""
Quick test to see what KOSMOS is doing
"""

import sys
sys.path.insert(0, '/Users/carsonjohnson/Documents/KOSMOS')

from kosmos import Kosmos

def quick_test():
    print("🧪 Quick KOSMOS Test")
    print("=" * 30)
    
    try:
        # Initialize KOSMOS
        print("🔍 Initializing KOSMOS...")
        kosmos = Kosmos()
        print("✅ KOSMOS initialized")
        
        # Test one step
        print("🔍 Testing one step...")
        messages, reward, done, info = kosmos.step()
        
        print(f"✅ Step completed!")
        print(f"📊 Reward: {reward}")
        print(f"📊 Done: {done}")
        print(f"📊 Info: {info}")
        print(f"📊 Messages: {len(messages)} messages")
        
        # Show the last message if it's from AI
        if messages and len(messages) > 1:
            last_message = messages[-1]
            print(f"📝 Last message type: {type(last_message).__name__}")
            if hasattr(last_message, 'content'):
                print(f"📝 Last message preview: {str(last_message.content)[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    quick_test()
