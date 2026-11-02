import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # max 26 columns supported
MIN_PLAYERS = 2
MAX_PLAYERS = 5

NUM_PLAYERS = 2  # For submission: 2 players
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, columns=COLUMNS):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    rows = len(board)
    columns = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:columns])
    sep = '+' + '---+' * columns
    print(header)
    print(sep)
    for row in range(rows):
        line = '| ' + ' | '.join(board[row]) + ' |'
        print(line)
        print(sep)

def get_valid_column(input_str, columns):
    if len(input_str) != 1:
        return None
    char = input_str.upper()
    if char not in string.ascii_uppercase[:columns]:
        return None
    return ord(char) - ord('A')

def place_checker(board, col, checker):
    # Check from bottom row up for empty space
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(columns - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(columns):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(rows - 3):
        for c in range(columns - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check diagonal up-right
    for r in range(3, rows):
        for c in range(columns - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    # If any space in top row is empty, not draw
    return all(cell != " " for cell in board[0])

def select_first_player(num_players):
    return random.randint(0, num_players - 1)

def main():
    rows = ROWS
    columns = COLUMNS
    num_players = NUM_PLAYERS
    players = CHECKERS[:num_players]
    board = create_board(rows, columns)
    current_player_idx = select_first_player(num_players)
    
    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        col = None
        turn_lost = False
        while True:
            user_input = input(prompt).strip()
            col = get_valid_column(user_input, columns)
            if col is None:
                print(f"Invalid input '{user_input}'. Please enter a letter from A to {string.ascii_uppercase[columns-1]}.")
                continue
            if board[0][col] != " ":
                # Column full, turn lost
                turn_lost = True
                break
            # Place checker
            place_checker(board, col, current_checker)
            break
        
        if turn_lost:
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_checker} loses the turn.")
        
        else:
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
