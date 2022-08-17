import numpy as np
import cv2
from PIL import Image


class GeneralExtractor:

    def __init__(self, left_lateral_esquerda, top_lateral_esquerda, width_lateral_esquerda, height_lateral_esquerda, left_lateral_direita, width_lateral_direita, left_base, top_base, width_base, height_base, left_painel_frontal_superior, top_painel_frontal_superior, width_painel_frontal_superior, height_painel_frontal_superior, left_painel_frontal_central, top_painel_frontal_central, width_painel_frontal_central, height_painel_frontal_central, left_painel_verso_superior, top_painel_verso_superior, width_painel_verso_superior, height_painel_verso_superior, top_painel_verso_central, height_painel_verso_central, left_painel_verso_inferior, top_painel_verso_inferior, height_painel_verso_inferior):

        zoom = 3
        
        self.left_lateral_esquerda  = left_lateral_esquerda * zoom
        self.top_lateral_esquerda = top_lateral_esquerda * zoom
        self.width_lateral_esquerda = width_lateral_esquerda * zoom
        self.height_lateral_esquerda = height_lateral_esquerda * zoom
        self.left_lateral_direita = left_lateral_direita * zoom
        self.width_lateral_direita = width_lateral_direita * zoom
        self.left_base = left_base * zoom
        self.top_base = top_base * zoom
        self.width_base = width_base * zoom
        self.height_base = height_base * zoom
        self.left_painel_frontal_superior = left_painel_frontal_superior * zoom
        self.top_painel_frontal_superior = top_painel_frontal_superior * zoom
        self.width_painel_frontal_superior = width_painel_frontal_superior * zoom
        self.height_painel_frontal_superior = height_painel_frontal_superior * zoom
        self.left_painel_frontal_central = left_painel_frontal_central * zoom
        self.top_painel_frontal_central = top_painel_frontal_central * zoom
        self.width_painel_frontal_central = width_painel_frontal_central * zoom
        self.height_painel_frontal_central = height_painel_frontal_central * zoom
        self.left_painel_verso_superior = left_painel_verso_superior * zoom
        self.top_painel_verso_superior = top_painel_verso_superior * zoom
        self.width_painel_verso_superior = width_painel_verso_superior * zoom
        self.height_painel_verso_superior = height_painel_verso_superior * zoom
        self.top_painel_verso_central = top_painel_verso_central * zoom
        self.height_painel_verso_central = height_painel_verso_central * zoom
        self.left_painel_verso_inferior = left_painel_verso_inferior * zoom
        self.top_painel_verso_inferior = top_painel_verso_inferior * zoom
        self.height_painel_verso_inferior = height_painel_verso_inferior * zoom


    def extract_inteira(self, image):
        image = image

        #Lateral Esquerda

        lateral_esquerda = image[self.top_lateral_esquerda:self.height_lateral_esquerda, self.left_lateral_esquerda:self.width_lateral_esquerda]
        lat = Image.fromarray(lateral_esquerda).rotate(90, expand=True)
        lateral_esquerda = np.asarray(lat)

        #Lateral Direita

        lateral_direita = image[self.top_lateral_esquerda:self.height_lateral_esquerda, self.left_lateral_direita:self.width_lateral_direita]
        lat = Image.fromarray(lateral_direita).rotate(270, expand=True)
        lateral_direita = np.asarray(lat)

        #Base

        base = image[self.top_base:self.height_base, self.left_base:self.width_base]

        #Painel frontal inferior

        painel_frontal_inferior = image[self.height_painel_frontal_central:self.top_base, self.left_painel_frontal_superior:self.width_painel_frontal_superior]

        #Painel frontal central

        painel_frontal_central = image[self.top_painel_frontal_central:self.height_painel_frontal_central, self.left_painel_frontal_central:self.width_painel_frontal_central]

        #Painel frontal superior

        painel_frontal_superior = image[self.top_painel_frontal_superior:self.height_painel_frontal_superior, self.left_painel_frontal_superior:self.width_painel_frontal_superior]

        #Painel verso superior

        painel_verso_superior = image[self.top_painel_verso_superior:self.height_painel_verso_superior, self.left_painel_verso_superior:self.width_painel_verso_superior]

        #Painel verso central

        painel_verso_central = image[self.top_painel_verso_central:self.height_painel_verso_central, self.left_painel_verso_superior:self.width_painel_verso_superior]

        #Painel verso inferior
    
        painel_verso_inferior = image[self.top_painel_verso_inferior:self.height_painel_verso_inferior, self.left_painel_verso_inferior:self.width_painel_verso_superior]

        return {
            'LATERAL ESQUERDA': lateral_esquerda,
            'LATERAL DIREITA': lateral_direita,
            'PAINEL FRONTAL SUPERIOR': painel_frontal_superior,
            'PAINEL FRONTAL CENTRAL': painel_frontal_central,
            'PAINEL FRONTAL INFERIOR': painel_frontal_inferior,
            'BASE': base,
            'PAINEL VERSO INFERIOR': painel_verso_inferior,
            'PAINEL VERSO SUPERIOR': painel_verso_superior,
            'PAINEL VERSO CENTRAL': painel_verso_central
        }

    def extract_aberta(self, image):
        image = image

        # Lateral Esquerda 

        lateral_esquerda = image[self.top_lateral_esquerda:self.height_lateral_esquerda, self.left_lateral_esquerda:self.width_lateral_esquerda]

        # Lateral Direita

        lateral_direita = image[self.top_lateral_esquerda:self.height_lateral_esquerda, self.left_lateral_direita:self.width_lateral_direita]

        # Base

        base = image[self.top_base:self.height_base, self.left_base:self.width_base]

        # Painel frontal inferior

        painel_frontal_inferior = image[self.height_painel_frontal_central:self.top_base, self.left_painel_frontal_superior:self.width_painel_frontal_superior]
        # Painel frontal central

        painel_frontal_central = image[self.top_painel_frontal_central:self.height_painel_frontal_central, self.left_painel_frontal_central:self.width_painel_frontal_central]

        # Painel frontal superior

        painel_frontal_superior = image[self.top_painel_frontal_superior:self.height_painel_frontal_superior, self.left_painel_frontal_superior:self.width_painel_frontal_superior]

        # Painel verso superior

        painel_verso_superior = cv2.flip(
        image[self.top_painel_verso_superior:self.height_painel_verso_superior, self.left_painel_verso_superior:self.width_painel_verso_superior], -1)

        # Painel verso central

        painel_verso_central = cv2.flip(
        image[self.top_painel_verso_central:self.height_painel_verso_central, self.left_painel_verso_superior:self.width_painel_verso_superior], -1)

        # Painel verso inferior

        painel_verso_inferior = cv2.flip(
        image[self.top_painel_verso_inferior:self.height_painel_verso_inferior, self.left_painel_verso_inferior:self.width_painel_verso_superior], -1)

        return {
            'LATERAL ESQUERDA': lateral_esquerda,
            'LATERAL DIREITA': lateral_direita,
            'PAINEL FRONTAL SUPERIOR': painel_frontal_superior,
            'PAINEL FRONTAL CENTRAL': painel_frontal_central,
            'PAINEL FRONTAL INFERIOR': painel_frontal_inferior,
            'BASE': base,
            'PAINEL VERSO INFERIOR': painel_verso_inferior,
            'PAINEL VERSO SUPERIOR': painel_verso_superior,
            'PAINEL VERSO CENTRAL': painel_verso_central
        }

