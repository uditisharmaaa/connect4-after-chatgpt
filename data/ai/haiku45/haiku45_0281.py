import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a board with empty spaces"""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board in the required format"""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(chr(65 + col), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * cols + "+")

def is_valid_column(column_letter, cols):
    """Check if the column input is valid"""
    if len(column_letter) != 1:
        return False
    
    col_index = ord(column_letter.upper()) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True

def get_column_index(column_letter):
    """Convert column letter to index"""
    return ord(column_letter.upper()) - ord('A')

def is_column_full(board, col_index):
    """Check if a column is full"""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Place a checker in the column and return the row where it was placed"""
    rows = len(board)
    
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1

def check_horizontal_win(board, row, col, checker):
    """Check if there's a horizontal win"""
    cols = len(board[0])
    count = 0
    
    # Check left
    for i in range(col, -1, -1):
        if board[row][i] == checker:
            count += 1
        else:
            break
    
    # Check right (excluding the current cell to avoid double counting)
    for i in range(col + 1, cols):
        if board[row][i] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_vertical_win(board, row, col, checker):
    """Check if there's a vertical win"""
    rows = len(board)
    count = 0
    
    # Check down
    for i in range(row, rows):
        if board[i][col] == checker:
            count += 1
        else:
            break
    
    # Check up (excluding the current cell)
    for i in range(row - 1, -1, -1):
        if board[i][col] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH

def check_diagonal_win(board, row, col, checker):
    """Check if there's a diagonal win (both directions)"""
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal from top-left to bottom-right
    count = 0
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == checker:
            count += 1
            i -= 1
            j -= 1
        else:
            break
    
    # Check down-right (excluding current cell)
    i, j = row + 1, col + 1
    while i < rows and j < cols:
        if board[i][j] == checker:
            count += 1
            i += 1
            j += 1
        else:
            break
    
    if count >= WIN_LENGTH - 1:  # -1 because we don't count the current cell
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 0
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols:
        if board[i][j] == checker:
            count += 1
            i -= 1
            j += 1
        else:
            break
    
    # Check down-left (excluding current cell)
    i, j = row + 1, col - 1
    while i < rows and j >= 0:
        if board[i][j] == checker:
            count += 1
            i += 1
            j -= 1
        else:
            break
    
    if count >= WIN_LENGTH - 1:  # -1 because we don't count the current cell
        return True
    
    return False

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win"""
    if check_horizontal_win(board, row, col, checker):
        return True
    
    if check_vertical_win(board, row, col, checker):
        return True
    
    if check_diagonal_win(board, row, col, checker):
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop"""
    board = create_board(ROWS, COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    winner = None
    
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        current_player_name = chr(88 + current_player_index) if current_player_index == 0 else chr(79 + current_player_index - 1)
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            column_input = input(f"Player {current_player_checker}, please enter a column: ")
            
            if not is_valid_column(column_input, COLS):
                print("Invalid input. Please enter a valid column (A-" + chr(65 + COLS - 1) + ").")
                continue
            
            col_index = get_column_index(column_input)
            
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row = place_checker(board, col_index, current_player_checker)
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
            winner = current_player_checker
        
        # Check for draw
        elif is_board_full(board):
            print("Draw!")
            game_over = True
        
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Start the game"""
    play_game()

if __name__ == "__main__":
    main()
