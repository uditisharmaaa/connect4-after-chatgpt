import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print board rows
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+' + '---+' * COLS)

def get_valid_column(board):
    while True:
        try:
            col = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if len(col) != 1 or col < 'A' or col > chr(65 + COLS - 1):
                print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
                continue
            
            col_idx = ord(col) - ord('A')
            if board[0][col_idx] != ' ':
                print("That column is full. Please choose another column.")
                continue
            
            return col_idx
        except EOFError:
            print("Please enter a valid column.")
        except:
            print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")

def place_checker(board, col_idx, checker):
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx
    return -1

def check_win(board, row_idx, col_idx, checker):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in the positive direction
        r, c = row_idx + dr, col_idx + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row_idx - dr, col_idx - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def play_game():
    global current_player
    board = initialize_board()
    print_board(board)
    
    while True:
        col_idx = get_valid_column(board)
        row_idx = place_checker(board, col_idx, PLAYER_CHECKERS[current_player])
        
        print_board(board)
        
        if check_win(board, row_idx, col_idx, PLAYER_CHECKERS[current_player]):
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

# Main
current_player = random.randint(0, PLAYERS - 1)
play_game()
