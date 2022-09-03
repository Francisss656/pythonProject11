import pygame
from random import randint

pygame.init()
pygame.mixer.music.load('sound/Infinite Game Music — TMNT Arcade - Highway (Konami) (www.lightaudio.ru) (1).mp3')
pygame.mixer.music.set_volume(0.1) #Звук игры оценивается от 0 до 1
pygame.mixer.music.play(-1)#С помощью минус 1 музыка будет зациклена и играть без остановки

sndFall = pygame.mixer.Sound('sound/sword-slash.mp3')

WIDTH, HEIGHT = 800, 600 #
FPS = 60 #

window = pygame.display.set_mode((WIDTH, HEIGHT)) #
clock = pygame.time.Clock()

pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('pictures/icon (1).png'))

font1 = pygame.font.Font(None, 35) #Вывод очков
font2 = pygame.font.Font(None, 80) #Вывод жизней
#Загрузка необходимых изображений
imgBG = pygame.image.load('pictures/BG.png')
imgBird = pygame.image.load('pictures/bd.png')
imgPT = pygame.image.load('pictures/pt.png')
imgPB = pygame.image.load('pictures/pb.png')

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 34, 24)
frame = 0

state = 'start'
timer = 10

pipes = []
bges = []
pipesScores = [] #Трубы относящиеся к очкам
pipe_gate_size = 200
pipe_gate_pos = HEIGHT // 2

pipeSpeed = 3

bges.append(pygame.Rect(0, 0, 288, 600))

lives = 3 #Жизни
scores = 0 #Очки

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer: timer -= 1 #Пайтон сам поймет, так как таймер равен 10

    frame = (frame + 0.2) % 4


    for i in range(len(bges) - 1, -1, -1):
        bg = bges[i]
        bg.x -= pipeSpeed // 2 #Нельзя ставить обычное деление так как такое деление будет добавлять дробную часть в позиции и это привдет к тому что первый фн будет двигаться медленнее чем другие

        if bg.right < 0: bges.remove(bg)

        if bges[len(bges) - 1].right <= WIDTH:
            bges.append(pygame.Rect(bges[len(bges) - 1].right, 0, 288, 600))

    for i in range(len(pipes) - 1, -1, -1): #Трубы
        pipe = pipes[i]
        pipe.x -= pipeSpeed#От этого зависит скорость движения

        if pipe.right < 0:
            pipes.remove(pipe)
        if pipe in pipesScores:
                 pipesScores.remove(pipe)

    if state == 'start':
        if click and timer == 0 and len(pipes) == 0: state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.y = py

    elif state == 'play': #Движение птицы относительно труб
        if click: ay = -2
        else: ay = 0

        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 52, pipe_gate_pos - pipe_gate_size // 2))
            pipes.append(pygame.Rect(WIDTH, pipe_gate_pos + pipe_gate_size // 2, 52, HEIGHT - pipe_gate_pos + pipe_gate_size // 2))

            pipe_gate_pos += randint(-100, 100)
            if pipe_gate_pos < pipe_gate_size:
                pipe_gate_pos = pipe_gate_size
            elif pipe_gate_pos > HEIGHT - pipe_gate_size:
                pipe_gate_pos = HEIGHT - pipe_gate_size

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'

            if pipe.right < player.left and pipe not in pipesScores:
                pipesScores.append(pipe)
                scores += 5


    elif state == 'fall':
        sndFall.play()
        sy, ay = 0, 0
        pipe_gate_pos = HEIGHT // 2


        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 60
        else:
            state = 'game over'
            timer = 120

    else:
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if timer == 0: play = False #Игра заавершится

    window.fill('black')
    for bg in bges:
        window.blit(imgBG, bg) #Вывод бэкграунда

    for pipe in pipes: #Вывод труб
        if pipe.y == 0:
            rect = imgPT.get_rect(bottomleft=pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPB.get_rect(topleft=pipe.topleft)
            window.blit(imgPB, rect)

    image = imgBird.subsurface(34 * int(frame), 0, 34, 24)#
    image = pygame.transform.rotate(image, -sy * 2)#Положение птицы
    window.blit(image, player)#

    text = font1.render('Очки: ' + str(scores), 1, 'black') #Вывод очков
    window.blit(text, (10, 10))

    text = font1.render('Жизни: ' + str(lives), 1, 'black') #Вывод жизней
    window.blit(text, (10, HEIGHT - 30)) #HEIGHT - нижняя граница экрана

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

