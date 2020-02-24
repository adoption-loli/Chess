from pprint import *
from math import *
import pygame


def between(start_point, end_point, chessboard):
    '''
    返回中间是否有棋子, 末尾是否是己方棋子
    :param start_point: 起始点
    :param end_point: 结束点
    :param chessboard: 棋盘
    :return: True表示无棋子
    '''
    res = []
    y1, x1 = start_point  # [0, 2]
    y2, x2 = end_point  # [6, 8]
    # 斜线情况
    try:
        k = (y1 - y2) / (x1 - x2)
        b = y1 - k * x1
        xmax = max(start_point[1], end_point[1])
        xmin = min(start_point[1], end_point[1])
        print('y={k}x+{b}\n'.format(k=k, b=b), start_point, end_point)
        for cell in range(xmin, xmax + 1):
            res.append([int(cell * k + b), cell])
    except:
        # 直线情况
        if y1 == y2:
            # 横线
            xmax = max(start_point[1], end_point[1])
            xmin = min(start_point[1], end_point[1])
            print('y={y}\n'.format(y=y1), start_point, end_point)
            for cell in range(xmin, xmax + 1):
                res.append([y1, cell])
        else:
            # 竖线
            ymax = max(start_point[0], end_point[0])
            ymin = min(start_point[0], end_point[0])
            print('x={x}\n'.format(x=x1), start_point, end_point)
            for cell in range(ymin, ymax + 1):
                res.append([cell, x1])
    print(res[1:])
    for cell in res[1:-1]:
        if chessboard[cell[0]][cell[1]].attr:
            return True
    if chessboard[res[-1][0]][res[-1][1]].attr == chessboard[res[0][0]][res[0][1]].attr:
        return True
    return False


class game():
    def __init__(self):
        self.blank = blank()
        self.chessboard = [[self.blank for y in range(8)] for x in range(8)]
        self.pieces = {
            'wk': King_white(),
            'wq': Queen_white(),
            'wr1': Rook_white(),
            'wr2': Rook_white(),
            'wb1': Bishop_white(),
            'wb2': Bishop_white(),
            'wn1': Knight_white(),
            'wn2': Knight_white(),
            'wp1': Pawn_white(),
            'wp2': Pawn_white(),
            'wp3': Pawn_white(),
            'wp4': Pawn_white(),
            'wp5': Pawn_white(),
            'wp6': Pawn_white(),
            'wp7': Pawn_white(),
            'wp8': Pawn_white(),

            'bk': King_black(),
            'bq': Queen_black(),
            'br1': Rook_black(),
            'br2': Rook_black(),
            'bb1': Bishop_black(),
            'bb2': Bishop_black(),
            'bn1': Knight_black(),
            'bn2': Knight_black(),
            'bp1': Pawn_black(),
            'bp2': Pawn_black(),
            'bp3': Pawn_black(),
            'bp4': Pawn_black(),
            'bp5': Pawn_black(),
            'bp6': Pawn_black(),
            'bp7': Pawn_black(),
            'bp8': Pawn_black(),
        }

        self.chessboard[0][0] = self.pieces['br1']
        self.pieces['br1'].pos = [0, 0]
        self.chessboard[0][7] = self.pieces['br2']
        self.pieces['br2'].pos = [0, 7]
        self.chessboard[7][0] = self.pieces['wr1']
        self.pieces['wr1'].pos = [7, 0]
        self.chessboard[7][7] = self.pieces['wr2']
        self.pieces['wr2'].pos = [7, 7]

        self.chessboard[0][1] = self.pieces['bn1']
        self.pieces['bn1'].pos = [0, 1]
        self.chessboard[0][6] = self.pieces['bn2']
        self.pieces['bn2'].pos = [0, 6]
        self.chessboard[7][1] = self.pieces['wn1']
        self.pieces['wn1'].pos = [7, 1]
        self.chessboard[7][6] = self.pieces['wn2']
        self.pieces['wn2'].pos = [7, 6]

        self.chessboard[0][2] = self.pieces['bb1']
        self.pieces['bb1'].pos = [0, 2]
        self.chessboard[0][5] = self.pieces['bb2']
        self.pieces['bb2'].pos = [0, 5]
        self.chessboard[7][2] = self.pieces['wb1']
        self.pieces['wb1'].pos = [7, 2]
        self.chessboard[7][5] = self.pieces['wb2']
        self.pieces['wb2'].pos = [7, 5]

        self.chessboard[0][4] = self.pieces['bk']
        self.pieces['bk'].pos = [0, 4]
        self.chessboard[7][4] = self.pieces['wk']
        self.pieces['wk'].pos = [7, 4]

        self.chessboard[0][3] = self.pieces['bq']
        self.pieces['bq'].pos = [0, 3]
        self.chessboard[7][3] = self.pieces['wq']
        self.pieces['wq'].pos = [7, 3]
        for i in range(1, 9):
            self.chessboard[1][i - 1] = self.pieces['bp' + str(i)]
            self.pieces['bp' + str(i)].pos = [1, i - 1]
            self.chessboard[-2][i - 1] = self.pieces['wp' + str(i)]
            self.pieces['wp' + str(i)].pos = [-2, i - 1]
        self.board_range = []
        for y in range(8):
            for x in range(8):
                self.board_range.append([y, x])

    def draw(self):
        # 显示棋盘
        showboard = [[self.blank for y in range(8)] for x in range(8)]
        for pieces in self.pieces:
            if self.pieces[pieces].alive:
                showboard[self.pieces[pieces].pos[0]][self.pieces[pieces].pos[1]] = self.pieces[pieces]
        self.chessboard = showboard
        if __name__ == '__main__':
            for row in showboard:
                for col in row:
                    print('%4s' % col.name, end='')
                print('')

    def player(self, x, y, tx, ty):
        # 玩家落子
        # x = int(input('x：')) - 1
        # y = int(input('y：')) - 1
        start_point = [y, x]
        # print('to')
        # tx = int(input('x：')) - 1
        # ty = int(input('y：')) - 1
        end_point = [ty, tx]
        # 调用检查落子函数
        if self.inboard(end_point) and self.chessboard[y][x].attr:
            if self.chessboard[ty][tx].attr:
                if self.chessboard[ty][tx].attr == self.chessboard[y][x].attr:
                    return False
            if self.chessboard[y][x].move(start_point, end_point, self.chessboard):
                # 成功移动判断是否吃子
                if self.chessboard[ty][tx].attr:
                    self.chessboard[ty][tx].die()
                    return '{attr}{name}被吃了'.format(attr=self.chessboard[ty][tx].attr,
                                                    name=self.chessboard[ty][tx].name)
                return True
        return False

    def computer(self):
        # 电脑落子
        pass

    def inboard(self, end_point):
        # 检查落子范围是否在棋盘内
        if end_point in self.board_range:
            return True
        return False

    def promotion(self):
        for i in range(8):
            if self.chessboard[0][i].attr == '白' and self.chessboard[0][i].name == '兵':
                return [0, i]
            if self.chessboard[7][i].attr == '黑' and self.chessboard[7][i].name == '兵':
                return [7, i]
        return False

    def game_over(self):
        if not (self.pieces['bk'].alive):
            return '白棋获胜'
        if not (self.pieces['wk'].alive):
            return '黑棋获胜'
        return False

    def get_chess(self, pos):
        aim = self.chessboard[pos[0]][pos[1]]
        for cell in self.pieces:
            if self.pieces[cell] == aim:
                return cell


class King_white():
    def __init__(self):
        self.name = '王'
        self.attr = '白'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/white_king.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        if fabs(start_point[0] - end_point[0]) <= 1 and fabs(start_point[1] - end_point[1]):
            self.pos = end_point
            return True
        else:
            return False

    def die(self):
        # 被吃
        self.alive = False


class Queen_white():
    def __init__(self):
        self.name = '后'
        self.attr = '白'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/white_queen.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        # 横着走
        if start_point[0] == end_point[0]:
            # 检查中间是否有障碍
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        # 竖着走
        if start_point[1] == end_point[1]:
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        # 斜着走
        if fabs(start_point[0] - end_point[0]) == fabs(start_point[1] - end_point[1]):
            if between(start_point, end_point, chessboard):
                return False
            self.pos = end_point
            return True

    def die(self):
        self.alive = False


class Rook_white():
    def __init__(self):
        self.name = '车'
        self.attr = '白'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/white_rook.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        if start_point[0] == end_point[0]:
            # 检查中间是否有障碍
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        # 竖着走
        if start_point[1] == end_point[1]:
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        pass

    def die(self):
        self.alive = False


class Bishop_white():
    def __init__(self):
        self.name = '象'
        self.attr = '白'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/white_bishop.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 斜着走
        if fabs(start_point[0] - end_point[0]) == fabs(start_point[1] - end_point[1]):
            if between(start_point, end_point, chessboard):
                return False
            self.pos = end_point
            return True

    def die(self):
        self.alive = False


class Knight_white():
    def __init__(self):
        self.name = '马'
        self.attr = '白'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/white_knight.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        rule = [(1, 2), (2, 1)]
        if (fabs(start_point[0] - end_point[0]), fabs(start_point[1] - end_point[1])) in rule:
            self.pos = end_point
            return True

    def die(self):
        self.alive = False


class Pawn_white():
    def __init__(self):
        self.name = '兵'
        self.attr = '白'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/white_pawn.png').convert_alpha()
        self.first = True

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        # 向上走 (白兵是向上走)
        if start_point[1] == end_point[1]:
            if end_point[0] - start_point[0] == -1:
                if chessboard[end_point[0]][end_point[1]].attr:
                    return False
                self.pos = end_point
                self.first = False
                return True
        # 斜着走（白兵斜上方吃）
        if end_point[0] - start_point[0] == -1:
            if fabs(start_point[1] - end_point[1]) == 1:
                if chessboard[end_point[0]][end_point[1]].attr:
                    self.pos = end_point
                    self.first = False
                    return True
                return False
        if self.first:
            # 向下走两步
            if start_point[1] == end_point[1]:
                if end_point[0] - start_point[0] == -2:
                    if chessboard[end_point[0]][end_point[1]].attr:
                        return False
                    self.pos = end_point
                    self.first = False
                    return True
        return False

    def die(self):
        # 被吃
        self.alive = False


class King_black():
    def __init__(self):
        self.name = '王'
        self.attr = '黑'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/black_king.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        if fabs(start_point[0] - end_point[0]) <= 1 and fabs(start_point[1] - end_point[1]):
            self.pos = end_point
            return True
        else:
            return False

    def die(self):
        # 被吃
        self.alive = False


class Queen_black():
    def __init__(self):
        self.name = '后'
        self.attr = '黑'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/black_queen.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        # 横着走
        if start_point[0] == end_point[0]:
            # 检查中间是否有障碍
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        # 竖着走
        if start_point[1] == end_point[1]:
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        # 斜着走
        if fabs(start_point[0] - end_point[0]) == fabs(start_point[1] - end_point[1]):
            if between(start_point, end_point, chessboard):
                return False
            self.pos = end_point
            return True

    def die(self):
        self.alive = False


class Rook_black():
    def __init__(self):
        self.name = '车'
        self.attr = '黑'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/black_rook.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        if start_point[0] == end_point[0]:
            # 检查中间是否有障碍
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        # 竖着走
        if start_point[1] == end_point[1]:
            if between(start_point, end_point, chessboard):
                return False
            # 无障碍
            self.pos = end_point
            return True
        return False

    def die(self):
        self.alive = False


class Bishop_black():
    def __init__(self):
        self.name = '象'
        self.attr = '黑'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/black_bishop.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 斜着走
        if fabs(start_point[0] - end_point[0]) == fabs(start_point[1] - end_point[1]):
            if between(start_point, end_point, chessboard):
                return False
            self.pos = end_point
            return True

    def die(self):
        self.alive = False


class Knight_black():
    def __init__(self):
        self.name = '马'
        self.attr = '黑'
        self.alive = True
        self.pos = None
        self.img = pygame.image.load('imgs/black_knight.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        rule = [(1, 2), (2, 1)]
        if (fabs(start_point[0] - end_point[0]), fabs(start_point[1] - end_point[1])) in rule:
            self.pos = end_point
            return True

    def die(self):
        self.alive = False


class Pawn_black():
    def __init__(self):
        self.name = '兵'
        self.attr = '黑'
        self.alive = True
        self.pos = None
        self.first = True
        self.img = pygame.image.load('imgs/black_pawn.png').convert_alpha()

    def move(self, start_point, end_point, chessboard):
        # 移动棋子
        # 向下走
        if start_point[1] == end_point[1]:
            if end_point[0] - start_point[0] == 1:
                if chessboard[end_point[0]][end_point[1]].attr:
                    return False
                self.pos = end_point
                self.first = False
                return True
        # 斜着走（黑兵斜下方吃）
        if end_point[0] - start_point[0] == 1:
            if fabs(start_point[1] - end_point[1]) == 1:
                if chessboard[end_point[0]][end_point[1]].attr:
                    self.pos = end_point
                    self.first = False
                    return True
                return False
        if self.first:
            # 向下走两步
            if start_point[1] == end_point[1]:
                if end_point[0] - start_point[0] == 2:
                    if chessboard[end_point[0]][end_point[1]].attr:
                        return False
                    self.pos = end_point
                    self.first = False
                    return True
        return False

    def die(self):
        # 被吃
        self.alive = False


class blank():
    def __init__(self):
        self.name = '·'
        self.attr = None


if __name__ == '__main__':
    test = game()
    test.draw()
    while True:
        print(test.player())
        test.draw()
        if test.game_over():
            break
