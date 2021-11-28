# Bruno Silva 97931, Francisco Cardita 97640, Pedro Guerra 98610
import asyncio
import getpass
import json
from logging import NullHandler
import os
import websockets
from copy import deepcopy
from pieces import PIECES, I, L, S, T, J, O, Z
 
async def agent_loop(server_address="localhost:8000", agent_name="97931"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        
        piece = None
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                
                # game=[]
                print(state['score'])
                
                if 'piece' in state: # and "game" in state:
                    piece=state['piece']
                    game=state['game']
                
                flag = False
                while(piece == None):
                    state = json.loads(
                        await websocket.recv()
                    )  # receive game update, this must be called timely or your game will get out of sync with the server
                    if 'piece' in state: # and "game" in state:
                        piece=state['piece']
                        game=state['game']
                        type_piece = get_piece(piece)
                    
                    if piece != None:
                        ideal_pos_rot_piece = simulate_all_possibilities(piece,game, type_piece)
                        translate = compare_pieces(rotate(piece, type_piece, ideal_pos_rot_piece[1]), ideal_pos_rot_piece[0])
                        keys = get_keys(translate, ideal_pos_rot_piece[1])
                        flag = True

                if(flag):
                    for key in keys:            
                        state = json.loads(
                            await websocket.recv()
                        )  # receive game update, this must be called timely or your game will get out of sync with the server    
                        await websocket.send(
                            json.dumps({"cmd": "key", "key": key})
                        )  # send key command to server - you must implement this send in the AI agent

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


def get_piece(piece):
    for p in PIECES:
        if piece in p:
            if p == I:
                return 'I'
            elif p == L:
                return 'L'
            elif p == S:
                return 'S'
            elif p == T:
                return 'T'
            elif p == J:
                return 'J'
            elif p == O:
                return 'O'
            elif p == Z:
                return 'Z'

    return 'Not found'

def get_rows(game):
    rows=[[0,0,0,0,0,0,0,0,0] for i in range(30)]

    for p in game:
        rows[p[1]][p[0]] = 1
    
    for i in range(len(rows)):
        del rows[i][0]

    return rows

def rotate(piece, type_piece, numOfrotations):
    #type_piece = get_piece(piece)
    #print(type_piece)
    piece = deepcopy(piece)
    center = [0,0]     
    if type_piece == 'O':
        return piece
    elif type_piece == 'T':
        #center = get_center(piece, type_piece)
        center = piece[1]
        for i in range(numOfrotations):
            for block in piece:
                if block != center:
                    if block[0] == center[0] and block[1] < center[1]:
                        block[0] += 1
                        block[1] += 1
                    elif block[0] > center[0] and block[1] == center[1]:
                        block[0] -= 1
                        block[1] += 1
                    elif block[0] == center[0] and block[1] > center[1]:
                        block[0] -= 1
                        block[1] -= 1
                    elif block[0] < center[0] and block[1] == center[1]:
                        block[0] += 1
                        block[1] -= 1
        return piece
    elif type_piece == 'S':
        #center = get_center(piece, type_piece)
        center = piece[1]
        if numOfrotations % 2 != 0:
            for block in piece:
                if block != center:         # atençao à ordem das peças
                    if block[0] == center[0] and block[1] == center[1] - 1:
                        block[0] -= 1
                        block[1] += 2
                    if block[0] == center[0] + 1 and block[1] == center[1] + 1:
                        block[0] -= 1
        return piece
    elif type_piece == 'Z':
        #center = get_center(piece, type_piece)
        center = piece[2]
        if numOfrotations % 2 != 0:
            for block in piece:
                if block != center:         # atençao à ordem das peças
                    if block[0] == center[0] and block[1] == center[1] - 1:
                        block[0] += 1
                        block[1] += 2
                    if block[0] == center[0] - 1 and block[1] == center[1] + 1:
                        block[0] += 1
        return piece
    elif type_piece == 'L' or type_piece == 'J':
        #center = get_center(piece, type_piece)
        if type_piece == 'L':
            center = piece[1]  
        elif type_piece == 'J':
            center = piece[2]      
        
        for i in range(numOfrotations):
            for block in piece:
                if block != center:
                    if block[0] == center[0] and block[1] < center[1]:
                        block[0] += 1
                        block[1] += 1 
                    elif block[0] > center[0] and block[1] == center[1]:
                        block[0] -= 1 
                        block[1] += 1 
                    elif block[0] == center[0] and block[1] > center[1]:
                        block[0] -= 1
                        block[1] -= 1
                    elif block[0] < center[0] and block[1] == center[1]:
                        block[0] += 1
                        block[1] -= 1
                    else:
                        if block[0] > center[0] and block[1] < center[1]:        # trata se do bloco "cauda", o unico que nao está diretamente conectado ao centro 
                            block[1] += 2
                        elif block[0] > center[0] and block[1] > center[1]:
                            block[0] -= 2
                        elif block[0] < center[0] and block[1] > center[1]:
                            block[1] -= 2
                        elif block[0] < center[0] and block[1] < center[1]:
                            block[0] += 2
        return piece
    elif type_piece == 'I':
        #center = get_center(piece, type_piece)
        center = piece[2]                              
        if numOfrotations % 2 != 0:    
            for block in piece:
                if block != center:
                    if block[0] == center[0] - 2:
                        block[0] += 2
                        block[1] -= 2
                    elif block[0] == center[0] - 1:
                        block[0] += 1
                        block[1] -= 1
                    else:
                        block[0] -= 1
                        block[1] += 1
        return piece
    return piece
    

def get_aggregate_height(game):
    rows = get_rows(game)
    column_height = 0
    aggregate_height = 0
    for x in range(8):
        for y in range(30):
            if rows[29-y][x] == 1:
                column_height = y + 1
        aggregate_height += column_height
    return aggregate_height

def get_columns_height(game):
    rows = get_rows(game)
    heightPerColumn=[0,0,0,0,0,0,0,0]
    column_height = 0
    for x in range(8):
        for y in range(30):
            if rows[29-y][x] == 1:
                column_height = y + 1
            heightPerColumn[x] = column_height
    return heightPerColumn

def get_bumpiness(game):
    columns_heigths = get_columns_height(game)
    total_bumpiness = 0
    for i in range(7):
        total_bumpiness += abs(columns_heigths[i] - columns_heigths[i+1])
    
    return total_bumpiness

def get_numberOfHoles(game):
    rows = get_rows(game)
    columns_heigths = get_columns_height(game)
    for x in range(8):
        height = columns_heigths[x]
        for y in range(height, 30):
            rows[29-y][x] = -1
    
    countHoles = 0
    for x in range(8):
        for y in range(30):
            if rows[29-y][x] == 0:
                countHoles += 1
    return countHoles

def complete_lines(game):
    rows = get_rows(game)
    numberOflines = 0
    for r in rows:
        if sum(r) == 8:
            numberOflines += 1
    return numberOflines


def simulate_fall(piece, game):
    sim_game = deepcopy(game)
    piece_clone = deepcopy(piece)
    while piece_clone[0][1] < 29 and piece_clone[1][1] < 29 and piece_clone[2][1] < 29 and piece_clone[3][1] < 29 :
        for block in piece_clone:
            block[1] = block[1] + 1
    
        for block in piece_clone:
            if block in game:
                for block in piece_clone:
                    block[1] = block[1] - 1
                
                sim_game += piece_clone
                return sim_game
    sim_game += piece_clone
    return sim_game 

def simulate_all_possibilities(piece, game, type_piece):
    if piece == None:
        return None
    original_piece_real = piece
    #type_piece = get_piece(piece)
    numbOfrotations=0
    iterations = 1
    original_piece = []
    scores=[]
    total_numberOfpositions=[]
    if type_piece == 'O':
        numbOfrotations = 0
    elif type_piece == 'I' or type_piece == 'S' or type_piece == 'Z':
        numbOfrotations = 1
    else:
        numbOfrotations = 3

    iterations = numbOfrotations + 1
        
    for i in range(iterations):
        if i > 0:
            piece = rotate(original_piece_real, type_piece, i)
        
        x_min = 8
        for block in piece:     #check the minimum x coordenate of the blocks  
            if block[0] < x_min:
                x_min = block[0]
        
        ini_translate = 1 - x_min    
        piece = translate(piece, ini_translate - 1) # put the piece's block on the left on x=0
        original_piece.append(translate(piece,1))
        numberOfpositions = 0
        while piece[0][0] < 8 and piece[1][0] < 8 and piece[2][0] < 8 and piece[3][0] < 8:
            piece = translate(piece, 1)
            game1 = simulate_fall(piece, game)
            total_height = get_aggregate_height(game1)
            completeLines = complete_lines(game1)
            numberOfHoles = get_numberOfHoles(game1)
            bumpiness = get_bumpiness(game1)
            score = calculateHeuristic(total_height, completeLines, numberOfHoles, bumpiness)
            scores.append(score)
            numberOfpositions += 1
        total_numberOfpositions.append(numberOfpositions)

    ind = scores.index(max(scores))
    if ind < total_numberOfpositions[0]:
        piece = translate(original_piece[0], ind)
        return [piece, 0]                       # Retorna a peça e o numero de rotaçoes a executar
    elif ind < total_numberOfpositions[0] + total_numberOfpositions[1]:
        piece = translate(original_piece[1], ind - total_numberOfpositions[0])
        return [piece, 1]
    elif ind < total_numberOfpositions[0] + total_numberOfpositions[1] + total_numberOfpositions[2]:
        piece = translate(original_piece[2], ind - (total_numberOfpositions[0] + total_numberOfpositions[1]))
        return [piece, 2]
    else:
        piece = translate(original_piece[3], ind - (total_numberOfpositions[0] + total_numberOfpositions[1] + total_numberOfpositions[2]))
        return [piece, 3]
    
# The heuristics were based on the information of this site: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/?fbclid=IwAR0ysYYxA2_lOfirvRJ5etTZ6UsEEGKM_c9XfKmimWM9h3hd-NvICGDkTts
def calculateHeuristic(total_height, completeLines, numberOfHoles, bumpiness):
    a = -0.51006
    b = 0.760666
    c = -0.35663
    d = -0.184483
    return total_height*a + completeLines*b + numberOfHoles*c + bumpiness*d

def translate(piece, value):
    return [[block[0] + value, block[1]] for block in piece]

def compare_pieces(original_piece, new_piece):
    if original_piece == None or new_piece == None:
        return 0
    return new_piece[0][0] - original_piece[0][0]

def get_keys(translate, numberOfrotations):
    keys = []
    for i in range(numberOfrotations):
        keys.append("w")
          
    if translate < 0:
        for i in range(abs(translate)):
            keys.append("a")
    elif translate > 0:
        for i in range(translate):
            keys.append("d")
    keys.append("s")
    return keys

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
