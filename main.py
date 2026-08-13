import pygame
import math
import random
import os

# Untuk awalan seperti inisialisasi, lebaserta panjang layar, judul dan icon
pygame.init()
screen=pygame.display.set_mode((280,510))
pygame.display.set_caption('Flying Bird')
icon=pygame.image.load('assets/image/favicon.png').convert_alpha()
pygame.display.set_icon(icon)

# pecapaian
Skor=0
Highscore=0

# File buat highscore
def HighScoreFile():
  if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as file:
      file.write("0") 
    return 0
  else:
    with open("highscore.txt", "r") as file:
      return int(file.read())

def MenambahScoreFile(skor):
    global Highscore
    with open("highscore.txt", "w+") as file:
        file.write(str(skor))
        file.seek(0)
        Highscore = int(file.read())

Highscore = HighScoreFile()

#audio
pygame.mixer.init()
wing=pygame.mixer.Sound('assets/audio/wing.wav')
wing.set_volume(0.5)
swoosh=pygame.mixer.Sound('assets/audio/swoosh.wav')
swoosh.set_volume(0.5)
die=pygame.mixer.Sound('assets/audio/die.wav')
die.set_volume(0.5)
hit=pygame.mixer.Sound('assets/audio/hit.wav')
hit.set_volume(0.5)
point=pygame.mixer.Sound('assets/audio/point.wav')
point.set_volume(0.5)

# gambar latar belakang
Chose_Background=0
Base=pygame.image.load('assets/image/base.png').convert_alpha()
background_day=[pygame.image.load('assets/image/background-day.png').convert_alpha(),pygame.image.load('assets/image/background-night.png').convert_alpha()]
message=pygame.image.load('assets/image/message.png').convert_alpha()
GameOver=pygame.image.load('assets/image/gameover.png').convert_alpha()

# gambar pipa pennghalang
pipa = [pygame.image.load('assets/image/pipe-green.png'),pygame.image.load('assets/image/pipe-red.png')]
pipa_x = 300
pipa_x_change = 1
pipa_y = random.randint(140,340)

# gambar karakter player
Bird=[[pygame.image.load('assets/image/bluebird-upflap.png').convert_alpha(),pygame.image.load('assets/image/bluebird-midflap.png').convert_alpha(),pygame.image.load('assets/image/bluebird-downflap.png').convert_alpha()],
      [pygame.image.load('assets/image/redbird-upflap.png').convert_alpha(),pygame.image.load('assets/image/redbird-midflap.png').convert_alpha(),pygame.image.load('assets/image/redbird-downflap.png').convert_alpha()],
      [pygame.image.load('assets/image/yellowbird-upflap.png').convert_alpha(),pygame.image.load('assets/image/yellowbird-midflap.png').convert_alpha(),pygame.image.load('assets/image/yellowbird-downflap.png').convert_alpha()]
      ]
rotasi=0
choseflap=0

# render gambar
def ImageRender(Image,LokasiX,LokasiY):
    screen.blit(Image,(LokasiX,LokasiY))

# Tempat interksi berada
loby=True
Game=False

# Tulisan
font = pygame.font.Font(None,64)

# render huruf
def FontRender(Font,LokasiX,LokasiY):
    teks = Font.render('<     >',True,(255,255,255))
    ImageRender(teks,LokasiX,LokasiY)

# variabel aksi ganti karakter
Choose=0
Flybird=268 # Posisi Y karakter
#Change_Flybird=10  Penambahan posisi Y karakter
def tabrakan(x,y,X,Y):
    return math.sqrt((math.pow(x,2)-math.pow(X,2))+(math.pow(y,2)-math.pow(Y,2)))

# skor image
angka=[pygame.image.load('assets/image/0.png').convert_alpha(),
       pygame.image.load('assets/image/1.png').convert_alpha(),
       pygame.image.load('assets/image/2.png').convert_alpha(),
       pygame.image.load('assets/image/3.png').convert_alpha(),
       pygame.image.load('assets/image/4.png').convert_alpha(),
       pygame.image.load('assets/image/5.png').convert_alpha(),
       pygame.image.load('assets/image/6.png').convert_alpha(),
       pygame.image.load('assets/image/7.png').convert_alpha(),
       pygame.image.load('assets/image/8.png').convert_alpha(),
       pygame.image.load('assets/image/9.png').convert_alpha()
       ]

running = True
while running:
    pygame.time.Clock().tick(60)
    pygame.display.update()
    ImageRender(background_day[Chose_Background],0,0)
    if Skor==200 or Highscore==200 and not Game:
        ImageRender(font.render('WIN',True,(255,255,255)),90,390)

    if Skor==100:
        Chose_Background=1
    else:
        Chose_Background=0

    if Skor==200:
        Game=False
        
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                swoosh.play()
                if Choose>=2  and loby:
                    Choose=0
                elif Choose<=2 and loby:
                    Choose+=1
                if Game:
                    pipa_x-=15
            if event.key == pygame.K_LEFT:
                swoosh.play()
                if Choose<=0 and loby:
                    Choose=2
                elif Choose>=0 and loby:
                    Choose-=1
            if event.key == pygame.K_SPACE :
                if loby:
                    loby=False
                    Game=True
                elif Game:
                    for i in range(40):   
                        Flybird-=1
                    rotasi=20 
                    choseflap=2
                    wing.play()
                else:
                    loby=True

        if event.type == pygame.KEYUP:
            for i in range(10):
                Flybird+=1
    if loby:
        ImageRender(message,45,100)
        FontRender(font,80,260)
        ImageRender(Bird[Choose][0],120,268)
        for kali,number in enumerate(str(Highscore)):
            kali+=1
            ImageRender(angka[int(number)],20*kali,10)

    elif Game:

        Flybird+=1+(pipa_x_change//10)

        ImageRender(pipa[Chose_Background],pipa_x,pipa_y)
        ImageRender(pygame.transform.rotate(pipa[Chose_Background],180),pipa_x,pipa_y-440)
        if pipa_x<=-60:
            pipa_x=300
            pipa_y=random.randint(140,360)
            Skor+=10
            point.play()
            if Skor%100==0 and Skor//10>00:
                pipa_x_change+=0.2
        else:
            pipa_x-=pipa_x_change

        ImageRender(Base,0,400)
        if rotasi>=-20:
            rotasi-=1
        ImageRender(pygame.transform.rotate(Bird[Choose][choseflap],rotasi),20,Flybird)
        choseflap=0

        for kali,number in enumerate(str(Skor)):
            kali+=1
            ImageRender(angka[int(number)],20*kali,10)

        if tabrakan(0,400,0,Flybird) < 160:
            hit.play()
            Game=False
            die.play()

        # print(pipa_x[0],pipa_y[0]-440,pipa_y[0],Flybird)
        if (pipa_x<60 and pipa_x>-15) and (Flybird>=pipa_y-30 or Flybird<=pipa_y-130) :
            # print("yessss, masuk")
            hit.play()
            Game=False
            die.play()

    else:
        ImageRender(GameOver,45,220)
        pipa_x_change=0
        Flybird=268
        pipa_x=300
        pipa_y=random.randint(140,360)
        if Skor > Highscore:
            MenambahScoreFile(Skor)
            Highscore=Skor
        Skor=0
    
pygame.quit()