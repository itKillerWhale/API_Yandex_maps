import pygame
import sys

from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtWidgets import QWidget
from io import BytesIO

from geocoder import get_coordinates, get_toponym_info, get_index
from mapapi_PG import get_map
from classes import Check_box

pygame.init()

gtoponym = None


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.run()
        self.close()

    def initUI(self):
        self.setGeometry(-100, -100, 1, 1)
        self.setWindowTitle("Костыль? Нет!!! ФИЧА!")

    def run(self):
        global gtoponym
        toponym, ok_pressed = QInputDialog.getText(self, "Место",
                                                   "Куда?")
        if ok_pressed:
            gtoponym = toponym
        else:
            gtoponym = None


def get_toponym():
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        # sys.exit(app.exec_())

    return gtoponym


if __name__ == '__main__':

    pygame.display.set_caption('API')
    size = width, height = 450, 550
    screen = pygame.display.set_mode(size)
    running = True
    v = 30
    fps = 60
    screen.fill(pygame.Color("black"))
    pygame.display.flip()
    clock = pygame.time.Clock()

    layers = ["map", "skl", "sat"]
    params = []
    toponim_list = []

    font = pygame.font.Font("font/MercutioNbpBasic.ttf", 35)
    text_info_1 = font.render("", True, (0, 255, 0))
    text_info_2 = font.render("", True, (0, 255, 0))

    font2 = pygame.font.Font("font/MercutioNbpBasic.ttf", 25)
    text2 = font.render("", True, (0, 255, 0))

    l1, l2 = 39.576167, 50.196061
    spn = 0.005
    z = 0

    map = get_map(f"{l1},{l2}", f"{spn},{spn}", str(z), layers[0], "~".join(params))
    image = pygame.image.load(BytesIO(map.content))

    all_sprites = pygame.sprite.Group()
    check_box = Check_box(all_sprites)

    screen.blit(image, (0, 0))
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event.pos)

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
                    z = abs((z + 1) % 17)
                elif pygame.key.get_pressed()[pygame.K_KP_MINUS]:
                    z = abs((z - 1) % 17)

                if pygame.key.get_pressed()[pygame.K_UP]:
                    l2 += 0.001 % 90

                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    l2 -= 0.001 % 90

                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    l1 += 0.001 % 180

                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    l1 -= 0.001 % 180

                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    layers = layers[1:] + layers[:1]

                if pygame.key.get_pressed()[pygame.K_t]:
                    toponim = get_toponym()
                    toponim_list.append(toponim)
                    l1, l2 = get_coordinates(toponim)
                    l1, l2 = float(l1), float(l2)
                    params.append(f"{l1},{l2}")

                if pygame.key.get_pressed()[pygame.K_c]:
                    if bool(params):
                        del params[-1]

                    if bool(toponim_list):
                        del toponim_list[-1]

                map = get_map(f"{l1},{l2}", f"{spn},{spn}", str(z), layers[0], "~".join(params))
                image = pygame.image.load(BytesIO(map.content))
                if bool(toponim_list):
                    info = get_toponym_info(toponim_list[-1]).split(",")
                    info_1 = ",".join(info[:2]).strip()
                    ifo_2 = ",".join(info[2:]).strip()
                    text_info_1 = font.render(info_1, True, (0, 255, 0))
                    text_info_2 = font.render(ifo_2, True, (0, 255, 0))
                    font.render("", True, (0, 255, 0))

                    index = get_index(toponim_list[-1])
                    text2 = font.render(index, True, (0, 255, 0))
                else:
                    text_info_1 = font.render("", True, (0, 255, 0))
                    text_info_2 = font.render("", True, (0, 255, 0))
                    text2 = font.render("", True, (0, 255, 0))

        screen.fill((0, 0, 0))

        all_sprites.draw(screen)

        if check_box.ischecked:
            screen.blit(text2, (5, 515))

        screen.blit(image, (0, 0))
        screen.blit(text_info_1, (5, 450))
        screen.blit(text_info_2, (5, 480))

        pygame.display.flip()

        clock.tick(v)
    pygame.quit()

# Россошь, Малышева, 1
# Москва, Кислозаводская, 1е
