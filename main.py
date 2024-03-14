import pygame
import sys
import random
import csv
from pygame import mixer

# Paramètres du jeu
LARGEUR_ECRAN = 400
HAUTEUR_ECRAN = 600
blanc = (255, 255, 255)
X = 50
Y = 40

# Initialisation de Pygame
pygame.init()
# Initialisation du son
pygame.mixer.init()
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
horloge = pygame.time.Clock()

#Sans sortie audio intégrée, le programme ne fonctionnera pas
#Dans ce cas, désactivez les commandes suivantes:
#"pygame.mixer.init" 15
#"pygame.mixer.music.load("Corneria.mp3")" 122
#"pygame.mixer.music.play(-1)" 123
#"pygame.mixer.music.load("Explosion.mp3")" 152
#"pygame.mixer.music.play(0)" 153

# Chargement et redimensionnement des images
fond = pygame.image.load("fond.JPG").convert()
fond = pygame.transform.scale(fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

menu = pygame.image.load("menu.png").convert()
menu = pygame.transform.scale(menu, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

oiseau_img = pygame.image.load("oiseau.png").convert_alpha()
oiseau_img = pygame.transform.scale(oiseau_img, (34, 24))

obstacle_haut_img = pygame.image.load("obstacle_haut.PNG").convert_alpha()
obstacle_haut_img = pygame.transform.scale(obstacle_haut_img, (52, HAUTEUR_ECRAN))

obstacle_bas_img = pygame.image.load("obstacle_bas.PNG").convert_alpha()
obstacle_bas_img = pygame.transform.scale(obstacle_bas_img, (52, HAUTEUR_ECRAN))

def charger_parametres():
  # On charge les parametres du fichier CSV
  #OUT: les paramètres inscrits dans le CSV
  parametres = {}
  
  with open('config.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      nom_image = row["nom_image"]
      width = int(row["width"])
      height = int(row["height"])
      parametres[nom_image] = (width, height)
    
  return parametres

charger_parametres()

# On crée les fonctions destinées à gérer les obstacles 
LARGEUR_OBSTACLE = 52
ESPACE = 150
 
def creer_obstacle():
  # Génération d'un obstacle à une hauteur et une position aléatoire avec la fonction random
  #OUT: obstacle_haut et obstacle_bas à une hauteur et une position aléatoire
  global decalage
  decalage = 50 + int(random.random() * (HAUTEUR_ECRAN - 300))
  obstacle_haut = pygame.Rect(LARGEUR_ECRAN, 0, LARGEUR_OBSTACLE, decalage)
  obstacle_bas = pygame.Rect(LARGEUR_ECRAN, decalage + ESPACE, LARGEUR_OBSTACLE,
  HAUTEUR_ECRAN - decalage - ESPACE)
  return obstacle_haut, obstacle_bas

def deplacer_obstacles(obstacles):
  # Déplace les obstacles vers la gauche 
  #IN: Les éléments du groupe "obstacles"
  #OUT: Un obstacle dont la position a été modifiée 
  for obstacle in obstacles:
    obstacle.move_ip(-4, 0)
  return [obstacle for obstacle in obstacles if obstacle.right > 0]
  
def dessiner_obstacles(obstacles):
  # Dessine les obstacles sur l'écran en utilisant les images d’obstacles existantes. 
  #IN: Les éléments du groupe "obstacles"
  #OUT: Un obstacle à une hauteur spécifique
  for obstacle in obstacles:
    if obstacle.bottom <= HAUTEUR_ECRAN - ESPACE:
      ecran.blit(obstacle_haut_img, (obstacle.x,
      obstacle.y + obstacle.height - obstacle_haut_img.get_height()))
    else:
      ecran.blit(obstacle_bas_img, (obstacle.x, obstacle.y))


# On crée les fonctions destinées à gérer l'oiseau
GRAVITE = 1
SAUT = -10

def afficher_oiseau(oiseau_rect):
  # Dessine l'oiseau sur l'écran à partir de l'image fournie
  #IN: La zone de collision de l'oiseau 
  #OUT: L'image de l'oiseau superposée à sa zone de collision
  ecran.blit(oiseau_img, oiseau_rect)
  
def collision_test(oiseau_rect, obstacles):
  # Vérifie si l'oiseau rentre en contact avec les obstacles, ou sort de l'écran
  #IN: Les éléments du groupe "obstacles", la zone de collision de l'oiseau 
  #OUT: False si l'oiseau touche un obstacle, False s'il sort de l'écran
  for obstacle in obstacles:
    if oiseau_rect.colliderect(obstacle):
      return False
  if oiseau_rect.top <= 0 or oiseau_rect.bottom >= HAUTEUR_ECRAN:
    return False 
  return True

# On crée la boucle principale de jeu et la gestion des évènements
def flappy_bird():
  # Création de la boucle de jeu principale gérant les évènements, la mise à jour de l'état du jeu et le rafraichissement de l'affichage
  #OUT: Un message de défaite, un son et une remise à zéro si le joueur perd, sinon la boucle continue
  pygame.mixer.music.load("Corneria.mp3")
  pygame.mixer.music.play(-1)
  oiseau_rect = oiseau_img.get_rect(center=(50, HAUTEUR_ECRAN / 2))
  obstacles = []
  vitesse_verticale = 0
  temps_obstacle = 0
  points = 0 
  
  while True:
    ecran.blit(fond, (0, 0))
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        vitesse_verticale = SAUT
        
    vitesse_verticale += GRAVITE
    oiseau_rect.move_ip(0, vitesse_verticale)
      
    if temps_obstacle >= 60:
      temps_obstacle = 0
      obstacles.extend(creer_obstacle())
    elif temps_obstacle >= 25:
        points = points + 1
        points = round(points)
        print(points)
             
    obstacles = deplacer_obstacles(obstacles)
    dessiner_obstacles(obstacles)
    afficher_oiseau(oiseau_rect)
    

    if not collision_test(oiseau_rect, obstacles):
      pygame.mixer.music.load("Explosion.mp3")
      pygame.mixer.music.play(0)
      pygame.display.set_caption("Afficher un texte")
      font = pygame.font.Font('freesansbold.ttf', 40)
      
      text = font.render('Perdu!', True, True, blanc)
      textRect = text.get_rect()
      textRect.center = (200, 200)
      ecran.blit(text, textRect)
      
      text2 = font.render(str(points), True, True, blanc)
      text2Rect = text2.get_rect()
      text2Rect.center = (200, 300)
      ecran.blit(text2, text2Rect)
      break
        
    pygame.display.update()    
    horloge.tick(60)
    temps_obstacle += 1

parametres = charger_parametres()

# On modifie les dimensions des données chargées 
fond = pygame.image.load("fond.JPG").convert()
oiseau_img = pygame.image.load("oiseau.png").convert_alpha()
menu = pygame.image.load("menu.png").convert()

fond = pygame.transform.scale(fond, parametres["fond.JPG"])
oiseau_img = pygame.transform.scale(oiseau_img, parametres["oiseau.png"])
menu = pygame.transform.scale(menu, parametres["menu.png"])

obstacle_haut_images = [key for key in parametres.keys() if key.startswith("obstacle_haut.PNG")]
obstacle_bas_images = [key for key in parametres.keys() if key.startswith("obstacle_bas.PNG")]
obstacle_haut_img = pygame.image.load(obstacle_haut_images[0]).convert_alpha()
obstacle_bas_img = pygame.image.load(obstacle_bas_images[0]).convert_alpha()

obstacle_haut_img = pygame.transform.scale(obstacle_haut_img, (52, HAUTEUR_ECRAN)) # voir code plus haut
obstacle_bas_img = pygame.transform.scale(obstacle_bas_img, (52, HAUTEUR_ECRAN)) # voir code plus haut


def menu_jeu():
  # Création du menu du jeu
  #OUT: quit si le joueur quitte la page, lancement de la boucle de jeu dans le cas contraire
  while True:
    ecran.blit(menu, (0, 0))
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        flappy_bird()
      if event.type == pygame.QUIT :
          pygame.quit()
          quit()
      pygame.display.update()

#On permet le lancement du jeu
if __name__ == "__main__":
  menu_jeu()