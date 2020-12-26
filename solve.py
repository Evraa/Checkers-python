#Global imports
import random
from collections import deque
from copy import deepcopy
import time
from numpy import random

#Local imports
from move_logic import where_can_i_move_next
from common import init_board, how_many, non_zeros_count, define_depth,evaluate
from constants import N, DEPTH, MAX_NEG, MAX_POS, GREEDY, AGAINST, TUNE, GFX, VERBOSE, PRUNE, VERBOSE_DEEP
from board import Board
from tree import Node, Tree

def construct_full_tree(board, pl):
    '''
        + The main part starts here.
        + this function constructs nodes, a node represents a state.
        + state is the board after certain moves.
        + this function returns only the min_max Tree with pruning if asked for.
        + The algorithm keeps creating nodes as long as the last depth (level) nodes
            didn't exceed the time when they were being created.
        + Inputs: board and a player
        + Outputs: tree
    '''    

    #Crete the Root Node, add it to the tree and the Q
    player = deepcopy(pl)       #just to make sure, no shallow copy occurs
    root = Node(board,player,evaluate(board))   #the root
    tree = Tree(root)
    tree.inc_depth()
    switch = "switch"
    Q = deque()                 #Q for adding nodes to be spanned later
    Q.append(root)              #append the root of course
    Q.append(switch)            #switch: new generation is comming. ie. new level, new depth.
    new_gen = True              #for tree construction
    this_is_root = True
    start_time, end_time = None, None
    
    while len(Q) > 1:
        
        root = Q.popleft()
        if root == "switch":
            #swap players
            player = 1 if player == -1 else -1
            Q.append(switch)
            end_time = time.time()

            if start_time == None:
                tree.inc_depth()
            elif end_time - start_time < TUNE:
                if VERBOSE: print (f'Tree depth till now: {tree.depth}\t\tTime: {end_time-start_time}')
                tree.inc_depth()
                #after each level produced, prune if you want to.
                if PRUNE: tree.prune()
                if VERBOSE_DEEP: tree.print_tree()
            else:
                print (f"Time Exceeded at depth: {tree.depth}\t\tTime: {end_time-start_time}")

                return tree
            start_time = time.time()
            new_gen = True
            #this will never happen, unless you have a SUPER computer and N is like 1e4
            if tree.depth == DEPTH:
                break
            continue
        
        if root.pruned:
            if VERBOSE: print ("Can't Go Down there, it's pruned")
            continue

        #Get the possible moves from this Node
        possible_moves = where_can_i_move_next(root.board, player)
        
        #No moves from here
        if len(possible_moves) == 0:
            #cost will be massive, cuz this is a WIN
            new_cost = MAX_POS if player == 1 else MAX_NEG
            root.update_cost(new_cost)

        for pos in possible_moves:
            #for each possible move create and append a node
            node = Node (pos[3], player, pos[2])
            tree.append_node(node, root, new_gen)
            new_gen = False
            player_swap = 1 if player == -1 else -1
            score = how_many (pos[3],player_swap)
            if score == 0:
                new_cost = MAX_POS if player == 1 else MAX_NEG
                node.update_cost(new_cost)
            if len(possible_moves) == 1 and this_is_root:
                Q.append(node)
                return tree
            else:
                Q.append(node)
        this_is_root = False

    return tree


def go_greedy(board, player):
    '''
        + Allows the agent to move greedily, when it repeats itself.
        + So that we don't get cought up with cyclic moves.
        + Also if option GREEDY is not picked, the game ends in a DRAW
        + Inputs: States (board and player)
        + Ouputs: Greedy move is possible.

    '''
    if GREEDY:
        print("Player: {player} Repeated Move! GO GREEDY \n")
        possible_moves = where_can_i_move_next(board, player)
        #best move
        max_win = 0
        best_move = None
        #search the moves
        for pos in possible_moves:
            if abs(pos[2]) > max_win:
                best_move = pos
                max_win = abs(pos[2])
        #if none of them is even good enough, pick randomly
        if max_win == 0:
            ev = random.randint(0,len(possible_moves)-1) #for root
            best_move = possible_moves[int(ev)]
        return best_move[3]

    else:
        print (f'Player: {player} Proposes DRAW!')
        return None
    
def play_against(board, player=-1):
    '''
        + Allows the user to pick one possible move; to play against ai.
        + Inputs are the state of the current board.
    '''
    #make him choose a move
    possible_moves = where_can_i_move_next(board, player)
    if len(possible_moves) == 0:
        print ("Computer Won, no more move allowed")
        return None

    print ("Pick a number of these Allowed Moves:\n")
    for i,pos in enumerate(possible_moves):
        print (f'{i}: Start: {pos[0]}\tEnd: {pos[1]}')

    move_numb = int(input("Move picked: "))
    while not isinstance(move_numb, int) or move_numb < 0 or move_numb >= len(possible_moves):
        print ("Please choose a reasonable number!")
        move_numb = int(input("Move picked: "))

    return possible_moves[move_numb][3]


def main():
    '''
        + The main arena where two players compete.
        + Simply it checks -from the `constants` file- flags and act accordingly.
        + The game goes on until one player can't move, due to loss of all its pieces
            or no moves allowed
        + The game can end in a draw, if in 100 moves (rounds) no pieces got eaten
        + If a state is repeated multiple times, the game can end in a draw with a probability = 50%
            or agent can move Greedly.
    '''
    #init the board
    board = init_board(N)
    #draw the board?
    if GFX:
        br = Board(N)
        br.draw_board(board)
    #variables for the arena
    player = 1                                              #Starting player
    pl_1_prev_move,pl_2_prev_move = None, None              #last board record
    pl_1_prev_prev_move, pl_2_prev_prev_move = None, None   #last last board record
    rounds = 0                                              #Round count with no kills
    total_count = non_zeros_count(board)                    #first total count of all pieces
    #Main Loop
    while True:
        tree=None
        if rounds == 50:
            print("\n\nDRAW: 100 Moves -50 each- and none got eaten.\n")
            return
        #against is a flag for playing against the computer
        if player == -1 and AGAINST:
            board = play_against(board,player)
            if board == None: return
        else:
            tree = construct_full_tree(board, player)   #the main work is here. constructing the tree with pruning
            board, lost = tree.update_board()           #minmax pick

        if player == 1:
            #for round count
            check = non_zeros_count(board)
            if check == total_count: #no one was eaten
                rounds += 1
            else:
                rounds = 1
                total_count = check

            if VERBOSE: print(f'Player: {player}\t\t Cost: {tree.root.cost}\n')
            if pl_1_prev_prev_move == None and pl_1_prev_move != None:
                pl_1_prev_prev_move = pl_1_prev_move
            if pl_1_prev_move == None:
                pl_1_prev_move = board

            if pl_1_prev_move != None and pl_1_prev_prev_move != None:
                if board == pl_1_prev_prev_move:
                    #GO GREEDY
                    board = go_greedy(pl_1_prev_move, player)
                    if board == None:
                        return
                pl_1_prev_prev_move = pl_1_prev_move
                pl_1_prev_move = board

        if player == -1 and not AGAINST:
            if VERBOSE: print(f'Player: {player}\t\t Cost: {tree.root.cost}\n')
            if pl_2_prev_prev_move == None and pl_2_prev_move != None:
                pl_2_prev_prev_move = pl_2_prev_move
            if pl_2_prev_move == None:
                pl_2_prev_move = board

            if pl_2_prev_move != None and pl_2_prev_prev_move != None:
                if board == pl_2_prev_prev_move:
                    #GO GREEDY
                    board = go_greedy(pl_2_prev_move, player)
                    if board == None:
                        return
                pl_2_prev_prev_move = pl_2_prev_move
                pl_2_prev_move = board
        
        if VERBOSE: tree.print_tree()
        
        if lost:
            player_swap = 1 if player == -1 else -1
            print (f'Player: {player_swap} Won: No moves allowed for opponent.')
            del tree
            break
        br.draw_board(board)
        player_swap = 1 if player == -1 else -1
        score = how_many (board,player_swap)
        if score == 0:
            print (f'Player: {player} Won: All pieces are taken.')
            del tree
            break
        #next player
        player = 1 if player == -1 else -1
        #free memory
        del tree


main()
