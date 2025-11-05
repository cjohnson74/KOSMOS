import json
import re
from typing import Any, Dict, Union
from .file_utils import f_join


def json_load(*file_path, **kwargs):
    file_path = f_join(file_path)
    try:
        with open(file_path, "r") as fp:
            return json.load(fp, **kwargs)
    except FileNotFoundError:
        # Return empty dict for missing files (common case for checkpoints)
        return {}


def json_loads(string, **kwargs):
    return json.loads(string, **kwargs)


def json_dump(data, *file_path, **kwargs):
    file_path = f_join(file_path)
    with open(file_path, "w") as fp:
        json.dump(data, fp, **kwargs)


def json_dumps(data, **kwargs):
    """
    Returns: string
    """
    return json.dumps(data, **kwargs)


# ---------------- Aliases -----------------
# add aliases where verb goes first, json_load -> load_json
load_json = json_load
loads_json = json_loads
dump_json = json_dump
dumps_json = json_dumps


def extract_char_position(error_message: str) -> int:
    """Extract the character position from the JSONDecodeError message.
    Args:
        error_message (str): The error message from the JSONDecodeError
          exception.
    Returns:
        int: The character position.
    """
    import re

    char_pattern = re.compile(r"\(char (\d+)\)")
    if match := char_pattern.search(error_message):
        return int(match[1])
    else:
        raise ValueError("Character position not found in the error message.")


def add_quotes_to_property_names(json_string: str) -> str:
    """
    Add quotes to property names in a JSON string.
    Args:
        json_string (str): The JSON string.
    Returns:
        str: The JSON string with quotes added to property names.
    """

    def replace_func(match):
        return f'"{match.group(1)}":'

    property_name_pattern = re.compile(r"(\w+):")
    corrected_json_string = property_name_pattern.sub(replace_func, json_string)

    try:
        json.loads(corrected_json_string)
        return corrected_json_string
    except json.JSONDecodeError as e:
        raise e


def balance_braces(json_string: str) -> str:
    """
    Balance the braces in a JSON string.
    Args:
        json_string (str): The JSON string.
    Returns:
        str: The JSON string with braces balanced.
    """

    open_braces_count = json_string.count("{")
    close_braces_count = json_string.count("}")

    while open_braces_count > close_braces_count:
        json_string += "}"
        close_braces_count += 1

    while close_braces_count > open_braces_count:
        json_string = json_string.rstrip("}")
        close_braces_count -= 1

    try:
        json.loads(json_string)
        return json_string
    except json.JSONDecodeError as e:
        raise e


def fix_invalid_escape(json_str: str, error_message: str) -> str:
    while error_message.startswith("Invalid \\escape"):
        bad_escape_location = extract_char_position(error_message)
        json_str = json_str[:bad_escape_location] + json_str[bad_escape_location + 1 :]
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError as e:
            error_message = str(e)
    return json_str


def correct_json(json_str: str) -> str:
    """
    Correct common JSON errors.
    Args:
        json_str (str): The JSON string.
    """

    try:
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError as e:
        error_message = str(e)
        if error_message.startswith("Invalid \\escape"):
            json_str = fix_invalid_escape(json_str, error_message)
        if error_message.startswith(
            "Expecting property name enclosed in double quotes"
        ):
            json_str = add_quotes_to_property_names(json_str)
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError as e:
                error_message = str(e)
        if balanced_str := balance_braces(json_str):
            return balanced_str
    return json_str


def fix_and_parse_json(
    json_str: str, try_to_fix_with_gpt: bool = True
) -> Union[str, Dict[Any, Any]]:
    """Fix and parse JSON string"""
    import re
    
    # Handle None or empty string
    if not json_str or json_str.strip() == "":
        raise json.JSONDecodeError("Empty or None JSON string", "", 0)
    
    # First, try to extract JSON from markdown code blocks
    # Handle both JSON objects {...} and arrays [...], with various language tags
    json_patterns = [
        # JSON objects in code blocks (with various language tags or no tag) - use greedy matching
        re.compile(r"```(?:json|python|py)?\s*(\{.*\})\s*```", re.DOTALL),
        # JSON arrays in code blocks (with various language tags or no tag) - use greedy matching  
        re.compile(r"```(?:json|python|py)?\s*(\[.*\])\s*```", re.DOTALL),
        # Try without any language tag specification - greedy matching
        re.compile(r"```\s*(\{.*\})\s*```", re.DOTALL),
        re.compile(r"```\s*(\[.*\])\s*```", re.DOTALL),
        # Fallback: non-greedy matching for edge cases
        re.compile(r"```(?:json|python|py)?\s*(\{.*?\})\s*```", re.DOTALL),
        re.compile(r"```(?:json|python|py)?\s*(\[.*?\])\s*```", re.DOTALL),
    ]
    
    for pattern in json_patterns:
        match = pattern.search(json_str)
        if match:
            extracted = match.group(1)
            print(f"DEBUG: Extracted JSON from code block: {extracted[:200]}...")
            json_str = extracted
            break
    
    # Clean up whitespace and normalize
    json_str = json_str.strip()
    
    # Remove any leading/trailing whitespace from each line (common LLM formatting issue)
    lines = json_str.split('\n')
    json_str_cleaned = '\n'.join(line.strip() for line in lines)
    
    # Try direct parsing first
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"DEBUG: Initial JSON parse failed: {e}")
    
    # Try with cleaned version
    try:
        return json.loads(json_str_cleaned)
    except json.JSONDecodeError:
        pass
    
    # Remove tabs but preserve newlines in strings
    json_str_no_tabs = json_str.replace("\t", "    ")
    try:
        return json.loads(json_str_no_tabs)
    except json.JSONDecodeError:
        pass
    
    # Try fixing common JSON errors
    try:
        json_str_fixed = correct_json(json_str)
        return json.loads(json_str_fixed)
    except json.JSONDecodeError as e:
        print(f"DEBUG: Corrected JSON parse failed: {e}")
    
    # Check if JSON is missing opening/closing braces
    # Sometimes LLMs return just the fields without the enclosing {}
    if "{" not in json_str:
        print(f"DEBUG: No opening brace found, attempting to add braces")
        # Try wrapping in braces
        try:
            wrapped = "{" + json_str.strip() + "}"
            return json.loads(wrapped)
        except json.JSONDecodeError:
            pass
    
    # Check if JSON is missing closing brace
    if "{" in json_str and "}" not in json_str:
        print(f"DEBUG: No closing brace found, attempting to add closing brace")
        try:
            fixed = json_str.strip() + "}"
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass
    
    # Manual extraction: find JSON objects {...} or arrays [...]
    # This handles cases where there's text before/after the JSON
    def extract_json_structure(json_str, start_char, end_char):
        try:
            # Find first opening character
            start_pos = json_str.index(start_char)
            # Count characters to find the matching closing character
            char_count = 0
            end_pos = -1
            in_string = False
            escape_next = False
            
            for i in range(start_pos, len(json_str)):
                char = json_str[i]
                
                # Handle string content (don't count brackets/braces inside strings)
                if escape_next:
                    escape_next = False
                    continue
                if char == '\\':
                    escape_next = True
                    continue
                if char == '"':
                    in_string = not in_string
                    continue
                
                # Count brackets/braces only outside strings
                if not in_string:
                    if char == start_char:
                        char_count += 1
                    elif char == end_char:
                        char_count -= 1
                        if char_count == 0:
                            end_pos = i
                            break
            
            if end_pos > start_pos:
                extracted_json = json_str[start_pos:end_pos + 1]
                print(f"DEBUG: Extracted {start_char}...{end_char} from position {start_pos} to {end_pos}")
                return extracted_json
        except ValueError:
            return None
        return None
    
    # Try extracting JSON object first
    extracted = extract_json_structure(json_str, '{', '}')
    if extracted:
        try:
            return json.loads(extracted)
        except json.JSONDecodeError:
            try:
                # Try fixing the extracted JSON
                fixed = correct_json(extracted)
                return json.loads(fixed)
            except json.JSONDecodeError as e:
                print(f"DEBUG: Object extraction and fix failed: {e}")
    
    # Try extracting JSON array
    extracted = extract_json_structure(json_str, '[', ']')
    if extracted:
        try:
            return json.loads(extracted)
        except json.JSONDecodeError:
            try:
                # Try fixing the extracted JSON
                fixed = correct_json(extracted)
                return json.loads(fixed)
            except json.JSONDecodeError as e:
                print(f"DEBUG: Array extraction and fix failed: {e}")
    
    # If all else fails, raise an error with useful debugging info
    preview = json_str[:500] if len(json_str) > 500 else json_str
    raise json.JSONDecodeError(
        f"Failed to parse JSON after all attempts. Preview: {repr(preview)}",
        json_str,
        0
    )