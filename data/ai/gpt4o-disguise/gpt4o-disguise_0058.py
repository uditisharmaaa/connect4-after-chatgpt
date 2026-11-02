import random
import os

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def is_valid_move(board, col):
    return col >= 0 and col < COLS and board[0][col] == ' '

def make_move(board, col, checker):
    for i in range(ROWS-1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = checker
            break

def check_for_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and all(board[row][col+i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row+i][col] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if row >= 3 and col <= COLS - 4 and all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def player_turn(board, player):
    while True:
        move = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if len(move) == 1 and 'A' <= move <= chr(ord('A') + COLS - 1):
            col = ord(move) - ord('A')
            if is_valid_move(board, col):
                make_move(board, col, CHECKERS[player])
                return
            else:
                print(f"Column {move} is full. Try another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def play_game():
    board = create_board()
    player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        player_turn(board, player)
        print_board(board)
        if check_for_winner(board, CHECKERS[player]):
            print(f"Player {CHECKERS[player]} won!")
            break
        if check_for_draw(board):
            print("It's a draw!")
            break
        player = (player + 1) % PLAYERS

play_game()
