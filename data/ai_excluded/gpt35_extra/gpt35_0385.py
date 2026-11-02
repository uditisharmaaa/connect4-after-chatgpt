import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLUMNS)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(labels))
    # Print the board rows
    for row in board:
        print("+---" * COLUMNS + "+")
        row_str = ""
        for cell in row:
            row_str += "| " + cell + " "
        row_str += "|"
        print(row_str)
    print("+---" * COLUMNS + "+")

def is_valid_column(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(ord('A') + COLUMNS - 1)

def column_to_index(col):
    return ord(col) - ord('A')

def place_checker(board, col_index, checker):
    # Place checker in the lowest available spot in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        count = 0
        for col in range(COLUMNS):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for col in range(COLUMNS):
        count = 0
        for row in range(ROWS):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal check (down-right)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLUMNS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Diagonal check (up-right)
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLUMNS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False

def is_draw(board):
    # If no empty spaces
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS -1)
    
    print_board(board)

    while True:
        checker = players[current_player_index]
        player_prompt = f"Player {checker}, please enter a column: "
        valid_input = False
        lost_turn = False

        while not valid_input:
            col = input(player_prompt).strip().upper()
            if not is_valid_column(col):
                continue
            col_index = column_to_index(col)
            if col_index < 0 or col_index >= COLUMNS:
                continue
            # Try to place checker
            if not place_checker(board, col_index, checker):
                # Column full, lose turn
                lost_turn = True
            valid_input = True

        print_board(board)

        if lost_turn:
            # Player loses this turn, next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Check win
        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if is_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
