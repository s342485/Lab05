import flet as ft
from flet.core import page
from alert import AlertManager
from automobile import Automobile
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
    input_marca = ft.TextField(label="Marca")
    input_modello = ft.TextField(label="Modello")
    input_anno = ft.TextField(label="Anno", keyboard_type=ft.KeyboardType.NUMBER)

    # Campo per il CONTATORE (solo visualizzazione)
    txt_number = ft.TextField(
        value="0",
        text_align=ft.TextAlign.CENTER,
        width=60,
        read_only=True  #con read_only=True → il testo può essere letto ma non scritto a mano dall’utente;
                        #con read_only=False (comportamento predefinito) → l’utente può cliccare dentro la casella e scrivere qualsiasi valore
    )
    # Handler per incrementare e decrementare
    def minus_click(e):
        if txt_number.value > 0:
            txt_number.value = int(txt_number.value) - 1
            page.update()
        else:
            txt_number.value=0

    def plus_click(e):
        txt_number.value = int(txt_number.value) + 1
        page.update()

    # Riga con pulsanti - e +
    contatore_posti = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.REMOVE, on_click=minus_click, icon_color="red"), #on click vuol dire quando schiaccio il click
            txt_number,
            ft.IconButton(icon=ft.Icons.ADD, on_click=plus_click, icon_color="green"),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

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
    def aggiungi_auto(e):
        marca = input_marca.value
        modello = input_modello.value
        anno = input_anno.value
        num_posti = int(txt_number.value)

        if not marca or not modello or not anno or not num_posti:
            alert.show_alert("⚠️ Compila tutti i campi prima di aggiungere l'auto.")
            return

        # Controlla che anno e numero posti siano numeri validi
        if not anno.isdigit() or num_posti == 0:
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e posti")
            return
        try:
            #aggiungo l'automobile alla lista fisica e poi aggiorno l'interfaccia
            autonoleggio.aggiungi_automobile(marca, modello, anno, num_posti)
            aggiorna_lista_auto()

            # Pulisco i campi dopo l'inserimento
            input_marca.value = ""
            input_modello.value = ""
            input_anno.value = ""
            txt_number.value = "0"
            page.update()
        except Exception as e:
            alert.show_alert(f"Errore verificatosi nell'aggiunta dell'automobile. Errore {e}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)
    # Bottoni per la gestione de l'inserimento di una nuova auto
    pulsante_aggiungi_auto = ft.ElevatedButton("Aggiungi Auto", on_click=aggiungi_auto)

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
        ft.Divider(),

        # Sezione 3
        ft.Text("Aggiungi Nuova Automobile", size=20),
        ft.Row(spacing=50, controls=[input_marca, input_modello, input_anno, contatore_posti]),
        ft.Row(spacing=150, controls=[pulsante_aggiungi_auto], alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
