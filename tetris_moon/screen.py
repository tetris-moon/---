import pygame
import sys
import single.game as game
import online.online as online

# 기본 설정
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
FPS = 60
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Menu")
clock = pygame.time.Clock()
playing = True

# 색상
WHITE = (255, 255, 255)
BOX_COLOR = (245, 238, 230)       # 기본 버튼 색
HOVER_COLOR = (220, 200, 180)     # hover 시 버튼 색
CLICK_COLOR = (180, 160, 140)     # 클릭 시 버튼 색
BORDER_COLOR = (80, 50, 20)
TEXT_COLOR = (40, 20, 10)
    
# 폰트
font_name = "malgungothic"
title_font = pygame.font.Font("fonts/DepartureMono-Regular.otf", 64)
option_font = pygame.font.SysFont(font_name, 36, bold=True)

# 제목
title_surf = title_font.render("TETRIS", True, (0, 0, 0))
title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))

# 버튼 텍스트
online_surf = option_font.render("Online", True, TEXT_COLOR)
offline_surf = option_font.render("Solo", True, TEXT_COLOR)
exit_surf = option_font.render("Exit", True, TEXT_COLOR)  

# 박스 크기 절반 줄이기
pad_x, pad_y = 10, 6
spacing = 20
box_w = max(online_surf.get_width(), offline_surf.get_width(), exit_surf.get_width()) + pad_x*2
box_h = online_surf.get_height() + pad_y*2

total_w = box_w*2 + spacing
start_x = (SCREEN_WIDTH - total_w)//2
y_top = SCREEN_HEIGHT//2 - box_h - spacing//2
y_bottom = y_top + box_h + spacing

# 버튼 Rect
online_box = pygame.Rect(start_x, y_top, box_w, box_h)
offline_box = pygame.Rect(start_x + box_w + spacing, y_top, box_w, box_h)
exit_box = pygame.Rect(SCREEN_WIDTH//2 - box_w//2, y_bottom, box_w, box_h)

boxes = [online_box, offline_box, exit_box]
labels = [online_surf, offline_surf, exit_surf]
actions = ["online", "solo", "exit"]

# 클릭 상태 추적
clicked_index = None

while playing:
    mouse_pos = pygame.mouse.get_pos()  # 마우스 위치 가져오기

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(boxes):
                if r.collidepoint(mouse_pos):
                    clicked_index = i  # 어떤 버튼 클릭했는지 저장

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if clicked_index is not None:
                if boxes[clicked_index].collidepoint(mouse_pos):
                    if actions[clicked_index] == "solo":
                        game.main()
                    elif actions[clicked_index] == "online":
                        online.main()
                    print(f"{actions[clicked_index]} 버튼 클릭됨!")
                    if actions[clicked_index] == "exit":
                        playing = False
            clicked_index = None  # 클릭 해제

    # 화면 채우기
    screen.fill(WHITE)

    # 제목
    screen.blit(title_surf, title_rect)

    # 버튼
    for i, r in enumerate(boxes):
        if clicked_index == i:  # 클릭 중
            draw_rect = r.inflate(-2, -2)  # 눌리면 살짝 작아짐 (절반만 축소)
            color = CLICK_COLOR
        elif r.collidepoint(mouse_pos):  # hover
            draw_rect = r.inflate(10, 10)
            color = HOVER_COLOR
        else:  # 기본
            draw_rect = r
            color = BOX_COLOR

        pygame.draw.rect(screen, color, draw_rect, border_radius=8)
        pygame.draw.rect(screen, BORDER_COLOR, draw_rect, width=3, border_radius=8)

        # 텍스트 중앙 정렬
        label = labels[i]
        label_pos = (draw_rect.centerx - label.get_width()//2,
                     draw_rect.centery - label.get_height()//2)
        screen.blit(label, label_pos)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
sys.exit()