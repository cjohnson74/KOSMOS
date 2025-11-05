import importlib.util
import os
import kosmos.utils as U

def load_control_primitives(primitive_names=None):
    package_path = importlib.util.find_spec("kosmos").submodule_search_locations[0]
    if primitive_names is None:
        primitive_names = [
            primitive[:-3]
            for primitive in os.listdir(f"{package_path}/control_primitives")
            if primitive.endswith(".py") and primitive != "__init__.py"
        ]
    primitives = [
        U.load_text(f"{package_path}/control_primitives/{primitive_name}.py")
        for primitive_name in primitive_names
    ]
    return primitives