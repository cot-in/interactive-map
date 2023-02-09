import os
import sys
import pygame
import requests

lat = 55.703118  # широта
lon = 37.530887  # долгота
delta = 0.005  # зум

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
    global delta
    if change_delta == -1:
        delta /= 2
    else:
        delta *= 2
    delta = max(delta, 0.00125)
    delta = min(delta, 20.48)
    params["spn"] = f"{delta},{delta}"


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
    pygame.quit()
