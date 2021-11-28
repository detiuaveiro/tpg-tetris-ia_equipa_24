# Bruno Silva 97931, Francisco Cardita 97640, Pedro Guerra 98610

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
    for i in range(2): # add and sub vectors
        for v in vectors:
            new_piece=[]
            flag = True

            for block in piece:
                if i == 0:
                    x = block[0] + v[0]
                    y = block[1] + v[1]
                else:
                    x = block[0] - v[0]
                    y = block[1] - v[1]

                if(x >= 0 and x <= 8 and y >= 0):
                    new_piece.append([x, y])
                else:
                    flag = False
                    break
            
            if(flag):
                possible_positions.append(new_piece)
    return possible_positions

# Examples of each piece were obtained directly from the state['piece']
I = get_all_positions([[2,2],[3,2],[4,2],[5,2]])
L = get_all_positions([[2,1],[2,2],[2,3],[3,3]])
S = get_all_positions([[2,1],[2,2],[3,2],[3,3]])
T = get_all_positions([[4,2],[4,3],[5,3],[4,4]])
J = get_all_positions([[2,1],[3,1],[2,2],[2,3]])
O = get_all_positions([[3,3],[4,3],[3,4],[4,4]])
Z = get_all_positions([[2,1],[1,2],[2,2],[1,3]])

PIECES=[I,L,S,T,J,O,Z]

def get_list_pieces():
    return PIECES