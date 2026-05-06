import pyperclip
import PySimpleGUI as sg
from core.password_manager import PasswordManager
from core.hotkey_handler import HotKeyHandler
from config import GUI_THEME, UI_REFRESH_MS, HOTKEY

def build_window():
    sg.theme(GUI_THEME)
    layout = [
        [sg.Text("Password Manager", font=("Helvetica", 16, "bold"))],
        [sg.Text("Contraseña:"), sg.Input(key="-PWD-", password_char="●")],
        [sg.Button("Activar (1h)", key="-ACTIVATE-"),
         sg.Button("Desactivar", key="-DEACTIVATE-")],
        [sg.Text("Estado: INACTIVA", key="-STATUS-", size=(40, 1))],
        [sg.Text(f"Atajo: {HOTKEY.upper()}", text_color="gray")],
    ]
    return sg.Window("Password Manager", layout, finalize=True)

def main():
    pm = PasswordManager()
    handler = HotKeyHandler(pm)
    handler.start_listening()

    window = build_window()

    while True:
        event, values = window.read(timeout=UI_REFRESH_MS)

        if event == sg.WIN_CLOSED:
            break

        if event == "-ACTIVATE-":
            if pm.activate(values["-PWD-"]):
                window["-PWD-"].update("")  # Limpia el campo

        if event == "-DEACTIVATE-":
            pm.deactivate()

        # Auto-desactivación al expirar
        pm.check_and_auto_deactivate()

        # Actualizar estado en la UI
        if pm.is_active:
            remaining = pm.get_remaining_time()
            mins, secs = divmod(remaining, 60)
            window["-STATUS-"].update(f"Estado: ACTIVA ({mins}m {secs}s)")
        else:
            window["-STATUS-"].update("Estado: INACTIVA")

    handler.stop_listening()
    pyperclip.copy("")  # Limpia el portapapeles al cerrar
    window.close()

if __name__ == "__main__":
    main()