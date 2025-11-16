from gzip import WRITE
import pygame
import sys
import os
import random
from block import Block
from colors import BLACK, BLUE, WHITE, GOLD, GRAY, AQUA, VIOLET , LIME , ORANGE , RED
FPS = 60 #Frame per Second 1초당 Frame 의 재생 률.
MAX_WIDTH = 500 #화면 너비 500
MAX_HEIGHT = 600 #화면 높이 600
cnt = 0
pygame.init()
font = pygame.font.SysFont(None, 30)

keep = None #홀드한 블록이 들어갈 곳
Canhold = True #홀드 할 수 있나? 검사

# ARCADE.TTF 경로 지정 (game.py 기준)
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "fonts", "ARCADE.TTF")

# font1 (ARCADE.TTF 없으면 기본 폰트로 대체)
if os.path.exists(font_path):
    font1 = pygame.font.Font(font_path, 24)
else:
    font1 = pygame.font.SysFont("malgungothic", 24)
class Map():
    current_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()
    score = (current_time - start_time) //1000###점수 시스템 바꾸기
    score_text1 = font.render("SCORE", True, WHITE)
    score_text2 = font.render(f"{score}", True, WHITE)

    def __init__(self):
        self.blockState=[]  
        self.initBlockState()
        self.pause = False

    def initBlockState(self):
        self.blockState =[[0]*10 for _ in range(20)]

    def checkLine(self, blockState):
        for a in range(int(len(blockState))):
            cnt = 0
            for b in range(int(len(blockState[a]))):
                if blockState[a][b] != 0:
                    cnt += 1
            if cnt == 10:
                blockState[a] = [0]*10
                for i in range(a, 0, -1):
                    blockState[i] = blockState[i - 1][:]
                    blockState[0] = [0]*10
    def draw(self):
        for i in range(len(self.blockState)):
            for j in range(len(self.blockState[i])):
                if self.blockState[i][j] == 1:
                    pygame.draw.rect(screen, GOLD , (j *30,i * 30,30,30))
                elif self.blockState[i][j] == 2:
                   pygame.draw.rect(screen, BLUE , (j *30,i * 30,30,30))
                elif self.blockState[i][j] == 3:
                   pygame.draw.rect(screen, ORANGE , (j *30,i * 30,30,30))
                elif self.blockState[i][j] == 4:
                   pygame.draw.rect(screen, LIME , (j *30,i * 30,30,30))
                elif self.blockState[i][j] == 5:
                   pygame.draw.rect(screen, RED , (j *30,i * 30,30,30))
                elif self.blockState[i][j] == 6:
                   pygame.draw.rect(screen, VIOLET , (j *30,i * 30,30,30))
                elif self.blockState[i][j] == 7:
                   pygame.draw.rect(screen, AQUA , (j *30,i * 30,30,30))
#============================
#그리기
#============================
    def draw_info(self,screen,game_surface, start_time, score , next_block_type , keep): #점수판 그리기 , 다음 블록 그리기

        pygame.draw.rect(screen,BLACK,(300,0,180,600))
        block.draw(screen=game_surface)
        score_text1 = font.render("SCORE", True, WHITE)
        score_text2 = font.render(f"{score}", True, WHITE)
        screen.blit(score_text1, (320, 30))  # 첫 줄
        screen.blit(score_text2, (320, 60))  # 두 번째 줄, y좌표 조절
        screen.blit(game_surface, (0, 0)) 

        common_x = 320 # 오른쪽 미리보기 글자 좌표
        next_y = 150 # 미리보기 글자 y
        hold_y = 400 #hold y
 # temp 블록 그리기 (미리보기)
        temp_block = Block(next_block_type) #미리보기 블록

        # BLOCK_COORDS 기준으로 임시 위치로 이동
        min_x = min(temp_block.x1, temp_block.x2, temp_block.x3, temp_block.x4)
        min_y = min(temp_block.y1, temp_block.y2, temp_block.y3, temp_block.y4)

        dx = common_x - min_x #temp
        dy = next_y - min_y
        # 미리보기 블록의 x,y
        temp_block.x1 += dx
        temp_block.x2 += dx
        temp_block.x3 += dx
        temp_block.x4 += dx

        temp_block.y1 += dy
        temp_block.y2 += dy
        temp_block.y3 += dy
        temp_block.y4 += dy
        #블록 그리기
        temp_block.draw(screen)
        # NEXT 텍스트 표시
        next_text = font.render("NEXT", True, WHITE)
        screen.blit(next_text, (common_x, next_y - 40))

# hold 블록 그리기
        if keep is not None:
            hold_block = Block(keep) #홀드 된 블록
            min_x = min(hold_block.x1, hold_block.x2, hold_block.x3, hold_block.x4)
            min_y = min(hold_block.y1, hold_block.y2, hold_block.y3, hold_block.y4)
            
            hx = common_x - min_x #hold
            hy = hold_y - min_y

            # hold 된 블록의 x,y
            hold_block.x1 += hx
            hold_block.x2 += hx
            hold_block.x3 += hx
            hold_block.x4 += hx

            hold_block.y1 += hy
            hold_block.y2 += hy
            hold_block.y3 += hy
            hold_block.y4 += hy
            #블록 그리기
            hold_block.draw(screen)
            # HOLDING 텍스트 표시
            hold_text = font.render("HOLDING", True,WHITE)
            screen.blit(hold_text, (common_x, hold_y - 40))
#============================
#블록 타입
#============================

map = Map()
current_block_type = random.randint(1,7) * 10
next_block_type = random.randint(1,7) * 10  #미리만들기
block = Block(current_block_type)
#init_block_type = 60 #정하기
next_block = Block(next_block_type)
clock = pygame.time.Clock() #모듈, 라이브러리
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT)) #보여질 screen 설정.
game_surface = pygame.Surface((300, 600))
score_file_path = "records/highscore.txt"

#============================
#최고점수
#============================
def save_highscore(new_score): #저장
    with open(score_file_path, "w") as f:
        f.write(str(new_score))


def load_highscore(): #불러옥;
    try:
        with open(score_file_path, "r") as f:
            highscore = int(f.read())
    except FileNotFoundError:  # 파일 없으면 0
        highscore = 0
    return highscore

#============================
#메인 로직
#============================

def main():
    global cnt , block ,next_block,next_block_type, keep
    start_time = pygame.time.get_ticks()
    while True:
        x = block.x1 // 30
        y = block.y1 // 30
        cnt += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for i in range(len(map.blockState)):
                    print(map.blockState[i])
                pygame.quit()
                sys.exit()   

            if event.type == pygame.KEYDOWN and block.is_moving:#방향키 왼쪽
                if event.key == pygame.K_LEFT:
                    block.moveLeft(map.blockState)
                    blockIdx = block.getIndexFromPos()
                    try:
                        map.blockState[blockIdx[0][1]][blockIdx[0][0]]
                        map.blockState[blockIdx[1][1]][blockIdx[1][0]]
                        map.blockState[blockIdx[2][1]][blockIdx[2][0]]
                        map.blockState[blockIdx[3][1]][blockIdx[3][0]]
                    except IndexError: 
                        block.moveRight(map.blockState)

                elif event.key == pygame.K_RIGHT:#방향키 오른쪽
                    block.moveRight(map.blockState)
                    blockIdx = block.getIndexFromPos()
                    try:
                        map.blockState[blockIdx[0][1]][blockIdx[0][0]]
                        map.blockState[blockIdx[1][1]][blockIdx[1][0]]
                        map.blockState[blockIdx[2][1]][blockIdx[2][0]]
                        map.blockState[blockIdx[3][1]][blockIdx[3][0]]
                    except IndexError:
                        block.moveLeft(map.blockState)

                elif event.key == pygame.K_UP:#방향키 위쪽 / 로테이트
                    block.rotate(map)
                    block.rotate_numbers()
                    
                elif event.key == pygame.K_SPACE:#스페이스 바 / 하드드랍
                    block.HardDrop(map)
                

                elif event.key == pygame.K_c:
                    if Canhold:  # 홀드
                        if keep is None:
                            keep = block.block_type #keep에 넣기
                            current_block_type = next_block_type #현재 블록 다음 블록으로
                            block = Block(current_block_type) #새 블록
                            next_block_type = random.randint(1,7)*10
                            print(f"keep:{keep}")
                        else:
                            temp = keep
                            print(temp)
                            keep = block.block_type
                            block = Block(temp) #홀드 된 블록으로 교체
                            print(f"keep:{keep}")
                        Canhold = False #홀드 후 떨어질 때까지 다시 홀드 못함

        keys = pygame.key.get_pressed()#방향키 아래쪽
        if keys[pygame.K_DOWN] and block.is_moving:
            if block.isGround(map):  # 내려갈 수 있으면
                    block.is_moving = False
            else:
                block.y1 += 30
                block.y2 += 30
                block.y3 += 30
                block.y4 += 30

        current_time = pygame.time.get_ticks()
        score = (current_time - start_time) //1000
        clock.tick(FPS) #그리기는 여기 밑에서
        screen.fill(WHITE) #항상 그리기는 여기밑에서 시작 (self.blockState=[]) <-- 리스트
        game_surface.fill(GRAY)

        block.move(cnt, map)
        map.checkLine(map.blockState)

        map.draw_info(screen, game_surface, start_time, score, next_block_type, keep)
        map.draw()

        if block.is_moving == False:
            current_block_type = next_block_type
            block= Block(current_block_type)
            next_block_type= random.randint(1,7)*10  #블록 땅에 닿으면 랜덤으로 뽑기'
            Canhold = True
            print(next_block_type)
        for i in range(10):
            if map.blockState[0][i] != 0:
                highscore = load_highscore() # 최고 기록 불러오기
                if score > highscore:
                    save_highscore(score)
                    print("최고 기록 갱신!")
                print("이전 최고 기록 :",highscore,"점") #대충 이런 식으로 이전 기록 최고 기록 보여주고 그 최고 기록보다 이번 점수가 높으면 점수 갱신
                print("이번 기록 :",score,"점") #이전 기록은 새 변수 또는 파일 만들어서 저장, 꺼내 쓰기,그리고 지금 print 하는거 score 처럼 화면에 띄우기 <-- 이전 공룡게임과 비슷,종료 버튼 만들기
                print("Game Over")
                pygame.quit()
                sys.exit()
        if cnt >= 30:
            cnt = 0
        pygame.display.update()

if __name__ == '__main__':
    main()