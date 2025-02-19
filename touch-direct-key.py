import spidev
import RPi.GPIO as GPIO
import time
import evdev

# === Configuração dos GPIOs ===
KEY1 = 6
KEY2 = 19
KEY3 = 26
TOUCH_IRQ = 17  # Pino de interrupção do touchscreen (se aplicável)

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# === Configuração do SPI para touchscreen XPT2046 ===
spi = spidev.SpiDev()
spi.open(0, 1)  # Bus 0, Device 1 (CS1 para touchscreen)
spi.max_speed_hz = 1000000  # Velocidade SPI

# === Descobrir dispositivo touchscreen (evdev) ===
touch_device = None
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if "touchscreen" in device.name.lower():
        touch_device = evdev.InputDevice(device.path)
        print(f"Touchscreen encontrado em: {device.path}")
        break

# === Função para ler os botões físicos ===
def check_buttons():
    if GPIO.input(KEY1) == 0:
        print("KEY1 pressionado!")
        time.sleep(0.3)
    if GPIO.input(KEY2) == 0:
        print("KEY2 pressionado!")
        time.sleep(0.3)
    if GPIO.input(KEY3) == 0:
        print("KEY3 pressionado!")
        time.sleep(0.3)

# === Função para ler o toque via SPI (XPT2046) ===
def read_touch():
    def read_channel(channel):
        cmd = (0b1001 << 4) | (channel << 4)
        resp = spi.xfer2([cmd, 0x00, 0x00])
        return ((resp[1] << 8) | resp[2]) >> 3

    x = read_channel(1)
    y = read_channel(5)
    print(f"Toque detectado: X={x}, Y={y}")

# === Loop principal ===
print("Aguardando interação...")

try:
    while True:
        # Verifica os botões
        check_buttons()

        # Verifica o toque SPI
        if GPIO.input(TOUCH_IRQ) == 0:  # Quando TOQUE detectado
            read_touch()

        # Verifica o toque via evdev (caso esteja disponível)
        if touch_device:
            for event in touch_device.read_loop():
                if event.type == evdev.ecodes.EV_ABS:
                    abs_event = evdev.categorize(event)
                    print(f"Touchscreen: Tipo={abs_event.event.type}, Código={abs_event.event.code}, Valor={abs_event.event.value}")

except KeyboardInterrupt:
    print("\nSaindo...")
    spi.close()
    GPIO.cleanup()
