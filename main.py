# TODO: Ensure all other modes work
# TODO: Add a "fast" mode that removes the api call for mapper, also maybe the beatmap
# TODO: Get leaderboard ranking of score through get_user_beatmap_score()
# TODO: Look at threading/something else to be able to run concurrent maps
#note: potential issue could be rate limit

import os
import osu
import csv
import time
import json
from dotenv import load_dotenv

score_dictionary = {}
available_modes = ["osu", "taiko", "fruits", "mania"]

load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_url = os.getenv('redirect_url')

with open("settings.json", "r") as f:
    settings = json.load(f)

def calculate_time(length):
    rounded_length = round(length)
    minutes = rounded_length // 60
    if rounded_length < 60:
        if rounded_length < 10:
            return f"0:0{rounded_length}"
        return f"0:{rounded_length}"
    else:
        seconds = rounded_length - (minutes * 60)
        if seconds < 10:
            return f"{minutes}:0{seconds}"
        return f"{minutes}:{seconds}"

def return_mods(mods):
    string = ""
    for x in mods:
        string += x.mod.value
    
    return string

client = osu.Client.from_client_credentials(client_id, client_secret, redirect_url)

user_id = settings["user_id"]
mode = settings["mode"]

if mode not in available_modes:
    print("This mode is not valid.")
    exit()
elif mode == "":
    mode = "osu"

try:
    user = client.get_user(user_id)
    print(f"Getting {user.username}'s top plays")
except:
    print("This user doesn't exist")
    exit()


scores = client.get_user_scores(user_id, "best", mode=mode, limit=100)

start_time = time.time()

for i, x in enumerate(range(0, int(settings["limit"]))):
    print(f"Getting top play: {x+1}")

    try:
        score = scores[x]
    except:
        break

    beatmap = client.get_beatmap(score.beatmap_id)
    try:
        mapper = client.get_user(beatmap.user_id)
    except:
        mapper = None

    dict = {
        "score_number": x+1,
        "user_id": user_id,
        "user_country_code": user.country_code,
        "beatmap_id": score.beatmap_id,
        "beatmapset_id": beatmap.beatmapset_id,
        "last_updated": beatmap.beatmapset.last_updated.strftime("%Y-%m-%d %H:%M:%S"),
        "ranked_date": beatmap.beatmapset.ranked_date.strftime("%Y-%m-%d %H:%M:%S"),
        "artist": beatmap.beatmapset.artist,
        "title": beatmap.beatmapset.title,
        "difficulty": beatmap.version,
        "bpm": beatmap.bpm,
        "od": beatmap.accuracy,
        "ar": beatmap.ar,
        "cs": beatmap.cs,
        "hp": beatmap.drain,
        "length": calculate_time(beatmap.total_length),
        "drain_length": calculate_time(beatmap.hit_length),
        "beatmap_mode": beatmap.mode.value,
        "mapper": mapper.username if mapper != None else "Restricted",
        "mapper_user_id": mapper.id if mapper != None else "Restricted",
        "mapper_country_code": mapper.country_code if mapper != None else "Restricted",
        "score_id": score.id,
        "time": score.ended_at.strftime("%Y-%m-%d %H:%M:%S"),
        "score": score.total_score,
        "max_combo": score.max_combo,
        "rank": score.rank.value,
        "count_50": score.statistics.meh if score.statistics.meh else "0",
        "count_100": score.statistics.ok if score.statistics.ok else "0",
        "count_300": score.statistics.great if score.statistics.great else "0",
        "count_miss": score.statistics.miss if score.statistics.miss else "0",
        "accuracy": score.accuracy,
        "mods": return_mods(score.mods) if score.mods else "None",
        "pp": score.pp,
        "replay": score.replay
    }
    score_dictionary[x+1] = dict

end_time = time.time()
print(f"The script took {end_time - start_time} seconds to run")

if settings["output"] == "csv":
    with open(f"{user_id}_top_plays.csv", mode="w") as csv_file:
        fieldnames = list(score_dictionary[1].keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for x in score_dictionary:
            writer.writerow(score_dictionary[x])
elif settings["output"] == "json":
    with open(f"{user_id}_top_plays.json", "w") as json_file:
        f = json.dumps(score_dictionary)
        json_file.write(f)
else:
    print("Output setting invalid, defaulting to csv.")
    with open(f"{user_id}_top_plays.csv", mode="w") as csv_file:
        fieldnames = list(score_dictionary[1].keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for x in score_dictionary:
            writer.writerow(score_dictionary[x])
