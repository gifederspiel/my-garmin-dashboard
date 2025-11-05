# scripts/fetch_garmin.py
import os
import json
import base64

import garth
from garminconnect import Garmin


def get_client():
    # 1) try session from base64 (best for GitHub Actions)
    session_b64 = os.environ.get("GARMIN_SESSION_B64")
    if session_b64:
        try:
            raw = base64.b64decode(session_b64)
            data = json.loads(raw.decode())
            # load tokens into garth
            garth.client.load_dict(data) if hasattr(garth.client, "load_dict") else garth.client.load(data)
            # create Garmin client that uses current garth session
            return Garmin()
        except Exception as e:
            print("⚠️ Failed to load session from GARMIN_SESSION_B64, will try username/password:", e)

    # 2) fallback to username/password
    username = os.environ.get("GARMIN_USERNAME")
    password = os.environ.get("GARMIN_PASSWORD")
    if username and password:
        g = Garmin(username, password)
        g.login()
        return g

    raise RuntimeError("No valid session and no username/password available")


def main():
    client = get_client()

    # fetch last 5 activities
    activities = client.get_activities(0, 5)
    for a in activities:
        # print something visible in GitHub logs
        print(f"{a['startTimeLocal']} - {a['activityName']} - {a.get('distance', 0)}m")


if __name__ == "__main__":
    main()
