import pygame
from pygame.locals import *
import chess
import sys

pygame.init()
bg_size = (800, 690)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('将来做成萝莉象棋')
font = pygame.font.Font('msyhbd.ttf', 25)
font_slim = pygame.font.Font('msyh.ttf', 25)


def draw_chessborad():
    pygame.draw.rect(screen, BLACK, (0, 0, 690, 690))
    pygame.draw.rect(screen, WHITE, (18, 18, 654, 654))
    pygame.draw.rect(screen, (55, 55, 55), (21, 21, 648, 648))
    for row in range(8):
        for col in range(8):
            if (row + col) % 2:
                pygame.draw.rect(screen, BLACK, (25 + 80 * col, 25 + 80 * row, 80, 80))
            else:
                pygame.draw.rect(screen, WHITE, (25 + 80 * col, 25 + 80 * row, 80, 80))


def main():
    clock = pygame.time.Clock()
    game = chess.game()
    selected_chess = False
    selected_pos = []
    round = '白'
    gameover = False
    delay = 30 * 3
    die_code = ''
    score = {'black': 0, 'white': 0}
    promotion = False
    promotion_choies = [chess.Queen_white(), chess.Bishop_white(), chess.King_white(), chess.Rook_white(),
                        chess.Queen_black(), chess.Bishop_black(), chess.King_black(), chess.Rook_black()]
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                die_code += '%c' % event.key
                if 'whitewin' in die_code:
                    game.pieces['bk'].alive = False
                    die_code = ''
                elif 'blackwin' in die_code:
                    game.pieces['wk'].alive = False
                    die_code = ''
                elif 'whitepromotion' in die_code:
                    for cell in range(1, 9):
                        pos = game.pieces['wp' + str(cell)].pos
                        game.pieces['wp' + str(cell)] = chess.Queen_white()
                        game.pieces['wp' + str(cell)].pos = pos
                    die_code = ''
                elif 'blackpromotion' in die_code:
                    for cell in range(1, 9):
                        pos = game.pieces['bp' + str(cell)].pos
                        game.pieces['bp' + str(cell)] = chess.Queen_black()
                        game.pieces['bp' + str(cell)].pos = pos
                    die_code = ''
                if len(die_code) >= 64:
                    die_code = ''
            if event.type == MOUSEBUTTONDOWN and not gameover:
                if event.button == 1 and promotion:
                    pos = event.pos
                    aim = (pos[1] - 420) // 40
                    if aim >= 0 and aim < 4 and pos[0] > 680 and pos[0] < 780:
                        # 此处因为回合提前发生了变化，因此反向改变
                        if round == '黑':
                            promotion_aim = promotion_choies[aim]
                        else:
                            promotion_aim = promotion_choies[aim + 4]
                        promotion_aim.pos = promotion
                        game.pieces[game.get_chess(promotion)] = promotion_aim
                        promotion = False
                if event.button == 1 and not promotion:
                    pos = event.pos
                    x, y = (pos[0] - 25) // 80, (pos[1] - 25) // 80
                    if x < 0 or x > 7 or y < 0 or y > 7:
                        pass
                    else:
                        if game.chessboard[y][x].attr and not selected_chess:
                            if game.chessboard[y][x].attr == round:
                                print('{attr}{name}被选中'.format(attr=game.chessboard[y][x].attr,
                                                               name=game.chessboard[y][x].name))
                                sx, sy = x, y
                                selected_pos = [x, y]
                                selected_chess = True
                            else:
                                print('未选中任何{round}棋'.format(round=round))
                        elif selected_chess:
                            tx, ty = x, y
                            selected_chess = False
                            selected_pos = []
                            if game.player(sx, sy, tx, ty):
                                if round == '白':
                                    round = '黑'
                                else:
                                    round = '白'
        # 画棋盘
        screen.fill(BLACK)
        draw_chessborad()
        # 画选中区域
        if selected_pos:
            pygame.draw.rect(screen, (99, 99, 99), (25 + 80 * selected_pos[0], 25 + 80 * selected_pos[1], 80, 80))
        pos = pygame.mouse.get_pos()
        x, y = (pos[0] - 25) // 80, (pos[1] - 25) // 80
        if x < 0 or x > 7 or y < 0 or y > 7:
            pass
        else:
            pygame.draw.rect(screen, (170, 170, 170), (25 + 80 * x, 25 + 80 * y, 80, 80))
        game.draw()
        # 画棋子
        for row in range(8):
            for col in range(8):
                if game.chessboard[row][col].attr:
                    aim_img = pygame.transform.scale(game.chessboard[row][col].img, (80, 80))
                    screen.blit(aim_img, (25 + 80 * col, 25 + 80 * row))
        # 画计分板
        pygame.draw.rect(screen, WHITE, (680, 20, 110, 150), 4)
        font_round = font_slim.render(round + '棋行', True, WHITE)
        score_white = str(score['white'])
        score_black = str(score['black'])
        score_white = font_slim.render('白:' + score_white, True, WHITE)
        score_black = font_slim.render('黑:' + score_black, True, WHITE)
        screen.blit(font_round, (700, 25))
        screen.blit(score_white, (690, 70))
        screen.blit(score_black, (690, 110))
        # 兵升变
        promotion = game.promotion()
        if promotion:
            pygame.draw.rect(screen, WHITE, (680, 400, 110, 200), 4)
            choies = ['皇后', '象', '马', '车']
            if pos[0] > 680 and pos[0] < 780 and pos[1] > 420 and pos[1] < 580:
                pygame.draw.rect(screen, (99, 99, 99), (684, (pos[1] - 420) // 40 * 40 + 420, 100, 40))
            for i in range(4):
                choies[i] = font_slim.render(choies[i], True, WHITE)
                screen.blit(choies[i], (690, 420 + 40 * i))
        if game.game_over():
            win = font.render(' '.join(game.game_over()), True, BLACK)
            if game.game_over()[0] == '白':
                score['white'] += 1
            elif game.game_over()[0] == '黑':
                score['black'] += 1
            round = '白'
            gameover = True
            delay = 30 * 3
            game.__init__()
        if gameover:
            pygame.draw.rect(screen, BLACK, (195, 315, 300, 60))
            pygame.draw.rect(screen, WHITE, (196, 316, 298, 58))
            screen.blit(win, (280, 325))
            delay -= 1
            if not delay:
                gameover = False

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
