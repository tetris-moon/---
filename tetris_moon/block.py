import pygame
import random
import block_info
from block_info import BLOCK_COORDS
MAX_WIDTH = 300
MAX_HEIGHT = 600
from colors import BLUE, GOLD, AQUA, VIOLET , LIME , ORANGE , RED

class Block():
    def __init__(self, type):

        self.info = [[120,0],[120,0],[120,0],[120,0]]


        self.x1 = 120
        self.x2 = 150
        self.x3 = 120
        self.x4 = 150
        self.y1 = 0
        self.y2 = 0
        self.y3 = 30
        self.y4 = 30
        self.is_moving = True
        self.block_type = type
        self.initBlockPos()

    def initBlockPos(self):
        self.x1, self.y1 = BLOCK_COORDS[self.block_type][0]
        self.x2, self.y2 = BLOCK_COORDS[self.block_type][1]
        self.x3, self.y3 = BLOCK_COORDS[self.block_type][2]
        self.x4, self.y4 = BLOCK_COORDS[self.block_type][3]
    


    def rotate_numbers(self):  #블록이 돌아 갈때 숫자 높이기
        if self.block_type == 10:
            return
        else:
            if self.block_type in [20, 30, 40, 50, 60, 70]:
                self.block_type += 1
            elif self.block_type in [21, 22, 31, 32, 41, 42, 51, 52, 61, 62, 71, 72]:
                self.block_type += 1
            elif self.block_type in [23, 33, 43, 53, 63, 73]:
                self.block_type -= 3
            else:
                self.block_type -= 1

    def rotate(self, map):   #블록 90도 씩 돌리기
        if self.block_type == 10:
            return
        else:
            #중심을 x2, y2로 고정
            cx, cy = self.x2, self.y2

            def rotate_point(x, y, cx, cy):
                dx, dy = x - cx, y - cy
                return cx - dy, cy + dx  # 시계방향 90도 회전

            #블럭 4개의 회전 좌표 계산
            rotated_points = [
                rotate_point(self.x1, self.y1, cx, cy),
                rotate_point(self.x2, self.y2, cx, cy),
                rotate_point(self.x3, self.y3, cx, cy),
                rotate_point(self.x4, self.y4, cx, cy)
            ]

            #회전된 좌표가 맵 밖이거나 충돌하는지 검사
            for x, y in rotated_points:
                if x < 0 or x >= MAX_WIDTH or y < 0 or y >= MAX_HEIGHT:
                    return
                if map:
                    xi, yi = x // 30, y // 30
                    try:
                        if map.blockState[yi][xi] != 0:
                            return
                    except IndexError:
                        return

            #문제 없으면 회전 적용
            #print("rotate")
            self.x1, self.y1 = rotated_points[0]
            self.x2, self.y2 = rotated_points[1]
            self.x3, self.y3 = rotated_points[2]
            self.x4, self.y4 = rotated_points[3]

            
    def draw(self, screen):
        font = pygame.font.Font(None, 24)  # 기본 폰트, 크기 24
        if self.block_type == 10:
            color = GOLD
        elif 20 <= self.block_type <= 23:
            color = BLUE
        elif 30 <= self.block_type <= 33:
            color = ORANGE
        elif 40 <= self.block_type <= 43:
            color = LIME
        elif 50 <= self.block_type <= 53:
            color = RED
        elif 60 <= self.block_type <= 63:
            color = VIOLET
        elif 70 <= self.block_type <= 73:
            color = AQUA

        rects = [
            (self.x1, self.y1, "1"),
            (self.x2, self.y2, "2"), #블럭 번호
            (self.x3, self.y3, "3"),
            (self.x4, self.y4, "4")
        ]

        for x, y, num in rects:
            # 사각형 그리기
            pygame.draw.rect(screen, color, (x, y, 30, 30))
            # 텍스트 렌더링
            text = font.render(num, True, (0, 0, 0))  # 검정색 글자
            text_rect = text.get_rect(center=(x + 15, y + 15))  # 중앙 정렬
            screen.blit(text, text_rect)


    def move(self, cnt, map):
        if self.is_moving and cnt == 30:
            if self.isGround(map): #땅에 닿았을 때.
                self.is_moving = False
            else: #땅에 닿지 않았을 때.
                self.y1 += 30
                self.y2 += 30
                self.y3 += 30
                self.y4 += 30

    def moveLeft(self, board):
        if min(self.x1, self.x2, self.x3, self.x4) <= 0: #왼쪽 벽 못감
            return
        if (board[self.y1 // 30][(self.x1 - 30) // 30] != 0 or #왼쪽에 다른 블록 있으면 못감
            board[self.y2 // 30][(self.x2 - 30) // 30] != 0 or
            board[self.y3 // 30][(self.x3 - 30) // 30] != 0 or
            board[self.y4 // 30][(self.x4 - 30) // 30] != 0):
            return
        # 문제 없으면 이동
        self.x1 -= 30
        self.x2 -= 30
        self.x3 -= 30
        self.x4 -= 30


    def moveRight(self, board):
        if max(self.x1, self.x2, self.x3, self.x4) >= MAX_WIDTH - 30: #오른쪽 벽 못감
            return
        if (board[self.y1 // 30][(self.x1 + 30) // 30] != 0 or #오른쪽에 다른 블록 있으면 못감
            board[self.y2 // 30][(self.x2 + 30) // 30] != 0 or
            board[self.y3 // 30][(self.x3 + 30) // 30] != 0 or
            board[self.y4 // 30][(self.x4 + 30) // 30] != 0):
            return
        #문제없으면 이동
        self.x1 += 30
        self.x2 += 30
        self.x3 += 30
        self.x4 += 30
        
    def HardDrop(self,map):
        while not self.isGround(map):
            self.y1 += 30
            self.y2 += 30
            self.y3 += 30
            self.y4 += 30
        for x, y in self.getIndexFromPos():
            map.blockState[y][x] = self.block_type//10
        self.is_moving = False

    def getIndexFromPos(self):
        return [
        (self.x1 // 30, self.y1 // 30),
        (self.x2 // 30, self.y2 // 30),
        (self.x3 // 30, self.y3 // 30),
        (self.x4 // 30, self.y4 // 30)
        ]


    def isGround(self, map):
        print(self.block_type)
        x1 = self.x1 // 30
        x2 = self.x2 // 30
        x3 = self.x3 // 30
        x4 = self.x4 // 30
        y1 = self.y1 // 30
        y2 = self.y2 // 30
        y3 = self.y3 // 30
        y4 = self.y4 // 30
        
        try:
            


            if self.block_type == 10: #블럭이 O고
                if self.y3+30 < MAX_HEIGHT: #공중에 있는데,
                    if map.blockState[y3+1][x3] != 0 or map.blockState[y4+1][x4] !=0: #발아래 블럭이 있으면.
                        map.blockState[y1][x1] = 1
                        map.blockState[y2][x2] = 1
                        map.blockState[y3][x3] = 1
                        map.blockState[y4][x4] = 1
                        return True
                else:
                    map.blockState[y1][x1] = 1
                    map.blockState[y2][x2] = 1
                    map.blockState[y3][x3] = 1
                    map.blockState[y4][x4] = 1
                    return True
            elif self.block_type == 50:  # Z 기본
                if self.y4 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y3+1][x3] != 0 or map.blockState[y4+1][x4] != 0:
                        map.blockState[y1][x1] = 5
                        map.blockState[y2][x2] = 5
                        map.blockState[y3][x3] = 5
                        map.blockState[y4][x4] = 5
                        return True
                else:
                    map.blockState[y1][x1] = 5
                    map.blockState[y2][x2] = 5
                    map.blockState[y3][x3] = 5
                    map.blockState[y4][x4] = 5
                    return True

            elif self.block_type == 51:  # Z 90도
                if self.y4 + 30 < MAX_HEIGHT:
                    if map.blockState[y2+1][x2] != 0 or map.blockState[y4+1][x4] != 0:
                        map.blockState[y1][x1] = 5
                        map.blockState[y2][x2] = 5
                        map.blockState[y3][x3] = 5
                        map.blockState[y4][x4] = 5
                        return True
                else:
                    map.blockState[y1][x1] = 5
                    map.blockState[y2][x2] = 5
                    map.blockState[y3][x3] = 5
                    map.blockState[y4][x4] = 5
                    return True
                
            elif self.block_type == 52:#뒤집힌 z
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y2+1][x2] != 0 or map.blockState[y4+1][x4] != 0:
                        map.blockState[y1][x1] = 5
                        map.blockState[y2][x2] = 5
                        map.blockState[y3][x3] = 5
                        map.blockState[y4][x4] = 5
                        return True
                else:
                    map.blockState[y1][x1] = 5
                    map.blockState[y2][x2] = 5
                    map.blockState[y3][x3] = 5
                    map.blockState[y4][x4] = 5
                    return True
                
            elif self.block_type == 53:#뒤집힌 90도 z
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y3+1][x3] != 0:
                        map.blockState[y1][x1] = 5
                        map.blockState[y2][x2] = 5
                        map.blockState[y3][x3] = 5
                        map.blockState[y4][x4] = 5
                        return True
                else:
                    map.blockState[y1][x1] = 5
                    map.blockState[y2][x2] = 5
                    map.blockState[y3][x3] = 5
                    map.blockState[y4][x4] = 5
                    return True
                
            elif self.block_type == 40:  # S 기본
                if self.y4 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y3+1][x3] != 0 or map.blockState[y4+1][x4] != 0:
                        map.blockState[y1][x1] = 4
                        map.blockState[y2][x2] = 4
                        map.blockState[y3][x3] = 4
                        map.blockState[y4][x4] = 4
                        return True
                else:
                    map.blockState[y1][x1] = 4
                    map.blockState[y2][x2] = 4
                    map.blockState[y3][x3] = 4
                    map.blockState[y4][x4] = 4
                    return True

            elif self.block_type == 41:  # S 90도
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y4+1][x4] != 0:
                        map.blockState[y1][x1] = 4
                        map.blockState[y2][x2] = 4
                        map.blockState[y3][x3] = 4
                        map.blockState[y4][x4] = 4
                        return True
                else:
                    map.blockState[y1][x1] = 4
                    map.blockState[y2][x2] = 4
                    map.blockState[y3][x3] = 4
                    map.blockState[y4][x4] = 4
                    return True
            
            elif self.block_type == 42:  # S 기본
                if self.y2 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y2+1][x2] != 0 or map.blockState[y3+1][x3] != 0:
                        map.blockState[y1][x1] = 4
                        map.blockState[y2][x2] = 4
                        map.blockState[y3][x3] = 4
                        map.blockState[y4][x4] = 4
                        return True
                else:
                    map.blockState[y1][x1] = 4
                    map.blockState[y2][x2] = 4
                    map.blockState[y3][x3] = 4
                    map.blockState[y4][x4] = 4
                    return True
                
            elif self.block_type == 43:  # S 90도
                if self.y3 + 30 < MAX_HEIGHT:
                    if map.blockState[y2+1][x2] != 0 or map.blockState[y3+1][x3] != 0:
                        map.blockState[y1][x1] = 4
                        map.blockState[y2][x2] = 4
                        map.blockState[y3][x3] = 4
                        map.blockState[y4][x4] = 4
                        return True
                else:
                    map.blockState[y1][x1] = 4
                    map.blockState[y2][x2] = 4
                    map.blockState[y3][x3] = 4
                    map.blockState[y4][x4] = 4
                    return True
                
            elif self.block_type == 60:
                if self.y4 +30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y3+1][x3] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1]= 6
                        map.blockState[y2][x2]= 6
                        map.blockState[y3][x3]= 6
                        map.blockState[y4][x4]= 6
                        return True
                else:
                    map.blockState[y1][x1]= 6
                    map.blockState[y2][x2]= 6
                    map.blockState[y3][x3]= 6
                    map.blockState[y4][x4]= 6
                    return True
            elif self.block_type == 61:
                if self.y3 + 30 < MAX_HEIGHT:
                    if map.blockState[y3+1][x3] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1] = 6
                        map.blockState[y2][x2] = 6
                        map.blockState[y3][x3] = 6
                        map.blockState[y4][x4] = 6
                        return True
                else:
                    map.blockState[y1][x1] = 6
                    map.blockState[y2][x2] = 6
                    map.blockState[y3][x3] = 6
                    map.blockState[y4][x4] = 6
                    return True
            elif self.block_type == 62:
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y2+1][x2] !=0 or map.blockState[y3+1][x3] !=0:
                        map.blockState[y1][x1] = 6
                        map.blockState[y2][x2] = 6
                        map.blockState[y3][x3] = 6
                        map.blockState[y4][x4] = 6
                        return True
                else:
                    map.blockState[y1][x1] = 6
                    map.blockState[y2][x2] = 6
                    map.blockState[y3][x3] = 6
                    map.blockState[y4][x4] = 6
                    return True
            elif self.block_type == 63:
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1] = 6
                        map.blockState[y2][x2] = 6
                        map.blockState[y3][x3] = 6
                        map.blockState[y4][x4] = 6
                        return True
                else:
                    map.blockState[y1][x1] = 6
                    map.blockState[y2][x2] = 6
                    map.blockState[y3][x3] = 6
                    map.blockState[y4][x4] = 6
                    return True
            elif self.block_type == 20:
                if self.y4 +30  < MAX_HEIGHT: #블럭의 높이가 3인 녀석들
                    if map.blockState[y2+1][x2] !=0 or map.blockState[y3+1][x3] !=0 or map.blockState[y4+1][x4]:
                        map.blockState[y1][x1] = 2
                        map.blockState[y2][x2] = 2
                        map.blockState[y3][x3] = 2
                        map.blockState[y4][x4] = 2
                        return True
                else:
                    map.blockState[y1][x1] = 2
                    map.blockState[y2][x2] = 2
                    map.blockState[y3][x3] = 2
                    map.blockState[y4][x4] = 2
                    return True
            elif self.block_type == 21:
                if self.y3 + 30 < MAX_HEIGHT:
                    if map.blockState[y3+1][x3] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1] = 2
                        map.blockState[y2][x2] = 2
                        map.blockState[y3][x3] = 2
                        map.blockState[y4][x4] = 2
                        return True
                else:
                    map.blockState[y1][x1] = 2
                    map.blockState[y2][x2] = 2
                    map.blockState[y3][x3] = 2
                    map.blockState[y4][x4] = 2
                    return True
            elif self.block_type == 22:
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y2+1][x2] !=0 or map.blockState[y3+1][x3] !=0:
                        map.blockState[y1][x1] = 2
                        map.blockState[y2][x2] = 2
                        map.blockState[y3][x3] = 2
                        map.blockState[y4][x4] = 2
                        return True
                else:
                    map.blockState[y1][x1] = 2
                    map.blockState[y2][x2] = 2
                    map.blockState[y3][x3] = 2
                    map.blockState[y4][x4] = 2
                    return True
            elif self.block_type == 23:
                if self.y4 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1] = 2
                        map.blockState[y2][x2] = 2
                        map.blockState[y3][x3] = 2
                        map.blockState[y4][x4] = 2
                        return True
                else:
                    map.blockState[y1][x1] = 2
                    map.blockState[y2][x2] = 2
                    map.blockState[y3][x3] = 2
                    map.blockState[y4][x4] = 2
                    return True
            elif self.block_type == 30: #################################################여기부터
                if self.y4 +30  < MAX_HEIGHT: #블럭의 높이가 3인 녀석들
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y2+1][x2] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1]= 3
                        map.blockState[y2][x2]= 3
                        map.blockState[y3][x3]= 3
                        map.blockState[y4][x4]= 3
                        return True
                else:
                    map.blockState[y1][x1]= 3
                    map.blockState[y2][x2]= 3
                    map.blockState[y3][x3]= 3
                    map.blockState[y4][x4]= 3
                    return True
            elif self.block_type == 31:
                if self.y4 + 30 < MAX_HEIGHT:
                    if map.blockState[y3+1][x3] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1] = 3
                        map.blockState[y2][x2] = 3
                        map.blockState[y3][x3] = 3
                        map.blockState[y4][x4] = 3
                        return True
                else:
                    map.blockState[y1][x1] = 3
                    map.blockState[y2][x2] = 3
                    map.blockState[y3][x3] = 3
                    map.blockState[y4][x4] = 3
                    return True
            elif self.block_type == 32:
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y2+1][x2] !=0 or map.blockState[y3+1][x3]:
                        map.blockState[y1][x1] = 3
                        map.blockState[y2][x2] = 3
                        map.blockState[y3][x3] = 3
                        map.blockState[y4][x4] = 3
                        return True
                else:
                    map.blockState[y1][x1] = 3
                    map.blockState[y2][x2] = 3
                    map.blockState[y3][x3] = 3
                    map.blockState[y4][x4] = 3
                    return True
            elif self.block_type == 33:
                if self.y1 + 30 < MAX_HEIGHT:
                    if map.blockState[y1+1][x1] !=0 or map.blockState[y4+1][x4] !=0:
                        map.blockState[y1][x1] = 3
                        map.blockState[y2][x2] = 3
                        map.blockState[y3][x3] = 3
                        map.blockState[y4][x4] = 3
                        return True
                else:
                    map.blockState[y1][x1] = 3
                    map.blockState[y2][x2] = 3
                    map.blockState[y3][x3] = 3
                    map.blockState[y4][x4] = 3
                    return True
            elif self.block_type == 70:
                if self.y4 + 30 < MAX_HEIGHT:#블럭 높이가 4
                    if map.blockState[y4+1][x1] != 0 or map.blockState[y1+1][x1] != 0:
                        map.blockState[y1][x1]= 7
                        map.blockState[y2][x2]= 7
                        map.blockState[y3][x3]= 7
                        map.blockState[y4][x4]= 7
                        return True
                else:
                    map.blockState[y1][x1]= 7
                    map.blockState[y2][x2]= 7
                    map.blockState[y3][x3]= 7
                    map.blockState[y4][x4]= 7
                    return True
            elif self.block_type == 71:
                if self.y1 + 30  < MAX_HEIGHT:#블럭 높이가 4
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y2+1][x2] != 0 or map.blockState[y3+1][x3] != 0 or map.blockState[y4+1][x4] != 0:
                        map.blockState[y1][x1]= 7
                        map.blockState[y2][x2]= 7
                        map.blockState[y3][x3]= 7
                        map.blockState[y4][x4]= 7
                        return True
                else:
                    map.blockState[y1][x1]= 7
                    map.blockState[y2][x2]= 7
                    map.blockState[y3][x3]= 7
                    map.blockState[y4][x4]= 7
                    return True
            elif self.block_type == 72:
                if self.y1 + 30 < MAX_HEIGHT:#블럭 높이가 4
                    if map.blockState[y4+1][x1] != 0 or map.blockState[y1+1][x1] != 0:
                        map.blockState[y1][x1]= 7
                        map.blockState[y2][x2]= 7
                        map.blockState[y3][x3]= 7
                        map.blockState[y4][x4]= 7
                        return True
                else:
                    map.blockState[y1][x1]= 7
                    map.blockState[y2][x2]= 7
                    map.blockState[y3][x3]= 7
                    map.blockState[y4][x4]= 7
                    return True
            elif self.block_type == 73:
                if self.y1 + 30  < MAX_HEIGHT:#블럭 높이가 4
                    if map.blockState[y1+1][x1] != 0 or map.blockState[y2+1][x2] != 0 or map.blockState[y3+1][x3] != 0 or map.blockState[y4+1][x4] != 0:
                        map.blockState[y1][x1]= 7
                        map.blockState[y2][x2]= 7
                        map.blockState[y3][x3]= 7
                        map.blockState[y4][x4]= 7
                        return True
                else:
                    map.blockState[y1][x1]= 7
                    map.blockState[y2][x2]= 7
                    map.blockState[y3][x3]= 7
                    map.blockState[y4][x4]= 7
                    return True
            return False
        except IndexError:
            print('idex error')