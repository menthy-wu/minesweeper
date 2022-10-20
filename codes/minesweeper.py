import sys, pygame,random
SCREEN_W,SCREEN_H = 700,650
d_x,d_y = [1,1,1,0,0,-1,-1,-1],[1,-1,0,1,-1,1,-1,0]
d = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
my_font = 'bahnschrift.ttf'
class CLS_minesweeper(object):
    def creat_board(self):
        #print('hi',self.num)
        self.boardList = [] 
        for y in range(self.num):
            l = []
            for x in range(self.num):
                l.append([0,0])
            self.boardList.append(l)
    def __init__(self):
        self.num = 10                #格子数
        self.boomNum = 10            #雷数
        self.record = 0              #标记数
        self.boardList = []          #网格定义
        self.flag = 0                #游戏状态 0为游戏中，1为game over，5为选择难度
        self.s = 50                  #坐标
        self.w = 20                  #格子宽
        self.b = 2                   #间距
        self.firstClick = 0          #点第一下
        self.creat_board()
    def boom(self,xx,yy):                  #随机生成雷
        num,boom,count = self.num,self.boomNum,0
        while True:
          x = random.randint(0,num-1)
          y = random.randint(0,num-1)
          if xx == x and yy == y:
              print(x,y)
              continue
          if self.boardList[y][x][0] == 0:
            self.boardList[y][x][0] = 10
            count+=1
          if count == boom:
            break
    def number(self):                #生成数字
        board,num = self.boardList,self.num
        for y in range (num):
          for x in range(num):
            if board[y][x][0] == 0:
              for d in range(8):
                x1,y1 = x+d_x[d],y+d_y[d]
                if 0<=x1<self.num and 0<=y1<self.num:
                    if board[y1][x1][0] == 10:
                        board[y][x][0] += 1
    def draw(self,screen):
        screen.fill((255,255,255))
        w,b,s = self.w,self.b,self.s
        board = self.boardList
        font = pygame.font.Font(my_font, 18)
        if self.num == 30:
            font = pygame.font.Font(my_font, 15)   
        for y in range(self.num):
            for x in range(self.num):
                x1,y1 = (w+b)*x+s,(w+b)*y+s
                #print(self.num)
                #print(x,y)
                if self.boardList[y][x][1] == 1:         #如果状态为1，画为蓝绿色
                    pygame.draw.rect(screen,(0,200,200),(x1,y1,w,w),0)
                    if self.boardList[y][x][0] == 10:    #如果踩到雷，画红点，游戏结束
                        pygame.draw.circle(screen,(255,50,50),(x1+w//2,y1+w//2),w//2-2,0)
                        f = pygame.font.Font(my_font, 100)
                        img_gg = f.render('GAME OVER',True,(255,100,100))
                    elif self.boardList[y][x][0]!=0:     #如果数字不为0，写出数字
                        img = font.render(str(self.boardList[y][x][0]),True,(100,100,100))
                        screen.blit( img ,(x1+w/3,y1))
                else:                                    #格子没被点过，画为绿色
                    pygame.draw.rect(screen,(0,200,0),(x1,y1,w,w),0)
                if self.boardList[y][x][1] == 2:         #标记
                    pygame.draw.circle(screen,(50,100,125),(x1+w//2,y1+w//2),w//2-2,0)
        #重新开始按钮
        pic = pygame.image.load('again.jpg')
        pic.set_colorkey( (0,0,0) )
        img = pygame.transform.scale(pic,(45, 45))
        screen.blit(img,(2,50))
        #title
        font = pygame.font.Font(my_font, 50)
        img = font.render('MINESWEEPER',True,(30,200,200))
        screen.blit( img ,(100,-3))
        pic = pygame.image.load('minesweeper.PNG')
        pic.set_colorkey( (0,0,0) )
        img = pygame.transform.scale(pic,(45, 45))
        screen.blit(img,(50,5))
        #雷数
        font = pygame.font.Font(my_font, 20)
        if self.num == 30 or self.num == 20:
            font = pygame.font.Font(my_font, 15)
        img = font.render(str(self.boomNum)+'/'+str(self.record),True,(30,200,200))
        screen.blit( img ,(2,100))
        #难度选择  简单：10*10 10  中等20*20 100   困难30*30 160
        font = pygame.font.Font(my_font, 18)
        if self.num == 10:
            pygame.draw.rect(screen,(0,200,0),(500,5,90,30),0)
            img = font.render('EASY',True,(255,255,255))
            screen.blit( img ,(520,10))
        elif self.num == 20:
            pygame.draw.rect(screen,(250,180,50),(500,5,90,30),0)
            img = font.render('MEDIUM',True,(255,255,255))
            screen.blit( img ,(510,10))
        else:
            pygame.draw.rect(screen,(250,100,100),(500,5,90,30),0)
            img = font.render('DIFFICULT',True,(255,255,255))
            screen.blit( img ,(503,10))
        if self.flag == 5:
            pygame.draw.rect(screen,(0,200,0),(500,40,90,30),0)
            img = font.render('EASY',True,(255,255,255))
            screen.blit( img ,(520,45))
            pygame.draw.rect(screen,(250,180,50),(500,75,90,30),0)
            img = font.render('MEDIUM',True,(255,255,255))
            screen.blit( img ,(510,80))
            pygame.draw.rect(screen,(250,100,100),(500,110,90,30),0)
            img = font.render('DIFFICULT',True,(255,255,255))
            screen.blit( img ,(503,115))
        if self.flag == 1:       #game over
            screen.blit( img_gg ,(100,200))
        if self.is_ok() == True:
            f = pygame.font.Font(my_font, 100)
            img_win = f.render('YOU WIN',True,(255,100,100))
            screen.blit( img_win ,(100,200))
    def mousedown(self,pos,botton):
        #print(self.firstClick)
        mx,my = pos
        x,y = (mx-self.s)//(self.w+self.b),(my-self.s)//(self.w+self.b)
        if 0<=x<self.num and 0<=y<self.num and self.firstClick == 0:
            self.firstClick = 1
            self.boom(x,y)
            self.number()
            #return
        if 2<=mx<=47 and 50<=my<=95 and botton == 1 and self.firstClick == 1:   #重置
            self.flag = 0
            #self.boom()
            #self.number()
            self.creat_board()
            self.firstClick = 0
            self.record = 0
            #print(self.firstClick)
            return
        if 500<=mx<=590 and 5<=my<=35:   #难度选择
            self.flag = 5
        if self.flag == 5:
            flag = 0
            if 500<=mx<=590 and 40<=my<=70:    #简单
                self.num=10
                self.creat_board()
                self.firstClick = 0
                self.boomNum = 10 
                flag = 1
            if 500<=mx<=590 and 75<=my<=105:     #中等
                self.num=20
                self.boomNum = 100
                self.creat_board()
                self.firstClick = 0
                flag = 1
            elif 500<=mx<=590 and 110<=my<=140:   #困难
                self.num=30
                self.creat_board()
                self.firstClick = 0
                self.w = 18
                self.boomNum = 160
                flag = 1
            if flag == 1:
                self.flag = 0
                #self.boom()
                #self.number()
        elif self.flag == 0 :
            if 0<=x<self.num and 0<=y<self.num:
                if botton == 1 and self.boardList[y][x][1] != 2:              #左击
                    self.boardList[y][x][1] = 1
                    if self.boardList[y][x][0] == 10:
                        self.boardList[y][x][1] = 1
                        self.flag = 1
                    elif self.boardList[y][x][0] == 0:
                        self.manyan(self.boardList,x,y)
                if botton == 3:              #右击
                    self.boardList[y][x][1] = 2-self.boardList[y][x][1]
                    if self.boardList[y][x][1] == 2:
                        self.record+=1
                    else:
                        self.record -= 1
    def manyan(self,grid,x,y):            #点到空格子，小本子发蔓延查找
        mem = [[x,y]]
        while True:
            if mem == []:
                return
            x,y = mem.pop(0)
            if grid[y][x][1] == 2:
                self.record-=1
            grid[y][x][1] = 1
            for i in d:
                nx,ny = x+i[0],y+i[1]
                if 0<=nx<self.num and 0<=ny<self.num:
                    if grid[ny][nx][0] == 0 and (grid[ny][nx][1] == 0 or grid[ny][nx][1] == 2):
                        mem.append([nx,ny])
                    if grid[ny][nx][0] != 10:
                        if grid[ny][nx][1] == 2:
                            self.record-=1
                        grid[ny][nx][1] = 1
    def is_ok(self):
        count = 0
        grid = self.boardList
        f = 0
        for i in grid:
            for p in i:
                if p[0] == 10 and p[1] !=2:
                    return False
                if p[0] != 0:
                    f = 1
        if f == 0:
            return False
        return True
                    
#————————————————————————————————————————————————————————-main——————————————————————————————————-------————
minesweeper = CLS_minesweeper()
#minesweeper.boom()
#minesweeper.number()
pygame.init()
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
screen.fill((255,255,255))
while True:
    minesweeper.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            minesweeper.mousedown(event.pos,event.button)
