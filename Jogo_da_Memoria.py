import pygame
import random
import os

pygame.init()

#Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

#Tamanho tela
LARGURA_TELA = 1000
ALTURA_TELA = 600
TAMANHO_CARTA = 100
MARGEM = 20

#Tamanho para as grades
LARGURA_GRADE = 4 * TAMANHO_CARTA + 5 * MARGEM
ALTURA_GRADE = 4 * TAMANHO_CARTA + 5 * MARGEM
offset_x = (LARGURA_TELA - LARGURA_GRADE) // 2
offset_y = (ALTURA_TELA - ALTURA_GRADE) // 2


tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Memória Sonora")


sons = [pygame.mixer.Sound(os.path.join("sons", f"{i}.wav")) for i in range(1, 9)]
som_acerto = pygame.mixer.Sound(os.path.join("sons", "acerto.wav"))
som_erro = pygame.mixer.Sound(os.path.join("sons", "erro.wav"))

#faces das cartas e seus sons
nomes_cartas = [
    "Face_Cachorro",  # 1
    "Face_Leao",      # 2
    "Face_Sapo",      # 3
    "Face_Cavalo",    # 4
    "Face_Elefante",  # 5
    "Face_Passaro",   # 6
    "Face_Macaco",    # 7
    "Face_Gato"       # 8
]
imagens_cartas = [pygame.image.load(os.path.join("imagens", f"{nome}.png")) for nome in nomes_cartas]
verso_carta = pygame.image.load((os.path.join("imagens", "card_back.png")))


pares = list(range(8)) * 2
random.shuffle(pares)


cartas_reveladas = [False] * 16
carta_selecionada = []


fonte = pygame.font.SysFont(None, 48)

def desenhar_cartas():
    tela.fill(PRETO)
    for i in range(4):
        for j in range(4):
            idx = i * 4 + j
            x = offset_x + MARGEM + j * (TAMANHO_CARTA + MARGEM)
            y = offset_y + MARGEM + i * (TAMANHO_CARTA + MARGEM)
            if cartas_reveladas[idx] or idx in carta_selecionada:
                imagem = imagens_cartas[pares[idx]]
                tela.blit(pygame.transform.scale(imagem, (TAMANHO_CARTA, TAMANHO_CARTA)), (x, y))
            else:
                tela.blit(pygame.transform.scale(verso_carta, (TAMANHO_CARTA, TAMANHO_CARTA)), (x, y))
    pygame.display.flip()

def indice_carta(pos):
    x, y = pos
    for i in range(4):
        for j in range(4):
            idx = i * 4 + j
            cx = offset_x + MARGEM + j * (TAMANHO_CARTA + MARGEM)
            cy = offset_y + MARGEM + i * (TAMANHO_CARTA + MARGEM)
            if cx <= x <= cx + TAMANHO_CARTA and cy <= y <= cy + TAMANHO_CARTA:
                return idx
    return None

def restart(texto):
    tela.fill(PRETO)
    msg = fonte.render(texto, True, BRANCO)
    msg_rect = msg.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 50))
    tela.blit(msg, msg_rect)

    botao_largura, botao_altura = 200, 60
    botao_x = (LARGURA_TELA - botao_largura) // 2
    botao_y = ALTURA_TELA // 2 + 20
    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)

    pygame.draw.rect(tela, (255, 0, 0), botao_rect)
    texto_botao = fonte.render("Restart", True, BRANCO)
    texto_rect = texto_botao.get_rect(center=botao_rect.center)
    tela.blit(texto_botao, texto_rect)

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    esperando = False  # Sai do loop → restart
    return True



jogando = True
while jogando:
    desenhar_cartas()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            idx = indice_carta(evento.pos)
            if idx is not None and not cartas_reveladas[idx] and len(carta_selecionada) < 2:
                carta_selecionada.append(idx)
                sons[pares[idx]].play()
                desenhar_cartas()

                if len(carta_selecionada) == 2:
                    pygame.time.wait(500)
                    i1, i2 = carta_selecionada
                    if pares[i1] == pares[i2]:
                        cartas_reveladas[i1] = True
                        cartas_reveladas[i2] = True
                        som_acerto.play()
                    else:
                        som_erro.play()
                    carta_selecionada = []

                    if all(cartas_reveladas):
                        restart("Você venceu!")
                        pares = list(range(8)) * 2
                        random.shuffle(pares)
                        cartas_reveladas = [False] * 16
                        carta_selecionada = []

pygame.quit()
