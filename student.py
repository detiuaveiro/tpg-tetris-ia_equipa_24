import asyncio
import getpass
import json
from logging import NullHandler
import os
import websockets

import game
from shape import SHAPES 

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # Next 3 lines are not needed for AI agent
        SCREEN = pygame.display.set_mode((299, 123))
        SPRITES = pygame.image.load("data/pad.png").convert_alpha()
        SCREEN.blit(SPRITES, (0, 0))

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                piece=state['piece']
                game=state['game']
                print(piece)
                #print(game)
                #print(get_piece(piece))
                print(get_rows(game))
                #print(get_aggregate_height(game))
                print(numberOfHoles(game))
                #print(numberOfHoles(game))
                #print(get_all_positions(piece))
                # print(len(get_all_positions(piece))==(len(vectors)*2))

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                key = ""
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            key = "w"
                        elif event.key == pygame.K_LEFT:
                            key = "a"
                        elif event.key == pygame.K_DOWN:
                            key = "s"
                        elif event.key == pygame.K_RIGHT:
                            key = "d"

                        elif event.key == pygame.K_d:
                            import pprint

                            #pprint.pprint(state)

                
                        await websocket.send(
                            json.dumps({"cmd": "key", "key": key})
                        )  # send key command to server - you must implement this send in the AI agent
                        break
                

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

            # Next line is not needed for AI agent
            pygame.display.flip()


vectors=[[0,1], [0,2], [0,3], [0,4], 
        [1,0], [1,1], [1,2], [1,3], [1,4], 
        [2,0], [2,1], [2,2], [2,3], [2,4],
        [3,0], [3,1], [3,2], [3,3], [3,4],
        [4,0], [4,1], [4,2], [4,3], [4,4],
        [-1,1], [-1,2], [-1,3], [-1,4], 
        [-2,1], [-2,2], [-2,3], [-2,4],
        [-3,1], [-3,2], [-3,3], [-3,4],
        [-4,1], [-4,2], [-4,3], [-4,4]]

def get_all_positions(piece):
    if(piece == None):
        return None

    possible_positions=[piece]
    for v in vectors:
        new_piece=[]
        flag = True
        for block in piece:
            x = block[0] + v[0]
            y = block[1] + v[1]
            if(x >= 0 and x < 6 and y < 6 and y >= 0):
                new_piece += [[x, y]]
            else:
                flag = False
                break
        
        if(flag):
            possible_positions += [new_piece]

        new_piece=[]
        flag = True
        for block in piece:
            x = block[0] - v[0]
            y = block[1] - v[1]
            if(x >= 0 and x < 6 and y < 6 and y >= 0):
                new_piece += [[x, y]]
            else:
                flag = False
                break

        if(flag):
            possible_positions += [new_piece]
    return possible_positions

I = get_all_positions([[2,2],[3,2],[4,2],[5,2]])
L = get_all_positions([[2,1],[3,1],[2,2],[2,3]])
S = get_all_positions([[2,1],[1,2],[2,2],[1,3]])
T = get_all_positions([[4,2],[4,3],[5,3],[4,4]])
J = get_all_positions([[2,1],[2,2],[2,3],[3,3]])
O = get_all_positions([[3,3],[4,3],[3,4],[4,4]])
Z = get_all_positions([[2,1],[2,2],[3,2],[3,3]])
PIECES=[I,L,S,T,J,O,Z]

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
            else:
                return 'Z'

    return 'Not found'

def get_rows(game):
    rows=[[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]
   
    for p in game:
        rows[p[1]][p[0]] = 1
    
    for i in range(len(rows)):
        del rows[i][0]

    return rows

def get_height(game):
    temp = 30
    for p in game:
        if p[1] < temp:
            temp = p[1]
    return 30 - temp 

def get_aggregate_height(game):
    rows = get_rows(game)
    #altura_colunas=[0,0,0,0,0,0,0,0]
    column_height = 0
    aggregate_height = 0
    for x in range(8):
        for y in range(30):
            if rows[29-y][x] == 1:
                column_height = y + 1
            #altura_colunas[x] = column_height
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

# def numberOfHoles(game):
#     rows = get_rows(game)
#     holesColumn = 0
#     totalHoles = 0
#     holesPerColumn = [0,0,0,0,0,0,0,0]
#     for x in range(8):
#         for y in range(30):
#             if rows[29-y][x] == 0: #and rows[29-y-1][x] == 1:
#                 for y2 in range(y,30):
#                     if rows[29-y2][x] == 1:
#                         holesColumn = y2 - y -1 
#                     holesPerColumn[x] = holesColumn
#         totalHoles += holesColumn
#     return holesPerColumn

def numberOfHoles(game):
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
    sim_game = game
    for block in piece:
        a = 0
    return 0


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
