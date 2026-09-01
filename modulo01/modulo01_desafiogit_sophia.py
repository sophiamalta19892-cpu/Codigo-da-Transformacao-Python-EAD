import tkinter as tk
from tkinter import messagebox


produtos = [
    {
        "nome": "açaí comum",
        "estoque": 100,
        "preco": 8.90,
        "validade": "10/12/2026",
        "descricao": "Açaí comum, ideal para quem gosta de um sabor clássico."
    },
    {
        "nome": "açaí guarana",
        "estoque": 50,
        "preco": 12.90,
        "validade": "10/10/2026",
        "descricao": "Açaí guarana, com sabor refrescante e ingredientes de qualidade."
    },
    {
        "nome": "açaí cupuaçu",
        "estoque": 130,
        "preco": 15.90,
        "validade": "10/12/2026",
        "descricao": "Açaí cupuaçu, com ingredientes locais e sabor autêntico."
    }
]


def limpar_campos():
    entrada_nome.delete(0, tk.END)
    entrada_estoque.delete(0, tk.END)
    entrada_preco.delete(0, tk.END)
    entrada_validade.delete(0, tk.END)
    entrada_descricao.delete(0, tk.END)


def cadastrar_produto():
    nome = entrada_nome.get().strip()
    estoque = entrada_estoque.get().strip()
    preco = entrada_preco.get().strip()
    validade = entrada_validade.get().strip()
    descricao = entrada_descricao.get().strip()

    if not nome or not estoque or not preco or not validade or not descricao:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        estoque = int(estoque)
        preco = float(preco.replace(",", "."))
    except ValueError:
        messagebox.showerror("Erro", "Estoque deve ser número inteiro e preço deve ser número.")
        return

    if estoque < 0 or preco <= 0:
        messagebox.showerror("Erro", "Estoque e preço devem ser valores válidos.")
        return

    produto = {
        "nome": nome,
        "estoque": estoque,
        "preco": preco,
        "validade": validade,
        "descricao": descricao
    }

    produtos.append(produto)
    messagebox.showinfo("Sucesso", f'Produto "{nome}" cadastrado com sucesso!')
    limpar_campos()
    listar_produtos()


def listar_produtos():
    lista_produtos.delete(0, tk.END)

    if len(produtos) == 0:
        lista_produtos.insert(tk.END, "Nenhum produto cadastrado.")
        return

    for i, produto in enumerate(produtos, start=1):
        texto = (
            f'{i}. {produto["nome"]} | '
            f'R$ {produto["preco"]:.2f} | '
            f'Estoque: {produto["estoque"]} | '
            f'Validade: {produto["validade"]}'
        )
        lista_produtos.insert(tk.END, texto)


def realizar_venda():
    nome_venda = entrada_venda_nome.get().strip()
    qtd_venda = entrada_venda_qtd.get().strip()

    if not nome_venda or not qtd_venda:
        messagebox.showerror("Erro", "Digite o nome do produto e a quantidade.")
        return

    try:
        qtd_venda = int(qtd_venda)
    except ValueError:
        messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
        return

    if qtd_venda <= 0:
        messagebox.showerror("Erro", "A quantidade deve ser maior que zero.")
        return

    for produto in produtos:
        if produto["nome"].lower() == nome_venda.lower():
            if qtd_venda <= produto["estoque"]:
                produto["estoque"] -= qtd_venda
                total = qtd_venda * produto["preco"]

                messagebox.showinfo(
                    "Venda realizada",
                    f'Produto: {produto["nome"]}\n'
                    f'Quantidade: {qtd_venda}\n'
                    f'Total: R$ {total:.2f}\n'
                    f'Estoque atual: {produto["estoque"]}'
                )

                entrada_venda_nome.delete(0, tk.END)
                entrada_venda_qtd.delete(0, tk.END)
                listar_produtos()
                return
            else:
                messagebox.showerror(
                    "Estoque insuficiente",
                    f'Temos apenas {produto["estoque"]} unidades.'
                )
                return

    messagebox.showerror("Erro", "Produto não encontrado!")


def ver_detalhes():
    selecionado = lista_produtos.curselection()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto na lista.")
        return

    indice = selecionado[0]

    if indice >= len(produtos):
        messagebox.showwarning("Aviso", "Nenhum produto válido selecionado.")
        return

    produto = produtos[indice]

    messagebox.showinfo(
        "Detalhes do produto",
        f'Nome: {produto["nome"]}\n'
        f'Estoque: {produto["estoque"]}\n'
        f'Preço: R$ {produto["preco"]:.2f}\n'
        f'Validade: {produto["validade"]}\n'
        f'Descrição: {produto["descricao"]}'
    )


def excluir_produto():
    selecionado = lista_produtos.curselection()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
        return

    indice = selecionado[0]

    if indice >= len(produtos):
        messagebox.showwarning("Aviso", "Nenhum produto válido selecionado.")
        return

    produto = produtos[indice]

    confirmar = messagebox.askyesno(
        "Confirmar exclusão",
        f'Deseja realmente excluir o produto "{produto["nome"]}"?'
    )

    if confirmar:
        produtos.pop(indice)
        listar_produtos()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")


def sair_sistema():
    confirmar = messagebox.askyesno(
        "Sair",
        "Deseja realmente sair do sistema?"
    )

    if confirmar:
        janela.destroy()


janela = tk.Tk()
janela.title("Sistema de Vendas - Açaiteria")
janela.geometry("820x780")
janela.resizable(True, True)

titulo = tk.Label(
    janela,
    text="Sistema de Vendas - Açaiteria",
    font=("Arial", 18, "bold")
)
titulo.pack(pady=10)

frame_cadastro = tk.LabelFrame(janela, text="Cadastrar produto", padx=10, pady=10)
frame_cadastro.pack(fill="x", padx=15, pady=10)

tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky="w")
entrada_nome = tk.Entry(frame_cadastro, width=35)
entrada_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Estoque:").grid(row=0, column=2, sticky="w")
entrada_estoque = tk.Entry(frame_cadastro, width=15)
entrada_estoque.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_cadastro, text="Preço:").grid(row=1, column=0, sticky="w")
entrada_preco = tk.Entry(frame_cadastro, width=35)
entrada_preco.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Validade:").grid(row=1, column=2, sticky="w")
entrada_validade = tk.Entry(frame_cadastro, width=15)
entrada_validade.grid(row=1, column=3, padx=5, pady=5)

tk.Label(frame_cadastro, text="Descrição:").grid(row=2, column=0, sticky="w")
entrada_descricao = tk.Entry(frame_cadastro, width=65)
entrada_descricao.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

botao_cadastrar = tk.Button(
    frame_cadastro,
    text="Cadastrar Produto",
    command=cadastrar_produto,
    bg="#7b2cbf",
    fg="white",
    width=20
)
botao_cadastrar.grid(row=3, column=1, pady=10)

botao_limpar = tk.Button(
    frame_cadastro,
    text="Limpar Campos",
    command=limpar_campos,
    width=20
)
botao_limpar.grid(row=3, column=2, pady=10)

frame_lista = tk.LabelFrame(janela, text="Produtos cadastrados", padx=10, pady=10)
frame_lista.pack(fill="both", expand=True, padx=15, pady=10)

lista_produtos = tk.Listbox(frame_lista, width=100, height=10)
lista_produtos.pack(side="left", fill="both", expand=True)

barra_rolagem = tk.Scrollbar(frame_lista)
barra_rolagem.pack(side="right", fill="y")

lista_produtos.config(yscrollcommand=barra_rolagem.set)
barra_rolagem.config(command=lista_produtos.yview)

frame_botoes_produto = tk.Frame(janela)
frame_botoes_produto.pack(pady=5)

botao_detalhes = tk.Button(
    frame_botoes_produto,
    text="Ver detalhes",
    command=ver_detalhes,
    width=20
)
botao_detalhes.grid(row=0, column=0, padx=5)

botao_excluir = tk.Button(
    frame_botoes_produto,
    text="Excluir Produto",
    command=excluir_produto,
    bg="#ffb703",
    fg="black",
    width=20
)
botao_excluir.grid(row=0, column=1, padx=5)

frame_venda = tk.LabelFrame(janela, text="Realizar venda", padx=10, pady=10)
frame_venda.pack(fill="x", padx=15, pady=10)

tk.Label(frame_venda, text="Nome do produto:").grid(row=0, column=0, sticky="w")
entrada_venda_nome = tk.Entry(frame_venda, width=35)
entrada_venda_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_venda, text="Quantidade:").grid(row=0, column=2, sticky="w")
entrada_venda_qtd = tk.Entry(frame_venda, width=15)
entrada_venda_qtd.grid(row=0, column=3, padx=5, pady=5)

botao_venda = tk.Button(
    frame_venda,
    text="Realizar Venda",
    command=realizar_venda,
    bg="#38b000",
    fg="white",
    width=20
)
botao_venda.grid(row=1, column=1, pady=10)

botao_sair = tk.Button(
    janela,
    text="Sair do Sistema",
    command=sair_sistema,
    bg="#d00000",
    fg="white",
    width=25
)
botao_sair.pack(pady=10)

listar_produtos()

janela.mainloop()
