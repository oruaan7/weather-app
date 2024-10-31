import flet as ft
import requests
from datetime import datetime
import pytz

def main(page: ft.Page):
    page.title = "Clima"
    page.window_width = 400
    page.window_height = 700
    page.padding = 20
    page.bgcolor = ft.colors.CYAN_300
    page.scroll = "auto"

    # Widgets
    local_input = ft.TextField(
        label="Digite a cidade",
        width=280,
        bgcolor=ft.colors.BLUE_GREY_900,
        color=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.WHITE),
        border_radius=20,
        # Define a cidade inicial
        value="Divinópolis"  
    )
    ver_clima_button = ft.ElevatedButton(
        text="Ver Previsão",
        on_click=lambda e: obter_clima(e, local_input.value),
        width=200,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            color=ft.colors.WHITE,
            bgcolor=ft.colors.INDIGO_ACCENT_400,
            elevation=5
        ),
    )
    cidade_label = ft.Text(size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    data_label = ft.Text(size=18, color=ft.colors.WHITE70)
    temperatura_label = ft.Text(size=50, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_400)
    temperatura_simbolo_label = ft.Text("°C", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_ACCENT)
    umidade_label = ft.Text(size=50, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT)
    umidade_simbolo_label = ft.Text("%", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT)
    umidade_nome_label = ft.Text("Umidade", size=14, color=ft.colors.WHITE70)
    pressao_label = ft.Text(size=16, color=ft.colors.WHITE70)
    velocidade_label = ft.Text(size=16, color=ft.colors.WHITE70)
    descricao_label = ft.Text(size=18, color=ft.colors.LIGHT_BLUE_ACCENT)
    icon_image = ft.Image(width=130, height=130)
    

    def obter_clima(e, cidade):
        weather_key = ''
        api_link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={weather_key}&lang=pt&units=metric"

        try:
            r = requests.get(api_link)
            data = r.json()

            # Processamento dos dados
            pais_codigo = data["sys"]["country"]
            zona_fuso = pytz.country_timezones[pais_codigo]
            pais = pytz.country_names[pais_codigo]
            zona = pytz.timezone(zona_fuso[0])
            zona_horas = datetime.now(zona).strftime("%d/%m/%Y | %H:%M:%S %p")
            temperatura = data["main"]["temp"]
            pressao = data["main"]["pressure"]
            umidade = data["main"]["humidity"]
            velocidade = data["wind"]["speed"]
            descricao = data["weather"][0]["description"]


            # Atualizando informações
            cidade_label.value = f"{cidade} - {pais}"
            data_label.value = zona_horas
            temperatura_label.value = f"{temperatura:.1f}"
            umidade_label.value = f"{umidade}"
            pressao_label.value = f"Pressão: {pressao} hPa"
            velocidade_label.value = f"Vento: {velocidade} m/s"
            descricao_label.value = descricao.capitalize()
            
            # Icones do sol e da lua
            zona_periodo = int(datetime.now(zona).strftime("%H"))
            if zona_periodo <= 5 or zona_periodo > 18:
                icon_image.src = "imagens/lua.png"
                page.bgcolor = ft.colors.BLUE_GREY_900
            elif zona_periodo <= 11:
                icon_image.src = "imagens/sol_dia.png"
                page.bgcolor = ft.colors.LIGHT_BLUE
            else:
                icon_image.src = "imagens/sol_tarde.png"
                page.bgcolor = ft.colors.ORANGE_ACCENT_100

            # Redesenhando a página
            page.update()

        except:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Cidade não encontrada, tente novamente!", color=ft.colors.WHITE70),
                bgcolor=ft.colors.RED_900,
            )
            page.snack_bar.open = True
            page.update()

    # Layout da página
    page.add(
        ft.Column(
            [
                ft.Text("Weather", size=28, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                local_input,
                ver_clima_button,
                ft.Container(height=20),
                ft.Container(
                    content=ft.Column(
                        [
                            cidade_label,
                            data_label,
                            ft.Row(
                                [icon_image,],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                [temperatura_label, temperatura_simbolo_label],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                [umidade_label, umidade_simbolo_label],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            umidade_nome_label,
                            pressao_label,
                            velocidade_label,
                            descricao_label,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border_radius=30,
                    padding=25,
                    bgcolor=ft.colors.BLUE_GREY_800,
                    width=320,
                    shadow=ft.BoxShadow(blur_radius=12, spread_radius=5, color=ft.colors.BLACK26)
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Chama a função para obter o clima de Divinópolis ao iniciar
    obter_clima(None, "Divinopolis")

ft.app(target=main)