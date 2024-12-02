import flet as ft
import base64

def main(page: ft.Page):
    page.title = "Cotizador Condominios"
    page.scroll = "auto"

    # Conversión de imagen a base64
    def convertir_imagen_base64(ruta_imagen):
        with open(ruta_imagen, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    imagen_base64 = convertir_imagen_base64("imagen2.jpg")
    filas = []

    # Calcular valores
    def calcular_valores(edificio, cantidad):
        incendio_sismo = float(edificio) * float(cantidad) * (2.6 / 1000)
        incendio_solo = float(edificio) * float(cantidad) * (0.40 / 1000)
        return round(incendio_sismo, 2), round(incendio_solo, 2)

    # Actualizar totales generales
    def actualizar_totales():
        total_edificio = sum(float(f.cells[1].content.value or 0) for f in filas)
        total_cantidad = sum(float(f.cells[2].content.value or 0) for f in filas)
        total_pn_incendio_sismo = sum(float(f.cells[6].content.value or 0) for f in filas)
        total_pn_incendio = sum(float(f.cells[7].content.value or 0) for f in filas)

        totales_row.cells[1].content.value = str(round(total_edificio, 2))
        totales_row.cells[2].content.value = str(round(total_cantidad, 2))
        totales_row.cells[6].content.value = str(round(total_pn_incendio_sismo, 2))
        totales_row.cells[7].content.value = str(round(total_pn_incendio, 2))

        page.update()

    # Función para agregar una nueva fila
    def agregar_fila(e):
        def on_change_text(e, fila, index):
            try:
                edificio_value = fila.cells[1].content.value
                cantidad_value = fila.cells[2].content.value

                incendio_sismo, incendio_solo = calcular_valores(edificio_value, cantidad_value)

                # Actualizar las celdas de primas netas
                fila.cells[6].content.value = str(incendio_sismo)  # P.Neta Incendio/Sismo
                fila.cells[7].content.value = str(incendio_solo)  # Prima Neta Incendio

                # Actualizar totales generales
                actualizar_totales()
            except ValueError:
                pass  # Manejar valores no numéricos

        nueva_fila = ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("Departamento"),
                            ft.dropdown.Option("Espacios Comunes"),
                            ft.dropdown.Option("Oficina"),
                            ft.dropdown.Option("Locales Comerciales"),
                        ],
                        value="Departamento",
                        width=180,
                    )
                ),
                ft.DataCell(ft.TextField(value="100.00", max_length=6, width=120,text_align=ft.TextAlign.RIGHT)), # Ajusta la altura para evitar que se muestre el contador (si aparece)
                ft.DataCell(ft.TextField(value="1", max_length=3, width=80,text_align=ft.TextAlign.RIGHT)),
                ft.DataCell(ft.Text("2.60", width=120)),
                ft.DataCell(ft.Text("0.40", width=120)),
                ft.DataCell(ft.Text("-", width=100)),
                ft.DataCell(ft.Text("0.00", width=150)),
                ft.DataCell(ft.Text("0.00", width=150)),
            ]
        )

        # Vincular eventos a las celdas de la nueva fila
        for idx, cell in enumerate(nueva_fila.cells):
            if isinstance(cell.content, ft.TextField):  # Cambiar 'control' por 'content'
                cell.content.on_change = lambda e, fila=nueva_fila, index=idx: on_change_text(e, fila, index)

        filas.append(nueva_fila)
        actualizar_tabla()

    # Función para eliminar la última fila
    def eliminar_ultima_fila(e):
        if filas:
            filas.pop()
            actualizar_tabla()
            actualizar_totales()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("No hay filas para eliminar"))
            page.snack_bar.open = True
            page.update()

    # Actualizar la tabla
    def actualizar_tabla():
        tabla_flet.rows = filas + [totales_row]
        page.update()

    # Fila de totales
    totales_row = ft.DataRow(
        cells=[
            ft.DataCell(ft.Text("Totales", weight="bold")),
            ft.DataCell(ft.Text("                   0.00", width=150)),
            ft.DataCell(ft.Text("              0", width=100)),
            ft.DataCell(ft.Text("", width=150)),
            ft.DataCell(ft.Text("", width=150)),
            ft.DataCell(ft.Text("", width=120)),
            ft.DataCell(ft.Text("0.00", width=150)),
            ft.DataCell(ft.Text("0.00", width=150)),
        ]
    )

    # Tabla
    tabla_flet = ft.DataTable(
        column_spacing=15,
        columns=[
            ft.DataColumn(ft.Text("Riesgo", width=180)),
            ft.DataColumn(ft.Text("Edificio", width=150)),
            ft.DataColumn(ft.Text("Cantidad", width=100)),
            ft.DataColumn(ft.Text("Incendio y Sismo", width=150)),
            ft.DataColumn(ft.Text("Incendio Solo", width=150)),
            ft.DataColumn(ft.Text("Asistencia", width=120)),
            ft.DataColumn(ft.Text("P.Neta Incendio/Sismo", width=150)),
            ft.DataColumn(ft.Text("Prima Neta Incendio", width=150)),
        ],
        rows=filas + [totales_row],
    )

    # Botones
    botones_control = ft.Row(
        [
            ft.ElevatedButton("Agregar línea", icon=ft.icons.ADD, on_click=agregar_fila),
            ft.ElevatedButton("Eliminar última línea", icon=ft.icons.REMOVE, on_click=eliminar_ultima_fila),
        ],
        alignment=ft.MainAxisAlignment.END,
    )

    # Botón para el enlace PDF
    boton_pdf = ft.TextButton(
        "PDF",
        on_click=lambda e: page.launch_url("COTIZACION_CONDOMINIO.pdf"),
    )
    
    # Sección de información adicional con ComboBox para opciones Sí/No
    info_section = ft.Row(
        [
            ft.Column(
                [
                    ft.Row([ft.Text("Sucursal:      "),
                        ft.Dropdown(
                            options=[ft.dropdown.Option("Matriz"), ft.dropdown.Option("La Florida"), ft.dropdown.Option("Iquique")],
                            value="No",
                            width=200,
                        )]),
                    ft.Row([ft.Text("Ej.Comercial:"), ft.TextField(value="Roxana Perez", width=200)]),
                    ft.Row([ft.Text("Corredor:     "), ft.TextField(value="Orlando Navarro", width=200)]),
                    ft.Row([ft.Text("RUT:            "), ft.TextField(value="56047380-K", width=200)]),
                    ft.Row([ft.Text("Nombre:     "), ft.TextField(value="EDIFICIO JUAN FRANCISCO GONZALEZ", width=350)]),
                    ft.Row([ft.Text("Fecha  Vcto:"), ft.TextField(value="30-01-2024", width=200)]),
                    ft.Row([ft.Text("Recargo:     "), ft.TextField(value="0%", width=100)]),
                ],
                spacing=10,
                width=500,
            ),
            ft.Column(
                [
                    ft.Row([ft.Text("Descuento Max:"), ft.TextField(value="0%", width=100)]),
                    ft.Row([ft.Text("Descuento:        "), ft.TextField(value="0%", width=100)]),
                    ft.Row([
                        ft.Text("T. Construcción:"),
                        ft.Dropdown(
                            options=[ft.dropdown.Option("A:Incombustible"), ft.dropdown.Option("B:Mixto"), ft.dropdown.Option("C:Combustible")],
                            value="No",
                            width=200,
                        )
                    ]),
                    ft.Row([
                        ft.Text("Borde Costero:  "),
                        ft.Dropdown(
                            options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")],
                            value="No",
                            width=150,
                        )
                    ]),
                    ft.Row([
                        ft.Text("Zona:                 "),
                        ft.Dropdown(
                            options=[ft.dropdown.Option("Región 1 - 4"), ft.dropdown.Option("Región 5"), ft.dropdown.Option("Región 1 -12"), ft.dropdown.Option("Región 13 Met"), ft.dropdown.Option("Región 14")],
                            value="No",
                            width=150,
                        )
                    ]),
                    ft.Row([ft.Text("Capacidad por Categoría:"), ft.TextField(value="510.000", width=150)]),
                    ft.Row([ft.Text("Control Suscripción:         "), ft.TextField(value="En Contrato", width=150)]),
                ],
                spacing=10,
                width=500,
            ),
            ft.Column(
                [
                    ft.Text("Siniestralidad", weight="bold", size=18),
                    ft.Row([ft.Text("Inc. adic.:  "), ft.TextField(value="45", width=100)]),
                    ft.Row([ft.Text("Sismo:       "), ft.TextField(value="-", width=100)]),
                    ft.Row([ft.Text("Terrorismo:"), ft.TextField(value="-", width=100)]),
                    ft.Row([ft.Text("42%", color="green", size=16)]),
                ],
                spacing=10,
                width=300,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )
    
    # Se agrega todo a la página
    page.add(
        ft.Image(src_base64=imagen_base64),
        ft.Text("Cotizador Condominios", size=24, weight="bold", color="green"),
        boton_pdf,  # Aquí se agrega el botón PDF
        info_section,
        ft.Divider(height=20),
        ft.Column(
            [
                ft.Text("COTIZACIÓN", size=20, weight="bold"),
                tabla_flet,
                botones_control,
            ],
            spacing=20,
        ),
    )
    
ft.app(target=main)
