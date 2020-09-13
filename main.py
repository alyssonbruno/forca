import random
import pygame
from pygame.locals import K_BACKSPACE

from functools import reduce

TENTATIVA2IMAGEM: dict = {
    0: 'Forca.png',
    1: 'Forca_cabeca.png',
    2: 'Forca_cabeca_corpo.png',
    3: 'Forca_cabeca_corpo_pe_direito.png',
    4: 'Forca_cabeca_corpo_pes.png',
    5: 'Forca_cabeca_corpo_pes_mao_direita.png',
    6: 'Forca_cabeca_corpo_pes_maos.png',
    7: 'Morreu.png'
}
RESOLUCAO = (800, 600)
workdir = '.'

def escolhe_palavra() -> str:
    arquivo = open(f'{workdir}/palavras.txt', 'r')
    linha = random.sample(arquivo.readlines(), 1)
    return linha[0].lower().strip()


def carregar_imagem(nome: str):
    return pygame.image.load(f'{workdir}/Imagens/{nome}')


def desenha_forca(tentativa):
    try:
        return carregar_imagem(TENTATIVA2IMAGEM[tentativa])
    except KeyError:
        return carregar_imagem(TENTATIVA2IMAGEM[7])


def escreve_texto(texto: str, tamanho: int = 60, cor: list = [0,0,0]) -> pygame.Surface:
    fonte = pygame.font.Font(None, tamanho)
    return fonte.render(texto, True, cor)


def escreve_palavra(palavra: str, letras_certas: list) -> pygame.Surface:
    mostrar = ''
    for letra in palavra:
        mostrar += letra if letra in letras_certas else '*'
    fonte = pygame.font.Font(None, 100)
    return fonte.render(mostrar, True, [0, 0, 0])

def monta_tela(screen, palavra_certa: str, letras_digitadas: list = []) -> str:
    palavra_display: str = ""
    letras_display: str = ""
    letras_certas = list(filter(lambda c: c in palavra_certa, letras_digitadas))
    qtd_letras_erradas = reduce(lambda count, c: count + (0 if c in palavra_certa else 1), letras_digitadas, 0)
    qtde_letras_descobertas = reduce(lambda count, c: count + palavra_certa.count(c), letras_digitadas, 0)
    imagem = desenha_forca(qtd_letras_erradas)
    background = pygame.transform.scale(imagem, RESOLUCAO)
    pygame.display.set_caption("Forca")
    titulo = escreve_texto('Entre com uma letra')
    if qtde_letras_descobertas < len(palavra_certa):
        if qtd_letras_erradas < 7:
            palavra_display = escreve_palavra(palavra_certa, letras_certas)
            letras_display = escreve_texto("-".join(letras_digitadas))
        else:
            palavra_display = escreve_texto(palavra_certa, cor=[255,0,0])
            letras_display = escreve_texto("Perdeu!", cor=[255,0,0])
    else:
        palavra_display = escreve_texto(palavra_certa)
        letras_display = escreve_texto("Você ganhou! Parabéns!", cor=[0,200,0])
    screen.blit(background, (0, 0))
    screen.blit(titulo, (10, 10))
    screen.blit(palavra_display, (40, 450))
    screen.blit(letras_display, (300, 50))
    pygame.display.flip()
    return letras_certas


def principal() -> None:
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    letras = []
    palavra = escolhe_palavra()

    # define a variable to control the main loop
    running = True
    screen = pygame.display.set_mode(RESOLUCAO)
    # main loop
    pygame.key.set_repeat(0)
    monta_tela(screen, palavra, letras)
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYUP:
                if event.key == K_BACKSPACE:
                    running = False
                    pygame.quit()
                else:
                    k = pygame.key.name(event.key).lower()
                    if k in 'abcdefghijklmnopqrstuvwxyz':
                        if k in letras:
                            continue
                        letras.append(k)
                        monta_tela(screen, palavra, letras)

if __name__ == '__main__':
    import os
    workdir = os.path.split(os.path.abspath(__file__))[0]
    principal()
