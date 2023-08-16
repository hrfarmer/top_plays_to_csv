# top_plays_to_csv
Simple python script that generates a csv/json file of an osu! user's top plays

(Note: while you can input other modes, I haven't tested with other modes just yet, but I will ensure they work properly soon)


## To setup:

1. Install python (made this with 3.11.4, idk how earlier you can get away with)
2. Clone the repository
3. Open the directory in a terminal and install dependencies with `pip install -r requirements.txt`
4. Go to your [osu account settings](https://osu.ppy.sh/home/account/edit) and scroll down to OAuth
5. Create a new OAuth application, name it whatever you want, and set the Application Callback URL to `http://127.0.0.1:8080`
6. Run setup.py with `python setup.py` in your terminal and follow the instructions

## To use:
1. Open settings.json and change the settings to your preferences
```json
"limit": "10", // How many plays the script will generate up to, the max is 100
"user_id": "13473514", // Set this to the user id of the user you want to generate for
"mode": "osu", // The mode you want to run the script for, available modes are "osu", "taiko", "fruits", and "mania"
"output": "csv" // The other option for output is "json"
```
2. Run the script with `python main.py`
3. That's it! (As long as nothing breaks) the output will go in the base directory of the project.

If you encounter any issues, make an issue on GitHub and I'll take a look at it.
