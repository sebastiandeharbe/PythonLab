import psutil
import os

pid_actual = os.getpid()

for proc in psutil.process_iter(['pid', 'name']):
    try:
        pid = proc.info['pid']

        # Evitar matar este script y procesos críticos
        if pid != pid_actual and proc.info['name'].lower() not in [
            "explorer.exe", "system", "system idle process"
        ]:
            proc.terminate()

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

print("💀 Todo cerrado. Tu PC acaba de experimentar el apocalipsis controlado.")
