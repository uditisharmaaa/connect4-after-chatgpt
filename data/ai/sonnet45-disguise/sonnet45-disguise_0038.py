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
        letter = chr(65 + i)
        print(letter + "   ", end="")
    print()
    
    # Print rows
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
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
            return row
    return -1

def check_win(board, row, col, checker):
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (down-right)
    for start_row in range(ROWS):
        for start_col in range(COLS):
            count = 0
            r = start_row
            c = start_col
            while r < ROWS and c < COLS:
                if board[r][c] == checker:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
                r += 1
                c += 1
    
    # Check diagonal (up-right)
    for start_row in range(ROWS):
        for start_col in range(COLS):
            count = 0
            r = start_row
            c = start_col
            while r >= 0 and c < COLS:
                if board[r][c] == checker:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
                r -= 1
                c += 1
    
    return False

def check_draw(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    while True:
        move = input("Player " + player_checker + ", please enter a column: ")
        
        if len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        move = move.upper()
        col = ord(move) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a valid column.")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def main():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = players[current_player]
        col = get_player_move(board, checker)
        row = place_checker(board, col, checker)
        
        print_board(board)
        
        if check_win(board, row, col, checker):
            print("Player " + checker + " won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

main()
