import asyncio
import getpass
import json
from logging import NullHandler
import os
import game
from shape import SHAPES 
import websockets

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)

class Event():
    type = None
    key = None

    def __init__(self,type, key):
        self.type = type
        self.key = key

counter = 0
def run_ai(game_field, game_figure, game_width, game_heigth):
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    e = Event(pygame.KEYDOWN, pygame.K_UP)
    return [e]
    

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

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                key = ""
                # for event in list(pygame.event.get()) + run_ai():
                #     if event.type == pygame.QUIT:
                #         pygame.quit()

                #     if event.type == pygame.KEYDOWN:
                #         if event.key == pygame.K_UP:
                #             key = "w"
                #         elif event.key == pygame.K_LEFT:
                #             key = "a"
                #         elif event.key == pygame.K_DOWN:
                #             key = "s"
                #         elif event.key == pygame.K_RIGHT:
                #             key = "d"

                #         elif event.key == pygame.K_d:
                #             import pprint

                #             pprint.pprint(state)
                
                piece=state['piece']
                game=state['game']
                print(piece)
                print(game)
                print(get_piece(piece))
                #print(I)
                #print(get_all_positions(piece))
                # print(len(get_all_positions(piece))==(len(vectors)*2))
                
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent
                

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



        

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
