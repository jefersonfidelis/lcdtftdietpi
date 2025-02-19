import spidev
import RPi.GPIO as GPIO
import evdev
import time
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from PIL import Image, ImageDraw, ImageFont

# === CONFIG DA TELA ILI9341 ===
serial = spi(port=0, device=0, gpio_DC=22, gpio_RST=27)
device = ili9341(serial, width=320, height=240)

# === CONFIG DOS BOTOES ===
KEY1 = 6  # Cima
KEY2 = 19  # Baixo
KEY3 = 26  # Selecionar
TOUCH_IRQ = 17  # Interrupcao do touchscreen (caso aplicavel)

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# === CONFIG SPI PARA TOUCHSCREEN (XPT2046) ===
spi_touch = spidev.SpiDev()
spi_touch.open(0, 1)  # Bus 0, Device 1 (CS1 para touchscreen)
spi_touch.max_speed_hz = 1000000

# === TENTAR DETECTAR TOUCHSCREEN VIA EVDEV ===
touch_device = None
#devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
#for device in devices:
#    if "touchscreen" in device.name.lower():
#        touch_device = evdev.InputDevice(device.path)
#        print(f"Touchscreen encontrado em: {device.path}")
#        break

# === CONFIGURAÇÃO DO MENU ===
menu_options = ["Cadastro", "Config", "Acesso", "Sair"]
selected_index = 0
font = ImageFont.load_default()

# === FUNC PARA DESENHAR O MENU ===
def draw_menu():
    #img = Image.new("RGB", (320, 240), "black")
    img = Image.new("RGB", (device.width, device.height), "black")
    draw = ImageDraw.Draw(img)

    for i, option in enumerate(menu_options):
        y = 50 + i * 40
        color = "white" if i == selected_index else "gray"
        draw.text((60, y), option, font=font, fill=color)

    device.display(img)

# === FUNÇÃO PARA LER O TOUCHSCREEN (XPT2046) ===
def read_touch():
    def read_channel(channel):
        cmd = (0b1001 << 4) | (channel << 4)
        resp = spi_touch.xfer2([cmd, 0x00, 0x00])
        return ((resp[1] << 8) | resp[2]) >> 3

    x = read_channel(1)
    y = read_channel(5)
    return x, y

# === FUNÇÃO PARA LER OS BOTÕES ===
def check_buttons():
    global selected_index

    if GPIO.input(KEY1) == 0:  # Cima
        selected_index = (selected_index - 1) % len(menu_options)
        draw_menu()
        time.sleep(0.3)

    if GPIO.input(KEY2) == 0:  # Baixo
        selected_index = (selected_index + 1) % len(menu_options)
        draw_menu()
        time.sleep(0.3)

    if GPIO.input(KEY3) == 0:  # Selecionar
        execute_option(menu_options[selected_index])
        time.sleep(0.3)

# === FUNÇÃO PARA LER O TOUCHSCREEN E DETECTAR CLIQUES ===
def check_touchscreen():
    global selected_index

    if GPIO.input(TOUCH_IRQ) == 0:  # Se toque detectado
        x, y = read_touch()
        print(f"Toque detectado em X={x}, Y={y}")

        if 2879 <= y < 3280:
            selected_index = 0
        elif  2397 <= y < 2580:
            selected_index = 1
        elif 1200 <= y < 2200:
            selected_index = 2
        elif 500 <= y < 1100:
            selected_index = 3

        draw_menu()
        time.sleep(0.3)  # Debounce

# === FUNÇÃO PARA EXECUTAR A OPÇÃO SELECIONADA ===
def execute_option(option):
    print(f"Executando: {option}")
    if option == "Sair":
        print("Saindo do menu...")
        GPIO.cleanup()
        device.clear()
        exit()

# === LOOP PRINCIPAL ===
draw_menu()
print("Menu iniciado! Use o touchscreen ou os botoes.")

try:
    while True:
        check_buttons()
        check_touchscreen()
except KeyboardInterrupt:
    print("\nSaindo...")
    spi_touch.close()
    GPIO.cleanup()
