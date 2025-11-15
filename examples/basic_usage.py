#!/usr/bin/env python3
"""
KOSMOS Basic Usage Example
Similar to Voyager's interface, showing how to use KOSMOS for different scenarios.
"""

import os
from kosmos import Kosmos


def basic_mission():
    """Basic mission execution - similar to Voyager's voyager.learn()"""
    print("🚀 Starting basic KOSMOS mission...")
    
    # Initialize KOSMOS (similar to Voyager initialization)
    kosmos = Kosmos(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        checkpoint_dir="checkpoint",
        max_iterations=160,
    )
    
    # Connect to KSP and start mission
    events, info = kosmos.env.reset()
    print(f"✅ Connected to vessel: {info.get('vessel_name', 'Unknown')}")
    
    # Start the mission (equivalent to voyager.learn())
    # TODO: Implement main mission loop
    print("Mission execution not yet implemented")
    
    # Cleanup
    kosmos.env.close()


def resume_mission():
    """Resume from checkpoint - similar to Voyager's resume functionality"""
    print("🔄 Resuming KOSMOS mission from checkpoint...")
    
    kosmos = Kosmos(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        checkpoint_dir="checkpoint",
        resume=True,  # Resume from checkpoint
    )
    
    # Continue mission from where we left off
    events, info = kosmos.env.reset()
    print(f"✅ Resumed mission with vessel: {info.get('vessel_name', 'Unknown')}")
    
    # TODO: Implement resume logic
    print("Resume functionality not yet implemented")
    
    kosmos.env.close()


def specific_task(task_name):
    """Execute specific task - similar to Voyager's task decomposition"""
    print(f"🎯 Executing specific task: {task_name}")
    
    kosmos = Kosmos(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        checkpoint_dir="checkpoint",
        # TODO: Add skill_library_dir parameter when implemented
    )
    
    # Connect to KSP
    events, info = kosmos.env.reset()
    print(f"✅ Connected to vessel: {info.get('vessel_name', 'Unknown')}")
    
    # TODO: Implement task decomposition and execution
    # Similar to:
    # sub_goals = kosmos.decompose_task(task=task_name)
    # kosmos.execute_task(sub_goals=sub_goals)
    
    print(f"Task '{task_name}' execution not yet implemented")
    
    kosmos.env.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python basic_usage.py basic          # Run basic mission")
        print("  python basic_usage.py resume         # Resume from checkpoint")
        print("  python basic_usage.py task 'launch'  # Execute specific task")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "basic":
        basic_mission()
    elif command == "resume":
        resume_mission()
    elif command == "task":
        if len(sys.argv) < 3:
            print("Please specify a task name")
            sys.exit(1)
        task_name = sys.argv[2]
        specific_task(task_name)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
