import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from mapUtils import readMap
from PRM import generateRoadMap

fixed_nodes = [[60, 38], [51, 47], [50, 33], [51, 71], [69, 72], [36, 38], [19, 61], [5, 93], [5, 93], [26, 95],
               [82, 96], [55, 97], [49, 16], [83, 37], [4, 5], [6, 22], [10, 37], [26, 34], [24, 10], [47, 5], [27, 3],
               [46, 30], [68, 3], [70, 20], [70, 32], [92, 6], [93, 27], [7, 61], [5, 79], [24, 73], [47, 64], [36, 60],
               [71, 59], [89, 59], [91, 78], [70, 87], [47, 89], [64, 5], [52, 60], [48, 61], [51, 38], [48, 36]]

vertices, edges = generateRoadMap(0,25, fixed_nodes)
multiplier = 10

map = readMap("map.txt")

pygame.init()
screen = pygame.display.set_mode([len(map) * multiplier, len(map[0]) * multiplier])
screen.fill((0, 0, 0))

for i in range(len(map[0])):
    for j in range(len(map)):
        if map[j][i] == 1:
            pygame.draw.rect(screen, (255, 255, 255), (i * multiplier, j * multiplier, multiplier, multiplier))

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)

for point in vertices:
    pygame.draw.circle(screen, (100,100,255), (point[0]*multiplier, point[1] * multiplier), 4)
    textsurface = myfont.render(str(point), True, (255, 255, 255))
    screen.blit(textsurface, (point[0]*multiplier, point[1] * multiplier))

for edge in edges:
        pygame.draw.aaline(screen, (100,100, 255), (vertices[edge[0]][0] * multiplier, vertices[edge[0]][1] * multiplier), (vertices[edge[1]][0] * multiplier, vertices[edge[1]][1] * multiplier))

running = True
pos = []
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos.append([int(pygame.mouse.get_pos()[0]/ multiplier), int(pygame.mouse.get_pos()[1]/ multiplier)])

    pygame.display.flip()
print(pos)

pygame.quit()
