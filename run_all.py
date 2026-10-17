import subprocess, sys, time, os

print("Starting all 3 tasks...")

base = os.path.dirname(os.path.abspath(__file__))

p1 = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--port", "8000"], cwd=os.path.join(base, "knowledge_brain"))
p2 = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--port", "8001"], cwd=os.path.join(base, "inbox_agent"))
p3 = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--port", "8002"], cwd=os.path.join(base, "meeting_to_scope"))

print("ALL RUNNING:")
print("8000 - http://127.0.0.1:8000/docs")
print("8001 - http://127.0.0.1:8001/docs")
print("8002 - http://127.0.0.1:8002/docs")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    p1.terminate()
    p2.terminate()
    p3.terminate()