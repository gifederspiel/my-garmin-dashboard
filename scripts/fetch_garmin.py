import os, json, base64
from pathlib import Path
import garth
from garminconnect import Garmin

def write_from_env(env_name, path):
    b64 = os.environ.get(env_name)
    if not b64:
        return False
    data = json.loads(base64.b64decode(b64).decode())
    path.write_text(json.dumps(data))
    return True

def get_client():
    tmp = Path("/tmp/garth_session")
    tmp.mkdir(parents=True, exist_ok=True)

    # oauth1 + garth_session use the same data
    wrote1 = write_from_env("GARMIN_OAUTH1_B64", tmp / "oauth1_token.json")
    wrote2 = write_from_env("GARMIN_OAUTH2_B64", tmp / "oauth2_token.json")
    if wrote1:
        (tmp / "garth_session.json").write_text((tmp / "oauth1_token.json").read_text())

    if wrote1 or wrote2:
        garth.client.load(str(tmp))
        return Garmin()

    user, pw = os.getenv("GARMIN_USERNAME"), os.getenv("GARMIN_PASSWORD")
    if user and pw:
        g = Garmin(user, pw)
        g.login()
        return g

    raise RuntimeError("No tokens or credentials")

def main():
    client = get_client()
    acts = client.get_activities(0, 5)
    for a in acts:
        print(f"{a['startTimeLocal']} - {a['activityName']} - {a.get('distance', 0)}m")

if __name__ == "__main__":
    main()
