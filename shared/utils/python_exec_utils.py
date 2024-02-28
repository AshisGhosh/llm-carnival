import asyncio

# Utility function to extract python code
def extract_python_code(response):
    start_delimiter = "```python\n" 
    end_delimiter = "\n```"
    code_start_index = response.find(start_delimiter) + len(start_delimiter)
    code_end_index = response.find(end_delimiter, code_start_index)
    python_code = response[code_start_index:code_end_index].strip()
    return python_code

def extract_retry(var_name, max_attempts=3, conditions_to_retry=(SyntaxError, NameError, ValueError)):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                if attempts > 0:
                    print(f"Attempt {attempts + 1} to convert to list")
                try:
                    result = await func(*args, **kwargs)
                    if not result:
                        raise ValueError("No response from LLM")
                    
                    python_code = extract_python_code(result)
                    print("Python code:")
                    print(python_code)
                    print("---" * 10)
                    exec_globals = {}
                    exec(python_code, exec_globals)
                    # Access the variable using var_name from exec_globals
                    var = exec_globals.get(var_name, None)
                    if var is None:
                        raise ValueError(f"Variable '{var_name}' not found")
                    print(f"Variable '{var_name}': {var}.")
                    return var
                except conditions_to_retry as e:
                    attempts += 1
                    print(f"Error parsing: {e}, retrying...")
                    continue
            return None
        return wrapper
    return decorator