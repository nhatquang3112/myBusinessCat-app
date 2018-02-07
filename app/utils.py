import scipy as sp
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
from datetime import datetime
cred = credentials.Certificate("app/task-based-app-firebase-adminsdk-xbkwi-45e8c764a2.json")
firebase_admin.initialize_app(cred)

def create_game():
    thresholds = [20,25,30]
    weights = [15,16,17,18,19]
    return thresholds, weights
    # to change
def get_game(userid):
    db = firestore.client()
    waiting_game = db.collection(u'games').document(u'waiting_game').get().to_dict()
    if waiting_game == {}:
        gameid = str(uuid.uuid4())
        thresholds, weights = create_game()
        num_players = len(weights)
        status = u'waiting'
        timestamp = str(datetime.now())
        data = {u'status' : status, u'thresholds' : thresholds, u'weights': weights, u'timeStart' : timestamp}
        db.collection(u'games').document(gameid).set(data)
        assigned_players = [userid]
        w_game = {u'id' : gameid, u'num_players': num_players, u'assigned_players' : assigned_players}
        db.collection(u'games').document(u'waiting_game').set(w_game)
        return gameid, 0
    else:
        gameid = waiting_game[u'id']
        num_players = int(waiting_game[u'num_players'])
        assigned_players = waiting_game["assigned_players"]
        if userid in assigned_players:
            return gameid, assigned_players.index(userid)
        rank = len(assigned_players)
        assigned_players.append(userid)
        db.collection(u'games').document(u'waiting_game').update({u'assigned_players' : assigned_players})
        if len(assigned_players) == num_players:
            data = {u'id' : firestore.DELETE_FIELD,
            u'num_players': firestore.DELETE_FIELD,
            u'assigned_players' : firestore.DELETE_FIELD}
            db.collection(u'games').document(u'waiting_game').update(data)
        return gameid, rank
