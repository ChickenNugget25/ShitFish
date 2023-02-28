import pygame
import os
import random
import math

pygame.init()

width,height=(500,500)

screen = pygame.display.set_mode((width,height))

piecesM = [i[:-4] for i in os.listdir('Images/')]
piecesImg=[pygame.image.load('Images/'+i) for i in os.listdir('Images/')]

running = True

isBlack=0

board = [7,4,1,6,3,1,4,7,
         5,5,5,5,5,5,5,5,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         10,10,10,10,10,10,10,10,
         12, 9, 2, 11, 8, 2, 9, 12]

def background(screen):
    for x in range(8):
        for y in range(8):
            if((x+y+isBlack)%2!=0):
                pygame.draw.rect(screen,(50,50,50),pygame.Rect(x*(width/8),y*(height/8),math.ceil(width/8),math.ceil(height/8)))
            else:
                pygame.draw.rect(screen,(0,200,0),pygame.Rect(x*(width/8),y*(height/8),math.ceil(width/8),math.ceil(height/8)))

def pieces(screen):
    for i,e in enumerate(board):
        if(e!=0):
            screen.blit(piecesImg[e-1],(i%8*(height/8),math.floor(i/8)*(width/8)))

def drawHeld(screen,holding):
    #print(mouseDown,holding != -1,holding)
    if(mouseDown and holding != -1):
        #print(holding)
        screen.blit(piecesImg[holding],pygame.mouse.get_pos())
    return holding

def tick(pos,holding,original,showing,moves):
    if(mouseDown and board[pos[0]+(pos[1]*8)] != 0 and holding == -1):
        holding=board[pos[0]+(pos[1]*8)]-1
        original=pos
        board[pos[0]+(pos[1]*8)]=0
        print(piecesM[holding])
    elif(not mouseDown and holding !=-1 and originalSquare != 0):
        pos=math.floor(pygame.mouse.get_pos()[0]/(width/8)),math.floor(pygame.mouse.get_pos()[1]/(height/8))
        if(pos in moves):
            board[pos[0]+(pos[1]*8)]=holding+1
        else:
            board[original[0]+(original[1]*8)]=holding+1
            showing=True
        holding=-1
    return holding,original,showing

def test(piece,x,y,taking,either=False):
    if(x<0 or x>7 or y<0 or y>7):
        return False
    if((not taking or either) and board[x+(y*8)]==0): #not taking and space is empty
        return True
    #space isn't empty, object isn't on the same team
    elif(board[x+(y*8)] != 0 and ('B' in piece) == (not 'B' in piecesM[board[x+(y*8)]-1]) and (taking or either)):
        return True

def spaceOpen(x,y):
    if(x<0 or x>7 or y<0 or y>7):
        return False
    if(board[x+(y*8)] == 0):
        return True

def colorDifferent(piece,x,y):
    if(x<0 or x>7 or y<0 or y>7):
        return False
    else:
        if(board[x+(y*8)] != 0):
            return ('B' in piece) == (not 'B' in piecesM[board[x+(y*8)]+1])
        else:
            return False
        
def showMoves(screen,showing, holding,original,moves,check):
    piece = piecesM[holding]
    moves = []
    if(original==0 or holding==-1):
        return moves,check
    if('pawn' in piece):
        if('B' in piece):
            if(original[1]==1 and test(piece,original[0],original[1]+2,False)):
                moves.append((original[0],original[1]+2))
            if(test(piece,original[0],original[1]+1,False)):
                moves.append((original[0],original[1]+1))
            for i in range(-1,2,2):
                if(test(piece,original[0]+i,original[1]+1,True)):
                    moves.append((original[0]+i,original[1]+1))
        else:
            if(original[1]==6 and test(piece,original[0],original[1]-2,False)):
                moves.append((original[0],original[1]-2))
            if(test(piece,original[0],original[1]-1,False)):
                moves.append((original[0],original[1]-1))
            for i in range(-1,2,2):
                print(i)
                if(test(piece,original[0]+i,original[1]-1,True)):
                    moves.append((original[0]+i,original[1]-1))
    elif('knight' in piece):
        for i in range(-1,2,2):
            for z in range(-1,2,2):
                if(test(piece,original[0]+i,original[1]+(z*2),False,True)):
                    moves.append((original[0]+i,original[1]+(z*2)))
        for i in range(-1,2,2):
            for z in range(-1,2,2):
                if(test(piece,original[0]+(i*2),original[1]+z,False,True)):
                    moves.append((original[0]+(i*2),original[1]+z))
    elif('bishop' in piece):
        RU=True
        LU=True
        RD=True
        LD=True
        for i in range(1,original[0]+1):
            if(test(piece,original[0]-i,original[1]-i,False,True) and LU):
                moves.append((original[0]-i,original[1]-i))
            if(test(piece,original[0]-i,original[1]+i,False,True) and LD):
                moves.append((original[0]-i,original[1]+i))
            if(not spaceOpen(original[0]-i,original[1]-i)):
                LU=False
            if(not spaceOpen(original[0]-i,original[1]+i)):
                LD=False
        for i in range(1,8-original[0]):
            if(test(piece,original[0]+i,original[1]+i,False,True) and RU):
                moves.append((original[0]+i,original[1]+i))
            if(test(piece,original[0]+i,original[1]-i,False,True) and RD):
                moves.append((original[0]+i,original[1]-i))
            if(not spaceOpen(original[0]+i,original[1]+i)):
                RU=False
            if(not spaceOpen(original[0]+i,original[1]-i)):
                RD=False
    elif('king' in piece):
        for i in [-1,0,1]:
            for z in [-1,0,1]:
                if(test(piece,original[0]+i,original[1]+z,False,True) and (original[0]+i,original[1]+z) != original):
                    moves.append((original[0]+i,original[1]+z))
    elif('rook' in piece):
        U=True
        D=True
        L=True
        R=True
        for i in range(1,original[0]+1):
            if(test(piece,original[0]-i,original[1],False,True) and L):
                moves.append((original[0]-i,original[1]))
            if(not spaceOpen(original[0]-i,original[1])):
                L=False
        for i in range(1,8-original[0]):
            if(test(piece,original[0]+i,original[1],False,True) and R):
                moves.append((original[0]+i,original[1]))
            if(not spaceOpen(original[0]+i,original[1])):
                R=False
        for i in range(1,original[1]+1):
            if(test(piece,original[0],original[1]-i,False,True) and U):
                moves.append((original[0],original[1]-i))
            if(not spaceOpen(original[0], original[1]-i)):
                U=False
        for i in range(1,8-original[1]):
            if(test(piece,original[0],original[1]+i,False,True) and D):
                moves.append((original[0],original[1]+i))
            if(not spaceOpen(original[0],original[1]+i)):
                D=False
    elif('queen' in piece):
        U=True
        D=True
        L=True
        R=True
        RU=True
        LU=True
        RD=True
        LD=True
        for i in range(1,original[0]+1):
            if(test(piece,original[0]-i,original[1]-i,False,True) and LU):
                moves.append((original[0]-i,original[1]-i))
            if(test(piece,original[0]-i,original[1]+i,False,True) and LD):
                moves.append((original[0]-i,original[1]+i))
            if(not spaceOpen(original[0]-i,original[1]-i)):
                LU=False
            if(not spaceOpen(original[0]-i,original[1]+i)):
                LD=False
        for i in range(1,8-original[0]):
            if(test(piece,original[0]+i,original[1]+i,False,True) and RU):
                moves.append((original[0]+i,original[1]+i))
            if(test(piece,original[0]+i,original[1]-i,False,True) and RD):
                moves.append((original[0]+i,original[1]-i))
            if(not spaceOpen(original[0]+i,original[1]+i)):
                RU=False
            if(not spaceOpen(original[0]+i,original[1]-i)):
                RD=False
        for i in range(1,original[0]+1):
            if(test(piece,original[0]-i,original[1],False,True) and L):
                moves.append((original[0]-i,original[1]))
            if(not spaceOpen(original[0]-i,original[1])):
                L=False
        for i in range(1,8-original[0]):
            if(test(piece,original[0]+i,original[1],False,True) and R):
                moves.append((original[0]+i,original[1]))
            if(not spaceOpen(original[0]+i,original[1])):
                R=False
        for i in range(1,original[1]+1):
            if(test(piece,original[0],original[1]-i,False,True) and U):
                moves.append((original[0],original[1]-i))
            if(not spaceOpen(original[0], original[1]-i)):
                U=False
        for i in range(1,8-original[1]):
            if(test(piece,original[0],original[1]+i,False,True) and D):
                moves.append((original[0],original[1]+i))
            if(not spaceOpen(original[0],original[1]+i)):
                D=False
    check=False
    for move in moves:
        if(not check):
            if(board[move[0]+(move[1]*8)] != 0):
                if('king' in piecesM[board[move[0]+(move[1]*8)]-1]):
                    print('check')
                    check=True
                else:
                    pygame.draw.rect(screen,(182,194,185),pygame.Rect(move[0]*(width/8),move[1]*(height/8),math.ceil(width/8),math.ceil(height/8)),math.floor(width/8))
            else:
                pygame.draw.circle(screen,(182, 194, 185),(math.floor(move[0]*(width/8)+((width/8)/2)),math.floor(move[1]*(height/8)+((height/8)/2))),10)
        else:
            if(board[move[0]+(move[1]*8)] != 0):
                if('king' in piecesM[board[move[0]+(move[1]*8)]-1]):
                    k=board[move[0]+(move[1]*8)]
                    if()
    return moves,check
def draw(screen,holding,showing,original,moves,check):
    background(screen)
    moves,check=showMoves(screen,showing,holding,original,moves,check)
    pieces(screen)
    drawHeld(screen,holding)
    pygame.display.flip()
    return moves,check

pos=0
mouseDown=False
holding=-1
originalSquare=0
showing=False
moves=[]
check=False

while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running=False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button==1):
                pos=math.floor(event.pos[0]/(width/8)),math.floor(event.pos[1]/(height/8))
                mouseDown=True
        elif(event.type == pygame.MOUSEBUTTONUP):
            if(event.button==1):
                mouseDown=False
    holding,originalSquare,showing=tick(pos,holding,originalSquare,showing,moves)
    moves,check=draw(screen,holding,showing,originalSquare,moves,check)
pygame.quit()