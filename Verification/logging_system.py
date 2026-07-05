from datetime import datetime

def log_event(filename, status, reason=""):
    with open("logs/verification.log", "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} | {filename} | {status} | {reason}\n")
