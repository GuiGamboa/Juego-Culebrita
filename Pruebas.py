#CREACIÓN DEL REPOSITORIO EN GIT-HUB PROBANDO QUE PUEDE VER Y SUBIRSE EL AVANCE. 

#Definimos las diferentes librerías que utilizaremos. 
import pygame
import random

pygame.init()
pygame.font.init()

#Clase Principal
class DISEÑO():
    def __init__(self):
        pass

    def variables(self):
        
        #-------------------COLORES
        self.rojo_fuerte=(255,0,0)
        self.rojo_claro=(207,100,79)
        self.blanco=(255,255,255)
        self.negro=(0,0,0)
        self.verde=(95,230,49)       

        #-------------------IMÁGENES
        self.fondo=pygame.image.load("fondo.png")
        #self.icono=pygame.image.load("icono.png")

        #-------------------FUENTES DE TEXTO
        self.fuente_numeros=pygame.font.SysFont("Snap ITC",40)
        self.fuente_titulos=pygame.font.SysFont("Cooper",80)
        self.fuente_textos=pygame.font.SysFont("Arial",20)
        
        #-------------------VARIABLES DE APOYO
        self.inicio=True
        self.cuadritos=50
        self.x=random.randrange(self.cuadritos,self.tamaño_pantalla[0]-self.cuadritos,self.cuadritos)
        self.y=random.randrange(self.cuadritos*2,self.tamaño_pantalla[1]-self.cuadritos,self.cuadritos)
        self.angulo=0
        self.direccion="derecha"
        self.coorde_x_culebra=400
        self.coorde_y_culebra=350
        self.coorde_x_cuerpo=400
        self.coorde_y_cuerpo=350
        self.velocidad_culebra=3
        self.contador=0
        self.apoyo=0
        self.fps=pygame.time.Clock()
        self.pila_direcciones=[]
        self.pila_angulos=[]
        self.pila_angulosletras=[]
   
    def pantalla_de_juego(self):

        self.tamaño_pantalla=[900,650]
        self.pantalla=pygame.display.set_mode(self.tamaño_pantalla)
        pygame.display.set_caption("CULEBRITA")
        #pygame.display.set_icon(self.icono) ---> AÚN FALTA EL ÍCONO

    def marco(self):
        grosor = 8
        
        # Líneas horizontales del área de juego
        pygame.draw.line(self.pantalla,self.negro,(50,100),(850,100), grosor)
        pygame.draw.line(self.pantalla,self.negro,(50,600),(850,600), grosor)

        # Líneas verticales del área de juego.
        pygame.draw.line(self.pantalla,self.negro,(50,97),(50,604), grosor)
        pygame.draw.line(self.pantalla,self.negro,(850,97),(850,604), grosor)    
 
class SPRITES(DISEÑO,pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def sprites(self):
        pygame.sprite.Sprite.__init__
                #---Comida
        self.comida=pygame.image.load("comida.png").convert()
        self.comida.set_colorkey(self.blanco)
        self.rect=self.comida.get_rect()
        
                #---Cabeza de la serpiente
        self.cabeza=pygame.image.load("cabeza.png").convert()
        self.cabeza.set_colorkey(self.blanco)
        self.rect=self.cabeza.get_rect()

                #---Cabeza de la serpiente al morir
        self.cabeza_fin=pygame.image.load("fin.png").convert()
        self.cabeza_fin.set_colorkey(self.blanco)
        self.rect=self.cabeza_fin.get_rect()

                #---Cuerpo de la serpiente
        self.cuerpo=pygame.image.load("cuerpo.png").convert()
        self.cuerpo_original=pygame.image.load("cuerpo.png")
        self.cuerpo.set_colorkey(self.blanco)
        self.rect=self.cuerpo.get_rect()

                #---Cola de la serpiente
        self.cola=pygame.image.load("cola.png").convert()
        self.cola.set_colorkey(self.blanco)
        self.rect=self.cola.get_rect() 

class LOGICA(SPRITES):
    def __init__(self):
        super().__init__()

    def comida_aleatoria(self):
        #---La comida aparece en lugares aleatorios del área de juego
        self.x=random.randrange(self.cuadritos,self.tamaño_pantalla[0]-self.cuadritos,self.cuadritos)
        self.y=random.randrange(self.cuadritos*2,self.tamaño_pantalla[1]-self.cuadritos,self.cuadritos)

    def cuerpo_serpiente(self):
        self.avance_x_cuerpo()
        self.avance_y_cuerpo()
        for cuerpos in range (self.contador):
            for x in range(len(self.pila_angulos)):
                self.apoyo=(self.cuadritos*cuerpos)+50
                if self.coorde_x_cuerpo==self.pila_direcciones[x][0] and self.coorde_y_cuerpo==self.pila_direcciones[x][1]:
                    self.cambio_direccion_cuerpo(self.pila_angulosletras[x],self.pila_angulos[x])
                    self.pantalla.blit(self.cuerpo,(self.coorde_x_cuerpo-self.apoyo,self.coorde_y_cuerpo))
                else:
                    self.pantalla.blit(self.cuerpo_original,(self.coorde_x_cuerpo-self.apoyo,self.coorde_y_cuerpo))
        apoyo2=self.apoyo+45
        self.pantalla.blit(self.cola,(self.coorde_x_culebra-apoyo2,self.coorde_y_culebra))
        #self.pantalla.blit(self.cuerpo,(self.coorde_x_cuerpo-self.apoyo,self.coorde_y_cuerpo))
        
    def cambio_direccion(self):
        #---Dependiendo del ángulo en el que se encuentre la serpiente así será su moviemiento
        #---Evitando que hagamos un movimiendo en sentido contrario
        if self.direccion=="abajo":
            if self.angulo==0:
                self.cabeza=pygame.transform.rotate(self.cabeza,-90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,-90)

            elif self.angulo==180:
                self.cabeza=pygame.transform.rotate(self.cabeza,90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,90)

        elif self.direccion=="arriba":
            if self.angulo==0:
                self.cabeza=pygame.transform.rotate(self.cabeza,90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,90)

            elif self.angulo==180:
                self.cabeza=pygame.transform.rotate(self.cabeza,-90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,-90)

        elif self.direccion=="izquierda":
            if self.angulo==90:
                self.cabeza=pygame.transform.rotate(self.cabeza,90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,90)

            elif self.angulo==270:
                self.cabeza=pygame.transform.rotate(self.cabeza,-90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,-90)
                
        elif self.direccion=="derecha":
            if self.angulo==270:
                self.cabeza=pygame.transform.rotate(self.cabeza,90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,90)

            elif self.angulo==90:
                self.cabeza=pygame.transform.rotate(self.cabeza,-90)
                self.cabeza_fin=pygame.transform.rotate(self.cabeza_fin,-90)

    def cambio_direccion_cuerpo(self,direccion,angulo):
        if direccion=="abajo":
            if angulo==0:
                self.cuerpo=pygame.transform.rotate(self.cuerpo,-90)
                #self.cola=pygame.transform.rotate(self.cola,-90)

            elif angulo==180:
                self.cuerpo=pygame.transform.rotate(self.cuerpo,90)

        elif direccion=="arriba":
            if angulo==0:
                self.cuerpo=pygame.transform.rotate(self.cuerpo,90)

            elif angulo==180:
                self.cuerpo=pygame.transform.rotate(self.cuerpo,-90)

        elif direccion=="izquierda":
            if angulo==90:
                self.cuerpo=pygame.transform.rotate(self.cuerpo,90)

            elif angulo==270:
                self.cuerpo=pygame.transform.rotate(self.cuerpo,-90)
                
        elif direccion=="derecha":
            if angulo==270:
                self.cuerpo=pygame.transform.rotate(self.cabeza,90)

            elif angulo==90:
                self.cuerpo=pygame.transform.rotate(self.cabeza,-90)

    def avance_cabeza(self):
        #---Dependiendo del ángulo al que se dirija así será su desplazamiento
        if self.angulo==0:
            self.coorde_x_culebra+=self.velocidad_culebra

        elif self.angulo==180:
            self.coorde_x_culebra-=self.velocidad_culebra

        elif self.angulo==270:
            self.coorde_y_culebra+=self.velocidad_culebra

        elif self.angulo==90:
            self.coorde_y_culebra-=self.velocidad_culebra
    
    def avance_x_cuerpo(self):
        if self.coorde_x_culebra<50 or self.coorde_x_culebra>800 or self.coorde_y_culebra<100 or self.coorde_y_culebra>550:
            self.pantalla.blit(self.cabeza_fin,(self.coorde_x_culebra,self.coorde_y_culebra))
        else:
            if self.angulo==0:
                self.coorde_x_cuerpo+=self.velocidad_culebra
            
            elif self.angulo==180:
                self.coorde_x_cuerpo-=self.velocidad_culebra

    def avance_y_cuerpo(self):
        if self.coorde_x_culebra<50 or self.coorde_x_culebra>800 or self.coorde_y_culebra<100 or self.coorde_y_culebra>550:
            self.pantalla.blit(self.cabeza_fin,(self.coorde_x_culebra,self.coorde_y_culebra))
        else: 
            if self.angulo==90:
                self.coorde_y_cuerpo-=self.velocidad_culebra

            elif self.angulo==270:
                self.coorde_y_cuerpo+=self.velocidad_culebra

    def colisiones_puntos(self):
            #---Detecta las coordenadas de los bordes del área de juego.        
        if self.coorde_x_culebra<50 or self.coorde_x_culebra>800 or self.coorde_y_culebra<100 or self.coorde_y_culebra>550:
            self.pantalla.blit(self.cabeza_fin,(self.coorde_x_culebra,self.coorde_y_culebra))
        else: 
            self.avance_cabeza()
            
            #PUNTOS - NO FUNCIONA AL 100%
        if self.coorde_x_culebra>=self.x-10 and self.coorde_x_culebra<=self.x+50 and self.coorde_y_culebra>=self.y-10 and self.coorde_y_culebra<=self.y+50:
            self.comida_aleatoria()
            self.contador+=1

    def guardar_direcciones(self,direc,ang,direc2):
        self.pila_direcciones.append(direc)
        self.pila_angulos.append(ang)
        self.pila_angulosletras.append(direc2)

class JUEGO_FINAL(LOGICA):
    def __init__(self):
        super().__init__()

    def eventos_general(self):
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                self.inicio=False
            
            # TECLAS
            if evento.type==pygame.KEYDOWN:
                #SOLAMENTE EJEMPLO DE COMIDA ALEATORIA
                if evento.key==pygame.K_DOWN:
                    self.direccion="abajo"
                    self.cambio_direccion()
                    if self.angulo==90:
                        self.angulo=90
                    else:
                        self.angulo=270
                    apoyo3=[]
                    apoyo3.append(self.coorde_x_culebra)
                    apoyo3.append(self.coorde_y_culebra)
                    self.guardar_direcciones(apoyo3,self.angulo,self.direccion)

                if evento.key==pygame.K_UP:
                    self.direccion="arriba"
                    self.cambio_direccion()
                    if self.angulo==270:
                        self.angulo=270
                    else:
                        self.angulo=90
                    apoyo3=[]
                    apoyo3.append(self.coorde_x_culebra)
                    apoyo3.append(self.coorde_y_culebra)
                    self.guardar_direcciones(apoyo3,self.angulo,self.direccion)


                if evento.key==pygame.K_LEFT:
                    self.direccion="izquierda"
                    self.cambio_direccion()
                    if self.angulo==0:
                        self.angulo=0
                    else:
                        self.angulo=180
                    apoyo3=[]
                    apoyo3.append(self.coorde_x_culebra)
                    apoyo3.append(self.coorde_y_culebra)
                    self.guardar_direcciones(apoyo3,self.angulo,self.direccion)

                if evento.key==pygame.K_RIGHT:
                    self.direccion="derecha"
                    self.cambio_direccion()
                    if self.angulo==180:
                        self.angulo=180
                    else:
                        self.angulo=0
                    apoyo3=[]
                    apoyo3.append(self.coorde_x_culebra)
                    apoyo3.append(self.coorde_y_culebra)
                    self.guardar_direcciones(apoyo3,self.angulo,self.direccion)

        self.marco()

    def juego_culebrita(self):
        self.pantalla_de_juego()
        self.variables()
        self.sprites()
        
        while self.inicio:
            self.fps.tick(60)
            self.pantalla.blit(self.fondo,(0,0))
            self.pantalla.blit(self.cabeza,(self.coorde_x_culebra,self.coorde_y_culebra))
            self.cuerpo_serpiente()

            self.eventos_general()
            self.pantalla.blit(self.comida,(self.x,self.y))

            self.colisiones_puntos()
            contador=self.fuente_numeros.render("Puntos:  "+str(self.contador),1,self.negro)
            self.pantalla.blit(contador,(10,5))

            #Coordenadas Comida
            comidacoor=self.fuente_textos.render("X: "+str(self.x)+" Y: "+str(self.y),1,self.negro)
            self.pantalla.blit(comidacoor,(500,5))

            #Coordenadas Serpiente Cabeza
            coorserp=self.fuente_textos.render("X: "+str(self.coorde_x_culebra)+" Y: "+str(self.coorde_y_culebra),1,self.negro)
            self.pantalla.blit(coorserp,(500,50))

            #----Detectar Colisiones


            #Actualizar pantalla
            pygame.display.flip()
        print(self.pila_angulos)
        for x in self.pila_direcciones:
            print(x)
        print(self.pila_angulosletras)

pruebas=JUEGO_FINAL()
pruebas.juego_culebrita()

#----------------------IDEAS---------------------
# Utilizar las dos clases de coord_x(y)_cuerpo para cambiar los angulos, por el momento el avance se sigue guiando
# según el ángulo marcado, en ese momento usar la pila_angulos para que eso nos guie.
# También distribuir el avance en x_y dentro de los ciclos for
