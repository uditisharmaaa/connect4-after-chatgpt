import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # Only first NUM_PLAYERS will be used

def clear_screen():
    os.system('clear')

def create_board():
    # Create a ROWS x COLS board filled with " "
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(COLS):
        labels += "  " + chr(ord('A') + i) + " "
    print(labels)
    # Print top border line
    print("+" + "---+" * COLS)
    # Print each row
    for row in board:
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
        print("+" + "---+" * COLS)

def input_valid(column_input, board):
    # Validate if input is a single uppercase letter for a valid column and the column is not full
    if len(column_input) != 1:
        return False
    col = ord(column_input) - ord('A')
    if col < 0 or col >= COLS:
        return False
    # Check if column is full (top row not empty)
    if board[0][col] != " ":
        return True  # still valid as input, but the turn lost - handled separately
    return True

def place_checker(board, col, checker):
    # Place checker in lowest available spot in column col, return True if placed, False if column full
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # column full

def check_for_win(board, checker):
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row][col + i] == checker for i in range(WIN_COUNT)):
                return True
    # Check vertical locations for win
    for col in range(COLS):
        for row in range(ROWS - WIN_COUNT + 1):
            if all(board[row + i][col] == checker for i in range(WIN_COUNT)):
                return True
    # Check positively sloped diagonals (bottom-left to top-right)
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    # Check negatively sloped diagonals (top-left to bottom-right)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def check_for_draw(board):
    # Draw if no empty space in top row (means all columns full)
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS-1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()
            if not input_valid(user_input, board):
                # invalid input format or out of range
                continue
            col = ord(user_input) - ord('A')
            if board[0][col] != " ":
                # Column full, player loses turn
                break  # skip placing checker and switch players
            else:
                placed = place_checker(board, col, current_checker)
                if placed:
                    break
                else:
                    # Should not reach here because of the check above
                    break

        print_board(board)

        # If placed a checker, check for win or draw
        if board[0][col] != " " or (board[0][col] == " " and placed):
            if placed:
                if check_for_win(board, current_checker):
                    print(f"Player {current_checker} won!")
                    break
                if check_for_draw(board):
                    print("Game is a draw!")
                    break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
