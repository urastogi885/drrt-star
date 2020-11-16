import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from mapUtils import readMap
from prm import generate_roadmap

vertices, edges = generate_roadmap((5,5), (95,95), 2)
multiplier = 5

map = readMap("map.txt")

pygame.init()
screen = pygame.display.set_mode([len(map) * multiplier, len(map[0]) * multiplier])
screen.fill((0, 0, 0))

for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == 1:
            pygame.draw.rect(screen, (255, 255, 255), (i * multiplier, j * multiplier, multiplier, multiplier))

for point in vertices:
    pygame.draw.circle(screen, (100,100,255), (point[0]*multiplier, point[1] * multiplier), 4)

print(len(vertices))
for edge in edges:
        print(edge)
        pygame.draw.aaline(screen, (100,100, 255), (vertices[edge[0]][0] * multiplier, vertices[edge[0]][1] * multiplier), (vertices[edge[1]][0] * multiplier, vertices[edge[1]][1] * multiplier))

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
