import pygame, sys, random

def animace_base(): #načtení dvou obrázku base za sebou, aby při posouvání, které je na ř 118,
    obrazovka.blit(base, (x, 400)) #došlo k téměř neviditelnému přechodu z jedné na druhé
    obrazovka.blit(base, (x + 288, 400))

def nova_prekazka():
    index = random.randint(200, 400) #načtení random indexu, ve kterém budou umístěny nové překážky
    novaprekazka1 = prekazka1.get_rect(midtop = (300,index)) #jedna na base, druhá vzhůru nohama
    novaprekazka2 = prekazka2.get_rect(midbottom = (300,index - 180 ))
    return novaprekazka1, novaprekazka2

def kredity(): #zobrazení počtu kreditů
    kredity = font.render(f' Kredity: ' + str(int(skore) ),True, (255,255,255))
    kredity_rect = kredity.get_rect(center = (144,80))
    obrazovka.blit(kredity, kredity_rect)

def game_over(pocetkreditu): #game over obrazovka, která zobrazí počet kreditů a do jakého ročníku ses dostal
    kredity = font.render('Dosazene kredity: ' + str(int(pocetkreditu) ),True, (255,255,255))
    kredity_rect = kredity.get_rect(center = (140,80))
    obrazovka.blit(kredity, kredity_rect)

    if pocetkreditu < 45:
        vysledek = font.render('Nedokoncil jsi ani',True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (148,120))
        obrazovka.blit(vysledek, vysledek_rect)
        vysledek = font.render('prvni rocnik :(',True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (148,140))
        obrazovka.blit(vysledek, vysledek_rect)
    if pocetkreditu < 95 and pocetkreditu > 45:
        vysledek = font.render(f'Vyhozen po prvnim' ,True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (148,120))
        obrazovka.blit(vysledek, vysledek_rect)
        vysledek = font.render(f'rocniku :( ' ,True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (190,140))
        obrazovka.blit(vysledek, vysledek_rect)
    if pocetkreditu < 180 and pocetkreditu > 95:
        vysledek = font.render(f'Vyhozen po druhem' ,True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (148,120))
        obrazovka.blit(vysledek, vysledek_rect)
        vysledek = font.render(f'rocniku :( ' ,True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (190,140))
        obrazovka.blit(vysledek, vysledek_rect)
    if pocetkreditu > 180:
        vysledek = font.render(f'Gratulace!',True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (190,120))
        obrazovka.blit(vysledek, vysledek_rect)
        vysledek = font.render(f'Bc. Flappy Bird',True, (255,255,255))
        vysledek_rect = kredity.get_rect(center = (170,140))
        obrazovka.blit(vysledek, vysledek_rect)
    playagain = font.render('SPACE to play',True, (255,255,255))
    playagain_rect = kredity.get_rect(center = (170,300))
    obrazovka.blit(playagain, playagain_rect)
    
pygame.init()
font = pygame.font.Font('04B_19.ttf',20)
obrazovka = pygame.display.set_mode((288,512)) #inicializace obrazovky pygame šířky 288, výšky 512 (zvoleno takto, protože odpovídají backround odrázku Flappy Bird)
pozadi =pygame.image.load('flappybird/mff_background.png').convert() #načte obrázek pozadí ze složky x a zvětší obrázek 2x, aby odpovídal rozměrům obrazovky
hodiny = pygame.time.Clock() #slouží k určení frames per second
skore = 0

pohyb_ptacka = 0
padani_ptacka = 0.20
ptacek = pygame.image.load('flappybird/bluebird-midflap.png').convert()
ptacek_rect = ptacek.get_rect(center = (100,256))

base = pygame.image.load('flappybird/base.png').convert()
x = 0

prekazka1 = pygame.image.load('flappybird/mff_pipe.png').convert()
prekazka2 = pygame.image.load('flappybird/mff_pipe2.png').convert()
prekazky_list = []
load_prekazdy = pygame.USEREVENT  # nastavení triger, kdy se bude načítat nová překážka
pygame.time.set_timer(load_prekazdy,1200) #a triger se bude spouštět každé 1,2 sekundy

running = True
while True: #game loop
    for udalost in pygame.event.get(): #pygame vyhledá všechny eventy, které proběhly
        if udalost.type == pygame.QUIT:  #ukončení programu
            pygame.quit()
            sys.exit()

        elif udalost.type == pygame.KEYUP and udalost.key == pygame.K_ESCAPE: #ukončení hry, pokud zmáčneme ESC
           running = False
        elif udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_SPACE and running: #skákání ptáčka
                pohyb_ptacka = 0
                pohyb_ptacka -= 6
            elif udalost.key == pygame.K_SPACE and running == False: #gameover a restart hry
                running = True
                prekazky_list = []
                ptacek_rect.center = (100,256)
                pohyb_ptacka = 0
                skore = 0
        elif udalost.type == load_prekazdy: #načítání překážek
            prekazky_list.append(nova_prekazka()) #pokud se spustí event load_prekazky, tak se do listu přidá nová překážka

    obrazovka.blit(pozadi, (0,0)) #umisteni obrazku pozadi na obrazovku do souradnic 0,0

    if running:    
        pohyb_ptacka += padani_ptacka 
        ptacek_rect.centery += pohyb_ptacka #zajištění, aby ptáček padal o 0.2 pixelu
        obrazovka.blit(ptacek, ptacek_rect) #umisteni ptacka na obrazovku
        for prekazka in prekazky_list:
            if ptacek_rect.colliderect(prekazka[0]) or ptacek_rect.colliderect(prekazka[1]): #pokud se ptáček srazí s překážkou
                running = False #k poznání kolize slouží funkce colliderect, která pozná, jestli se dva obdélníky protnuly
                
        if ptacek_rect.top < 0 or ptacek_rect.bottom > 530: #pokud je ptáček mimo obrazovku -> game over
            running = False 
            
        for prekazka in prekazky_list: #pohyb překážek
            prekazka[0].centerx -= 3
            prekazka[1].centerx -= 3
        for prekazka in prekazky_list: # zobrazení překážek na obrazovce
            obrazovka.blit(prekazka2, prekazka[1])                
            obrazovka.blit(prekazka1, prekazka[0])
        skore += 0.0076 #přičítání skóre tak, aby to cca vycházelo na dobu, kdy ptáček mine překážku
        kredity() #volání funkce kredity, která vypisuje 'kredity' a aktualni skore
    else: 
        game_over(skore) #načtení game over obrazovky (počet dosažených kreditů), pokud dojde ke kolizi
    x -= 1 #animace "země" (base), posouvá se o 1 pixel
    animace_base()
    if x <= -288: 
        x = 0
    pygame.display.update() #updatuje obrazovku o všechny změny, které proběhly před tímto příkazem
    hodiny.tick(100) #100 frames per second
