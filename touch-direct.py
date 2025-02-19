import spidev
import RPi.GPIO as GPIO

# Configuração do SPI
spi = spidev.SpiDev()
spi.open(0, 1)  # (bus 0, device 1 - geralmente touchscreen usa CS1)
spi.max_speed_hz = 1000000  # Velocidade SPI

# Configuração do pino de interrupção (caso necessário)
GPIO.setmode(GPIO.BCM)
TOUCH_IRQ = 17
GPIO.setup(TOUCH_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Função para ler coordenadas X e Y do XPT2046
def read_touch():
    def read_channel(channel):
        cmd = (0b1001 << 4) | (channel << 4)
        resp = spi.xfer2([cmd, 0x00, 0x00])
        return ((resp[1] << 8) | resp[2]) >> 3

    x = read_channel(1)
    y = read_channel(5)
    print(f"Toque detectado: X={x}, Y={y}")

# Loop de leitura
try:
    while True:
        if GPIO.input(TOUCH_IRQ) == 0:  # Toque detectado
            read_touch()
except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
