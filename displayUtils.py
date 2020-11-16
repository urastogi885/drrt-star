import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from mapUtils import readMap
from PRM import generateRoadMap

vertices, edges = generateRoadMap(100,20)
multiplier = 5

map = readMap("map.txt")

pygame.init()
screen = pygame.display.set_mode([len(map) * multiplier, len(map[0]) * multiplier])
screen.fill((0, 0, 0))

for i in range(len(map[0])):
    for j in range(len(map)):
        if map[j][i] == 1:
            pygame.draw.rect(screen, (255, 255, 255), (i * multiplier, j * multiplier, multiplier, multiplier))

for point in vertices:
    pygame.draw.circle(screen, (100,100,255), (point[0]*multiplier, point[1] * multiplier), 4)

for edge in edges:
        pygame.draw.aaline(screen, (100,100, 255), (vertices[edge[0]][0] * multiplier, vertices[edge[0]][1] * multiplier), (vertices[edge[1]][0] * multiplier, vertices[edge[1]][1] * multiplier))

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
