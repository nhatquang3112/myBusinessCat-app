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
def toBinList(C, n):
    res = [0] * n
    a = C
    for i in range(n):
        res[n-1-i] = 1 & a
        a = a >> 1
    return res
def generateTTG(n, k, max_weight, max_quota, max_value, mode='random'):
    weights = [randint(1, max_weight) for i in range(n)]
    thresholds = [randint(1, max_quota) for i in range(k)]
    thresholds = sorted(thresholds)
    if mode == 'non_empty_core':
        values = [max_value] * k
        payoff = [randint(0, max_value - 1) for i in range(n)]
        payoff = sorted(payoff)
        for j in range(k-1,-1,-1):
            for C in range(2**n):
                coeffs = toBinList(C, n)
                W = sum([weights[i] * coeffs[i] for i in range(n)])
                X = sum([payoff[i] * coeffs[i] for i in range(n)])
                if W >= thresholds[j]:
                    values[j] = min(values[j], X)
            if j < k - 1 and values[j] >= values[j + 1]:
                values[j] = values[j + 1] - 1
    if mode == 'empty_core': # not sure
        values = [max_value] * k
        random_noise = [0] * k
        payoff = [randint(0, max_value - 1) for i in range(n)]
        payoff = sorted(payoff)
        for j in range(k-1,-1,-1):
            for C in range(2**n):
                coeffs = toBinList(C, n)
                W = sum([weights[i] * coeffs[i] for i in range(n)])
                X = sum([payoff[i] * coeffs[i] for i in range(n)])
                if W >= thresholds[j]:
                    values[j] = min(values[j], X)
            if j < k - 1 and values[j] >= values[j + 1]:
                values[j] = values[j + 1] - 1
        a = max_value - values[-1]
        for j in range(k):
            random_noise[j] = randint(0,a)
        random_noise = sorted(random_noise)
        for j in range(k):
            values[j] += random_noise[j]
    else: # default to random
        values = [randint(0, max_value) for i in range(k)]
        values = sorted(values)
    return thresholds, values, weights
def create_game():
    n = randint(3,5)
    k = randint(3,5)
    max_quota = 50
    max_value = 25
    max_weight = 40
    return generateTTG(n, k, max_weight, max_quota, max_value)
    # to change
def get_game(userid):
    db = firestore.client()
    try:
        user = auth.get_user(userid)
        username = user.email
        waiting_game = db.collection(u'games').document(u'waiting_game').get().to_dict()
        if waiting_game == {}:
            gameid = str(uuid.uuid4())
            thresholds, values, weights = create_game()
            num_players = len(weights)
            status = u'waiting'
            timestamp = str((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
            data = {u'status' : status, u'thresholds' : thresholds, u'values': values,u'weights': weights, u'timeStart' : timestamp}
            db.collection(u'games').document(gameid).set(data)
            userdata = {u'name': username, u'score' : 0, u'stamina' : weights[0], u'status' : 'inPlay', u'uid' : userid, u'nickname' : "Red Cat"}
            db.collection(u'games').document(gameid).collection(u'users').document(userid).set(userdata)
            assigned_players = [userid]
            w_game = {u'id' : gameid, u'num_players': num_players, u'assigned_players' : assigned_players}
            db.collection(u'games').document(u'waiting_game').set(w_game)
            return gameid, weights[0]
        else:
            gameid = waiting_game[u'id']
            num_players = int(waiting_game[u'num_players'])
            assigned_players = waiting_game["assigned_players"]
            game = db.collection(u'games').document(gameid).get().to_dict()
            weights = game[u'weights']
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
                data = {u'id' : firestore.DELETE_FIELD,
                u'num_players': firestore.DELETE_FIELD,
                u'assigned_players' : firestore.DELETE_FIELD}
                db.collection(u'games').document(u'waiting_game').update(data)
                timestamp = str((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
                db.collection(u'games').document(gameid).update({u'status' : u'active', u'timeStart' : timestamp})
            else:
                db.collection(u'games').document(u'waiting_game').update({u'assigned_players' : assigned_players})
            return gameid, weight
    except Exception:
        return "error", -1
