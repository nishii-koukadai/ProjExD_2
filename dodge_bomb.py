import os
import pygame as pg
import random
import sys
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    img = pg.image.load("fig/3.png")#標準状態のこうかとん
    img_r = pg.transform.flip(img, True, False)#反転した状態のこうかとん

    kk_dict = {
        (0, 0): pg.transform.rotozoom(img_r, 0, 0.9),     # キー押下がない場合（右向きをデフォルト）
        (+5, 0): pg.transform.rotozoom(img_r, 0, 0.9),    # 右
        (+5, -5): pg.transform.rotozoom(img_r, 45, 0.9),  # 右上（反時計回りに45度）
        (0, -5): pg.transform.rotozoom(img_r, 90, 0.9),   # 上
        (+5, +5): pg.transform.rotozoom(img_r, -45, 0.9), # 右下（時計回りに45度）
        (0, +5): pg.transform.rotozoom(img_r, -90, 0.9),  # 下
        (-5, 0): pg.transform.rotozoom(img, 0, 0.9),      # 左（元画像をそのまま使用）
        (-5, -5): pg.transform.rotozoom(img, -45, 0.9),   # 左上
        (-5, +5): pg.transform.rotozoom(img, 45, 0.9),    # 左下
    }
    return kk_dict


def check_bound(rect) -> tuple[bool,bool]:
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    #背景を描画
    bg_img = pg.Surface((WIDTH, HEIGHT)) 
    pg.draw.rect(bg_img, (0, 0, 0), (0,0,WIDTH, HEIGHT),0) 
    bg_img.set_alpha(200)
    #文字を表示
    screen.blit(bg_img, [0, 0])
    fonto = pg.font.Font(None, 80) 
    txt = fonto.render("Game Over", True, (255, 255, 255)) 
    screen.blit(txt, [400, 300])
    #こうかとんと反転したこうかとんを表示
    kk_img = pg.image.load("fig/3.png") 
    kk_img2 = pg.transform.flip(kk_img, True, False) 
    kk_img = pg.transform.rotozoom(kk_img, 10, 1.0)
    screen.blit(kk_img2, [300, 300])
    screen.blit(kk_img, [750, 300])
    pg.display.update()
    time.sleep(5)#五秒停止
    
    
def main():
    #キーボードで移動方向を決定する辞書
    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) 
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) 
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    clock = pg.time.Clock()
    tmr = 0
    vx = 5
    vy = 5

    kk_imgs = get_kk_imgs() #辞書を取得
    kk_img = kk_imgs[(0, 0)] #初期状態を指定

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        #画面外に行ったら向きを変える
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        kk_rct.move_ip(sum_mv)
        
        #画面外に行ったら向きを変える
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        
        #ゲームオーバー判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("game over")
            return
        
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx = -vx
        if not tate:
            vy = -vy
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
