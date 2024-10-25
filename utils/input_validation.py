class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def input_with_validation(prompt, validation_func, error_message):
    """Solicita una entrada del usuario con validación."""
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        else:
            print(f"{Colors.RED}{error_message}{Colors.RESET}")