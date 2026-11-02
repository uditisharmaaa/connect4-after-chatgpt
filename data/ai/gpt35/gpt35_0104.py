import os
import random

# Constants for the board size and players
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_COUNT = 4
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(labels))
    # Print separator row
    separator = '+' + '---+' * len(board[0])
    for row in range(len(board)):
        print(separator)
        row_str = '|'
        for col in range(len(board[0])):
            row_str += ' ' + board[row][col] + ' |'
        print(row_str)
    print(separator)

def valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    c = inp.upper()
    if not ('A' <= c <= chr(ord('A') + cols - 1)):
        return False
    return True

def place_checker(board, col_index, checker):
    # place checker in the lowest available row in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index
    return None  # column full

def check_win(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (-1, 1)  # diagonal up-right
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check one direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        
        # Check opposite direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc
        
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS[:NUM_PLAYERS]
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        inp = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        # Validate input
        while not valid_column_input(inp, COLS):
            inp = input(f"Invalid input. Player {current_checker}, please enter a valid column: ").strip().upper()

        col = ord(inp) - ord('A')
        pos = place_checker(board, col, current_checker)
        if pos is None:
            # Column full, player loses turn
            print(f"Column {inp} is full. Player {current_checker} loses the turn.")
            # Switch player and continue
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        print_board(board)
        r, c = pos
        
        # Check for win
        if check_win(board, r, c, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
