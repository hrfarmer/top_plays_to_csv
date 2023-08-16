import os
import osu

client_id = input("Enter your client id: ")
client_secret = input("Enter your client secret: ")
redirect_url = "http://127.0.0.1:8080"


print("Testing credentials...")

try:
    client = osu.Client.from_client_credentials(client_id, client_secret, redirect_url)
    user = client.get_user("13473514")
except:
    print("Client information is incorrect, make sure to doublecheck you copied the right values and set the callback url to http://127.0.0.1:8080")
    exit()

print("Client information correct and saved!")

with open(".env", "w") as f:
    f.writelines([f"client_id={client_id}\n", f"client_secret={client_secret}\n", f"redirect_url={redirect_url}"])