import os
import random
import string

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supported up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    # Print board rows with separators
    sep = "+" + "---+" * len(board[0])
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def valid_column_input(user_input, board):
    if len(user_input) != 1:
        return False
    if user_input not in string.ascii_uppercase[:len(board[0])]:
        return False
    col = string.ascii_uppercase.index(user_input)
    # Check if column is full
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    # Start from bottom row to top row
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full, no space - should not reach here if validated correctly
    return None

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If any top row cell is empty, game is not draw
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} starts the game!")

    while True:
        player_checker = players[current_player_index]
        # Input loop until valid move or lose turn if column full
        while True:
            print(f"Player {player_checker}, please enter a column:")
            user_input = input().strip().upper()
            if not valid_column_input(user_input, board):
                # Check invalid input vs full column
                if len(user_input) == 1 and user_input in string.ascii_uppercase[:len(board[0])]:
                    col = string.ascii_uppercase.index(user_input)
                    if board[0][col] != " ":
                        # Column full, player loses turn
                        # Inform player but do NOT retry input
                        break
                print("Invalid input, please enter a valid column letter (A-G) that is not full.")
                continue

            col = string.ascii_uppercase.index(user_input)
            break

        if len(user_input) != 1 or user_input not in string.ascii_uppercase[:len(board[0])] or board[0][col] != " ":
            # Turn lost due to full column (or invalid, but input validation should prevent invalid)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        move = place_checker(board, col, player_checker)
        print_board(board)

        if move is not None:
            r, c = move
            if check_win(board, r, c, player_checker):
                print(f"Player {player_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        else:
            # Should not happen, but if no placement, turn lost
            pass

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
