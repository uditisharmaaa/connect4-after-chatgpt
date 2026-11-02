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
        print(f" {chr(65+i)}  ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+" + "---+" * COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == " "

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
            r = row - offset + i
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
            r = row - offset + i
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
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column: ", end="")
        
        user_input = input().strip().upper()
        
        # Validate input
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - 65
        
        if col < 0 or col >= COLS:
            print("Column out of range. Please try again.")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        row = place_checker(board, col, current_checker)
        print_board(board)
        
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
