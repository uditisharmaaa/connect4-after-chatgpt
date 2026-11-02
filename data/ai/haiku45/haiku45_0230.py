import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """Print the game board in the required format."""
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def get_column_from_input(user_input, cols):
    """
    Convert user input to column index.
    Returns the column index if valid, otherwise returns -1.
    """
    if len(user_input) != 1:
        return -1
    
    if not user_input.isalpha():
        return -1
    
    user_input = user_input.upper()
    col_index = ord(user_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def is_valid_move(board, col):
    """Check if a move in the given column is valid (column not full)."""
    rows = len(board)
    
    if col < 0 or col >= len(board[0]):
        return False
    
    if board[0][col] != " ":
        return False
    
    return True


def place_checker(board, col, checker):
    """
    Place a checker in the given column.
    Returns the row where the checker was placed.
    """
    rows = len(board)
    
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_horizontal_win(board, row, col, checker):
    """Check if there's a horizontal win at the given position."""
    cols = len(board[0])
    count = 0
    
    # Count checkers to the left
    for c in range(col, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    # Count checkers to the right (excluding the one we already counted)
    for c in range(col + 1, cols):
        if board[row][c] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """Check if there's a vertical win at the given position."""
    rows = len(board)
    count = 0
    
    # Count checkers downward
    for r in range(row, rows):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    # Count checkers upward (excluding the one we already counted)
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_diagonal_win_right(board, row, col, checker):
    """Check if there's a diagonal win (top-left to bottom-right) at the given position."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    
    # Count checkers going up-left
    r, c = row, col
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c -= 1
    
    # Count checkers going down-right (excluding the one we already counted)
    r, c = row + 1, col + 1
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win_left(board, row, col, checker):
    """Check if there's a diagonal win (top-right to bottom-left) at the given position."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    
    # Count checkers going up-right
    r, c = row, col
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r -= 1
        c += 1
    
    # Count checkers going down-left (excluding the one we already counted)
    r, c = row + 1, col - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
        else:
            break
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """Check if the current move resulted in a win."""
    if check_horizontal_win(board, row, col, checker):
        return True
    if check_vertical_win(board, row, col, checker):
        return True
    if check_diagonal_win_right(board, row, col, checker):
        return True
    if check_diagonal_win_left(board, row, col, checker):
        return True
    
    return False


def check_draw(board):
    """Check if the board is completely filled (draw condition)."""
    rows = len(board)
    
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    
    return True


def play_game():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        player_number = current_player + 1
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ")
            col = get_column_from_input(user_input, COLS)
            
            if col == -1:
                print("Invalid input. Please enter a valid column (A-G).")
                continue
            
            if not is_valid_move(board, col):
                print("That column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place checker and get placement row
        row = place_checker(board, col, checker)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """Main function to start the game."""
    play_game()


if __name__ == "__main__":
    main()
