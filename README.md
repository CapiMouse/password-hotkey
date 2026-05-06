# 🔐 Password Manager con Timer

Aplicación de escritorio en Python que permite activar una contraseña por tiempo limitado y pegarla en cualquier campo del sistema mediante un atajo de teclado.

---

## ¿Cómo funciona?

1. Escribe tu contraseña en la interfaz
2. Pulsa **Activar (1h)** — la contraseña queda lista durante 60 minutos
3. Ve a cualquier campo (navegador, aplicación, etc.) y pulsa **Ctrl + Alt + P**
4. La contraseña se pega automáticamente y el portapapeles se limpia al instante
5. Pulsa **Desactivar** cuando ya no la necesites

> 💡 La contraseña **nunca permanece en el portapapeles**. Se copia y se borra en milisegundos tras cada uso.

---

## Capturas

![Interfaz principal](assets/screenshot.png)

---

## Requisitos

- Python 3.10+
- Windows (recomendado) o Ubuntu con Xorg

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/password-manager.git
cd password-manager
```

### 2. Crear entorno virtual e instalar dependencias

**Con `uv` (recomendado):**
```bash
uv venv
uv pip install -r requirements.txt
```

**Con `pip` clásico:**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux
pip install -r requirements.txt
```

### 3. Ejecutar

```bash
# Con uv
uv run python main.py

# O directamente
python main.py
```

> ⚠️ **Windows**: Si el atajo de teclado no responde, ejecuta como **Administrador**.

> ⚠️ **Ubuntu**: Requiere sesión **Xorg** (no Wayland). En el login selecciona *"Ubuntu on Xorg"*.

---

## Uso

| Acción | Descripción |
|--------|-------------|
| Escribir contraseña | Campo de texto enmascarado |
| `Activar (1h)` | Activa el hotkey durante 1 hora |
| `Ctrl + Alt + P` | Pega la contraseña donde estés |
| `Desactivar` | Desactiva el hotkey manualmente |
| Cerrar ventana | Desactiva todo y limpia el portapapeles |

El contador de tiempo restante se actualiza en la interfaz cada 500ms.

---

## Estructura del Proyecto

```
password-manager/
├── main.py                  # Punto de entrada + GUI
├── config.py                # Constantes globales
├── core/
│   ├── __init__.py
│   ├── password_manager.py  # Lógica de estado y timer
│   └── hotkey_handler.py    # Listener de Ctrl+Alt+P
├── requirements.txt
├── CLAUDE.md                # Documentación técnica interna
└── README.md                # Este archivo
```

---

## Stack Tecnológico

| Librería | Uso |
|----------|-----|
| [PySimpleGUI](https://pysimplegui.readthedocs.io/) | Interfaz gráfica |
| [keyboard](https://github.com/boppreh/keyboard) | Hotkeys globales |
| [pyperclip](https://pyperclip.readthedocs.io/) | Portapapeles |
| [pyautogui](https://pyautogui.readthedocs.io/) | Simulación de Ctrl+V |

---

## Decisiones de Diseño

- **Sin almacenamiento persistente** — la contraseña vive solo en RAM durante la sesión
- **Sin encriptación** — aplicación de uso puntual en entorno de confianza
- **Portapapeles limpio** — se borra automáticamente tras cada pegado
- **Hotkey condicional** — solo funciona cuando está explícitamente activado

---

## Generar Ejecutable `.exe` (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PasswordManager" main.py
```

El ejecutable quedará en la carpeta `dist/`.

---

## Limitaciones conocidas

- No funciona en Ubuntu con **Wayland** (usar Xorg)
- En Windows puede requerir permisos de **Administrador**
- El historial extendido del portapapeles de Windows (`Win + V`) puede retener entradas previas

---

## Licencia

MIT — libre para uso personal y modificación.