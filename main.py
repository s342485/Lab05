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
    page.scroll = ft.ScrollMode.AUTO

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

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)
    lista_noleggi = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # TextField per aggiungere una nuova automobile
    input_marca = ft.TextField(label="Marca")
    input_modello = ft.TextField(label="Modello")
    input_anno = ft.TextField(label="Anno", keyboard_type=ft.KeyboardType.NUMBER)

    #Texfield per il noleggio
    input_data = ft.TextField(label="Data (es.27/10/2025)", keyboard_type=ft.KeyboardType.NUMBER)
    input_id_auto = ft.TextField(label="ID Auto", keyboard_type=ft.KeyboardType.NUMBER)
    input_cognome = ft.TextField(label="Cognome cliente")
    input_id_noleggio = ft.TextField(label="ID Noleggio", keyboard_type=ft.KeyboardType.NUMBER)

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

    def aggiorna_lista_noleggio():
        lista_noleggi.controls.clear()
        for noleggio in autonoleggio.noleggi:
            stato = "✅"
            lista_noleggi.controls.append(ft.Text(f"{stato} {noleggio}"))
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

    def aggiungi_noleggio(e):
        data = input_data.value.strip()
        id_automobile = input_id_auto.value.strip()
        cognome = input_cognome.value.strip()

        if not data or not id_automobile or not cognome:
            alert.show_alert("⚠️ Compila tutti i campi per registrare un noleggio.")
            return

        if not id_automobile.startswith("A"):
            alert.show_alert("❌ Il codice auto deve iniziare con 'A'.")
            return

        try:
            noleggio = autonoleggio.nuovo_noleggio(data, id_automobile, cognome)
            alert.show_alert(f"✅ Noleggio creato correttamente. "
                             f"Codice: {noleggio.codice} | Auto noleggiato dal signor/a {noleggio.cognome_cliente} in data {noleggio.data}")
            aggiorna_lista_auto()
            aggiorna_lista_noleggio()

            input_data.value = ""
            input_id_auto.value = ""
            input_cognome.value = ""
            page.update()

        except Exception as ex:
            alert.show_alert(f"❌ Errore: {ex}")


    def termina_noleggio(e):
        id_noleggio = input_id_noleggio.value.strip()

        if not id_noleggio:
            alert.show_alert("⚠️ Inserisci un ID noleggio.")
            return
        try:
            autonoleggio.termina_noleggio(id_noleggio)
            alert.show_alert(f"✅ Noleggio {id_noleggio} terminato correttamente.")
            #Pulisco il Textfield
            input_id_noleggio.value = ""
            aggiorna_lista_noleggio()
            #aggiorna l'auto in modo che tolga la x
            aggiorna_lista_auto()

            #aggiorna la pagina
            page.update()
        except Exception as ex:
            alert.show_alert(f"❌ Errore: {ex}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)
    pulsante_aggiungi_auto = ft.ElevatedButton("Aggiungi Auto", on_click=aggiungi_auto)
    pulsante_aggiungi_noleggio = ft.ElevatedButton("Aggiungi Noleggio", on_click=aggiungi_noleggio )
    pulsante_termina_noleggio = ft.ElevatedButton("Termina Noleggio", on_click=termina_noleggio)

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

        #Sezione 4
        ft.Divider(),
        ft.Text("Noleggio Automobile", size=20),
        ft.Row(spacing=50, controls=[input_data, input_id_auto, input_cognome]),
        ft.Row(spacing=150, controls=[pulsante_aggiungi_noleggio], alignment=ft.MainAxisAlignment.CENTER),

        #sezione 5
        ft.Divider(),
        ft.Text("Termine Noleggio", size=20),
        ft.Row(spacing=50, controls=[input_id_noleggio,pulsante_termina_noleggio], alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 6
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,

        #sezione 7
        ft.Divider(),
        ft.Text("Noleggi", size=20),
        lista_noleggi

    )
    aggiorna_lista_auto()

ft.app(target=main)
