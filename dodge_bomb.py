import random
import sys
import pygame as pg


# 練習4
delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0)
        }


def check_bound(scr_rect: pg.Rect, obj_rect: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外かを判定し、真理値タプルを返す関数
    引数１：画面SurfaceのRect
    引数２：こうかとん、または爆弾SurfaceのRect
    返り値：横方向、縦方向のはみ出し判定結果(画面内：True/画面外：False)
    """
    yoko, tate = True, True
    if (obj_rect.left < scr_rect.left or obj_rect.right > scr_rect.right):
        yoko = False
    if (obj_rect.top < scr_rect.top or obj_rect.bottom > scr_rect.bottom):
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    # 追加機能1
    kk_img_dict = {
        (0, -1): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90.0, 1.0),
        (+1, -1): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45.0, 1.0),
        (+1, 0): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0.0, 1.0),
        (+1, +1): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45.0, 1.0),
        (0, +1): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -90.0, 1.0),
        (-1, -1): pg.transform.rotozoom(kk_img, -45.0, 1.0),
        (-1, 0): pg.transform.rotozoom(kk_img, 0.0, 1.0),
        (-1, +1): pg.transform.rotozoom(kk_img, 45.0, 1.0)
    }
    kk_rect = kk_img.get_rect()  # 練習4
    kk_rect.center = 900, 400  # 練習4

    bb_img = pg.Surface((20, 20))  # 練習1
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習1
    bb_img.set_colorkey((0, 0, 0))  # 練習1
    x, y = random.randint(0, 1600), random.randint(0, 900)  # 練習2
    # screen.blit(bb_img, [x, y])  # 練習2
    vx, vy = +1, +1  # 練習3
    bb_rect = bb_img.get_rect()  # 練習3
    bb_rect.center = x, y  # 練習3
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        tmr += 1
        total_mvx, total_mvy = 0, 0
        # 練習4
        key_list = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_list[k]:
                kk_rect.move_ip(mv)
                total_mvx += mv[0]  # 追加機能1
                total_mvy += mv[1]  # 追加機能1
            # 練習5
            if check_bound(screen.get_rect(), kk_rect) != (True, True):
                kk_rect.move_ip(-mv[0], -mv[1])

        # 追加機能1
        for mvk, img in kk_img_dict.items():
            if (mvk == (total_mvx, total_mvy)):
                kk_img = img

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect)  # 練習4
        bb_rect.move_ip(vx, vy)  # 練習3
        yoko, tate = check_bound(screen.get_rect(), bb_rect)  # 練習5
        if not yoko:  # 練習5 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 練習5 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rect)  # 練習3
        if (kk_rect.colliderect(bb_rect)):  # 練習6
            return

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
