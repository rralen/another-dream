import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "SDiario"
    sueños = []
    contenido = ft.Column(scroll=ft.ScrollMode.AUTO)
    panel = ft.ExpansionPanelList(expand_icon_color=ft.Colors.AMBER, elevation=8, divider_color=ft.Colors.AMBER)
    
    # Estado del calendario
    fecha_hoy = datetime.date.today()
    fecha_actual = fecha_hoy.replace(day=1)
    sueños_por_fecha = {}
    
    def eliminar_sueño(e):
        sueño_a_eliminar = e.control.data
        panel.controls.remove(sueño_a_eliminar)
        sueños.remove((sueño_a_eliminar.header.title.value, sueño_a_eliminar.content.controls[0].title.value))
        page.update()
    
    def guardar_sueño(e):
        titulo = titulo_input.value
        descripcion = descripcion_input.value
        if titulo and descripcion:
            fecha_registro = datetime.datetime.now().strftime("%d/%m/%Y")
            eliminar_btn = ft.ElevatedButton("Eliminar", on_click=eliminar_sueño)
            nuevo_sueño = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text(f"{titulo} ({fecha_registro})")),
                content=ft.Column([
                    ft.ListTile(title=ft.Text(descripcion)),
                    ft.Row([eliminar_btn], alignment=ft.MainAxisAlignment.END)
                ]),
            )
            eliminar_btn.data = nuevo_sueño  # Asociar el botón con el panel
            panel.controls.append(nuevo_sueño)
            sueños.append((titulo, descripcion, fecha_registro))
            
            # Registrar el sueño en la fecha correspondiente
            if fecha_registro in sueños_por_fecha:
                sueños_por_fecha[fecha_registro] += 1
            else:
                sueños_por_fecha[fecha_registro] = 1
            
            titulo_input.value = ""
            descripcion_input.value = ""
            page.update()
    
    def mostrar_anotaciones():
        contenido.controls.clear()
        contenido.controls.append(ft.Text("Zona de Anotaciones", size=20))
        global titulo_input, descripcion_input
        titulo_input = ft.TextField(label="Título del Sueño")
        descripcion_input = ft.TextField(label="Descripción del Sueño", multiline=True, min_lines=5)
        guardar_btn = ft.Row([ft.ElevatedButton("Guardar Sueño", on_click=guardar_sueño)], alignment=ft.MainAxisAlignment.CENTER)
        contenido.controls.extend([titulo_input, descripcion_input, guardar_btn, panel])
        page.update()
    
    def crear_calendario():
        nonlocal fecha_actual
        mes = fecha_actual.month
        año = fecha_actual.year
        primer_dia = datetime.date(año, mes, 1)
        primer_dia_semana = primer_dia.weekday()
        dias_en_mes = (datetime.date(año, mes % 12 + 1, 1) - datetime.timedelta(days=1)).day
        
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        grid = ft.Column()
        grid.controls.append(ft.Row([ft.Text(d, weight=ft.FontWeight.BOLD, width=50, text_align=ft.TextAlign.CENTER) for d in dias_semana]))
        
        celdas = []
        for _ in range(primer_dia_semana):
            celdas.append(ft.Container(width=50, height=50))
        
        for dia in range(1, dias_en_mes + 1):
            fecha_str = f"{dia:02d}/{mes:02d}/{año}"
            es_hoy = fecha_hoy.year == año and fecha_hoy.month == mes and fecha_hoy.day == dia
            puntos = sueños_por_fecha.get(fecha_str, 0)
            puntos_rojos = ft.Row(
                [ft.Container(width=5, height=5, bgcolor=ft.Colors.RED, border_radius=5) for _ in range(puntos)],
                alignment=ft.MainAxisAlignment.CENTER
            )
            
            celdas.append(ft.Container(
                content=ft.Column([
                    ft.Text(str(dia), text_align=ft.TextAlign.CENTER),
                    puntos_rojos
                ], alignment=ft.MainAxisAlignment.CENTER),
                width=50,
                height=50,
                border=ft.border.all(1),
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.BLUE_100 if es_hoy else None
            ))
        
        for i in range(0, len(celdas), 7):
            grid.controls.append(ft.Row(celdas[i:i+7]))
        
        return grid
    
    def cambiar_mes(e, direccion):
        nonlocal fecha_actual
        nuevo_mes = fecha_actual.month + direccion
        nuevo_año = fecha_actual.year
        if nuevo_mes > 12:
            nuevo_mes = 1
            nuevo_año += 1
        elif nuevo_mes < 1:
            nuevo_mes = 12
            nuevo_año -= 1
        fecha_actual = datetime.date(nuevo_año, nuevo_mes, 1)
        mostrar_calendario()
    
    def mostrar_calendario():
        contenido.controls.clear()
        contenido.controls.append(
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: cambiar_mes(e, -1)),
                ft.Text(f"{fecha_actual.strftime('%B %Y')}", size=20),
                ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=lambda e: cambiar_mes(e, 1))
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        contenido.controls.append(crear_calendario())
        page.update()
    
    def cambiar_pagina(e):
        index = e.control.selected_index
        if index == 0:
            mostrar_anotaciones()
        elif index == 1:
            mostrar_calendario()
    
    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.Colors.AMBER_100,
        inactive_color=ft.Colors.GREY,
        active_color=ft.Colors.BLACK,
        on_change=cambiar_pagina,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.NOTE, label="Anotaciones"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="Calendario"),
        ]
    )
    
    page.add(ft.SafeArea(contenido))
    mostrar_anotaciones()  # Mostrar Anotaciones por defecto

ft.app(main)