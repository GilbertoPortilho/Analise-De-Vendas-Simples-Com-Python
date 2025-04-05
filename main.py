# Importação das bibliotecas necessárias
import tkinter as tk  # Interface gráfica padrão do Python
from tkinter import filedialog, messagebox  # Caixas de diálogo para abrir arquivo e exibir mensagens
from tkinter import ttk  # Widgets modernos do tkinter (botões, labels, etc.)
import pandas as pd  # Biblioteca para manipulação de dados
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integração do matplotlib com tkinter

# Função para processar os dados do CSV
def analisar_vendas(caminho_arquivo):
    try:
        # Lê o arquivo CSV usando o pandas e cria um DataFrame
        df = pd.read_csv(caminho_arquivo)

        # Soma os valores da coluna 'Total da Venda' para calcular o faturamento total
        faturamento_total = df["Total da Venda"].sum()

        # Agrupa os dados por produto, soma a quantidade vendida de cada um e retorna o que teve maior soma
        produto_mais_vendido = df.groupby("Produto")["Quantidade"].sum().idxmax()

        # Agrupa os dados por região e soma o total de vendas para cada uma
        receita_por_regiao = df.groupby("Região")["Total da Venda"].sum()

        # Retorna os dados calculados para serem usados na interface
        return faturamento_total, produto_mais_vendido, receita_por_regiao
    except Exception as e:
        # Exibe uma mensagem de erro caso ocorra alguma falha durante o processamento
        messagebox.showerror("Erro ao processar", str(e))
        return None, None, None

# Função para exibir o gráfico dentro do tkinter
def exibir_grafico(regioes, totais):
    # Cria uma figura do matplotlib com tamanho 6x4 polegadas
    fig, ax = plt.subplots(figsize=(6, 4))

    # Cria um gráfico de barras com os dados de receita por região
    ax.bar(regioes, totais, color="skyblue")
    ax.set_title("Receita por Região")  # Título do gráfico
    ax.set_ylabel("R$")  # Label do eixo Y
    ax.set_xlabel("Região")  # Label do eixo X

    # Limpa qualquer gráfico anterior do frame onde o gráfico será exibido
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Renderiza o gráfico na interface do tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Função que lida com a seleção de arquivo pelo usuário
def selecionar_arquivo():
    # Abre uma janela para o usuário escolher um arquivo CSV
    caminho = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if caminho:
        # Exibe o nome do arquivo escolhido pelo usuário
        lbl_arquivo.config(text=f"Arquivo carregado: {caminho.split('/')[-1]}")

        # Chama a função de análise para processar os dados do arquivo
        faturamento, produto, receita_regiao = analisar_vendas(caminho)

        if faturamento:
            # Mostra na tela o faturamento total e o produto mais vendido
            lbl_resultado.config(
                text=f"Faturamento Total: R$ {faturamento:,.2f}\nProduto Mais Vendido: {produto}"
            )
            # Gera o gráfico com os dados processados
            exibir_grafico(receita_regiao.index, receita_regiao.values)

# Criação da janela principal do aplicativo
janela = tk.Tk()  # Cria a janela do programa
janela.title("Analisador de Vendas")  # Define o título da janela
janela.geometry("700x500")  # Define o tamanho da janela

# Frame do topo onde ficará o botão para carregar arquivo
frame_topo = ttk.Frame(janela)
frame_topo.pack(pady=20)

# Botão que permite o usuário escolher o arquivo CSV para análise
btn_selecionar = ttk.Button(frame_topo, text="Selecionar Arquivo CSV", command=selecionar_arquivo)
btn_selecionar.pack()

# Label que exibe o nome do arquivo carregado ou uma mensagem padrão
lbl_arquivo = ttk.Label(janela, text="Nenhum arquivo carregado.")
lbl_arquivo.pack(pady=5)

# Label que vai mostrar os resultados dos cálculos após carregar o CSV
lbl_resultado = ttk.Label(janela, text="")
lbl_resultado.pack(pady=10)

# Frame onde será exibido o gráfico com os dados analisados
frame_grafico = ttk.Frame(janela)
frame_grafico.pack(expand=True, fill="both")

# Inicia o loop principal da interface gráfica, deixando a janela em execução
janela.mainloop()
