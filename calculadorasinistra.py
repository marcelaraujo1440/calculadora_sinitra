import PySimpleGUI as sg
import numpy as np
import os
import pandas as pd
import math


sg.theme('DarkTeal2')

# Funções para manipulação do arquivo CSV
def inicializar_arquivo_contagem():
    if not os.path.exists('contagem_cliques.csv'):
        df = pd.DataFrame(columns=['Botao', 'Contagem'])
        df.to_csv('contagem_cliques.csv', index=False)

def atualizar_contagem(botao):
    botoes_validos = ['Conjuntos', 'Função', 'Operações Básicas', 'Matrizes']
    if botao in botoes_validos:
        df = pd.read_csv('contagem_cliques.csv')
        if botao in df['Botao'].values:
            df.loc[df['Botao'] == botao, 'Contagem'] += 1
        else:
            df = df._append({'Botao': botao, 'Contagem': 1}, ignore_index=True)
        df.to_csv('contagem_cliques.csv', index=False)

def gerar_relatorio():
    df = pd.read_csv('contagem_cliques.csv')
    relatorio = ""
    for index, linha in df.iterrows():
        relatorio += f"{linha['Botao']}: {linha['Contagem']} vezes\n"
    return relatorio

# Inicializar arquivo de contagem
inicializar_arquivo_contagem()

def criar_layout_matriz(linhas, colunas, matrtiz_num):
    layout = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append(sg.Input(size=(5, 1), key=f'M{matrtiz_num}_r{i}c{j}'))
        layout.append(linha)
    return layout

def pegar_valores_matriz(window, linhas, colunas, matrtiz_num):
    matrtiz = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            valor = window[f'M{matrtiz_num}_r{i}c{j}'].get()
            if valor.replace('.', '', 1).isdigit() or (valor.startswith('-') and valor[1:].replace('.', '', 1).isdigit()):
                linha.append(float(valor))
            else:
                sg.popup_error(f"Valor inválido na matriz {matrtiz_num}, posição ({i},{j}).")
                return None
        matrtiz.append(linha)
    return np.array(matrtiz)

def criar_janela_inicial():
    layout = [
        [sg.Text('Olá, seja bem vindo(a) à', justification='center', font=("Bookman Old Style", 20), pad=(0, 20))],
        [sg.Text('"calculadora sinistra"', justification='center', font=('Cooper Black', 24), pad=(0, 20))],
        [sg.Button('INICIAR', size=(15, 1), font=("Courier", 15, 'bold'), pad=(0, 20))],
        [sg.Text('Desenvolvido por Gabriel Carmo e Marcel Araujo, todos os direitos reservados ©', 
                 justification='center', font=("Courier", 10), pad=(0, 60))]
    ]
    return sg.Window('Calculadora Sinistra', layout, size=(500, 450), element_justification='center', finalize=True)

def criar_janela_secundaria():
    layout = [
        [sg.Text('CALCULADORA SINISTRA', justification='center', font=('Cooper Black', 24), pad=(0, 20))],
        [sg.Text('Escolha uma opção:', justification='center', font=("Bookman Old Style", 20), pad=(0, 20))],
        [sg.Button('Entrar', size=(15, 1), font=("Courier", 15, 'bold')), 
         sg.Button('Voltar', size=(15, 1), font=("Courier", 15, 'bold'), pad=(0, 20))],
    ]
    return sg.Window('Calculadora Sinistra', layout, size=(500, 450), element_justification='center', finalize=True)

def janela_entrar():
    layout = [
        [sg.Text('CALCULADORA SINISTRA', justification='center', size=(50, 1), font=('Cooper Black', 24), pad=(0, 20))],
        [sg.Text('Entrar', justification='center', size=(50, 1), font=("Bookman Old Style", 20), pad=(20, 20))],
        [sg.Column([
            [sg.Frame(layout=[
                [sg.Text('Nome de usuário')],
                [sg.InputText(key='-USUARIO-', size=(30, 1))]
            ], title='', pad=(0, 10))]
        ], justification='center')],
        [sg.Button('Enviar', size=(15, 1), pad=(10,20)), sg.Button('Voltar', size=(15, 1), pad=(10, 20))]
    ]
    return sg.Window('Entrar', layout, size=(500, 450), element_justification='center', finalize=True)

def janela_op():
    layout = [
        [sg.Text("CALCULADORA SINISTRA", justification='center', font=("Bookman Old Style", 20), pad=(0, 20))],
        [sg.Text("Escolha a sua operação!", justification='center', font=("Bookman Old Style", 15), pad=(0, 20))],
        [sg.Button("Conjuntos", size=(15, 1), font=("Courier", 15, 'bold')), sg.Button("Matrizes", size=(15, 1), font=("Courier", 15, 'bold'))],
        [sg.Button("Função", size=(15, 1), font=("Courier", 15, 'bold')), sg.Button("Operações Básicas", size=(15, 1), font=("Courier", 15, 'bold'))],
        [sg.Button("Histórico", size=(15, 1), font=("Courier", 15, 'bold'), pad=(10,10))]
    ]
    return sg.Window('Calculadora Sinistra', layout, size=(500, 450), element_justification='center', finalize=True)

def janela_calculadorabasica():
    col_1 = [  # coluna 1
       [sg.Button('1', size=(8, 2), font="bold", pad=(5, 15)), sg.Button('2', size=(8, 2), font="bold", pad=(5, 15)), sg.Button('3', size=(8, 2), font="bold", pad=(5, 15))],
       [sg.Button('4', size=(8, 2), font="bold", pad=(5, 15)), sg.Button('5', size=(8, 2), font="bold", pad=(5, 15)), sg.Button('6', size=(8, 2), font="bold", pad=(5, 15))],
       [sg.Button('7', size=(8, 2), font="bold", pad=(5, 15)), sg.Button('8', size=(8, 2), font="bold", pad=(5, 15)), sg.Button('9', size=(8, 2), font="bold", pad=(5, 15))],
       [sg.Button('+/-', size=(8, 2), font="bold", key="-OPOSTO-", pad=(5, 15)), sg.Button('0', size=(8, 2), font="bold", pad=(5, 15)), sg.Button('.', size=(8, 2), font="bold", key="-PONTO-", pad=(5, 15))],
       [sg.Button("Voltar", size=(32, 2))]
    ]
    col_2 = [  # coluna 2
        [sg.Button('*', size=(8, 4), key="-MULTI-", font="bold")],
        [sg.Button('-', size=(8, 4), key="-MENOS-", font="bold")],
        [sg.Button('+', size=(8, 9), key="-MAIS-", font="bold")]
    ]
    
    col_3 = [  # coluna 3
        [sg.Button('/', size=(8, 2), key="-DIV-", font="bold")],
        [sg.Button('-->', size=(8, 2), key="-LIMPAR-", font="bold")],
        [sg.Button('CE', size=(8, 4), key="-LIMPARTD-", font="bold")],
        [sg.Button('=', size=(8, 8), key="-RESULTADO-", font="bold")]
    ]

    layout = [
        [sg.Input(key='-VALOR-', size=(31, 3), justification='right', font="bold")],
        [sg.Column(col_1), sg.Column(col_2), sg.Column(col_3)]
    ]

    return sg.Window('Calculadora Básica', layout, finalize=True)



def janela_func2():
    layout = [
        [sg.Text("Função do 2º grau", font=("Bookman Old Style", 20), justification='center', expand_x=True)],
        [sg.Text("Digite o valor de A", font=("Bookman Old Style", 10)), sg.InputText(key='-valA-', size=(7, 2))],
        [sg.Text("Digite o valor de B", font=("Bookman Old Style", 10)), sg.InputText(key='-valB-', size=(7, 2))],
        [sg.Text("Digite o valor de C", font=("Bookman Old Style", 10)), sg.InputText(key='-valC-', size=(7, 2))],
        [sg.Button("Calcular", size=(20, 2), pad=(20, 20))],
        [sg.Text("Resultado:", font=("Courier", 15))],
        [sg.Multiline(key='-RESULTADO-', size=(25, 5), disabled=True)],
        [sg.Button("Voltar", size=(20, 2), pad=(20, 20))]
    ]
    return sg.Window('Calculadora Sinistra', layout, size=(500, 450), element_justification='center', finalize=True)

def janela_matriz():
    layout = [
        [sg.Text("Calculadora de Matrizes",font=("Bookman Old Style", 20) , justification='center')],
        [sg.Text("Número de linhas e colunas da Matriz A:", font=("Bookman Old Style", 15) )],
        [sg.InputText(key='-linhaA-', size=(5, 1)), sg.InputText(key='-colunasA-', size=(5, 1))],
        [sg.Button("Criar Matriz A")],
        [sg.Text("Número de linhas e colunas da Matriz B:", font=("Courier", 15))],
        [sg.InputText(key='-linhaB-', size=(5, 1)), sg.InputText(key='-colunasB-', size=(5, 1))],
        [sg.Button("Criar Matriz B")],
        [sg.Frame("Matriz A", [[sg.Column([[]], key='-MATRIZ_A-')]]), 
         sg.Frame("Matriz B", [[sg.Column([[]], key='-MATRIZ_B-')]])],
        [sg.Button("Somar Matrizes"), sg.Button("Multiplicar Matrizes")],
        [sg.Button("Determinante Matriz A"), sg.Button("Determinante Matriz B")],
        [sg.Button("Transposta Matriz A"), sg.Button("Transposta Matriz B")],
        [sg.Text("Resultado:", font=("Courier", 15))],
        [sg.Multiline(key='-RESULTADO-', size=(40, 10), disabled=True)],
        [sg.Button("Voltar")]
    ]
    return sg.Window('Calculadora de Matrizes', layout, finalize=True)

def janela_matriz_valores(linhasA, colunasA, linhasB, colunasB):
    layoutA = criar_layout_matriz(linhasA, colunasA, 1)
    layoutB = criar_layout_matriz(linhasB, colunasB, 2)
    layout = [
        [sg.Frame('Matriz A', layoutA, font=("Bookman Old Style", 15))],
        [sg.Frame('Matriz B', layoutB, font=("Bookman Old Style", 15))],
        [sg.Button('Calcular', font=("Bookman Old Style", 10)), sg.Button('Voltar', font=("Bookman Old Style", 10))]
    ]
    return sg.Window('Valores das Matrizes', layout, finalize=True)

# Função de multiplicação de matrizes


def janela_inicial():
    layout = [
        [sg.Text('Escolha o tamanho dos conjuntos',font=("Bookman Old Style", 20))],
        [sg.Text('Tamanho do Conjunto A:', size=(20, 1),font=("Bookman Old Style", 20),pad=(20,20)), sg.Input(key='tamanho_a', size=(5, 1))],
        [sg.Text('Tamanho do Conjunto B:', size=(20, 1),font=("Bookman Old Style", 20),pad=(20,20)), sg.Input(key='tamanho_b', size=(5, 1))],
        [sg.Button("Voltar",size=(20,2),pad=(20,20)),sg.Button('Continuar',size=(20,2),pad=(20,20),)]
    ]
    return sg.Window('Calculadora Sinistra', layout, size=(500, 450), element_justification='center', finalize=True)

# Função para criar a janela dos conjuntos
def janela_conjuntos(tamanho_a, tamanho_b):
    layout_a = [[sg.Text(f'Elemento {i + 1}:', size=(10, 1)), sg.Input(key=f'elem_a_{i}', size=(7, 1))] for i in range(tamanho_a)]
    layout_b = [[sg.Text(f'Elemento {i + 1}:', size=(10, 1)), sg.Input(key=f'elem_b_{i}', size=(7, 1))] for i in range(tamanho_b)]
    
    layout = [
        [sg.Text('Elementos do Conjunto A',font=("Bookman Old Style", 20))],
        *layout_a,
        [sg.Text('Elementos do Conjunto B',font=("Bookman Old Style", 20))],
        *layout_b,
        [sg.Button('Calcular União',size=(10,2),pad=(10,10)), sg.Button('Calcular Interseção',size=(10,2)), sg.Button('Calcular Diferença',size=(10,2)), sg.Button('Voltar',size=(10,2))]
    ]
    return sg.Window('Calculadora Sinistra', layout, size=(500, 450), element_justification='center', finalize=True)


# Função para criar a janela de resultado
def janela_resultado(resultado):
    layout = [
        [sg.Text('Resultado:', size=(40, 1),font=("Bookman Old Style", 20))],
        [sg.Multiline(resultado, size=(20, 10), disabled=True)],
        [sg.Button('Voltar',size=(20,2))]
    ]
    return sg.Window('Calculadora Sinistra', layout, size=(500, 450), element_justification='center', finalize=True)

# Variáveis de controle de janelas
janela1= criar_janela_inicial()
janela2 = None #entrar ou voltar
janela3 =None #cadastro
janela4 =None #menu de operaçoes
janela5 =None #
janela6 =None #operações básicas
janela7 = None #janela matriz
janela8 = None #janela funcao 2 grau
janela9 = None#janela conjuntos
janela10= None
janela11= None

matriz_a_cria, matriz_b_cria = False, False
linhaA, colunasA, linhaB, colunasB = 0, 0, 0, 0
num = [str(i) for i in range(10)]
history = ''
operator = ["-DIV-","-MULTI-","-MAIS-","-MENOS-"]
while True:
    window, evento, valores = sg.read_all_windows()

    if evento == sg.WIN_CLOSED:
        window.close()
        if window == janela1:
            break
        continue

    if evento == 'INICIAR' and window == janela1:
        janela2 = criar_janela_secundaria()
        janela1.hide()

    if evento == 'Voltar':
        if window == janela2:
            janela1.un_hide()
            window.close()
        elif window == janela3:
            janela2.un_hide()
            window.close()
        elif window == janela4:
            janela2.un_hide()
            window.close()
        elif window == janela_calculadorabasica:
            janela4.un_hide()
            window.close()
        elif window == janela_matriz:
            janela4.un_hide()
            window.close()
        elif window == janela_matriz_valores:
            janela_matriz.un_hide()
            window.close()
            
    if window == janela2 and evento == 'Voltar':
        janela2.close()
        janela1.un_hide()
    if window == janela3 and evento == 'Voltar':
        janela3.close()
        janela2.un_hide()
    
    if window == janela4 and evento == 'Voltar':
        janela4.close()
        janela2.un_hide()

    if window == janela8 and evento == 'Voltar':
        janela8.hide()
        janela4.un_hide()

  
    if window == janela6 and evento == "Voltar":
        janela6.hide()
        janela4.un_hide()
    
    if window == janela7 and evento == "Voltar":
        janela7.hide()
        janela4.un_hide()

    if window == janela9 and evento == 'Voltar':
        janela9.hide()
        janela4.un_hide()

    if evento == 'Entrar' and window == janela2:
        janela3 = janela_entrar()
        janela2.hide()

    if evento == 'Enviar' and window == janela3:
        if valores['-USUARIO-']:
            sg.popup(f"Bem-vindo(a), {valores['-USUARIO-']}!")
            janela4 = janela_op()
            janela3.close()
        else:
            sg.popup_error("Por favor, insira um nome de usuário válido.")

    if window == janela4 and evento == 'Conjuntos':
        atualizar_contagem('Conjuntos')
        janela4.hide()
        janela9 = janela_inicial()
        

    if evento == 'Matrizes' and window == janela4:
        atualizar_contagem('Matrizes')
        janela4.hide()
        janela7 = janela_matriz()

    if evento == 'Função' and window == janela4:
        atualizar_contagem('Função')
        janela4.hide()
        janela8 = janela_func2()

    if evento == 'Operações Básicas' and window == janela4:
        atualizar_contagem('Operações Básicas')
        janela4.hide()
        janela6= janela_calculadorabasica()
        


    if evento == 'Histórico' and window == janela4:
        relatorio = gerar_relatorio()
        sg.popup_scrolled(relatorio, title="Histórico de Cliques")
    
    if evento == "Calcular":
            valA = valores['-valA-']
            valB = valores['-valB-']
            valC = valores['-valC-']
            
            if not valA or not valB or not valC:
                resultado = "Por favor, preencha todos os campos."
            elif not valA.replace('-', '').isdigit() or not valB.replace('-', '').isdigit() or not valC.replace('-', '').isdigit():
                resultado = "Por favor, insira valores numéricos válidos para A, B e C."
            else:
                a = int(valA)
                b = int(valB)
                c = int(valC)
                if a == 0:
                    resultado = "O valor de 'a' não pode ser zero."
                else:
                    delta = b**2 - 4*a*c
                    if delta < 0:
                        parte_real = -b / (2*a)
                        parte_imaginaria = math.sqrt(-delta) / (2*a)
                        resultado = (f"As raízes são complexas: {parte_real:.2f} + {parte_imaginaria:.2f}i "
                                    f"e {parte_real:.2f} - {parte_imaginaria:.2f}i\n")
                    elif delta == 0:
                        raiz = -b / (2*a)
                        resultado = f"A raiz é {raiz:.2f}"
                    else:
                        raiz1 = (-b + math.sqrt(delta)) / (2*a)
                        raiz2 = (-b - math.sqrt(delta)) / (2*a)
                        resultado = f"As raízes são {raiz1:.2f} e {raiz2:.2f}"
            
            window['-RESULTADO-'].update(resultado)

    if window == janela7 and evento == "Criar Matriz A":
        linhaA, colunasA = int(valores['-linhaA-']), int(valores['-colunasA-'])
        window['-MATRIZ_A-'].update(visible=True)
        window.extend_layout(window['-MATRIZ_A-'], criar_layout_matriz(linhaA, colunasA, 1))
        matriz_a_cria = True

    if window == janela7 and evento == "Criar Matriz B":
        linhaB, colunasB = int(valores['-linhaB-']), int(valores['-colunasB-'])
        window['-MATRIZ_B-'].update(visible=True)
        window.extend_layout(window['-MATRIZ_B-'], criar_layout_matriz(linhaB, colunasB, 2))
        matriz_b_cria = True

    if window == janela7 and evento == "Somar Matrizes" and matriz_a_cria and matriz_b_cria:
        matriz_a = pegar_valores_matriz(window, linhaA, colunasA, 1)
        matriz_b = pegar_valores_matriz(window, linhaB, colunasB, 2)
        if matriz_a is not None and matriz_b is not None:
            if matriz_a.shape == matriz_b.shape:
                result = matriz_a + matriz_b
                window['-RESULTADO-'].update(result)
            else:
                sg.popup_error("As matrizes devem ter o mesmo tamanho para serem somadas.")

    if window == janela7 and evento == "Multiplicar Matrizes" and matriz_a_cria and matriz_b_cria:
        matriz_a = pegar_valores_matriz(window, linhaA, colunasA, 1)
        matriz_b = pegar_valores_matriz(window, linhaB, colunasB, 2)
        if matriz_a is not None and matriz_b is not None:
            if colunasA == linhaB:
                result = np.dot(matriz_a, matriz_b)
                window['-RESULTADO-'].update(result)
            else:
                sg.popup_error("O número de colunas da Matriz A deve ser igual ao número de linhas da Matriz B.")

    if window == janela7 and evento == "Determinante Matriz A" and matriz_a_cria:
        matriz_a = pegar_valores_matriz(window, linhaA, colunasA, 1)
        if matriz_a is not None:
            if linhaA == colunasA:
                det_a = np.linalg.det(matriz_a)
                window['-RESULTADO-'].update(f'Determinante da Matriz A: {det_a}')
            else:
                sg.popup_error("A Matriz A deve ser quadrada para calcular o determinante.")

    if window == janela7 and evento == "Determinante Matriz B" and matriz_b_cria:
        matriz_b = pegar_valores_matriz(window, linhaB, colunasB, 2)
        if matriz_b is not None:
            if linhaB == colunasB:
                det_b = np.linalg.det(matriz_b)
                window['-RESULTADO-'].update(f'Determinante da Matriz B: {det_b}')
            else:
                sg.popup_error("A Matriz B deve ser quadrada para calcular o determinante.")

    if window == janela7 and evento == "Transposta Matriz A" and matriz_a_cria:
        matriz_a = pegar_valores_matriz(window, linhaA, colunasA, 1)
        if matriz_a is not None:
            trans_a = np.transpose(matriz_a)
            window['-RESULTADO-'].update(f'Transposta da Matriz A:\n{trans_a}')

    if window == janela7 and evento == "Transposta Matriz B" and matriz_b_cria:
        matriz_b = pegar_valores_matriz(window, linhaB, colunasB, 2)
        if matriz_b is not None:
            trans_b = np.transpose(matriz_b)
            window['-RESULTADO-'].update(f'Transposta da Matriz B:\n{trans_b}')
    
    if window == janela9 and evento == 'Continuar':
        tamanho_a = valores['tamanho_a']
        tamanho_b = valores['tamanho_b']
        if tamanho_a.isdigit() and tamanho_b.isdigit():
            tamanho_a = int(tamanho_a)
            tamanho_b = int(tamanho_b)
            janela9.hide()
            janela10 = janela_conjuntos(tamanho_a, tamanho_b)
        else:
            sg.popup('Por favor, insira números válidos para os tamanhos dos conjuntos')
    
    # Se clicar no botão 'Voltar' da janela dos conjuntos
    if window == janela10 and evento == 'Voltar':
        janela10.close()
        janela9.un_hide()
    
    # Se clicar nos botões de calcular
    if window == janela10 and evento in ['Calcular União', 'Calcular Interseção', 'Calcular Diferença']:
        conjunto_a = {valores[f'elem_a_{i}'] for i in range(tamanho_a)}
        conjunto_b = {valores[f'elem_b_{i}'] for i in range(tamanho_b)}
        
        if evento == 'Calcular União':
            resultado = conjunto_a | conjunto_b
            resultado_texto = f'União: {resultado}'
        elif evento == 'Calcular Interseção':
            resultado = conjunto_a & conjunto_b
            resultado_texto = f'Interseção: {resultado}'
        elif evento == 'Calcular Diferença':
            resultado = conjunto_a - conjunto_b
            resultado_texto = f'Diferença: {resultado}'
        
        janela10.hide()
        janela11 = janela_resultado(resultado_texto)
    
    # Se clicar no botão 'Voltar' da janela de resultado
    if window == janela11 and evento == 'Voltar':
        janela11.close()
        janela10.un_hide()
    
    elif evento in num:
        if len(history) < 12:
            history += evento
            window["-VALOR-"].update(int(history))
    elif evento in operator:
        op = evento
        num_1 = float(history)
        history = ''
    
    elif evento == "-RESULTADO-":
        num_2 = int(history)
        if op == "-MAIS-":
            result = num_1 + num_2
        elif op == "-MENOS-":
            result = num_1 - num_2
        elif op == "-MULTI-":
            result = num_1 * num_2
        elif op == "-DIV-":
            result = num_1 / num_2
        window["-VALOR-"].update(float(result))
    
    elif evento == "-LIMPAR-":
        if len(history)>0:
            history = history[:-1]
            window["-VALOR-"].update(history)
    
    elif evento == "-LIMPARTD-":
        history = ''
        num_1 = 0
        num_2 = 0
        op = ''
        window["-VALOR-"].update(history)
    elif evento == "-OPOSTO-":
        history = str(int(history) * -1)
        window["-VALOR-"].update(history)

       
window.close()
