import evdev

# Substitua 'eventX' pelo dispositivo correto identificado antes
device_path = "/dev/input/event0"

try:
    device = evdev.InputDevice(device_path)
    print(f"Escutando eventos de: {device.name}")

    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            abs_event = evdev.categorize(event)
            print(f"Eixo: {abs_event.event.code}, Valor: {abs_event.event.value}")

except FileNotFoundError:
    print("Dispositivo de touchscreen nao encontrado!")
