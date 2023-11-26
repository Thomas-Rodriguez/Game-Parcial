import pygame
import random

class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "left": False, "right": False}

        self.action = " "
        self.animation_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")
        self.last_mov = [0,0]

    def rect(self): #the rect of an object is twice the amount
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) #positon, then size

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()
            #creates  new instance of the ani, cus its more convinient rather than do the whole animation and then do the one thats happening

    def update(self, tilemap, movement=(0, 0)):
        self.collision = {"up": False, "down": False, "left": False, "right": False} #checks the type direction of collision we had

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])        

        self.pos[0] += frame_movement[0] #update the movement of postion X
        entity_rect = self.rect() #you adjust the player pos with taking int account with what they collieded with
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect): #if collision happens
                if frame_movement[0] > 0: #if you are moving right and collide with something
                    entity_rect.right = rect.left #the entity snaps back to the edge of the rect
                    self.collision["right"] = True
                if frame_movement[0] < 0: #if you are moving left and collide with something
                    entity_rect.left = rect.right #the entity snaps back to the edge of the rect
                    self.collision["left"] = True
                self.pos[0] = entity_rect.x

        if movement[0] > 0: #checks where its facing
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_mov = movement


        self.pos[1] += frame_movement[1] #upadte the movement of postion Y
        entity_rect = self.rect() #you adjust the player pos with taking int account with what they collieded with
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect): #if collision happens
                if frame_movement[1] > 0: #if you are moving up and collide with something
                    entity_rect.bottom = rect.top #the entity snaps back to the edge of the rect
                    self.collision["down"] = True
                if frame_movement[1] < 0: #if you are moving down and collide with something
                    entity_rect.top = rect.bottom #the entity snaps back to the edge of the rect
                    self.collision["up"] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1) #takes the lower value
        #is doing the same as self.velocity[1] += 0.5, but it takes thelower (5) value to cap the falling speed
        #gravity is acceleration times velocity

        if self.collision["up"] or self.collision["down"]: #bonks or stops your momentum
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surface, offset = (0,0)):
        surface.blit(pygame.transform.flip(self.animation.get_img(), self.flip, False), (self.pos[0] - offset[0] + self.animation_offset[0],self.pos[1] - offset[1] + self.animation_offset[1]))
        # takes the current animation, 

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.airtime = 0 #how long we have been in the air
        self.jumps = 2
        self.wall_slide = False
        self.dashing = 0
        self.score = 300

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement = movement)

        self.airtime += 1
        
        if self.collision["down"]:
            self.airtime = 0
            self.jumps = 2

        self.wall_slide = False
        if (self.collision["right"] or self.collision["left"]) and self.airtime > 4: #only when this happesn will be tru
            self.wall_slide = True
            self.airtime = 0
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collision["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_action("wall_slide") #updates the animation
        
        if not self.wall_slide:
            if self.airtime > 4:
                self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")

        if self.airtime > 120 and self.wall_slide == False:
            self.game.dead += 1

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51: #end of the dash frames
                self.velocity[0] *= 0.1 #cuts down the speed

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0) #tries to return the x movement but dont let it go below 0
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def render(self, surface, offset = (0,0)):
        if abs(self.dashing) <= 50: #if we arent in the first 10 frames
            super().render(surface, offset = offset)

    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_mov[0] < 0:
                self.velocity[0] = 3.5 #jumps away (x axis)
                self.velocity[1] = -2.5 #forces up
                self.airtime = 5 #updates the anim
                self.jumps = max(0, self.jumps - 1)
                return True
            elif self.flip == False and self.last_mov[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.airtime = 5
                self.jumps = max(0, self.jumps - 1) #jump is consumed
                return True
            
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.action = 5

    def dash(self):
        if not self.dashing:
            self.game.sound["dash"].play()
            if self.flip:
                self.dashing = -60  #direction, velocity is speed AND directon
            else:
                self.dashing = 60 #how long we dashin
                
class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        
        self.walking = 0
        
    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if (self.collision['right'] or self.collision['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.sound["megalovania"].play()
                return True
            
            
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))
