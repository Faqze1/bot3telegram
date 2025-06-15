from telethon.sync import TelegramClient
import json
import time
from datetime import datetime

# Tus datos de API de Telegram
api_id = 29426993
api_hash = 'a6fed145dabf6edf2b0bbbd907d5ba3e'

# ID del grupo o canal donde quieres enviar los mensajes
destino = -1002638091435

# Ruta al archivo mensajes.json (debe estar en la misma carpeta que este script)
ruta_mensajes = 'mensajes.json'

def cargar_mensajes():
    try:
        with open(ruta_mensajes, 'r', encoding='utf-8') as f:
            mensajes = json.load(f)
        mensajes.sort(key=lambda x: x['hora'])
        return mensajes
    except Exception as e:
        print(f"❌ Error cargando mensajes desde {ruta_mensajes}: {e}")
        return []

def main():
    mensajes = cargar_mensajes()
    if not mensajes:
        print("❌ No hay mensajes para enviar. Saliendo.")
        return

    print("📅 Mensajes programados:")
    for msg in mensajes:
        print(f"- {msg['hora']}: {msg['texto']}")
    print("\n⏳ Esperando para enviar mensajes...\n")

    with TelegramClient('sesion_telegram', api_id, api_hash) as client:
        for msg in mensajes:
            hora_objetivo = datetime.strptime(msg['hora'], "%H:%M").replace(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day
            )

            if hora_objetivo < datetime.now():
                print(f"⏭️ Saltando mensaje ya pasado: {msg['hora']} - {msg['texto']}")
                continue

            espera = (hora_objetivo - datetime.now()).total_seconds()
            print(f"⏰ Esperando hasta las {msg['hora']} para enviar: \"{msg['texto']}\"")
            time.sleep(espera)

            try:
                client.send_message(destino, msg['texto'])
                print(f"✅ Enviado a las {msg['hora']}: {msg['texto']}")
            except Exception as e:
                print(f"❌ Error enviando mensaje a las {msg['hora']}: {e}")

if __name__ == "__main__":
    main()
