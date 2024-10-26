import subprocess

def identify_web_technologies(url):
    """Utiliza WhatWeb para identificar tecnologías web en una URL dada."""
    command = ["whatweb", url]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None
