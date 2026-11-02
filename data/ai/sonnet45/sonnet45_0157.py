import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # Horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Diagonal (down-right)
    for offset in range(-max(ROWS, COLS), max(ROWS, COLS)):
        count = 0
        for i in range(max(ROWS, COLS)):
            r = row + offset + i
            c = col + i
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] == checker:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
    
    # Diagonal (down-left)
    for offset in range(-max(ROWS, COLS), max(ROWS, COLS)):
        count = 0
        for i in range(max(ROWS, COLS)):
            r = row + offset + i
            c = col - i
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] == checker:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
    
    return False

def is_draw(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move():
    while True:
        move = input().strip().upper()
        if len(move) == 1 and 'A' <= move <= chr(64 + COLS):
            return ord(move) - 65
        print(f"Invalid input. Please enter a column letter (A-{chr(64 + COLS)}):")

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        
        col = get_player_move()
        
        if not is_valid_move(board, col):
            print("Column is full or invalid. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        row = place_checker(board, col, checker)
        print_board(board)
        
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
