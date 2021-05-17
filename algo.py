#import Path_finding
import math, pygame
from queue import PriorityQueue

def reconstruct(came_from,current, draw, start):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
    for i in path:
        if i != start:
            i.make_path()
            draw()

def algorithm(draw,grid,start,end,h):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = g_score[start] + h(start.get_pos(),end.get_pos())

    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct(came_from,end,draw,start)
            end.make_end()
            return True
        for neighbour in current.neighbour:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(),end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()


















        draw()
        if current != start:
            current.make_closed()
