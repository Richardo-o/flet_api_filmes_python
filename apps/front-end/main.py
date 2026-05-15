import flet as ft
import requests

API_URL = "http://127.0.0.1:5000/filmes"


def main(page: ft.Page):

    # =========================
    # CONFIGURAÇÕES DA PÁGINA
    # =========================
    page.title = "Sistema de Filmes"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "auto"
    page.window_width = 500
    page.window_height = 700

    # =========================
    # COMPONENTES
    # =========================
    lista_filmes = ft.Column()

    nome_input = ft.TextField(
        label="Nome do Filme",
        width=400
    )

    genero_input = ft.TextField(
        label="Gênero",
        width=400
    )

    mensagem = ft.Text("")

    # =========================
    # FUNÇÃO LISTAR FILMES
    # =========================
    def carregar_filmes():

        lista_filmes.controls.clear()

        try:

            resposta = requests.get(API_URL)

            filmes = resposta.json()

            for filme in filmes:

                card = ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(
                                filme["nome"],
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                f'Gênero: {filme["genero"]}'
                            )
                        ])
                    )
                )

                lista_filmes.controls.append(card)

            page.update()

        except Exception as erro:

            mensagem.value = f"Erro ao carregar filmes: {erro}"
            page.update()

    # =========================
    # FUNÇÃO CADASTRAR FILME
    # =========================
    def cadastrar_filme(e):

        dados = {
            "nome": nome_input.value,
            "genero": genero_input.value
        }

        try:

            resposta = requests.post(
                API_URL,
                json=dados
            )

            if resposta.status_code == 201:

                mensagem.value = "✅ Filme cadastrado com sucesso!"

                nome_input.value = ""
                genero_input.value = ""

                carregar_filmes()

            else:

                mensagem.value = "❌ Erro ao cadastrar"

            page.update()

        except Exception as erro:

            mensagem.value = f"Erro: {erro}"

            page.update()

    # =========================
    # CARREGAR FILMES
    # =========================
    carregar_filmes()

    # =========================
    # BOTÃO
    # =========================
    botao = ft.ElevatedButton(
        "Cadastrar Filme",
        on_click=cadastrar_filme,
        width=400
    )

    # =========================
    # TELA
    # =========================
    page.add(

        ft.Text(
            "🎬 Catálogo de Filmes",
            size=30,
            weight=ft.FontWeight.BOLD
        ),

        ft.Text(
            "Sistema utilizando Flask + Flet",
            size=16
        ),

        ft.Divider(),

        ft.Text(
            "📋 Lista de Filmes",
            size=25,
            weight=ft.FontWeight.BOLD
        ),

        lista_filmes,

        ft.Divider(),

        ft.Text(
            "➕ Cadastrar Filme",
            size=25,
            weight=ft.FontWeight.BOLD
        ),

        nome_input,
        genero_input,

        botao,

        mensagem
    )


ft.app(target=main)