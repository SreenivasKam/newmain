import requests
key='752968603b6f1160bb64e70452cfd697'
api_secret='b24df5f3ef3d961c62babea14d79feda8cffd2203348f47b64fd4098574c7240'
token='6e9bc42c63c670cde41c2bf21156c59193166d9d179c13ea6a8ae5e5b99f7273'
id = '628376b9556c9821fcef6cac'
list_id ="62838ddecf433a07fbd3927a"

def create_board(board_name):
    url = "https://api.trello.com/1/boards/"
    querystring = {"name": board_name, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id
def create_list(list_name):
    url = f"https://api.trello.com/1/boards/{id}/lists"
    querystring = {"name": list_name, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    list_id = response.json()["id"]
    return list_id
def create_card(card_name):
    url = f"https://api.trello.com/1/cards"
    querystring = {"name": card_name, "idList": list_id, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    card_id = response.json()["id"]
    return card_id