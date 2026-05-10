import pyperclip
import PySimpleGUI as sg
from core.password_manager import PasswordManager
from core.hotkey_handler import HotKeyHandler
from config import GUI_THEME, UI_REFRESH_MS, HOTKEY

DURACIONES = {
    "15 minutos": 900,
    "30 minutos": 1800,
    "1 hora":     3600,
    "4 horas":    14400,
}

def build_window(timer_max):
    sg.theme(GUI_THEME)
    layout = [
        [sg.Text("Password Manager", font=("Helvetica", 16, "bold"))],

        # Campo contraseña + ojo
        [
            sg.Text("Contraseña:"),
            sg.Input(key="-PWD-", password_char="●", size=(20, 1), disabled_readonly_background_color="#555555",
                     disabled_readonly_text_color="#aaaaaa"),
            sg.Button("👁", key="-TOGGLE-PWD-", tooltip="Mostrar/ocultar contraseña"),
        ],

        # Duración + botones
        [
            sg.Combo(
                list(DURACIONES.keys()),
                default_value="1 hora",
                key="-DURATION-",
                readonly=True,
                size=(12, 1)
            ),
            sg.Button("Activar", key="-ACTIVATE-"),
            sg.Button("Desactivar", key="-DEACTIVATE-"),
        ],

        # Estado
        [sg.Text("Estado: INACTIVA", key="-STATUS-", size=(40, 1))],

        # Barra de progreso
        [sg.ProgressBar(
            timer_max,
            orientation="h",
            size=(38, 16),
            key="-PROGRESS-",
            bar_color=("green", "gray")
        )],

        # Atajo
        [sg.Text(f"Atajo: {HOTKEY.upper()}", text_color="gray")],
    ]
    return sg.Window("Password Manager", layout, finalize=True)


def get_bar_color(remaining, total):
    """Cambia color según tiempo restante."""
    ratio = remaining / total if total > 0 else 0
    if ratio > 0.5:
        return ("green", "gray")
    elif ratio > 0.15:
        return ("orange", "gray")
    else:
        return ("red", "gray")


def main():
    pm = PasswordManager()
    handler = HotKeyHandler(pm)
    handler.start_listening()

    timer_max = DURACIONES["1 hora"]
    show_password = False
    window = build_window(timer_max)

    while True:
        event, values = window.read(timeout=UI_REFRESH_MS)

        if event == sg.WIN_CLOSED:
            break

        # --- Mostrar/ocultar contraseña ---
        if event == "-TOGGLE-PWD-":
            show_password = not show_password
            char = "" if show_password else "●"
            window["-PWD-"].update(password_char=char)

        # --- Activar ---
        if event == "-ACTIVATE-":
            duracion_texto = values["-DURATION-"]
            segundos = DURACIONES.get(duracion_texto, 3600)
            pm.timer_duration = segundos

            if pm.activate(values["-PWD-"]):
                timer_max = segundos
                # Reconstruir barra con nuevo máximo
                window["-PROGRESS-"].update(segundos, max=segundos)
                # Bloquear campo y desplegable
                window["-PWD-"].update(disabled=True)
                window["-DURATION-"].update(disabled=True)
                window["-PWD-"].update("")

        # --- Desactivar ---
        if event == "-DEACTIVATE-":
            pm.deactivate()
            window["-PWD-"].update(disabled=False)
            window["-DURATION-"].update(disabled=False)
            window["-PROGRESS-"].update(0)

        # --- Auto-desactivación al expirar ---
        just_expired = pm.check_and_auto_deactivate()
        if just_expired:
            window["-PWD-"].update(disabled=False)
            window["-DURATION-"].update(disabled=False)
            window["-PROGRESS-"].update(0)
            sg.popup(
                "⏰ Sesión expirada",
                "La contraseña ha sido desactivada automáticamente.",
                title="Password Manager",
                keep_on_top=True,
            )

        # --- Actualizar UI ---
        if pm.is_active:
            remaining = pm.get_remaining_time()
            mins, secs = divmod(remaining, 60)
            window["-STATUS-"].update(f"Estado: ACTIVA ({mins}m {secs}s)")
            window["-PROGRESS-"].update(
                remaining,
                bar_color=get_bar_color(remaining, timer_max)
            )
        else:
            window["-STATUS-"].update("Estado: INACTIVA")

    handler.stop_listening()
    pyperclip.copy("")
    window.close()


if __name__ == "__main__":
    main()