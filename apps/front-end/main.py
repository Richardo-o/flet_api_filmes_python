import flet as ft
import requests

API_URL = "http://127.0.0.1:5000/filmes"


def main(page: ft.Page):

    page.title = "Sistema de Filmes"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a"
    page.scroll = "auto"
    page.window_width = 500
    page.window_height = 800
    page.padding = 20

    lista_filmes = ft.Column(spacing=15)

    nome_input = ft.TextField(
        label="Nome do Filme",
        border_radius=12,
        filled=True,
        width=400
    )

    genero_input = ft.TextField(
        label="Gênero",
        border_radius=12,
        filled=True,
        width=400
    )

    mensagem = ft.Text(color="white")

    def carregar_filmes():

        lista_filmes.controls.clear()

        try:

            resposta = requests.get(API_URL)
            filmes = resposta.json()

            for filme in filmes:

                card = ft.Container(
                    bgcolor="#1e293b",
                    border_radius=20,
                    padding=20,
                    animate=300,
                    content=ft.Column([
                        ft.Text(
                            filme["nome"],
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color="white"
                        ),

                        ft.Text(
                            f'{filme["genero"]}',
                            color="#cbd5e1",
                            size=16
                        )
                    ])
                )

                lista_filmes.controls.append(card)

            page.update()

        except Exception as erro:

            mensagem.value = f"Erro: {erro}"
            page.update()

    def cadastrar_filme(e):

        dados = {
            "nome": nome_input.value,
            "genero": genero_input.value
        }

        try:

            resposta = requests.post(API_URL, json=dados)

            if resposta.status_code == 201:

                mensagem.value = "✅ Filme cadastrado!"
                mensagem.color = "green"

                nome_input.value = ""
                genero_input.value = ""

                carregar_filmes()

            else:

                mensagem.value = "❌ Erro ao cadastrar"
                mensagem.color = "red"

            page.update()

        except Exception as erro:

            mensagem.value = f"Erro: {erro}"
            mensagem.color = "red"
            page.update()

    carregar_filmes()

    botao = ft.ElevatedButton(
        "Cadastrar Filme",
        width=400,
        height=50,
        bgcolor="#2563eb",
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12)
        ),
        on_click=cadastrar_filme
    )

    page.add(

        ft.Container(
            padding=20,
            border_radius=25,
            bgcolor="#111827",

            content=ft.Column([

                ft.Text(
                    "🎬 Catálogo de Filmes",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),

                ft.Text(
                    "Sistema utilizando Flask + Flet",
                    size=16,
                    color="#94a3b8"
                ),

                ft.Divider(color="#334155"),

                ft.Text(
                    "Lista de Filmes",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),

                lista_filmes,

                ft.Divider(color="#334155"),

                ft.Text(
                    "➕ Cadastrar Filme",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),

                nome_input,
                genero_input,

                botao,

                mensagem

            ],
            spacing=20)
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)