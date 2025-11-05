# scripts/fetch_garmin.py
import os
import json
import base64
from pathlib import Path

import garth
from garminconnect import Garmin


def write_from_b64(env_name: str, target: Path) -> bool:
    b64 = os.environ.get(env_name)
    if not b64:
        return False
    data = json.loads(base64.b64decode(b64).decode())
    target.write_text(json.dumps(data))
    return True


def get_client():
    session_dir = Path("/tmp/garth_session")
    session_dir.mkdir(parents=True, exist_ok=True)

    has_oauth1 = write_from_b64("GARMIN_OAUTH1_B64", session_dir / "oauth1_token.json")
    has_oauth2 = write_from_b64("GARMIN_OAUTH2_B64", session_dir / "oauth2_token.json")

    # your local dump also had garth_session.json, and it was the same as oauth1
    if has_oauth1:
        (session_dir / "garth_session.json").write_text(
            (session_dir / "oauth1_token.json").read_text()
        )

    if has_oauth1 or has_oauth2:
        garth.resume(str(session_dir))
        return Garmin()

    # fallback (may still fail on GH IPs, but we try)
    user = os.getenv("GARMIN_USERNAME")
    pw = os.getenv("GARMIN_PASSWORD")
    if user and pw:
        g = Garmin(user, pw)
        g.login()
        return g

    raise RuntimeError("no tokens and no credentials available")


def main():
    client = get_client()
    activities = client.get_activities(0, 5)
    for a in activities:
        print(f"{a['startTimeLocal']} - {a['activityName']} - {a.get('distance', 0)}m")


if __name__ == "__main__":
    main()
