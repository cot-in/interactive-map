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

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    os.remove(map_file)
    pygame.quit()
