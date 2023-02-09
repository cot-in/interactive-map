import os
import sys
import pygame
import requests

lat = 55.703118  # широта
lon = 37.530887  # долгота
delta = 0.005  # зум
coef = 1

params = {
    "ll": f"{lon},{lat}",
    "spn": f"{delta},{delta}",
    "l": "map",
}


def draw_map():
    map_request = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_request, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


def update_zoom(change_delta):
    global delta, coef
    if change_delta == -1:
        delta /= 2
        coef /= 2
    else:
        delta *= 2
        coef *= 2
    delta = max(delta, 0.00125)
    delta = min(delta, 20.48)
    params["spn"] = f"{delta},{delta}"


def update_coords(change_cords):
    global lat, lon, coef
    if change_cords == 'UP':
        lat += 0.001 * coef
    elif change_cords == 'DOWN':
        lat -= 0.001 * coef
    elif change_cords == 'RIGHT':
        lon += 0.001 * coef
    elif change_cords == 'LEFT':
        lon -= 0.001 * coef
    params["ll"] = f"{lon},{lat}"


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption("interactive map")
    running = True
    draw_map()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    update_zoom(-1)
                    draw_map()
                elif event.key == pygame.K_PAGEDOWN:
                    update_zoom(1)
                    draw_map()
                elif event.key == pygame.K_UP:
                    update_coords('UP')
                    draw_map()
                elif event.key == pygame.K_DOWN:
                    update_coords('DOWN')
                    draw_map()
                elif event.key == pygame.K_RIGHT:
                    update_coords('RIGHT')
                    draw_map()
                elif event.key == pygame.K_LEFT:
                    update_coords('LEFT')
                    draw_map()
                elif event.key == pygame.K_s:
                    params["l"] = "map"
                    draw_map()
                elif event.key == pygame.K_d:
                    params["l"] = "sat"
                    draw_map()
                elif event.key == pygame.K_f:
                    params["l"] = "sat,skl"
                    draw_map()

    pygame.quit()
