🌐 **Inglés** | [English](README.md)

# 🔐 Password Manager con Timer

Aplicación de escritorio en Python que permite activar una contraseña por tiempo limitado y pegarla en cualquier campo del sistema mediante un atajo de teclado.

---

## ¿Cómo funciona?

1. Escribe tu contraseña en la interfaz
2. Elige la duración: **15min, 30min, 1h o 4h**
3. Pulsa **Activar** — el campo se bloquea y el hotkey queda activo
4. Ve a cualquier campo (navegador, aplicación, etc.) y pulsa **Ctrl + Alt + P**
5. La contraseña se escribe automáticamente **sin pasar por el portapapeles**
6. Pulsa **Desactivar** cuando ya no la necesites

> 💡 La contraseña **nunca toca el portapapeles**. Se escribe carácter a carácter directamente en el campo destino, por lo que no aparece en el historial de `Win + V`.

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
git clone https://github.com/CapiMouse/password-hotkey.git
cd password-hotkey
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
| Escribir contraseña | Campo de texto enmascarado (👁 para mostrar/ocultar) |
| Elegir duración | Desplegable: 15min, 30min, 1h, 4h |
| `Activar` | Activa el hotkey y bloquea el campo |
| `Ctrl + Alt + P` | Escribe la contraseña en el campo activo |
| `Desactivar` | Desactiva el hotkey manualmente |
| Cerrar ventana | Desactiva todo automáticamente |

El contador de tiempo restante y la barra de progreso se actualizan cada 500ms. Al expirar el timer aparece un popup de aviso.

---

## Funcionalidades

- ⏱ **Timer configurable**: 15min, 30min, 1h o 4h
- 👁 **Mostrar/ocultar contraseña**: botón para revelar temporalmente
- 🔒 **Campo bloqueado**: mientras está activa no se puede modificar la contraseña
- 📊 **Barra de progreso**: indicador visual con colores (verde → naranja → rojo)
- ⏰ **Popup al expirar**: notificación automática cuando la sesión termina
- 🔐 **Sin portapapeles**: la contraseña se escribe directamente, nunca aparece en `Win + V`

---

## Estructura del Proyecto

```
password-hotkey/
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
Este repositorio incluye un archivo CLAUDE.md con orientación técnica para desarrolladores que usen Claude Code para contribuir o extender el proyecto.

---

## Stack Tecnológico

| Librería | Uso |
|----------|-----|
| [PySimpleGUI](https://pysimplegui.readthedocs.io/) | Interfaz gráfica |
| [keyboard](https://github.com/boppreh/keyboard) | Hotkeys globales + escritura directa |

---

## Decisiones de Diseño

- **Sin almacenamiento persistente** — la contraseña vive solo en RAM durante la sesión
- **Sin encriptación** — aplicación de uso puntual en entorno de confianza
- **Sin portapapeles** — `keyboard.write()` escribe directamente, evitando `Win + V`
- **Hotkey condicional** — solo funciona cuando está explícitamente activado
- **Campo bloqueado al activar** — evita modificaciones accidentales durante la sesión

---

## Generar Ejecutable `.exe` (Windows)

```bash
uv add pyinstaller --dev
pyinstaller --onefile --windowed --name "password-hotkey" main.py
```

El ejecutable quedará en la carpeta `dist/`.

---

## Limitaciones conocidas

- No funciona en Ubuntu con **Wayland** (usar Xorg)
- En Windows puede requerir permisos de **Administrador**
- `keyboard.write()` puede fallar con algunos caracteres Unicode poco comunes según la configuración del teclado del sistema

---

## Licencia

MIT — libre para uso personal y modificación.