import pygame, requests, sys, os


class MapParams(object):
    def __init__(self):
        self.lat = 51.32060
        self.lon = 46.813492
        self.zoom = 7
        self.type = "map"

    def ll(self):
        return str(self.lon) + "," + str(self.lat)


def load_map(mp):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={mp.ll()}&z={mp.zoom}&l={mp.type}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file



pygame.init()
screen = pygame.display.set_mode((600, 450))
mp = MapParams()
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    map_file = load_map(mp)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
