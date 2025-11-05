#!/usr/bin/env python3
"""
KOSMOS - AI Agents controlling Kerbal Space Program
Main entry point for the system.
"""

import os
import sys
import argparse

# Ensure we use the local kosmos package from this directory
# This prevents Python from importing from other locations (like Desktop)
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from kosmos import Kosmos

def main():
    parser = argparse.ArgumentParser(description='KOSMOS - Kerbal Space Program AI Agent System')
    parser.add_argument('mission', nargs='?', default='', 
                       help='Mission overview to execute (e.g., "Asteroid Redirect Mission: Orbital Rendezvous")')
    
    args = parser.parse_args()
    
    # Initialize KOSMOS with API key from environment
    openai_api_key = os.getenv("OPENAI")
    anthropic_api_key = os.getenv("ANTHROPIC")

    if not openai_api_key:
        print("❌ Error: OpenAI API key required.")
        print("Please set the OPENAI_API_KEY environment variable in your .env file")
        sys.exit(1)

    if not anthropic_api_key:
        print("❌ Error: Anthropic API key required.")
        print("Please set the ANTHROPIC_API_KEY environment variable in your .env file")
        sys.exit(1)

    # Get mission overview
    mission_overview = args.mission
    
    if not mission_overview:
        if args.interactive:
            mission_overview = input("🎯 Enter mission overview: ").strip()
        else:
            print("❌ Error: Mission overview required.")
            print("Usage: python main.py 'Mission Description'")
            print("   or: python main.py --interactive")
            print("   or: python main.py --help")
            sys.exit(1)
    
    if not mission_overview:
        print("❌ Error: No mission overview provided.")
        sys.exit(1)

    print("🚀 KOSMOS - AI Agents for Kerbal Space Program")
    print("=" * 50)
    print(f"🎯 Mission: {mission_overview}")
    print("=" * 60)

    kosmos = Kosmos(
        openai_api_key=openai_api_key,
        anthropic_api_key=anthropic_api_key,
        checkpoint_dir="checkpoint",
        max_iterations=160,
        initial_mission=mission_overview,
        resume=False,
    )

    print("✅ KOSMOS initialized successfully!")
    print("🎯 Starting mission execution...")

    # Execute the mission
    kosmos.learn()

if __name__ == "__main__":
    main()