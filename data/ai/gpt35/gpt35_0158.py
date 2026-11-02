import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(len(board[0])):
        labels += chr(ord('A') + i) + "   "
    print(labels)
    
    # Print top border
    print("+" + "---+" * len(board[0]))
    
    # Print rows
    for row in board:
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
        print("+" + "---+" * len(board[0]))

def get_valid_input(current_player, board):
    valid_columns = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        entry = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if entry not in valid_columns:
            # Invalid input: not a valid column letter
            continue
        col_index = ord(entry) - ord('A')
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full, player loses turn
            return None
        return col_index

def place_checker(board, col_index, checker):
    # Place checker in lowest empty row in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    # Should never reach here since we check if column is full before
    return None, None

def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])
    connect = 4
    
    # Horizontal check
    for r in range(rows):
        for c in range(columns - connect + 1):
            if all(board[r][c+i] == checker for i in range(connect)):
                return True
    
    # Vertical check
    for c in range(columns):
        for r in range(rows - connect + 1):
            if all(board[r+i][c] == checker for i in range(connect)):
                return True
    
    # Diagonal (top-left to bottom-right)
    for r in range(rows - connect + 1):
        for c in range(columns - connect + 1):
            if all(board[r+i][c+i] == checker for i in range(connect)):
                return True
    
    # Diagonal (bottom-left to top-right)
    for r in range(connect - 1, rows):
        for c in range(columns - connect + 1):
            if all(board[r - i][c + i] == checker for i in range(connect)):
                return True
    
    return False

def check_draw(board):
    # If any cell in top row is empty, not a draw
    if any(cell == " " for cell in board[0]):
        return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS -1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        col_index = get_valid_input(current_checker, board)
        
        if col_index is None:
            # Column full, player loses turn, switch player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        
        place_checker(board, col_index, current_checker)
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw.")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
