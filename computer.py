from pprint import pprint
from copy import deepcopy
import chess


class computer():
    def __init__(self):
        self.chessboard = []
        self.board_range = []
        for y in range(8):
            for x in range(8):
                self.board_range.append([y, x])

    def inboard(self, end_point):
        # 检查落子范围是否在棋盘内
        if end_point in self.board_range:
            return True
        return False

    def white(self):
        pass

    def black(self, chessboard, All_steps):
        weight = []
        for row in All_steps:
            temp = []
            self.chessboard = self.virtual_chessboard(chessboard)
            for step in row[1]:
                self.player(row[0][1], row[0][0], step[0], step[1])
                weight_sum = 0
                for y in self.chessboard:
                    for cell in y:
                        if cell.alive:
                            weight_sum += cell.weight
                temp.append(weight_sum)
            t_min = min(temp)
            t_index = temp.index(t_min)
            weight.append([t_min, t_index])
        t_aim = min(weight)[1]
        aim = weight.index(min(weight))
        y, x = All_steps[aim][0]
        print(aim, t_aim, weight)
        tx, ty = All_steps[aim][1][t_aim]
        return x, y, tx, ty

    def virtual_chessboard(self, chessboard):
        # 创建虚拟棋盘
        virtual = [[chess.blank for y in range(8)] for x in range(8)]
        for row in range(8):
            for col in range(8):
                if chessboard[row][col].name == '兵':
                    if chessboard[row][col].attr == '黑':
                        virtual[row][col] = chess.Pawn_black()
                    else:
                        virtual[row][col] = chess.Pawn_white()
                elif chessboard[row][col].name == '车':
                    if chessboard[row][col].attr == '黑':
                        virtual[row][col] = chess.Rook_black()
                    else:
                        virtual[row][col] = chess.Rook_white()
                elif chessboard[row][col].name == '象':
                    if chessboard[row][col].attr == '黑':
                        virtual[row][col] = chess.Bishop_black()
                    else:
                        virtual[row][col] = chess.Bishop_white()
                elif chessboard[row][col].name == '马':
                    if chessboard[row][col].attr == '黑':
                        virtual[row][col] = chess.Knight_black()
                    else:
                        virtual[row][col] = chess.Knight_white()
                elif chessboard[row][col].name == '后':
                    if chessboard[row][col].attr == '黑':
                        virtual[row][col] = chess.Queen_black()
                    else:
                        virtual[row][col] = chess.Queen_white()
                elif chessboard[row][col].name == '王':
                    if chessboard[row][col].attr == '黑':
                        virtual[row][col] = chess.King_black()
                    else:
                        virtual[row][col] = chess.King_white()
                else:
                    virtual[row][col] = chess.blank()
                virtual[row][col].pos = [row, col]
        return virtual

    def player(self, x, y, tx, ty, virtual=False):
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
                if self.chessboard[ty][tx].attr and not virtual:
                    self.chessboard[ty][tx].die()
                    return '虚拟{attr}{name}被吃了'.format(attr=self.chessboard[ty][tx].attr,
                                                      name=self.chessboard[ty][tx].name)
                return True
        return False
