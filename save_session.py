import json
import garth
from pathlib import Path

email = input("Garmin email: ")
password = input("Garmin password: ")

# log in
garth.login(email, password)

# dump session to a temp folder
out_dir = Path("session_tmp")
out_dir.mkdir(exist_ok=True)
garth.client.dump(str(out_dir))

# read the dumped file (should be sessions.json)
session_file = next(out_dir.glob("*.json"))
data = json.loads(session_file.read_text())

# save our own clean JSON file
with open("garth_session.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Session saved to garth_session.json")
