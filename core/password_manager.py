import time
from config import TIMER_DURATION

class PasswordManager:
    """
    Gestiona el estado de la contraseña activa.
    No tiene conocimiento de la GUI ni del hotkey.
    """

    def __init__(self):
        self.contraseña_actual: str = ""
        self.is_active: bool = False
        self.expiry_time: float | None = None
        self.timer_duration: int = TIMER_DURATION  # ← añadido

    def activate(self, password: str) -> bool:
        """Activa la contraseña por timer_duration segundos."""
        if not password:
            return False
        self.contraseña_actual = password
        self.is_active = True
        self.expiry_time = time.time() + self.timer_duration
        return True

    def deactivate(self) -> None:
        """Desactiva manualmente y limpia el estado."""
        self.is_active = False
        self.contraseña_actual = ""
        self.expiry_time = None

    def is_expired(self) -> bool:
        """True si el timer ha expirado."""
        if self.expiry_time is None:
            return True
        return time.time() > self.expiry_time

    def get_remaining_time(self) -> int:
        """Segundos restantes (0 si inactiva o expirada)."""
        if not self.is_active or self.is_expired():
            return 0
        return int(self.expiry_time - time.time())

    def check_and_auto_deactivate(self) -> bool:
        """
        Verifica si expiró. Si es así, desactiva automáticamente.
        Retorna True si se acaba de desactivar.
        """
        if self.is_active and self.is_expired():
            self.deactivate()
            return True
        return False