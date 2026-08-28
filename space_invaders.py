
import turtle
import random
import time
import os
import sys




# =========================
# Parâmetros / Constantes
# =========================


LARGURA, ALTURA = 600, 900
BORDA_X = (LARGURA // 2) - 20
BORDA_Y = (ALTURA // 2) - 10




PLAYER_SPEED = 20
PLAYER_BULLET_SPEED = 16




ENEMY_ROWS = 3
ENEMY_COLS = 10
ENEMY_SPACING_X = 60
ENEMY_SPACING_Y = 60
ENEMY_SIZE = 32
ENEMY_START_Y = BORDA_Y - ENEMY_SIZE    # topo visível
ENEMY_FALL_SPEED = 0.5
ENEMY_DRIFT_STEP = 2
ENEMY_FIRE_PROB = 0.006
ENEMY_BULLET_SPEED = 8
ENEMY_INVERT_CHANCE = 0.05
ENEMY_DRIFT_CHANCE = 0.5




COLLISION_RADIUS = 10
HIGHSCORES_FILE = "highscores.txt"
SAVE_FILE = "savegame.txt"
TOP_N = 10




STATE = None  # usado apenas para callbacks do teclado




# =========================
# Top Resultados (Highscores)
# =========================


def ler_highscores(filename):
    #Lê o ficheiro de highscores e devolve uma lista de tuplos (score, nome)
    highscores_list = []  #cria uma lista vazia para posteriormente colocar os nomes e pontuacoes


    if not os.path.exists(filename):   # Se o ficheiro não existe, não há pontuações
        return highscores_list


    with open(filename, "r") as ficheiro:    #abre o ficheiro no modo de leitura
        for linha in ficheiro:              
            linha = linha.strip()      
            partes = linha.split(maxsplit=1)    # separa score e nome
            if len(partes) == 2:
                score = int(partes[0])
                nome  = partes[1]
                highscores_list.append((score, nome))


    return highscores_list




def chave_score(tuplo):
    """Função auxiliar para ordenar por ordem entrada"""
    return tuplo[0]




def atualizar_highscores(filename, score):
    '''Pergunta o nome do jogador, valida, e guarda o score no ficheiro'''
    carateres_proibidos = "._:,;/@#$%&*+?'!-^~«»><()={]}[§£"


    while True:         # Loop até o nome ser válido
        nome = input("Nome: ")
        if nome == "":
            nome = "anonimo"


        # Verificação de caracteres proibidos
        invalido = False
        for c in carateres_proibidos:
            if c in nome:
                print("Erro: O nome apenas pode conter letras e números")
                print("Por favor, introduza um nome diferente.")
                invalido = True
                break  # sai do for, mas não do while


        if not invalido:
            break  # nome válido, sai do while


    # Lê highscores, junta nova pontuação, ordena e guarda no ficheiro
    highscores = ler_highscores(filename)
    highscores.append((score, nome))
    highscores.sort(key=chave_score, reverse=True)


    with open(filename, "w") as ficheiro:
        for s, n in highscores[:TOP_N]:
                ficheiro.write(f"{s} {n}\n")






# =========================
# Guardar / Carregar estado (texto)
# =========================


def guardar_estado_txt(filename, state):
    """Guarda o estado do jogo num ficheiro de texto"""


    # Guarda posição da nave
    player = state["player"]
    x_player = player.xcor()
    y_player = player.ycor()
    with open(filename, 'w') as ficheiro:
        ficheiro.write("{} {}\n". format(x_player, y_player))


    # Guarda posições dos inimigos
    for inimigo in state["enemies"]:
        x_inimigo = inimigo.xcor()
        y_inimigo = inimigo.ycor()
        with open(filename, 'a') as ficheiro:
            ficheiro.write("{} {} ". format(x_inimigo, y_inimigo))
    with open(filename, 'a') as ficheiro:
        ficheiro.write("\n")


    # Guarda direções dos inimigos
    for move in state["enemy_moves"]:
        with open(filename, 'a') as ficheiro:
            ficheiro.write("{} ". format(move))
    with open(filename, 'a') as ficheiro:
        ficheiro.write("\n")


    # Guarda balas inimigas
    for bala_inimiga in state["enemy_bullets"]:
        x_bala_i = bala_inimiga.xcor()
        y_bala_i = bala_inimiga.ycor()
        with open(filename, 'a') as ficheiro:
            ficheiro.write("{} {} ". format(x_bala_i, y_bala_i))
    with open(filename, 'a') as ficheiro:
        ficheiro.write("\n")


    # Guarda balas do jogador
    for bala_amiga in state["player_bullets"]:
        x_bala_a = bala_amiga.xcor()
        y_bala_a = bala_amiga.ycor()
        with open(filename, 'a') as ficheiro:
            ficheiro.write("{} {} ". format(x_bala_a, y_bala_a))
    with open(filename, 'a') as ficheiro:
        ficheiro.write("\n")


    # Guarda score e frame
    score = state["score"]
    frame = state["frame"]
    with open(filename, 'a') as ficheiro:
        ficheiro.write("{}\n". format(score))
        ficheiro.write("{} ". format(frame))




def carregar_estado_txt(filename):
    """Carrega estado guardado do ficheiro de texto, devolvendo dicionário simples"""
    if not os.path.exists(filename):        # Verifica se existe um save, caso não exista retorna none
        return None
   
    else:           # Existe um save, processa a informação e devolve um dicionário
        estado={
            "nave_player":[],
            "inimigos":[],
            "moves_inimigos":[],
            "balas_inimigos":[],
            "balas_player":[],
            "pontuação":0
        }


        # Lê todas as linhas relevantes
        with open(filename, 'r') as ficheiro:
            coordenadas_nave = ficheiro.readline().strip().split(" ")
            coordenadas_inimigos = ficheiro.readline().strip().split(" ")
            moves_inimigos = ficheiro.readline().strip().split(" ")
            balas_inimigos = ficheiro.readline().strip().split(" ")
            balas_player = ficheiro.readline().strip().split(" ")
            score = ficheiro.readline().strip()
            frame = ficheiro.readline().strip()


        # Processa posição da nave
        if coordenadas_nave:
            x_nave = [float(x) for x in coordenadas_nave[0::2] if x.strip()]
            y_nave = [float(y) for y in coordenadas_nave[1::2] if y.strip()]
            for i in range(1):
                estado["nave_player"].append((x_nave[i], y_nave[i]))


        # Processa inimigos
        if coordenadas_inimigos:
            x_inimigos = [float(x) for x in coordenadas_inimigos[0::2] if x.strip()]
            y_inimigos = [float(y) for y in coordenadas_inimigos[1::2] if y.strip()]
            pos_inimigos = estado["inimigos"]
            for i in range(len(x_inimigos)):
                pos_inimigos.append((x_inimigos[i], y_inimigos[i]))


        # Balas inimigas
        if balas_inimigos:
            x_bala_inimigo = [float(x) for x in balas_inimigos[0::2] if x.strip()]
            y_bala_inimigo = [float(y) for y in balas_inimigos[1::2] if y.strip()]
            pos_bala_inimigo = estado["balas_inimigos"]
            for i in range(len(x_bala_inimigo)):
                pos_bala_inimigo.append((x_bala_inimigo[i], y_bala_inimigo[i]))


        # Balas player
        if balas_player:
            x_bala_player = [float(x) for x in balas_player[0::2] if x.strip()]
            y_bala_player = [float(y) for y in balas_player[1::2] if y.strip()]
            pos_bala_player = estado["balas_player"]
            for i in range(len(x_bala_player)):
                pos_bala_player.append((x_bala_player[i], y_bala_player[i]))


        # Moves inimigos
        if moves_inimigos:
            moves_inimigos = [int(move) for move in moves_inimigos if move.strip()]
            for i in range(len(moves_inimigos)):
                estado["moves_inimigos"].append(moves_inimigos[i])


        # Score e frame
        estado["pontuação"] = int(score)
        estado["frame"] = int(frame)


        return estado






# =========================
# Criação de entidades (jogador, inimigo e balas)
# =========================


def criar_entidade(x,y, tipo="enemy"):
    t = turtle.Turtle(visible=False)
    if tipo == "player":
        t.shape("player.gif")
    else:
        t.shape("enemy.gif")
    t.penup()
    t.goto(x,y)
    t.showturtle()
    return t




def criar_bala(x, y, tipo):
    t = turtle.Turtle(visible=False)
    t.penup()
    t.shape("square")          
    t.shapesize(0.2, 0.5)       # Ajuste das dimensões da balas
    t.setx(x)  
    t.sety(y)    
    if tipo=="player":
        t.fillcolor("yellow")
    if tipo=="enemy":
        t.fillcolor("red")


    t.showturtle()
    return t




def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None):
    """Cria inimigos numa grelha inicial ou restaura a partir de posições guardadas"""
    if posicoes_existentes == None:
        enemies=state["enemies"]
        y=ENEMY_START_Y
        x=BORDA_X-ENEMY_SIZE/2
        for i in range(ENEMY_ROWS):
            for j in range(ENEMY_COLS):
                alien=criar_entidade(x,y)
                x = x-ENEMY_SPACING_X
                enemies.append(alien)
                state["enemy_moves"].append(1)      # Movimento inicial
            x = BORDA_X-ENEMY_SIZE/2
            y = y-ENEMY_SPACING_Y
   
    # Restaura inimigos a partir de posições guardadas
    else:
        lista_x=[]
        lista_y=[]
        for xs, ys in posicoes_existentes:
            lista_x.append(int(xs))
            lista_y.append(int(ys))
        for i in range(len(lista_x)):
            alien=criar_entidade(lista_x[i], lista_y[i])
            state["enemies"].append(alien)
            state["enemy_moves"].append(dirs_existentes[i])




def restaurar_balas(state, lista_pos, tipo):
    """Reposiciona graficamente as balas carregadas do ficheiro"""
    lista_x=[]
    lista_y=[]
    for xs, ys in lista_pos:
        lista_x.append(int(xs))
        lista_y.append(int(ys))
    for i in range(len(lista_x)):
        bala=criar_bala(lista_x[i], lista_y[i], tipo)
        if tipo == "player":
            state["player_bullets"].append(bala)
        if tipo == "enemy":
            state["enemy_bullets"].append(bala)






# =========================
# Handlers de tecla
# =========================


def mover_esquerda_handler():
    player=state["player"]
    if player.xcor()>=-BORDA_X+PLAYER_SPEED:
        player.penup()
        x=player.xcor()-PLAYER_SPEED
        player.setx(x)




def mover_direita_handler():
    player=state["player"]
    if player.xcor()<=BORDA_X-PLAYER_SPEED:
        player.penup()
        x=player.xcor()+PLAYER_SPEED
        player.setx(x)




def disparar_handler():
    player=state["player"]
    x=player.xcor()
    y=player.ycor()
    state["player_bullets"].append(criar_bala(x, y, "player"))
   


def gravar_handler():
    guardar_estado_txt(SAVE_FILE, state)




def terminar_handler():
    print("Pontuação Final: {}".format(state["score"]))
    STATE["screen"].bye()
    atualizar_highscores(HIGHSCORES_FILE,state["score"])
    sys.exit()
   


# =========================
# Atualizações e colisões
# =========================


def atualizar_balas_player(state):
    for i in state["player_bullets"]:
        if i.ycor()<BORDA_Y-50:
            i.seth(90)
            i.penup()
            i.fd(PLAYER_BULLET_SPEED)
        else:
            i.hideturtle()
            state["player_bullets"].remove(i)




def atualizar_balas_inimigos(state):
    for i in state["enemy_bullets"]:
        if i.ycor()>-BORDA_Y+50:
            i.seth(-90)
            i.penup()
            i.fd(ENEMY_BULLET_SPEED)
            i.pendown()
        else:
            i.hideturtle()
            state["enemy_bullets"].remove(i)
   


def atualizar_inimigos(state):
    """Move inimigos para baixo e aplica drift lateral aleatório"""
    enemy=state["enemies"]
    move=state["enemy_moves"]
    for i in range(len(enemy)):
        drift_chance=random.uniform(0,1)
        invert_chance=random.uniform(0,1)
        enemy[i].sety(enemy[i].ycor()-ENEMY_FALL_SPEED)


        # Probabilidade de inverter direção
        if invert_chance <= ENEMY_INVERT_CHANCE:
            move[i] = -move[i]


        # Movimento lateral
        if drift_chance <= ENEMY_DRIFT_CHANCE:
            if move[i] == 1:
                if ((enemy[i].xcor()+ENEMY_DRIFT_STEP) < BORDA_X):
                    enemy[i].setx(enemy[i].xcor()+ENEMY_DRIFT_STEP)




                else:
                    enemy[i].setx(enemy[i].xcor()-ENEMY_DRIFT_STEP)
                    move[i] = -move[i]
           
            else:
                if (-BORDA_X < (enemy[i].xcor()-ENEMY_DRIFT_STEP)):
                    enemy[i].setx(enemy[i].xcor()-ENEMY_DRIFT_STEP)
                else:
                    enemy[i].setx(enemy[i].xcor()+ENEMY_DRIFT_STEP)
                    move[i] = -move[i]




def inimigos_disparam(state):
    for i in state["enemies"]:
        chance=random.uniform(0,1)
        if chance <= ENEMY_FIRE_PROB:
            x=i.xcor()
            y=i.ycor()
            state["enemy_bullets"].append(criar_bala(x, y, "enemy"))




def verificar_colisoes_player_bullets(state):
    """Verifica colisões balas do jogador com inimigos"""
    player_bullets=state["player_bullets"]
    enemies=state["enemies"]
    gap = ENEMY_SIZE/2  
    for inimigo in enemies:
        x_inimigo=inimigo.xcor()
        y_inimigo=inimigo.ycor()
        for bullet in player_bullets:
            x_bala=bullet.xcor()
            y_bala=bullet.ycor()
            if (x_inimigo-gap <= x_bala <= x_inimigo+gap) and (y_inimigo-gap <= y_bala <= y_inimigo+gap):
                inimigo.hideturtle()
                enemies.remove(inimigo)
                bullet.hideturtle()
                player_bullets.remove(bullet)
                state["score"] += 100
               




def verificar_colisoes_enemy_bullets(state):
    """Verifica colisões balas inimigas com jogador"""
    player=state["player"]
    x_player=player.xcor()
    y_player=player.ycor()
    enemy_bullets=state["enemy_bullets"]
    for i in enemy_bullets:
        x_bala=i.xcor()
        y_bala=i.ycor()
        colisao = COLLISION_RADIUS
        if (x_player-colisao <= x_bala <= x_player+colisao) and (y_player-colisao <= y_bala <= y_player+colisao):
            player.hideturtle()
            i.hideturtle()
            enemy_bullets.remove(i)
            state["player"] = None
            return True
    return False




def inimigo_chegou_ao_fundo(state):
    enemies=state["enemies"]
    for inimigo in enemies:
        y_inimigo=inimigo.ycor()
        if y_inimigo < -BORDA_Y:
            return True
    return False




def verificar_colisao_player_com_inimigos(state):
    """Verifica colisão direta entre o jogador e um inimigo"""
    player=state["player"]
    x_player=player.xcor()
    y_player=player.ycor()
    enemies=state["enemies"]
    gap = ENEMY_SIZE/2
    for inimigo in enemies:
        x_inimigo=inimigo.xcor()
        y_inimigo=inimigo.ycor()
        if (x_inimigo-gap <= x_player < x_inimigo+gap) and (y_inimigo-gap <= y_player < y_inimigo+gap):
            player.hideturtle()
            inimigo.hideturtle()
            enemies.remove(inimigo)
            state["player"] = None
            return True
    return False






# =========================
# Execução principal
# =========================


if __name__ == "__main__":
    # Pergunta inicial: carregar?
    filename = input("Carregar jogo? Se sim, escreva nome do ficheiro, senão carregue Return: ").strip()
    loaded = carregar_estado_txt(filename)




    # Ecrã
    screen = turtle.Screen()
    screen.title("Space Invaders IPRP")
    screen.bgcolor("black")
    screen.setup(width=LARGURA, height=ALTURA)
    screen.tracer(0)




    # Imagens obrigatórias
    for img in ["player.gif", "enemy.gif"]:
        if not os.path.exists(img):
            print("ERRO: imagem '" + img + "' não encontrada.")
            sys.exit(1)
        screen.addshape(img)




    # Estado base
    state = {
        "screen": screen,
        "player": None,
        "enemies": [],
        "enemy_moves": [],          
        "player_bullets": [],
        "enemy_bullets": [],
        "score": 0,
        "frame": 0,
        "files": {"highscores": HIGHSCORES_FILE, "save": SAVE_FILE}
    }




    # Construção inicial
    if loaded:
        dicionario=loaded
        (xs, ys) = dicionario["nave_player"][0]         #[0] acede ao primeiro e único elemento da lista
        state["player"] = criar_entidade(int(xs), int(ys), "player")
        spawn_inimigos_em_grelha(state, dicionario["inimigos"], dicionario["moves_inimigos"])
        restaurar_balas(state,dicionario["balas_inimigos"], "enemy")
        restaurar_balas(state,dicionario["balas_player"], "player")
        state["score"]=dicionario["pontuação"]
        state["frame"]=dicionario["frame"]




    else:
        print("New game!")
        state["player"] = criar_entidade(0, -350,"player")
        spawn_inimigos_em_grelha(state, None, None)




    # Variavel global para os keyboard key handlers
    STATE = state




    # Teclas
    screen.listen()
    screen.onkeypress(mover_esquerda_handler, "Left")
    screen.onkeypress(mover_direita_handler, "Right")
    screen.onkeypress(disparar_handler, "space")
    screen.onkeypress(gravar_handler, "g")
    screen.onkeypress(terminar_handler, "Escape")




    # Loop principal
    while True:
        atualizar_balas_player(STATE)
        atualizar_inimigos(STATE)
        inimigos_disparam(STATE)
        atualizar_balas_inimigos(STATE)
        verificar_colisoes_player_bullets(STATE)
       
        if verificar_colisao_player_com_inimigos(STATE):
            print("Colisão direta com inimigo! Game Over")
            terminar_handler()
       
        if verificar_colisoes_enemy_bullets(STATE):
            print("Atingido por inimigo! Game Over")
            terminar_handler()




        if inimigo_chegou_ao_fundo(STATE):
            print("Um inimigo chegou ao fundo! Game Over")
            terminar_handler()




        if len(STATE["enemies"]) == 0:
            print("Vitória! Todos os inimigos foram destruídos.")
            terminar_handler()




        STATE["frame"] += 1
        screen.update()
        time.sleep(0.016)
    turtle.done()





