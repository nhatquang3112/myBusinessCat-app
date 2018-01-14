import scipy as sp
import numpy as np
import pyrebase as pb
import uuid
config = {
    "apiKey": "AIzaSyBP7lkvIuVG7o68osnPeq8zsewStu9Z8oI",
    "authDomain": "task-based-app.firebaseapp.com",
    "databaseURL": "https://task-based-app.firebaseio.com",
    "projectId": "task-based-app",
    "storageBucket": "task-based-app.appspot.com",
    "messagingSenderId": "52274371488"
  }

firebase = pb.initialize_app(config)

def create_game():
    thresholds = {0: 20, 1: 25, 2: 30}
    weights = {0: 15, 1: 16, 2: 17, 3: 18, 4: 19}
    return thresholds, weights
    # to change
def get_game(userid):
    db = firebase.database()
    waiting_game = db.child("games").child("waiting_game").get().val()
    if waiting_game == "":
        gameid = str(uuid.uuid4())
        thresholds, weights = create_game()
        status = "waiting"
        data = {"status" : status, "thresholds" : thresholds, "weights": weights}
        db.child("games").child(gameid).set(data)
        assigned_players = {0 : userid, 1 : False, 2 : False, 3 : False, 4 : False}
        w_game = {"id" : gameid, "num_players": 5, "assigned_players" : assigned_players}
        db.child("games").child("waiting_game").set(w_game)
        return gameid, 0
    else:
        gameid = waiting_game["id"]
        num_players = int(waiting_game["num_players"])
        all_assigned = True
        player = -1
        for i in range(num_players):
            if waiting_game["assigned_players"][i] == userid:
                return gameid, i
                
        for i in range(num_players):
            if waiting_game["assigned_players"][i] == False:
                player = i
                break

        for i in range(player + 1, num_players):
            if waiting_game["assigned_players"][i] == False:
                all_assigned = False
                break
        db.child("games").child("waiting_game").child("assigned_players").child(player).set(userid)
        if all_assigned:
            db.child("games").child("waiting_game").set("")
        return gameid, player
