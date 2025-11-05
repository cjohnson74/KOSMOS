import importlib.util
import os
import kosmos.utils as U

def load_prompt(prompt_name):
    # Use __file__ to get the actual prompts directory location
    # This ensures we use the correct prompts directory even if Python
    # finds the package from a different location
    current_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(current_dir, f"{prompt_name}.txt")
    
    if os.path.exists(prompt_path):
        return U.load_text(prompt_path)
    
    # Fallback to package path (for installed packages)
    package_path = importlib.util.find_spec("kosmos").submodule_search_locations[0]
    return U.load_text(f"{package_path}/prompts/{prompt_name}.txt")