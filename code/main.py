import pygame
from os.path import join
from random import randint,uniform

# initialization

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center= (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 500

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_durtation = 400

        mask = pygame.mask.from_surface(self.image)
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if(current_time - self.laser_shoot_time >= self.cooldown_durtation):
                self.can_shoot = True

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            laser = Laser(laser_surf,self.rect.midtop,(all_spirtes, laser_spirtes))
            self.can_shoot = False
            laser_sound.play( )
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()


class Stars(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center= (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self,surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
        mask = pygame.mask.from_surface(self.image)

    
    def update(self,dt):
        self.rect.centery -= 400 *dt
        if(self.rect.bottom <0):
            self.kill()
            

class Metor(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.roto_image = surf
        self.image = self.roto_image
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500)
        mask = pygame.mask.from_surface(self.image)
        self.rotation = 0

    
    def update(self,dt):
        self.rect.center += self.direction * self.speed *dt
        if(self.rect.top > WINDOW_HEIGHT):
            self.kill()
    
        #continously rotation 
        self.rotation += randint(100,700) * dt 
        self.image=pygame.transform.rotate(self.roto_image, self.rotation)
        self.rect = self.image.get_frect(center=self.rect.center)
    

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self,frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_ind = 0
        self.image = self.frames[self.frame_ind]
        self.rect = self.image.get_frect(center=pos)

    def update(self,dt):
        self.frame_ind += 20 * dt
        if self.frame_ind < len(self.frames) :
            self.image = self.frames[int(self.frame_ind)]
        else:
            self.kill()


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()
running = True 

def collision():
    global running
    collision = pygame.sprite.spritecollide(player, metor_spirtes, True, pygame.sprite.collide_mask  )
    if(collision):
        running = False
    for laser in laser_spirtes:
        collided_sprites = pygame.sprite.spritecollide(laser, metor_spirtes, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames,laser.rect.midtop, all_spirtes )
            explosion_sound.play()

def get_score():
    current_score = pygame.time.get_ticks()//100
    text_surf = font.render(str(current_score),True, (240,240,240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT-50))
    pygame.draw.rect(display_surface,(240,240,240),text_rect.inflate(20,10).move(0,-6),3,10)
    display_surface.blit(text_surf,text_rect)


# import image 
all_spirtes = pygame.sprite.Group()
metor_spirtes = pygame.sprite.Group()
laser_spirtes = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha( ) for i in range(21)]
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
game_sound = pygame.mixer.Sound(join('audio', 'game_music.wav'))
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
game_sound.set_volume(0.1)
game_sound.play(loops=-1)


for i in range(20):
    Stars(all_spirtes,star_surf)
player = Player(all_spirtes)
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)

metor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()

#metor timer
metor_event = pygame.event.custom_type()
pygame.time.set_timer(metor_event,500)

while running:
    dt = clock.tick()/1000
    
    #event loop
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if(event.type == metor_event):
            x,y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Metor(metor_surf,(x,y), (all_spirtes,metor_spirtes))

    all_spirtes.update(dt)
    collision()

    #draw the game
    display_surface.fill('#3a2e3f')
    get_score()
    all_spirtes.draw(display_surface)
    pygame.display.update()


#quit initialization
pygame.quit()