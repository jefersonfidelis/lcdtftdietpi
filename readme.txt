1. Habilitar SPI no DietPi

Antes de tudo, certifique-se de que o SPI est� ativado no DietPi:
dietpi-config

V� para "Interfacing Options" > "SPI" e ative.
Reinicie o Raspberry Pi:

sudo reboot

Verifique se o SPI est� ativo com:
ls /dev/spidev*

Se retornar algo como /dev/spidev0.0 e /dev/spidev0.1, ent�o o SPI est� funcionando.

2. Instalar as bibliotecas necess�rias
Atualize os pacotes e instale as depend�ncias:

sudo apt update
sudo apt install python3-pip python3-dev libopenjp2-7 libtiff5 -y

Instale as bibliotecas Python:
pip3 install luma.lcd spidev pillow

