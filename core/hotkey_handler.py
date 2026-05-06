import threading
import time
import keyboard
import pyperclip
import pyautogui
from config import HOTKEY, CLIPBOARD_CLEAR_DELAY, HOTKEY_DELAY

class HotKeyHandler:
    """
    Escucha el hotkey en un thread daemon.
    Solo ejecuta el pegado si la contraseña está activa.
    """

    def __init__(self, password_manager):
        self.password_manager = password_manager
        self._registered = False

    def start_listening(self) -> None:
        """Inicia el listener en un thread daemon."""
        if self._registered:
            return
        keyboard.add_hotkey(HOTKEY, self._on_hotkey_pressed, suppress=False)  # ← suppress=False
        self._registered = True

    def stop_listening(self) -> None:
        """Detiene el listener al cerrar la app."""
        if self._registered:
            keyboard.remove_hotkey(HOTKEY)
            self._registered = False

    def _on_hotkey_pressed(self) -> None:
        """Callback cuando se presiona Ctrl+Alt+P."""
        if not self.password_manager.is_active:
            return
        if self.password_manager.is_expired():
            self.password_manager.deactivate()
            return

        password = self.password_manager.contraseña_actual

        # Lanzar en thread separado para no bloquear el listener
        threading.Thread(
            target=self._paste_password,
            args=(password,),
            daemon=True
        ).start()

    def _paste_password(self, password: str) -> None:
        """Ejecuta el pegado en thread separado."""
        time.sleep(0.3)  # ← pausa mayor para que Windows cambie el foco
        pyperclip.copy(password)
        time.sleep(HOTKEY_DELAY)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(CLIPBOARD_CLEAR_DELAY)
        pyperclip.copy("")