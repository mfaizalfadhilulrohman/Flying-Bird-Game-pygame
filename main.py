import pygame
import math

# Untuk awalan seperti inisialisasi, lebaserta panjang layar, judul dan icon
pygame.init()
screen=pygame.display.set_mode((280,510))
pygame.display.set_caption('Flying Bird')
icon=pygame.image.load('assets/image/favicon.png').convert_alpha()
pygame.display.set_icon(icon)

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

# gambar latar belakang
Chose_Background=0
Base=pygame.image.load('assets/image/base.png').convert_alpha()
background_day=[pygame.image.load('assets/image/background-day.png').convert_alpha(),pygame.image.load('assets/image/background-night.png').convert_alpha()]
message=pygame.image.load('assets/image/message.png').convert_alpha()
GameOver=pygame.image.load('assets/image/gameover.png').convert_alpha()

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
gameover=False

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

# pecapaiana
Skor=0

running = True
while running:
    pygame.time.Clock().tick(60)
    pygame.display.update()

    ImageRender(background_day[Chose_Background],0,0)

    if Skor>=50:
        Chose_Background=1
    else:
        Chose_Background=0
        
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
                Flybird-=30
                rotasi=20 
                choseflap=2
                wing.play()
                if gameover:
                    loby=True
                    gameover=False
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT :
        #         Flybird+=5
    if loby:
        ImageRender(message,45,100)
        FontRender(font,80,260)
        ImageRender(Bird[Choose][0],120,268)
        continue
    if Game:
        ImageRender(Base,0,400)
        Flybird+=1
        if rotasi>=-35:
            rotasi-=4
        ImageRender(pygame.transform.rotate(Bird[Choose][choseflap],rotasi),20,Flybird)
        choseflap=0
        if tabrakan(0,400,0,Flybird) < 160:
            hit.play()
            Game=False
            die.play()
            gameover=True
        continue
    
    ImageRender(GameOver,45,220)
    Flybird=268
    
pygame.quit()