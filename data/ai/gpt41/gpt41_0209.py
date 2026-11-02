import os
import random

# ==== CONSTANTS ====
ROWS = 6
COLUMNS = 7   # Max 26!
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
NUMBER_OF_PLAYERS = 2  # 2-5 players allowed

# ==== HELPER FUNCTIONS ====

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Print column labels (A, B, ...)
    labels = "  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(labels)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_columns(board):
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid.append(col)
    return valid

def get_move_input(current_checker, board):
    valid_columns = get_valid_columns(board)
    col_labels = [chr(ord('A') + c) for c in valid_columns]
    while True:
        move = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input, please enter a single letter for a column.")
            continue
        col = ord(move) - ord('A')
        if 0 <= col < len(board[0]):
            if col in valid_columns:
                return col
            else:
                if board[0][col] != " ":
                    print("Column is full. You lose your turn!")
                    return None
        else:
            print("Invalid column, please enter a valid column.")

def place_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None  # Should not be reached for valid columns

def check_win(board, row, col, checker):
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal /
        (1, -1), # diagonal \
    ]
    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def check_draw(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

# ==== MAIN GAME LOOP ====

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUMBER_OF_PLAYERS]
    current_player = random.randint(0, NUMBER_OF_PLAYERS - 1)
    print_board(board)
    print(f"Player {players[current_player]} goes first!\n")

    game_over = False
    while not game_over:
        print_board(board)
        col = get_move_input(players[current_player], board)
        if col is None:
            # Column is full, player loses turn
            current_player = (current_player + 1) % NUMBER_OF_PLAYERS
            continue
        row, col_placed = place_checker(board, col, players[current_player])
        print_board(board)

        # Check for win
        if check_win(board, row, col_placed, players[current_player]):
            print(f"Player {players[current_player]} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUMBER_OF_PLAYERS

if __name__ == "__main__":
    main()
