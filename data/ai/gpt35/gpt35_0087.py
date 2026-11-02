import os
import random
import sys

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players, use first PLAYERS of these
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels A, B, C, ...
    labels = '  '
    for i in range(cols):
        labels += ' ' + chr(ord('A') + i) + '  '
    print(labels)
    # Print board with borders and cells
    for row in range(len(board)):
        print('+' + '---+' * cols)
        row_str = '|'
        for col in range(cols):
            row_str += ' ' + board[row][col] + ' |'
        print(row_str)
    print('+' + '---+' * cols)

def get_player_input(player_checker, board):
    cols = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Please enter exactly one uppercase letter from the columns.")
            continue
        if inp not in valid_cols:
            print("Invalid column. Please enter a valid uppercase letter corresponding to a column.")
            continue
        col_index = ord(inp) - ord('A')
        # Check if column is full
        if board[0][col_index] != ' ':
            # According to spec, player loses turn if column full
            print(f"Column {inp} is full. You lose your turn.")
            return None  # Signal lost turn due to full column
        return col_index

def place_checker(board, col_index, checker):
    """
    Place the checker in the lowest available row in col_index.
    Assumes column is not full.
    Returns True if placed successfully, False otherwise (should not happen if checked before).
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False  # If no space found

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # Check horizontal, vertical, diagonal down-right, diagonal up-right
    directions = [(0,1), (1,0), (1,1), (-1,1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(rr, cc) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LENGTH:
                    return True
    return False

def check_draw(board):
    # Draw if no empty spaces in top row (means board full)
    return all(cell != ' ' for cell in board[0])

def main():
    # Initialize
    board = create_board(ROWS, COLS)

    # Select players' checkers according to number of players
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly select starting player index
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)  # Show empty board before first move

    while True:
        current_checker = players_checkers[current_player_index]
        col_choice = get_player_input(current_checker, board)

        if col_choice is not None:
            placed = place_checker(board, col_choice, current_checker)
            # placed must be True here since we check full column before allowing input
            print_board(board)
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                return
            if check_draw(board):
                print("Game is a draw!")
                return
        else:
            # Column full: lose turn; just print the board again without change
            print_board(board)

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit()
