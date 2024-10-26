import subprocess

def capture_web_screenshots(urls):
    """Utiliza EyeWitness para capturar pantallas de URLs dadas."""
    eyewitness_command = ["eyewitness", "--web", "--threads", "10", "-f", urls]
    subprocess.run(eyewitness_command)
    print("Capturas de pantalla completadas.")
