from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from PIL import Image, ImageDraw, ImageFont

# Inicializa SPI com o chip select 0 (CS0)
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)

# Configura o display
device = ili9341(serial, width=240, height=320, rotate=180)  # Ajuste conforme necessário

# Criando um canvas para desenhar
img = Image.new("RGB", (device.width, device.height), "black")
draw = ImageDraw.Draw(img)

# Escrevendo no display
font = ImageFont.load_default()
draw.text((50, 100), "Hello, DietPi!", font=font, fill="white")

# Envia a imagem para o display
device.display(img)

