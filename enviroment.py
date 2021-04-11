import pygame, random
from CONSTANTS import VARIABLES, HEIGHT, WIDTH, BLACK
from neural_network import Network
import user_interface

import numpy as np


pipe_list, pipe_rect_list = [], []
gravity = .4


def positive(number):
    if number >= 0:
        return number
    else:
        return -number


class Display:
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.active = True
        self.clock = pygame.time.Clock()

    def update(self):
        pygame.font.init()
        myfont = pygame.font.Font('04B_19.ttf', 30)
        textsurface = myfont.render(f"GEN {VARIABLES.generation}", False, (255, 255, 255))
        textsurface2 = myfont.render(f"Score {VARIABLES.best_round_score}", False, (255, 255, 255))
        textsurface3 = myfont.render(f"Alive {VARIABLES.n_alive}", False, (255, 255, 255))
        self.display.blit(textsurface, (WIDTH - 150, 20))
        self.display.blit(textsurface2, (0, 20))
        self.display.blit(textsurface3, (300, 20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        self.clock.tick(120)

    def fill_black(self):
        pygame.draw.rect(self.display, BLACK, (0, 0, WIDTH, HEIGHT))

    def quit(self):
        self.active = False
        exit()


class Pipe:
    def __init__(self, spawnx):
        self.width = 80
        self.space = int(150 / 2)
        random_number = random.randint(self.space,HEIGHT - self.space)
        self.rect_upper = pygame.Rect((int(spawnx), 0, self.width, random_number - self.space))
        self.rect_lower = pygame.Rect((int(spawnx), random_number + self.space, self.width, HEIGHT))

    def reset(self):
        random_number = random.randint(self.space, HEIGHT - self.space)
        self.rect_upper = pygame.Rect((WIDTH, 0, self.width, random_number - self.space))
        self.rect_lower = pygame.Rect((WIDTH, random_number + self.space, self.width, HEIGHT))

    def draw(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.rect_upper)
        pygame.draw.rect(display, (255, 0, 0), self.rect_lower)

    def update(self):
        self.rect_upper.centerx -= 2
        self.rect_lower.centerx -= 2
        if self.rect_upper.right < -50:
            self.reset()


class Individual:
    def __init__(self):
        self.NN = Network(5, 1)
        self.alive = True
        self.reached_pilars = 0
        self.score = 0
        self.rect = pygame.Rect((int(WIDTH / 2), int(HEIGHT / 2)), (40, 40))
        self.movement_y = 0
        self.bool = True
        self.bool2 = True

    def draw(self, display):
        pygame.draw.rect(display, (0, 255, 0), self.rect, 1)

    def update(self):
        if self.alive:
            self.score+=1
            self.predict()
            self.movement_y += gravity
            self.rect.centery += self.movement_y
            self.check()
            VARIABLES.best_round_score = self.reached_pilars

    def check(self):
        global pipe_rect_list
        if self.rect.collidelist(pipe_rect_list) != -1:
            self.alive = False

        if pipe_rect_list[0].centerx - 10 < self.rect.centerx < pipe_rect_list[0].centerx + 10 and self.bool:
            self.bool = False
            self.reached_pilars += 1
        elif not pipe_rect_list[0].centerx - 10 < self.rect.centerx < pipe_rect_list[0].centerx + 10:
            self.bool = True

        if pipe_rect_list[2].centerx - 10 < self.rect.centerx < pipe_rect_list[1].centerx + 10 and self.bool2:
            self.bool2 = False
            self.reached_pilars += 1
        elif not pipe_rect_list[2].centerx - 10 < self.rect.centerx < pipe_rect_list[1].centerx + 10:
            self.bool2 = True

        if self.rect.bottom>HEIGHT or self.rect.top < 0:
            self.alive = False

    def jump(self):
        self.movement_y = -8

    def get_state(self):
        global pipe_list
        if pipe_list[0].rect_upper.right < self.rect.left and pipe_list[0].rect_upper.right < pipe_list[1].rect_upper.right:
            pipe = pipe_list[1]
        elif pipe_list[1].rect_upper.right < self.rect.left and pipe_list[1].rect_upper.right < pipe_list[0].rect_upper.right:
            pipe = pipe_list[0]
        else:
            pipe = pipe_list[0]
        return [self.rect.centery/HEIGHT, pipe.rect_upper.bottom/HEIGHT,
                pipe.rect_lower.top/HEIGHT, pipe.rect_lower.centerx/WIDTH,
                self.movement_y/20]

    def pair(self, other):
        new_weight1 = self.NN.get_flatted()
        new_weight2 = other.NN.get_flatted()
        gene = random.randint(0, len(new_weight1) - 1)
        new_weight1[gene:], new_weight2[:gene] = new_weight2[gene:], new_weight1[:gene]

        return new_weight1, new_weight2

    def predict(self):
        output = self.NN.predict(self.get_state())
        if output < 0.5:
            self.jump()

    def reset(self):
        self.rect.centery = int(HEIGHT / 2)
        self.alive = True
        self.reached_pilars = 0
        self.score = 0


screen = Display()

def run_simulation(individuals):
    global pipe_list, pipe_rect_list
    pipe_list = [Pipe(HEIGHT), Pipe(HEIGHT + HEIGHT / 1.8)]
    screen.active = True
    while screen.active:
        screen.fill_black()
        for i in range(VARIABLES.speed):
            user_interface.flip()
            pipe_rect_list = []
            for pipe in pipe_list:
                pipe.update()
                pipe.draw(screen.display)
                pipe_rect_list.append(pipe.rect_upper)
                pipe_rect_list.append(pipe.rect_lower)
            VARIABLES.n_alive = 0
            for individual in individuals:
                if individual.alive:
                    VARIABLES.n_alive+=1
                individual.update()


            if not True in [x.alive for x in individuals]:
                break

        if not True in [x.alive for x in individuals]:
            break
        for pipe in pipe_list:
            pipe.draw(screen.display)
        for individual in individuals:
            if individual.alive:
                individual.draw(screen.display)
        screen.update()