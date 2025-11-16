from gzip import WRITE
import pygame
import sys
import os
import random
from block import Block
import socket
import threading
import ast
from online.game_interface import Interface
from colors import BLACK, BLUE, WHITE, GOLD, GRAY, AQUA, VIOLET , LIME , ORANGE , RED
import json 

# 블럭 내려오는 

#=====+===============
#전역변수들
#=====================
FPS = 60 #Frame per Second 1초당 Frame 의 재생 률.
MAX_WIDTH = 1200 #화면 너비 1200
MAX_HEIGHT = 600 #화면 높이 400
cnt = 0
player_num = None #전역 변수 선언
game_started = False  #true가 되면 게임 시작
game_over = False #ture면 화면에 defeat
pygame.init()
font = pygame.font.SysFont(None, 30)

keep = None #홀드한 블록이 들어갈 곳 #고치기
Canhold = True #홀드 할 수 있나? 검사 #고치기

t = [0]*10 #상대 블록 스테이트를 담을 곳
 #상대 블록 스테이트
enemy_block_state = [[[0]*10 for _ in range(20)] for _ in range(6)] #상대 블록 스테이트
enemy_block_pos = [[(0, 0) for _ in range(4)] for _ in range(6)] #상대 실시간으로 떨어지고 있는 블록


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
    score = (current_time - start_time) //1000#########################점수 시스템 바꾸기
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
# 그리기
#============================
    def draw_info(self,screen,game_surface, score , next_block_type , keep): #점수판 그리기 , 다음 블록 그리기 , Hold블록 그리기

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


map = Map()
current_block_type = random.randint(1,7) * 10
next_block_type = random.randint(1,7) * 10  #다음 블록
block = Block(current_block_type)
next_block = Block(next_block_type)

clock = pygame.time.Clock() #모듈, 라이브러리
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT)) #보여질 screen 설정.
game_surface = pygame.Surface((300, 600))#이게 그건가
score_file_path = "records/highscore.txt"
interface = Interface()

#============================
# 대기 화면 
#============================

def draw_waiting_screen():
    overlay = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    overlay.set_alpha(150)        # 0~255, 150 정도면 살짝 비침
    overlay.fill((50, 50, 50))    # 회색
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.SysFont(None, 50)
    text = font.render("Waiting for Game Start...", True, (255, 255, 255)) #win인지 defeat인지 확인해서 고치기
    screen.blit(text, (MAX_WIDTH//2 - 200, MAX_HEIGHT//2 - 20))
    pygame.display.update()

def restart(): #재시작
    global map, current_block_type, next_block_type, block, Block, next_block, keep,Canhold, cnt, start_time
    map.blockState = [[0]*10 for _ in range(20)] 
    current_block_type = random.randint(1,7) * 10
    next_block_type = random.randint(1,7) * 10
    block = Block(current_block_type)
    next_block = Block(next_block_type)
    keep = None
    Canhold = True 
    cnt = 0
    start_time = pygame.time.get_ticks()
#============================
# 서버한테 받아오는 함수
#============================
def extract_json_list(raw_msg: str) -> list:
    result = []
    buffer = raw_msg
    start = None
    brace_count = 0

    for i, c in enumerate(buffer):
        if c == '{':
            if brace_count == 0:
                start = i
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0 and start is not None:
                json_str = buffer[start:i+1]
                try:
                    data = json.loads(json_str)
                    result.append(data)
                except json.JSONDecodeError:
                    # 잘못된 JSON은 무시
                    pass
                start = None
    return result

def receive_from_server(sock):  #여기 고치기
    global game_started, player_num, enemy_block_state, enemy_block_pos, game_over
    while True:
        try:
            raw_msg = sock.recv(4096).decode()
            if not raw_msg:
                print("[서버 연결 끊김]")
                break
            
            raw_msg = raw_msg.strip()
            if not raw_msg:
                continue
            print("[INFO] RAW_MSG:", raw_msg)
            # JSON 파싱
            result = extract_json_list(raw_msg=raw_msg)
            if not result:
                print(f"[서버] 올바르지 않은 메시지: {raw_msg}")
                continue

            for data in result:
                msg_type = data.get('msg')
                if msg_type == 1:  # 게임 시작
                    print("게임 시작 신호 받음")
                    restart()
                    game_started = True
                elif msg_type == 2:  # 게임 종료/중단
                    print("게임 종료/중단 신호 받음")
                    game_started = False
                elif msg_type == 3:  # 게임 종료
                    game_started = False
                elif msg_type == 4:  # 내 플레이어 번호
                    try:
                        player_num = data['player_id']
                        print(f"내 플레이어 번호: {player_num}")
                    except KeyError:
                        print("player_num 파싱 오류:", data)

                elif msg_type == "defeat":
                    if data['player_id'] == player_num:
                        game_over = True

                elif msg_type == 6: #blockState 
                    print("[INFO] ENEMY:",data['player_id'])
                    print("[INFO] ME:",player_num)
                    if data['player_id'] > player_num: #이상함...
                        enemy_block_state[data['player_id']-2] = data['blockState']
                        # for i in data['blockPos']:
                        #     # [120, 90], [120, 120], [120, 150], [120, 180]
                        #     #print(i)

                        #     enemy_block_state[data['player_id']-2][i[1] // 30][i[0] // 30] = 1

                        #enemy_block_pos[data['player_id']-2] = data['blockPos']
                    else:
                        enemy_block_state[data['player_id']-1] = data['blockState']
                        # for i in data['blockPos']:
                        #     # [120, 90], [120, 120], [120, 150], [120, 180]
                        #     #print(i)

                        #     enemy_block_state[data['player_id']-1][i[1] // 30][i[0] // 30] = 1

                        #enemy_block_pos[data['player_id']-1] = data['blockPos']
        except Exception as e:
            print("[EXCEPT] SOCKET DATA ISSUE: ", e)


#============================
# #메인 로직
#============================
def main():
    
    MAX_WIDTH = 1200
    screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT)) #보여질 screen 설정.
    send_cnt = 0
    global cnt , block ,next_block,next_block_type, keep, enemy_block_state , enemy_block_pos , clock, game_started
    start_time = pygame.time.get_ticks()

    # ========= 서버 연결 ===========
    host = "54.180.29.155"#host = ...
    port = 20001#...
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except:
        print("서버에 연결할 수 없습니다.")
        sys.exit()
    print("서버에 연결되었습니다.(Crtl+C로 종료)")
    receive_thread = threading.Thread(target=receive_from_server, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()
    threading.Thread(target=receive_from_server, args=(client,), daemon=True).start()


    while True:

        if game_over:
            
            screen.fill((100,100,100))
            font_defeat = pygame.font.Sysfont(None, 80)
            defeat_text = font_defeat.render("DEFEATED", True, (255,0,0))
            screen.blit(defeat_text , (MAX_WIDTH//2 - 100, MAX_HEIGHT//2 - 50))
            pygame.display.update()
            continue

        if not game_started:
            draw_waiting_screen()  # 대기 화면 갱신
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 여기서는 게임 시작 키 입력 무시하고 서버 Start 메시지만 기다림
            continue


        if send_cnt == 10:
            try:
                for i in block.info:
                    map.blockState[i[1]//30][i[0]//30] = 1

                map.blockState[block.y1 // 30][block.x1 // 30] = 1
                map.blockState[block.y2 // 30][block.x2 // 30] = 1
                map.blockState[block.y3 // 30][block.x3 // 30] = 1
                map.blockState[block.y4 // 30][block.x4 // 30] = 1
                msg_dict = {
                    "msg": 6,  # msg6 = 블록 정보
                    "player_id": player_num,  # 내 player 번호
                    "blockState": map.blockState,
                    # "blockPos": [
                    #     (block.x1, block.y1),
                    #     (block.x2, block.y2),
                    #     (block.x3, block.y3),
                    #     (block.x4, block.y4)
                    # ]
                }
                client.send(json.dumps(msg_dict).encode())
                
                map.blockState[block.y1 // 30][block.x1 // 30] = 0
                map.blockState[block.y2 // 30][block.x2 // 30] = 0
                map.blockState[block.y3 // 30][block.x3 // 30] = 0
                map.blockState[block.y4 // 30][block.x4 // 30] = 0

            except AttributeError:
                pass
            finally:
                send_cnt = 0
        else:
            send_cnt += 1

        cnt += 1 #이게 30이 되면 1칸 내림
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                        block.moveRight()

                elif event.key == pygame.K_RIGHT:#방향키 오른쪽
                    block.moveRight(map.blockState)
                    blockIdx = block.getIndexFromPos()
                    try:
                        map.blockState[blockIdx[0][1]][blockIdx[0][0]]
                        map.blockState[blockIdx[1][1]][blockIdx[1][0]]
                        map.blockState[blockIdx[2][1]][blockIdx[2][0]]
                        map.blockState[blockIdx[3][1]][blockIdx[3][0]]
                    except IndexError:
                        block.moveLeft()

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
                            print(f"temp : {temp}")
                            keep = block.block_type
                            block = Block(temp) #홀드 된 블록으로 교체
                            print(f"keep : {keep}")
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
        map.draw_info(screen, game_surface, score, next_block_type, keep)
        map.draw()
        interface.draw(screen)

        COLOR_MAP = {
                    1: GOLD,
                    2: BLUE,
                    3: ORANGE,
                    4: LIME,
                    5: RED,
                    6: VIOLET,
                    7: AQUA
                }
        
        # for i in range(len(enemy_block_pos)):
        #     for j in range(len(enemy_block_pos[i])):
        #         x,y = enemy_block_pos[i][j]
        #         screenx = interface.screens[i].screenx
        #         screeny = interface.screens[i].screeny
        #         pygame.draw.rect(screen, GOLD, (screenx + (x/3), screeny + (y/3), 10,10))


        
        # enemy_block_state 그리기
        for p in range(len(enemy_block_state)):
            for i in range(len(enemy_block_state[p])):  # 0~19
                row = enemy_block_state[p][i]
                for j in range(len(row)):  # 0~9
                    cell = row[j]
                    if cell in COLOR_MAP:
                        screenx = interface.screens[p].screenx
                        screeny = interface.screens[p].screeny      
                        pygame.draw.rect(
                            screen,
                            COLOR_MAP[cell],
                            (screenx + (j * 10), screeny + (i * 10), 10,10)
                        )
        

        if block.is_moving == False:
            current_block_type = next_block_type
            block= Block(current_block_type)
            next_block_type= random.randint(1,7)*10  #블록 땅에 닿으면 랜덤으로 뽑기
            Canhold = True

        for i in range(10):
            if map.blockState[0][i] != 0: #천장중 하나라도 블럭이 닿으면
                defeat_msg = {"msg":"defeat","player_id":player_num}#player_num도 보내야 할듯
                client.send(json.dumps(defeat_msg).encode()) #서버한테 defeat 보내기
                game_started = False #끄지말고 게임 종료상태로만 전환
        if cnt >= 30:
            cnt = 0
        pygame.display.update()

if __name__ == '__main__':
    main()