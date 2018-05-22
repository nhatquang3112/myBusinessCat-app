import scipy as sp
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import uuid
from datetime import datetime
cred = credentials.Certificate("app/task-based-app-firebase-adminsdk-xbkwi-45e8c764a2.json")
firebase_admin.initialize_app(cred)
from random import randint

def get_game(userid):
    db = firestore.client()
    try:
        user = auth.get_user(userid)
        username = user.email
        w_games = db.collection(u'waiting_games').where("status", "==", "waiting").limit(1).get()
        w_games_to_list = []
        for g in w_games:
            w_games_to_list.append(g)
        waiting_game = w_games_to_list[randint(0, len(w_games_to_list) - 1)].to_dict()
        gameid = w_games_to_list[randint(0, len(w_games_to_list) - 1)].id

        num_players = int(waiting_game[u'num_players'])
        assigned_players = waiting_game[u'assigned_players']
        thresholds, values, weights = waiting_game[u'thresholds'], waiting_game[u'values'], waiting_game[u'weights']
        if assigned_players == []:
            status = u'waiting'
            timestamp = str((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
            data = {u'status' : status, u'thresholds' : thresholds, u'values': values,u'weights': weights, u'timeStart' : timestamp}
            db.collection(u'games').document(gameid).set(data)
        # game = db.collection(u'games').document(gameid).get().to_dict()
        # weights = game[u'weights']
        if userid in assigned_players:
            return gameid, weights[assigned_players.index(userid)]
        rank = len(assigned_players)
        weight = weights[rank]
        assigned_players.append(userid)
        nickname = ""
        if rank == 0: nickname = "Red Cat"
        if rank == 1: nickname = "Blue Cat"
        if rank == 2: nickname = "Green Cat"
        if rank == 3: nickname = "Yellow Cat"
        if rank == 4: nickname = "Brown Cat"
        userdata = {u'name': username, u'score' : 0, u'stamina' : weight, u'status' : 'inPlay', u'uid' : userid, u'nickname' : nickname}
        db.collection(u'games').document(gameid).collection(u'users').document(userid).set(userdata)
        if len(assigned_players) == num_players:
            db.collection(u'waiting_games').document(gameid).update({u'status' : u'played', u'assigned_players' : assigned_players})
            timestamp = str((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
            db.collection(u'games').document(gameid).update({u'status' : u'active', u'timeStart' : timestamp})
        else:
            db.collection(u'waiting_games').document(gameid).update({u'assigned_players' : assigned_players})
        return gameid, weight
    except Exception:
        return "error", -1
