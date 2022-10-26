import random as rand


class Minesweeper:

    not_dug = -1
    mine = 9

    fail_reward = -20
    step_reward = -1
    success_reward = 20
    invalid_action_reward = -5

    def __init__(self, length, height, mines):
        self.length = length
        self.height = height
        self.mines = mines

        self.board = None
        self.mine_locations = None
        self.terminal = True

        self.possible_actions = list(range(length * height))
        return

    def dig(self, x, y, print_state=False):
        reward = Minesweeper.step_reward
        info = None

        if (x, y) in self.mine_locations:
            self.mark_board(x, y, Minesweeper.mine)
            self.terminal = True
            info = {'success': False}
            if print_state:
                self.print_current_state()
            return self.board.copy(), reward + Minesweeper.fail_reward, True, info

        to_reveal = [(x, y)]
        num_to_reveal = 1
        while num_to_reveal > 0:
            cord = to_reveal.pop()
            num_to_reveal -= 1
            x = cord[0]
            y = cord[1]

            value = self.get_value(x, y)
            if value is not Minesweeper.not_dug:
                continue

            value = self.find_value(x, y)
            self.mark_board(x, y, value)

            if value == 0:
                for j in range(y - 1, y + 2):
                    if j < 0 or j >= self.height:
                        continue
                    for i in range(x - 1, x + 2):
                        if (j == y and i == x) or i < 0 or i >= self.length:
                            continue
                        to_reveal.append((i, j))
                        num_to_reveal += 1

        only_mines_left = self.only_mines_left()
        if only_mines_left:
            reward += Minesweeper.success_reward
            info = {'success': True}

        if print_state:
            self.print_current_state()
        return self.board.copy(), reward, only_mines_left, info

    def find_value(self, x, y):
        value = 0

        for j in range(y - 1, y + 2):
            if j < 0 or j >= self.height:
                continue
            for i in range(x - 1, x + 2):
                if (j == y and i == x) or i < 0 or i >= self.length:
                    continue
                value += int((i, j) in self.mine_locations)
        return value

    def get_value(self, x, y):
        if self.board is None:
            raise ValueError("Game needs to be reset before getting value of board")
        return self.board[y][x]

    def mark_board(self, x, y, value):
        if self.board is None:
            raise ValueError("Game needs to be reset before getting value of board")
        self.board[y][x] = value
        return

    def print_current_state(self):
        for row in self.board:
            to_print = ""
            for elm in row:
                if 0 <= elm <= 9:
                    to_print += " "
                to_print += str(elm)
            print(to_print)
        return

    def only_mines_left(self):
        for y in range(self.height):
            for x in range(self.length):
                value = self.get_value(x, y)
                if value == Minesweeper.not_dug and (x, y) not in self.mine_locations:
                    return False

        return True

    def step(self, action=None, x=None, y=None, print_state=False):
        if self.terminal:
            raise AttributeError("Game needs to be reset before calling step")

        if action is not None:
            y = action // self.height
            x = action % self.length

        if self.get_value(x, y) is Minesweeper.not_dug:
            return self.dig(x, y, print_state=print_state)

        return self.board.copy(), Minesweeper.step_reward + Minesweeper.invalid_action_reward, False, None

    def reset(self, print_state=False):
        self.board = [[Minesweeper.not_dug for i in range(self.length)] for j in range(self.height)]

        self.mine_locations = []
        for _ in range(self.mines):
            new_mine = (rand.randint(0, self.length - 1), rand.randint(0, self.height - 1))
            while new_mine in self.mine_locations:
                new_mine = (rand.randint(0, self.length - 1), rand.randint(0, self.height - 1))
            self.mine_locations.append(new_mine)

        self.terminal = False

        if print_state:
            print("Num Mines: " + str(self.mines))
            self.print_current_state()
        return self.board
