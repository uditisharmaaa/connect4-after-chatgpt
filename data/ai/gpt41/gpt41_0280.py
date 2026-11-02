import os
import random
import string

# ==== Constants ====
ROW_COUNT = 6
COL_COUNT = 7  # Max: 26
PLAYER_COUNT = 2  # set to 2 for submission, can be up to 5.
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ==== Board Creation ====
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# ==== Board Printing ====
def print_board(board):
    os.system('clear')  # clear terminal screen
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * cols)

# ==== Input Validation ====
def valid_column(input_col, board):
    cols = len(board[0])
    if len(input_col) != 1 or input_col not in string.ascii_uppercase[:cols]:
        return False
    col_idx = string.ascii_uppercase.index(input_col)
    # Check if at least one spot left
    if board[0][col_idx] != ' ':
        return False  # Column full
    return True

# ==== Move Placement ====
def place_checker(board, col_letter, checker):
    col_idx = string.ascii_uppercase.index(col_letter)
    for i in range(len(board) - 1, -1, -1):  # from bottom up
        if board[i][col_idx] == ' ':
            board[i][col_idx] = checker
            return i, col_idx  # Return row, col of placement
    return None, None  # should only happen if column full

# ==== Win Checking ====
def check_for_win(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# ==== Draw Checking ====
def check_for_draw(board):
    return all(board[0][c] != ' ' for c in range(len(board[0])))

# ==== Main Game Loop ====
def main():
    # Set up
    board = create_board(ROW_COUNT, COL_COUNT)
    players = CHECKERS[:PLAYER_COUNT]
    player_names = [f"Player {c}" for c in players]
    
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)
    print(f"{player_names[current_player_idx]} ({players[current_player_idx]}) starts!\n")
    input("Press Enter to start the game...")

    winner = None
    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        player_name = player_names[current_player_idx]
        print(f"{player_name}, please enter a column:")

        # Input validation loop
        while True:
            input_col = input().strip().upper()
            if not valid_column(input_col, board):
                if len(input_col) != 1 or input_col not in string.ascii_uppercase[:COL_COUNT]:
                    print("Invalid column. Please enter a valid column letter (A-G).")
                elif board[0][string.ascii_uppercase.index(input_col)] != ' ':
                    print("Column full. You lose your turn!")
                    break  # Lose turn
                else:
                    print("Invalid input.")  # fallback
            else:
                # Place checker and check for win/draw
                row, col = place_checker(board, input_col, current_checker)
                # Check for win
                if check_for_win(board, row, col, current_checker):
                    print_board(board)
                    print(f"{player_name} won!")
                    return
                # Check for draw
                if check_for_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    return
                # Normal turn change
                break  # Valid move = break input loop

        # Next player (even if lost turn)
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
