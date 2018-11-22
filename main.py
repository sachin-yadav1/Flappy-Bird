from random import randint
import pygame
import time
from os import _exit                

#some common colours RGB codes
White=(255,255,255)                      
Black=(000,000,000)
SkyBlue=(0,255,255)
Blue=(0,0,255)
#pygame initiated here
pygame.init()                         

GroundHeight=100                       #height of ground above screen bottom line
BirdHeight=60
BirdWidth=60
GapSize=180                             #size of gap in beween the pillar  
PillarWidth=130
PillarHeight=1200
GroundVelocityIncrease=0.005             #proportional to increase in pillar speed over time
DisplaySize=DisplayWidth,DisplayHeight=(1300,850)           #Size of screen in pixels
GapBetweenPillars=DisplayWidth//3                       #gap between two consecutive pillars
InitialPillar=100
ScoreDisplayHeight=100                              #height for position of score display
InitialVelocity=5             #Velocity of bird to fall
x_Bird=300
y_Bird=100    #initial y coordinate of bird
FPS=60                                  #frames per sec
UPstep=60                               #distance the bird moves when presses spacebar
GroundVelocity=3
Mode=0                  #to keep track of character's skin ,by default set to bird image
Gravity=10.8/FPS          #corresponds to 10.8 m/sec^2 gravitational accelaeration

GameDisplay =pygame.display.set_mode(DisplaySize)   
pygame.display.set_caption("FLAPPY BIRD")       #written Flappy bird in title bar
Clock=pygame.time.Clock()
#loading all the required images from the images folder                        
#some images were made in paint and other taken from internet
BackGroundImg=pygame.image.load("Images/bg img.png")
#Images are edited using https://www110.lunapic.com/editor/ 
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

#to change character's image as per the mode chosen
def PlayerMode(Mode):
    global PlayerImg                
    if Mode==0:
        PlayerImg=BirdImg
    elif Mode==1:
        PlayerImg=SupermanImg
    elif Mode==2:
        PlayerImg=AirplaneImg

def Player(x,y):              #takes x,y coordinates of the top left corner of character and displays it
    GameDisplay.blit(PlayerImg,(x,y))

def Ground(x_ground):               #takes x coordinate of the ground and displays it
    GameDisplay.blit(GroundImg,(x_ground,DisplayHeight-GroundHeight))

def BackGround():               #displays backgroung image with its top left at 0,0
    GameDisplay.blit(BackGroundImg,(0,0))
                                

def MessageDisplay(text,y):      #the string to be displayed is passed as text
    font = pygame.font.Font('freesansbold.ttf',40) #font style=fresanbold and size=80
    TextSurf=font.render(text, True, Black)               
    GameDisplay.blit(TextSurf,(DisplayWidth//2-250,y))      #showing textSurf at given (x,y) tuple 

def PillarDisplay(x,y):                 #for displaying pillars
    GameDisplay.blit(PillarUpImg,(x,y-PillarHeight))    #displays upper pillar
    GameDisplay.blit(PillarDownImg,(x,y+GapSize))        #displays lower pillar

def ScoreDisplay(score):                        #for displaying current score
    Font=pygame.font.Font('freesansbold.ttf',60)      #fontstyle and size specified
    TextSurf = Font.render(score, True, Blue)
    GameDisplay.blit(TextSurf,(DisplayWidth//2-100,100))
    pygame.display.update()

def ending(score):                      #executed when player quits or hits a pillar
    pygame.mixer.Sound.play(DieSound)           #plays die sound
    GameDisplay.blit(GameOverImg,(0,0))         #displays gameover image
    
    font=pygame.font.Font('freesansbold.ttf',50)
    textSurface = font.render("YOUR SCORE: "+str(score), True, (255,0,0)) #displays player's final score
    GameDisplay.blit(textSurface,((DisplayWidth/2-200,ScoreDisplayHeight+550)))
    
    file=open("Logs/score.txt","r")              #opens Logs\score.txt to check the previous highscore
    HighScore=max(score,int(file.readline()))      #finds new HighScore
    
    Font=pygame.font.Font('freesansbold.ttf',50)   
    TextSurf = Font.render("HIGH SCORE: "+str(HighScore), True, (255,0,0))  #displays current HighScore
    GameDisplay.blit(TextSurf,(DisplayWidth/2-200,ScoreDisplayHeight+610))
    
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

    #these commands sets initail values for score ,pillar positions ,velocity and (x,y) of bird
    Score=0                                      
    y_change=0 
    x_ground=0     
    x_Pillar=[DisplayWidth+InitialPillar,DisplayWidth+InitialPillar+GapBetweenPillars,DisplayWidth+InitialPillar+2*GapBetweenPillars]                             
    y_Pillar=[ randint(60,680-GapSize) for i in range(3)]
    y=y_Bird
    velocity=InitialVelocity
    global GroundVelocity
    global Mode

    crashed=False                   #initially not crashed, not quitted, not started
    quit=False
    start=False
    
    IntroDisplay()              #displays splash image 
    pos,flag=0,0
    
    #waits till player starts the game
    while not start:                
        global Mode                        #waiting till player starts by pressing spacebar
        for event in pygame.event.get():
            if event.type==pygame.QUIT:             #if player clicks close
                pygame.display.flip()
                pygame.quit()
                _exit(0)
            if event.type==pygame.KEYDOWN:             
                if event.key==pygame.K_s:           #change character's mode by changing mode
                    Mode+=1
                    if Mode==3:
                        Mode=0
                if event.key==pygame.K_SPACE:          #if pressed spacebar ,the game starts
                    start=True
                    pygame.mixer.Sound.play(SwooshSound)
        PlayerMode(Mode)                        #updates the mode as chosen
    
        BackGround()
        if flag:                        #used flag to allow alternate up and then down motion of bird
            pos-=4
        else:
            pos+=4
        if pos>=130:
            flag=1
        elif pos<=0:
            flag=0    
        Player(x_Bird,y_Bird+pos)                   #displays bird at passed coordinates
        MessageDisplay("PRESS SPACEBAR TO START",120)
        MessageDisplay("PRESS S TO CHANGE THE CHARACTER",50)
        pygame.display.flip()
        Ground(x_ground)                #displays ground image
        
        pygame.display.flip()
        Clock.tick(FPS)              #60 FPS
                
    while not crashed and (not quit):
        
        for event in pygame.event.get():   #for every input observed 
            if event.type==pygame.QUIT:             #if clicked close
                quit=True

            if event.type == pygame.KEYDOWN and y>0:    #if pressed spacebar key down
                if event.key== pygame.K_SPACE and y>0:
                    y_change-=UPstep                       #changes y coordinate by UPstep of bird
                    pygame.mixer.Sound.play(FlapSound)

            if event.type==pygame.KEYUP:                #if removed pressure from spacebar key
                if event.key == pygame.K_SPACE:
                    y_change=0
                    velocity=InitialVelocity    #resets falling velocity to initial velocity
        
            y+=y_change              #changes the y coordinate of bird
        y=y+velocity
        velocity+=Gravity                #velocity of falling bird incerases with time
#this increase stimulates gravity in game
        #causes movement of pillars along with ground in rate of ground velocity
        x_Pillar=[ (x_Pillar[i]-GroundVelocity) for i in range(3)]
          
        BackGround()
        x_ground-=GroundVelocity            #ground also seems to move
        if x_ground<-600:                    #reset ground if gone too left
            x_ground=0
        
        GroundVelocity+=GroundVelocityIncrease   #increase speed and difficulty of pillars as game continues

        for i in range(3):
            PillarDisplay(x_Pillar[i],y_Pillar[i])          #displays the pillars

        Ground(x_ground)     #displays ground and then bird in next line
        Player(x_Bird,y)
        

        for i in range(3):  
            if x_Pillar[i]<-PillarWidth:        #if pillar vanishes on left, randomize its gap location
               y_Pillar[i]=randint(150,650-GapSize)
               x_Pillar[i]=DisplayWidth            #place pillar on right edge then
            #increases score when bird passes a pillar
            if x_Bird-(GroundVelocity/2)<x_Pillar[i]+PillarWidth<=x_Bird+(GroundVelocity/2): 
                Score+=1  
                pygame.mixer.Sound.play(PointSound)
            #crash condition for bird with pillar
            if x_Bird-PillarWidth<=x_Pillar[i]<=x_Bird+BirdWidth:
                if not (y>y_Pillar[i] and y+BirdHeight<y_Pillar[i]+GapSize):    #when bird hits pillar
                    crashed=True

        ScoreDisplay("Score: "+str(Score))   #to call function to display current score
       
       #crash condition of bird with ground
        if y+BirdHeight>DisplayHeight-GroundHeight:   #when it hits the ground
            crashed=True
        
        if crashed:
            pygame.time.delay(2000)
            pygame.mixer.Sound(HitSound)

        if crashed or quit:     #if crashed or quitted , then take to gameover screen and show score
            ending(Score)
        
        pygame.display.flip()
        Clock.tick(FPS)

GameLoop()          #initites the game at very first time