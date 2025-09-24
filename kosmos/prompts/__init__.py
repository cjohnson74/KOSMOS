import importlib.util
import os
import kosmos.utils as U

def load_prompt(prompt_name):
    package_path = importlib.util.find_spec("kosmos").submodule_search_locations[0]
    return U.load_text(f"{package_path}/prompts/{prompt_name}.txt")