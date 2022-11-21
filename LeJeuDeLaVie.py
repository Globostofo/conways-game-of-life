import pygame
import os
import time

class CreateText:
    """Permet de créer un texte à l'aide de pygame"""

    def __init__(self, surface, text, color, size, rotation, position, margin):
        """Définition des variables de l'objet"""
        self.font = pygame.font.SysFont('consolas', 48)
        self.render = ''
        self.surface = surface
        self.text = text
        self.color = color
        self.size = size
        self.rotation = rotation
        self.position = position
        self.margin = margin

        """Création de l'objet"""
        self.set_text()
        self.set_size()
        self.set_rotation()
        self.get_rect()
        self.set_position()

    def set_text(self):
        """Crée le texte avec la police d'écriture et la couleur demandée"""
        self.render = self.font.render(self.text, 1, self.color)

    def set_size(self):
        """Modifie la taille du texte"""
        self.render = pygame.transform.scale(self.render, self.size)

    def set_rotation(self):
        """Modifie la rotation du texte"""
        self.render = pygame.transform.rotate(self.render, self.rotation)

    def get_rect(self):
        """Récupère le rectangle du texte"""
        self.rect = self.render.get_rect()

    def set_position(self):
        """Positionne le texte sur la fenêtre"""

        if self.position[0] == "left":
            self.rect.x = self.margin[0]
        elif self.position[0] == "1quarter":
            self.rect.x = round(self.surface.get_width() / 4 - self.render.get_width() / 2) + self.margin[0]
        elif self.position[0] == "center":
            self.rect.x = round(self.surface.get_width() / 2 - self.render.get_width() / 2) + self.margin[0]
        elif self.position[0] == "3quarter":
            self.rect.x = round(self.surface.get_width() * (3/4) - self.render.get_width() / 2) + self.margin[0]
        elif self.position[0] == "right":
            self.rect.x = self.surface.get_width() - self.render.get_width() - self.margin[0]
        else:
            self.rect.x = self.position[0] + self.margin[0]

        if self.position[1] == "top":
            self.rect.y = self.margin[1]
        elif self.position[1] == "center":
            self.rect.y = round(self.surface.get_height() / 2 - self.render.get_height() / 2) - self.margin[1]
        elif self.position[1] == "bottom":
            self.rect.y = self.surface.get_height() - self.render.get_height() - self.margin[1]
        else:
            self.rect.y = self.position[1] + self.margin[1]

    def blit(self):
        """Permet d'afficher l'objet sur la fenêtre"""
        screen.blit(self.render, self.rect)

class Cellule:
    def __init__(self):
        self.state = 0
        self.border_rect = pygame.Rect(j * (taille_cellule+1), i * (taille_cellule+1), taille_cellule + 2, taille_cellule + 2)
        self.cell_rect = pygame.Rect(j * (taille_cellule+1) + 1, i * (taille_cellule+1) + 1, taille_cellule + 1, taille_cellule + 1)

    def draw(self):
        pygame.draw.rect(screen, couleurs[self.state], self.cell_rect)
        pygame.draw.rect(screen, couleurs["bordure"], self.border_rect, epaisseur_bordure)

    def check_mouse_collision(self):
        if self.cell_rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def calcul_next_gen(self, x, y):
        self.check_voisins(x, y)
        if self.state == 0:
            if self.voisins == 3:
                self.state_next_gen = 1
            else:
                self.state_next_gen = 0
        elif self.state == 1:
            if self.voisins < 2 or self.voisins > 3:
                self.state_next_gen = 0
            else:
                self.state_next_gen = 1

    def check_voisins(self, x, y):
        self.voisins = 0
        for k in range(x-1, x+2):
            for l in range(y-1, y+2):
                if (k != x or l != y) and (0 < k < longueur_grille and 0 < l < largeur_grille):
                    if grille[l][k].state == 1:
                        self.voisins += 1

def change_mode(mode, h):
    pygame.draw.rect(screen, couleurs[0], (gen_auto_stop_rect.x - 5, gen_auto_stop_rect.y - 5, 400, 80))
    pygame.draw.rect(screen, couleurs[0], (8, screen.get_height() - 97, 15, 90))
    selector.margin = (8, h)
    selector.set_position()
    selector.blit()
    return mode

def refresh_gen_auto_text():
    pygame.draw.rect(screen, couleurs[0], (screen.get_width() - 173, screen.get_height() - 70, 40, 40))
    gen_auto_speed_text.text = vitesse[speed]
    gen_auto_speed_text.size = (len(vitesse[speed]) * 20, 40)
    gen_auto_speed_text.set_text()
    gen_auto_speed_text.set_size()
    gen_auto_speed_text.get_rect()
    gen_auto_speed_text.set_position()
    gen_auto_speed_text.blit()

def generate_next_gen():
    to_update = []
    for i in range(0, len(grille)):
        for j in range(0, len(grille[i])):
            if grille[i][j].state == 1:
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if ((k, l) not in to_update) and (0 <= k < largeur_grille) and (0 <= l < longueur_grille):
                            to_update.append((k, l))
    for (i, j) in to_update:
        grille[i][j].calcul_next_gen(j, i)
    for (i, j) in to_update:
        grille[i][j].state = grille[i][j].state_next_gen
        grille[i][j].draw()

couleurs = {0         : (255, 255, 255),
            1         : (  0,   0,   0),
            "bordure" : (125, 125, 125),
            "croix"   : (255,   0,   0)}

vitesse = {0 : "0",
           1 : "1",
           2 : "2",
           3 : "4",
           4 : "5",
           5 : "10",
           6 : "15",
           7 : "30",
           8 : "60"}

grille = []
taille_cellule = 12
epaisseur_bordure = 1
longueur_grille = 100
largeur_grille = 60
mode = 1
speed = 0
end = 0

for i in range(0, largeur_grille):
    grille.append([])
    for j in range(0, longueur_grille):
        grille[i].append(Cellule())

pygame.init()
pygame.display.set_caption("Le Jeu de la Vie")
os.environ['SDL_VIDEO_WINDOW_POS']="0,30"
screen = pygame.display.set_mode((longueur_grille * (taille_cellule+1) + 1, largeur_grille * (taille_cellule+1) + 101))
clock = pygame.time.Clock()

selector = CreateText(screen, "X", couleurs["croix"], (15, 25), 0, ("left", "bottom"), (8, 67))
edit_text = CreateText(screen, "modifier", couleurs[1], (8 * 10, 20), 0, ("left", "bottom"), (30, 70))
gen_text = CreateText(screen, "génération pas à pas", couleurs[1], (20 * 10, 20), 0, ("left", "bottom"), (30, 40))
gen_auto_text = CreateText(screen, "génération automatique", couleurs[1], (22 * 10, 20), 0, ("left", "bottom"), (30, 10))

edit_text_collision = pygame.Rect(edit_text.rect.x - 25, edit_text.rect.y - 5, gen_auto_text.rect.w + 30, edit_text.rect.h + 10)
gen_text_collision = pygame.Rect(edit_text.rect.x - 25, gen_text.rect.y - 5, gen_auto_text.rect.w + 30, edit_text.rect.h + 10)
gen_auto_text_collision = pygame.Rect(edit_text.rect.x - 25, gen_auto_text.rect.y - 5, gen_auto_text.rect.w + 30, edit_text.rect.h + 10)

reset_text = CreateText(screen, "reset", couleurs[1], (5 * 10, 20), 0, ("left", "bottom"), (350, 40))
reset_collision = pygame.Rect(reset_text.rect.x - 10, reset_text.rect.y - 10, reset_text.rect.w + 20, reset_text.rect.h + 20)

next_gen_rect = pygame.Rect(screen.get_width() - 78, screen.get_height() - 80, 60, 60)

gen_auto_stop_rect = pygame.Rect(screen.get_width() - 400, screen.get_height() - 80, 60, 60)
gen_auto_speed_down_rect = pygame.Rect(screen.get_width() - 288,screen.get_height() - 80, 85, 60)
gen_auto_speed_text = CreateText(screen, vitesse[speed], couleurs[1], (len(vitesse[speed]) * 20, 40), 0, ("right", "bottom"), (133, 30))
gen_auto_speed_up_rect = pygame.Rect(screen.get_width() - 103, screen.get_height() - 80, 85, 60)

running = True

screen.fill(couleurs[0])

for i in range(0, len(grille)):
    for j in range(0, len(grille[i])):
        grille[i][j].draw()

selector.blit()
edit_text.blit()
gen_text.blit()
gen_auto_text.blit()

pygame.draw.rect(screen, couleurs["bordure"], reset_collision, 5)
reset_text.blit()

while running:

    if mode == 3 and speed != 0 and time.time() > end:
        generate_next_gen()
        start = time.time()
        end = start + 1 / int(vitesse[speed])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if mode == 1 and 0 <= event.pos[0] < longueur_grille * (taille_cellule+1) and 0 <= event.pos[1] < largeur_grille * (taille_cellule+1):
                grille[event.pos[1] // (taille_cellule+1)][event.pos[0] // (taille_cellule+1)].state += 1
                grille[event.pos[1] // (taille_cellule+1)][event.pos[0] // (taille_cellule+1)].state %= 2
                grille[event.pos[1] // (taille_cellule+1)][event.pos[0] // (taille_cellule+1)].draw()

            elif mode == 2:
                if next_gen_rect.collidepoint(event.pos):
                    generate_next_gen()

            elif mode == 3:
                if gen_auto_stop_rect.collidepoint(event.pos):
                    speed = 0
                    refresh_gen_auto_text()

                elif gen_auto_speed_down_rect.collidepoint(event.pos):
                    if speed > 0:
                        speed -= 1
                        refresh_gen_auto_text()

                        if speed != 0:
                            start = time.time()
                            end = start + 1 / int(vitesse[speed])

                elif gen_auto_speed_up_rect.collidepoint(event.pos):
                    if speed < 8:
                        speed += 1
                        refresh_gen_auto_text()

            if edit_text_collision.collidepoint(event.pos) and mode != 1:
                mode = change_mode(1, 67)
            elif gen_text_collision.collidepoint(event.pos) and mode != 2:
                mode = change_mode(2, 37)
                pygame.draw.rect(screen, couleurs["bordure"], next_gen_rect, 5)
                pygame.draw.polygon(screen, couleurs[1], ((screen.get_width() - 65, screen.get_height() - 70), (screen.get_width() - 65, screen.get_height() - 30), (screen.get_width() - 30, screen.get_height() - 50)))
            elif gen_auto_text_collision.collidepoint(event.pos) and mode != 3:
                mode = change_mode(3, 7)
                speed = 0
                refresh_gen_auto_text()
                pygame.draw.rect(screen, couleurs["bordure"], gen_auto_stop_rect, 5)
                pygame.draw.rect(screen, couleurs[1], (screen.get_width() - 390, screen.get_height() - 70, 40, 40))
                pygame.draw.rect(screen, couleurs["bordure"], gen_auto_speed_down_rect, 5)
                pygame.draw.polygon(screen, couleurs[1], ((screen.get_width() - 241, screen.get_height() - 70), (screen.get_width() - 241, screen.get_height() - 30), (screen.get_width() - 276, screen.get_height() - 50)))
                pygame.draw.polygon(screen, couleurs[1], ((screen.get_width() - 216, screen.get_height() - 70), (screen.get_width() - 216, screen.get_height() - 30), (screen.get_width() - 251, screen.get_height() - 50)))
                pygame.draw.rect(screen, couleurs["bordure"], gen_auto_speed_up_rect, 5)
                pygame.draw.polygon(screen, couleurs[1], ((screen.get_width() - 90, screen.get_height() - 70), (screen.get_width() - 90, screen.get_height() - 30), (screen.get_width() - 55, screen.get_height() - 50)))
                pygame.draw.polygon(screen, couleurs[1], ((screen.get_width() - 65, screen.get_height() - 70), (screen.get_width() - 65, screen.get_height() - 30), (screen.get_width() - 30, screen.get_height() - 50)))

            elif reset_collision.collidepoint(event.pos):
                mode = change_mode(1, 67)
                for i in range(0, len(grille)):
                    for j in range(0, len(grille[i])):
                        grille[i][j].state = 0
                        grille[i][j].draw()

    pygame.display.flip()
    dt = clock.tick(60)
    # print(1000 / dt)