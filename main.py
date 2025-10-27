import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    txt_marca = ft.TextField(value="Marca")
    txt_modello = ft.TextField(value="Modello")
    txt_anno = ft.TextField(value="Anno")
    num_posti = ft.TextField(value=0)
    def handlerPlus(e):
        currentVal = int(num_posti.value)
        currentVal = currentVal + 1
        num_posti.value = currentVal
        num_posti.update()

    def handlerMinus(e):
        currentVal = int(num_posti.value)
        if currentVal > 0:
            currentVal = currentVal - 1
            num_posti.value = currentVal
            num_posti.update()


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def conferma_auto(e):
        try:
            autonoleggio.aggiungi_automobile(txt_marca.value, txt_modello.value, txt_anno.value, num_posti.value)
            aggiorna_lista_auto()
            txt_marca.value = "marca"
            txt_modello.value = "modello"
            txt_anno.value = "anno"
            num_posti.value = 0
            page.update()
        except:
            alert.show_alert("❌ Errore: inserisci i valori numerici validi per anno e posti")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btnPlus = ft.IconButton(icon=ft.Icons.ADD_CIRCLE_ROUNDED, icon_size=24, on_click=handlerPlus)
    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_ROUNDED, icon_size=24, on_click=handlerMinus)
    pulsante_conferma_auto = ft.ElevatedButton("Conferma l'auto", on_click=conferma_auto)
    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi automobile", size=20),
        ft.Row([txt_marca, txt_modello, txt_anno, num_posti, btnPlus, btnMinus], alignment=ft.MainAxisAlignment.CENTER), pulsante_conferma_auto,
        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
