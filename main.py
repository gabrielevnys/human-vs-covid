import pygame, sys, random, math, time
pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((400, 600))

# Title screen
init_surface = pygame.image.load('assets/titlescreen.png').convert_alpha()
init_rect = init_surface.get_rect(center = (200,300))

# Game Running
running = False
clock = pygame.time.Clock()
FPS_dict = {'slow':100, 'medium':140, 'fast':180, 'very fast' : 220}
FPS = FPS_dict['slow']

# Street
street = pygame.image.load('assets/street.jpg').convert()
street_y_pos = 0

# Title and Icon
pygame.display.set_caption("Human vs Covid")
# icon = pygame.image.load("")
# pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("assets/player.png")
playerX = 10
playerY = 500
playerX_change = 0

# Object
object_img = []
mask = pygame.image.load('assets/mask.png').convert_alpha()
vaccine = pygame.image.load('assets/vaccine.png').convert_alpha()
sanitizer = pygame.image.load('assets/sanitizer.png').convert_alpha()
object_list = [mask, vaccine, sanitizer]
object_count = 500
objectX = []
objectY = []
objectY_change = []
objectX_list = [47, 167, 290]
objectY_list = []

# Enemy/Virus
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
enemy_count = 200
enemyX_list = [47, 167, 290]
enemyY_list = []

# Menambahkan koordinat y objek virus ke dalam list sebanyak loop
j = -30000
while j < 50:
    objectY_list.append(j)
    j += 125

# Menambahkan Gambar Objek Acak sebanyak looping & koordinat tiap2 objek
for i in range(object_count):
    object_img.append(random.choice(object_list))
    objectX.append(random.choice(objectX_list))
    objectY.append(random.choice(objectY_list))
    #  Kecepatan perpindahan objek ke bawah    
    objectY_change.append(3)


# Menambahkan koordinat y objek virus ke dalam list sebanyak loop
v = -40000
while v < 50:
    enemyY_list.append(v)
    v += 250

# Menambahkan Gambar Virus sebanyak looping & koordinat acak tiap2 objek
for i in range(enemy_count):
    enemyImg.append(pygame.image.load("assets/coronavirus.png").convert_alpha())
    enemyX.append(random.choice(enemyX_list))
    enemyY.append(random.choice(enemyY_list))
    # Kecepatan perpindahan objek ke bawah
    enemyY_change.append(3)

# Score
score_value = 0
high_score_value = 0

# Style Font
font = pygame.font.Font('assets/font/dogicapixel.ttf', 20)
speed_up_font = pygame.font.Font('assets/font/dogicapixel.ttf', 15)

# Posisi Score
textX = 10
textY = 10

# Nyawa
lifeImg = pygame.image.load("assets/heart.png")

# Posisi nyawa
lifeX = -30
lifeY = 50

# Song / Sound
dead_sound = pygame.mixer.Sound('assets/sound/game_over.mp3')
run_sound = pygame.mixer.Sound('assets/sound/run.mp3')

# FUNCTION
def player(x, y):
    screen.blit(playerImg, (x, y))

def player_animation():
    new_player = player_frames[player_index]
    new_player_rect = new_player.get_rect(center = (10,player_rect.centery))
    return new_player,new_player_rect

def object(x, y, i ):    
    screen.blit(object_img[i], (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))     

def draw_street():
    screen.blit(street,(0,street_y_pos))   
    screen.blit(street,(0, street_y_pos - 600))    

def isCollision(obj1X, obj1Y, obj2X, obj2Y):
    # Algoritma untuk Menghitung jarak 2 Objek
    distance = math.sqrt((math.pow(obj1X-obj2X,2)) + (math.pow(obj1Y-obj2Y,2)))
    # Memastikan jarak antara 2 objek berdekatan/bersentuhan 
    if distance < 60:
        return True
    else:
        return False

def show_life(x, y): 
    screen.blit(lifeImg, (x, y))

def show_score(x, y):
    if running:
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))
    else:
        score = font.render("Score: " + str(score_value) ,True,(255,255,255))
        screen.blit(score, (130,100))
        high_score = font.render("High Score: " + str(high_score_value),True,(255,255,255))
        screen.blit(high_score,(100,500))
           

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs            

def do_not_pile_obj(listObjY, listY, indexY):
    list = []
    temp = []
    for i in indexY:
        temp.append(listY[i])
        for y in temp:
            if y not in list:
                list.append(y)

    able = []           
    for i in listObjY:
        if i not in list:
            able.append(i)
    while len(list) < len(temp) :
        if len(able) > 0:
            ran = random.choice(able)       
            list.append(ran)
            able.remove(ran)
    return list   

def do_not_pile_vir(listY, indexY, able):
    list = []
    temp = []
    for i in indexY:
        temp.append(listY[i])
    for y in temp:
        if y not in list and y in able:
            list.append(y)    
    new_able = []        
    for x in able:
        if x not in list:
            new_able.append(x)    
           
    while len(list) < len(temp) :
        if len(new_able) > 0:
            ran = random.choice(new_able)       
            list.append(ran)
            new_able.remove(ran)

    return list     
 
# END FUNCTION 


# Merapikan kembali objek yg masih tertumpuk

# Mengatur Objek X 47 
indexX47 = list_duplicates_of(objectX, 47)
listY47 = do_not_pile_obj(objectY_list, objectY, indexX47)
for i in range(len(indexX47)):
    objectY[indexX47[i]] = listY47[i]

# Mengatur Objek X 167
indexX167 = list_duplicates_of(objectX, 167)
listY167 = do_not_pile_obj(objectY_list, objectY, indexX167)
for i in range(len(indexX167)):
    objectY[indexX167[i]] = listY167[i]   
    
# Mengatur Objek X 290 
indexX290 = list_duplicates_of(objectX, 290)
listY290 = do_not_pile_obj(objectY_list, objectY, indexX290)
for i in range(len(indexX290)):
    objectY[indexX290[i]] = listY290[i]   

# Mengatur Virus X 47 
listY_able = []
indexX47 = list_duplicates_of(enemyX, 47)
for item in enemyY_list:  
    if item not in listY47:
        listY_able.append(item)
vlistY47 = do_not_pile_vir(enemyY, indexX47, listY_able)       
for i in range(len(indexX47)):
    enemyY[indexX47[i]] = vlistY47[i]

# Mengatur Virus X 167 
listY_able = []
indexX167 = list_duplicates_of(enemyX, 167) 
for item in enemyY_list:  
    if item not in listY167:
        listY_able.append(item)
vlistY167 = do_not_pile_vir(enemyY, indexX167, listY_able)         
for i in range(len(indexX167)):
    enemyY[indexX167[i]] = vlistY167[i]    

# Mengatur Virus X 290 
listY_able = []
indexX290 = list_duplicates_of(enemyX, 290) 
for item in enemyY_list:  
    if item not in listY290:
        listY_able.append(item)
vlistY290 = do_not_pile_vir(enemyY, indexX290, listY_able)             
for i in range(len(indexX290)):
    enemyY[indexX290[i]] = vlistY290[i]       


# Game Loop
while True:
    clock.tick(FPS)
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit() 
        # Player Controller
        if event.type == pygame.KEYDOWN and not running:
            # Semua kembali ke value awal
            FPS = FPS_dict['slow']
            object_count = 500
            j = -30000
            v = -40000
            enemy_count = 200
            enemycol_counter = 0 # total tabrakan dengan virus
            enemycol_list = [[10,50],[50,50],[90,50]]
            score_value = 0
            time.sleep(1)
            run_sound.play()
            running = True
        if event.type == pygame.KEYDOWN and running:
            if event.key == pygame.K_LEFT:
                playerX_change = normal_playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = normal_playerX_change = 3    
        if event.type == pygame.KEYUP and running:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0    

    
    # Menampilkan jalanan bergerak          
    street_y_pos += 3
    draw_street()    
    if street_y_pos >= 600:
        street_y_pos = 0

    if running:
        playerX += playerX_change

        # Batasan Tempat player bergerak
        if playerX <= 10:
            playerX = 10
        elif playerX >= 290:    
            playerX = 290
        # End Player Controller    

        # Menampilkan Objek Poin (Vaksin, Masker, dll)            
        for i in range(object_count):
            # Menggerakkan Objek ke bawah
            objectY[i] += objectY_change[i]
            # Validasi saat Player menyentuh Objek
            collision = isCollision(objectX[i], objectY[i], playerX, playerY)
            if collision:
                score_value += 1
                objectX[i] = random.choice([47, 167, 290])
                objectY[i] -= 30000
            # Panggil fungsi untuk menampilkan ke layar
            object(objectX[i], objectY[i], i)

        # Menampilkan Objek Virus    
        for i in range(enemy_count):
            # Menggerakkan Objek ke bawah
            enemyY[i] += objectY_change[i]
            # Validasi saat Player menyentuh virus
            collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
            if collision:
                # Menghapus satu nyawa
                del enemycol_list[(len(enemycol_list)-1)]
                # Menghitung jumlah tabrakan dengan virus
                enemycol_counter += 1
                if enemycol_counter == 3:
                    run_sound.stop()
                    dead_sound.play()
                    time.sleep(2)
                    running = False
                enemyX[i] = random.choice([47, 167, 290])
                enemyY[i] -= 30000
            # Panggil fungsi untuk menampilkan ke layar
            enemy(enemyX[i], enemyY[i], i)    
        # Fungsi untuk menampilkan player
        player(playerX, playerY)

        # Speed jalanan bertambah cepat (FPS bertambah)
        if score_value != 0:
            if score_value >= 15 and score_value < 30:
                if score_value == 15:
                    speedup = speed_up_font.render("Speed Up, Watch Out!" ,True,(255,255,255))
                    screen.blit(speedup, (90,100))
                FPS = FPS_dict['medium']
            elif score_value >= 30 and score_value < 60:
                if score_value == 30:
                    speedup = speed_up_font.render("Speed Up, Watch Out!" ,True,(255,255,255))
                    screen.blit(speedup, (90,100))
                FPS = FPS_dict['fast']
            elif score_value >= 60:
                if score_value == 60:
                    speedup = speed_up_font.render("Speed Up, Watch Out!" ,True,(255,255,255))
                    screen.blit(speedup, (90,100))
                FPS = FPS_dict['very fast']    


        # Fungsi untuk menampilkan nyawa
        for lifepos in enemycol_list:
            show_life(lifepos[0],lifepos[1])
        
        # Set high score
        if running == False:
            if high_score_value < score_value:
                high_score_value = score_value    

    # Menampilkan title screen jika running == False
    else:
        # run_sound.stop()
        screen.blit(init_surface,init_rect)


    # Fungsi untuk menampilkan score
    show_score(textX, textY)                 
    pygame.display.update()                    
