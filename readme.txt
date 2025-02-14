1. Habilitar SPI no DietPi

Antes de tudo, certifique-se de que o SPI está ativado no DietPi:
dietpi-config

Vá para "Interfacing Options" > "SPI" e ative.
Reinicie o Raspberry Pi:

sudo reboot

Verifique se o SPI está ativo com:
ls /dev/spidev*

Se retornar algo como /dev/spidev0.0 e /dev/spidev0.1, então o SPI está funcionando.

2. Instalar as bibliotecas necessárias
Atualize os pacotes e instale as dependências:

sudo apt update
sudo apt install python3-pip python3-dev libopenjp2-7 libtiff5 -y

Instale as bibliotecas Python:
pip3 install luma.lcd spidev pillow

