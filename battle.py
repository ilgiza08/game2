import random
class MyException(Exception):
    pass

class BoardOutException(MyException): #выстрел вне доски
    pass

class DotTwice(MyException): #выстрел в одну и ту же клетку
    pass

class AddShipMyException(MyException): #точка вне доски или занята
    pass
class NotImplementedException(MyException):
    pass
class BoardWrongShipException(MyException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, l_ship, dot_beginner, ship_direction):
        self.l_ship = l_ship #длина 1-4 точек
        self.dot_beginner = dot_beginner # нос корабля самая маленькая координата
        self.ship_direction = ship_direction #horizontal вертикаль - меняем координаты x y
        self.free_dots = l_ship # сколько не подбитых точек


    @property
    def dots(self):#все точки корабля
        l_of_dots = []
        for i in range(self.l_ship):
            x = self.dot_beginner[0]
            y = self.dot_beginner[1]
            if self.ship_direction == "vertical":
                x += i
                l_of_dots.append(Dot(x, y))
            else:
                y += i
                l_of_dots.append(Dot(x, y))
        return l_of_dots

# tst = Ship(4, [0, 0], "vertical")
# print(tst.dots) # not iter

class Board:
    def __init__(self, hid=False):
        self.hid = hid
        self.busy = [] #нельзя ставить
        self.my_ships = []
        self.board_coord = [['O'] * 6 for _ in range(6)]
        self.count = 0

    def show_board(self):
        num = '   0 | 1 | 2 | 3 | 4 | 5 '
        print(num)
        for row, i in zip(self.board_coord, range(6)):
            res = f"{i} |{' | '.join(str(j) for j in row)}"
            if self.hid:
                res1 = res.replace("*", "O")
                print(res1)
            else: print(res)

# board1 = Board(True)
# print(board1.show_board())

    def out(self, dot):
        return any([dot.x<0, dot.x>6, dot.y<0, dot.y>6])


    def contour(self, ship):  # ставим контур до add ship
        near = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for i in ship.dots:
            for j1, j2 in near:
                a = Dot(i.x + j1, i.y + j2)
                if not self.out(a) and a not in self.busy:
                    self.busy.append(a)


    def add_ship(self, ship):
        try:
            for i in ship.dots:
                if self.out(i) or i in self.busy:
                    raise AddShipMyException()
        except AddShipMyException:
            print("Корабль не ставится на доску")
        else:
            for d in ship.dots:
                self.board_coord[d.x][d.y] = "*"
                self.busy.append(d)
            self.my_ships.append(ship)
            self.contour(ship)


    def shot(self, dot):
        try:
            if self.out(dot):
                raise BoardOutException()
        except AddShipMyException:
            print("Выстрел вне доски")
        else:
            for ship in self.my_ships:
                if dot in ship.dots:
                    ship.free_dots -= 1
                    self.board_coord[dot.x][dot.y] = "X"
                    if ship.free_dots == 0:
                        self.count += 1
                        print("Убит!")
                        return False
                    else:
                        print("Ранен")
                        return True
                else:
                    self.board_coord[dot.x][dot.y] = "T"
                    print("Мимо!")
                    return False

    def begin(self):
        self.busy = []

# print()
# print()
# board1 = Board(False)
# board2 = Board(False)
# ship1 = Ship(2, [1, 1], "gfhjg")
# ship2 = Ship(1, [3, 5], "jhj")
# board1.add_ship(ship1)
# print(board1.show_board())

class Player:
    def __init__(self, my_board, opp_board):
        self.my_board = my_board
        self.opp_board = opp_board

    def ask(self):
        raise NotImplementedException()

    def move(self):
        while True:
            try:
                dot = self.ask()
                a = self.opp_board.shot(dot)
                if a is False:
                    break
            except BoardOutException as e:
                print(e)


class AI(Player):
    def ask(self):
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)

class User(Player):
    def ask(self):
        x = int(input("Введите х"))
        y = int(input("Введите y"))
        return Dot(x, y)

# print()
# print()
# board1 = Board(False)
# board2 = Board(False)
# ship1 = Ship(3, [1, 1], "gfhjg")
# ship2 = Ship(1, [3, 5], "jhj")
# board1.add_ship(ship1)
# player2 = AI(board2, board1)
# print(player2.move())
#
# print(ship1.free_dots)
# print(board1.show_board())

class Game:
    def __init__(self):
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        a = ["horizontal", "vertical"]
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, [random.randrange(6), random.randrange(6)], random.choice(a))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-------------------")
        print("Приветствуем в игре")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.my_board.show_board())
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.my_board.show_board())
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.my_board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.my_board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()