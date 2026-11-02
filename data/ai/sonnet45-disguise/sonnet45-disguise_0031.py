import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+---" * COLS + "+")
        print("| ", end="")
        for cell in row:
            print(cell + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == checker and board[row+1][col-1] == checker and board[row+2][col-2] == checker and board[row+3][col-3] == checker:
                return True
    
    return False

def check_draw(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(player_checker):
    while True:
        move = input("Player " + player_checker + ", please enter a column: ")
        
        if len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not move.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        col_num = ord(move) - 65
        
        if col_num < 0 or col_num >= COLS:
            print("Invalid input. Column out of range.")
            continue
        
        return col_num

def main():
    board = create_board()
    
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        player_checker = players[current_player]
        
        col = get_player_move(player_checker)
        
        if not is_valid_move(board, col):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        place_checker(board, col, player_checker)
        print_board(board)
        
        if check_win(board, player_checker):
            print("Player " + player_checker + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

main()
