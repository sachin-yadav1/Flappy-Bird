from random import randint
import pygame
import time
from os import _exit                

White=(255,255,255)                      #some common colours RGB codes
Black=(000,000,000)
SkyBlue=(0,255,255)
Blue=(0,0,255)

pygame.init()                         #pygame initiated here

GroundHeight=100                       #height of ground above screen bottom line
BirdHeight=60
BirdWidth=60
GapSize=180                             #size of gap in beween the pillar  
PillarWidth=130
PillarHeight=1200
GroundVelocityIncrease=0.007             #proportional to increase in pillar speed over time
DisplaySize=DisplayWidth,DisplayHeight=(1300,850)           #Size of screen in pixels
GapBetweenPillars=DisplayWidth//3                       #gap between two consecutive pillars
InitialPillar=100
ScoreDisplayHeight=100                              #height for position of score display

GameDisplay =pygame.display.set_mode(DisplaySize)   
pygame.display.set_caption("FLAPPY BIRD")       #written Flappy bird in title bar
Clock=pygame.time.Clock()
                        #loading all the required images from the images folder
                        #some images were made in paint and other taken from internet
BackGroundImg=pygame.image.load("Images/bg img.png")
#Different skins for the player
BirdImg=pygame.image.load("Images/bird img.png")
AirplaneImg=pygame.image.load("Images/airplane img.png")
SupermanImg=pygame.image.load("Images/superman img.png")
PlayerImg=BirdImg           #initial skin is bird image

GroundImg=pygame.image.load("Images/ground2 img.png")
IntroImg=pygame.image.load("Images/intro img.png")
PillarUpImg=pygame.image.load("Images/pillar up img.png")
PillarDownImg=pygame.image.load("Images/pillar down img.png")
GameOverImg=pygame.image.load("Images/game over img.jpg")
                          #loading all the required sounds from sounds folder
                          #all sounds were taken from https://www.sounds-resource.com/mobile/flappybird/sound/5309/
HitSound=pygame.mixer.Sound("Sounds/sfx_hit.wav")
DieSound=pygame.mixer.Sound("Sounds/sfx_die.wav")
PointSound=pygame.mixer.Sound("Sounds/sfx_point.wav")
SwooshSound=pygame.mixer.Sound("Sounds/sfx_swoosh.wav")
FlapSound=pygame.mixer.Sound("Sounds/sfx_flap.wav")

def IntroDisplay():                     #for the display of splash image in the begiining
    GameDisplay.blit(IntroImg,(0,0))
    pygame.display.flip()
    pygame.time.delay(3000)   

def Bird(x,y):              #takes x,y coordinates of the top left corner of bird and displays it
    GameDisplay.blit(PlayerImg,(x,y))

def Ground(x_ground):               #takes x coordinate of the ground and displays it
    GameDisplay.blit(GroundImg,(x_ground,DisplayHeight-GroundHeight))

def BackGround():               #displays backgroung image with its top left at 0,0
    GameDisplay.blit(BackGroundImg,(0,0))
                                
                                #the reference from https://www.youtube.com/watch?v=kmXKFTu_IyQ for this function
def MesssageDisplay(text):      #the string to be displayed is passed as text
    font = pygame.font.Font('freesansbold.ttf',80) #font style=fresanbold and size=80
    TextSurf=font.render(text, True, Black)   
    TextRect=TextSurf.get_rect()             #gets text surface and the rectangle from the function
    TextRect.center = ((DisplayWidth/2),(DisplayHeight/2))   #text rectangle centre at mid 
    GameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()

def PillarDisplay(x,y):                 #for displaying pillars
    GameDisplay.blit(PillarUpImg,(x,y-PillarHeight))    #displays upper pillar
    GameDisplay.blit(PillarDownImg,(x,y+GapSize))        #displays lower pillar

def ScoreDisplay(score):                        #for displaying current score
    font=pygame.font.Font('freesansbold.ttf',60)      #fontstyle and size specified
    textSurface = font.render(score, True, Blue)
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    TextRect.center = (DisplayWidth/2,ScoreDisplayHeight)    #position for the rect to show scores
    GameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def ending(score):                      #executed when player quits or hits a pillar
    pygame.mixer.Sound.play(DieSound)           #plays die sound
    GameDisplay.blit(GameOverImg,(0,0))         #displays gameover image
    font=pygame.font.Font('freesansbold.ttf',50)
    textSurface = font.render("YOUR SCORE: "+str(score), True, (255,0,0)) #displays player's final score
    """TextSurf, TextRect = textSurface, textSurface.get_rect()
    TextRect.center = (DisplayWidth/2,ScoreDisplayHeight+200+300+100)"""
    GameDisplay.blit(textSurface,((DisplayWidth/2,ScoreDisplayHeight+200+300+100)))
    file=open("Logs/score.txt","r")              #opens Logs\score.txt to check the previous highscore
    HighScore=max(score,int(file.readline()))      #finds new HighScore
    font=pygame.font.Font('freesansbold.ttf',50)   
    textSurface = font.render("HIGH SCORE: "+str(HighScore), True, (255,0,0))  #displays current HighScore
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    TextRect.center = (DisplayWidth/2,ScoreDisplayHeight+200+75+300+100)
    GameDisplay.blit(TextSurf, TextRect)
    file.close()
    file=open("Logs/score.txt","w")
    file.write(str(HighScore))                      #writes updated high score to score.txt
    file.close()
    pygame.display.flip()
    for i in range(8):                              #waits for 8 seconds 
        for event in pygame.event.get():
         if event.type==pygame.QUIT:            #if user clicks close, it quits
              pygame.quit()
              _exit(0)
        pygame.time.delay(1000)
    GameLoop()                              #if not closed, then restart from splash image

def GameLoop():

    Score=0                                      
    Velocity=7      #velocity when falling down
    x=300             #initial position of Bird
    y=100
    y_change=0
    GroundVelocity=3        #velocity of pillars to move
    
    x_ground=0     
    x_pillar=[DisplayWidth+InitialPillar,DisplayWidth+InitialPillar+GapBetweenPillars,DisplayWidth+InitialPillar+2*GapBetweenPillars]                             
    y_pillar=[ randint(60,680-GapSize) for i in range(3)]
    
    crashed=False                   #initially not crashed, not quitted, not started
    quit=False
    start=False
    
    IntroDisplay()              #displays splash image 
    pos,flag=0,0
    
    while not start:                            #waiting till player starts by pressing any key
        for event in pygame.event.get():
            if event.type==pygame.QUIT:             #if player clicks close
                pygame.display.flip()
                pygame.quit()
                _exit(0)
            if event.type==pygame.KEYDOWN:              #if it presses key ,then break and start game
                start=True
                pygame.mixer.Sound.play(SwooshSound)
        #GameDisplay.fill(SkyBlue)
        BackGround()
        if flag:                        #used flag to allow alternate up and then down motion of bird
            pos-=4
        else:
            pos+=4
        if pos>=130:
            flag=1
        elif pos<=0:
            flag=0    
        Bird(x,y+pos)                   #displays bird at passed coordinates
        MesssageDisplay("PRESS SPACEBAR TO START")
        Ground(x_ground)                #displays ground image
        #StartButton()
        
        pygame.display.flip()
        Clock.tick(60)              #60 FPS
                
    while not crashed and (not quit):
        
        for event in pygame.event.get():   #for every input observed 
            if event.type==pygame.QUIT:             #if clicked close
                quit=True

            if event.type == pygame.KEYDOWN and y>0:    #if pressed spacebar key down
                if event.key== pygame.K_SPACE and y>0:
                    y_change-=60
                    pygame.mixer.Sound.play(FlapSound)

            if event.type==pygame.KEYUP:                #if removed pressure from spacebar key
                if event.key == pygame.K_SPACE:
                    y_change=00
                    Velocity=7        #resets falling velocity
        
            y+=y_change              #changes the y coordinate of bird
        y=y+Velocity
        Velocity+=0.18                  #velocity of falling bird incerases with time
#this increase stimulates gravity in game
        x_pillar=[ (x_pillar[i]-GroundVelocity) for i in range(3)]
          
        BackGround()
        x_ground-=GroundVelocity            #ground also seems to move
        if x_ground<-600:                    #reset ground if gone too left
            x_ground=0
        GroundVelocity+=GroundVelocityIncrease   #increase spped of pillars as game continues

        for i in range(3):
            PillarDisplay(x_pillar[i],y_pillar[i])

        Ground(x_ground)     #displays ground and then bird in next line
        Bird(x,y)
        
        for i in range(3):
            if x_pillar[i]<-PillarWidth:
               y_pillar[i]=randint(150,650-GapSize)
               x_pillar[i]=1300 
            if 300-(GroundVelocity/2)<x_pillar[i]+PillarWidth<=300+(GroundVelocity/2): 
                Score+=1  
                pygame.mixer.Sound.play(PointSound)
            if x-PillarWidth<=x_pillar[i]<=x+BirdWidth:
                if not (y>y_pillar[i] and y+BirdHeight<y_pillar[i]+GapSize):    #when bird hits pillar2
                    crashed=True

        ScoreDisplay("Score: "+str(Score))   #to call function to display current score
       
        if y+BirdHeight>DisplayHeight-GroundHeight:   #when it hits the ground
            crashed=True
        
        if crashed:
            pygame.time.delay(2000)
            pygame.mixer.Sound(HitSound)

        if crashed or quit:     #if crashed or quitted , then take to gameover screen
            ending(Score)
        
        
        pygame.display.flip()

        Clock.tick(60)

GameLoop()          #initites the game at very first time