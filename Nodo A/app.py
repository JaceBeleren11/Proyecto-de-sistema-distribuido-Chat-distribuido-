from flask import Flask, request, jsonify
from datetime import datetime
import os
import uuid
import requests

app = Flask(__name__)

# Nombre de este nodo
NODE_NAME = os.environ.get("NODE_NAME", "Nodo A")

# Lista de vecinos (otros nodos), separados por coma en la variable de entorno
# Ejemplo: NEIGHBORS="http://localhost:5002,http://localhost:5003"
NEIGHBORS = [n for n in os.environ.get("NEIGHBORS", "").split(",") if n]

# "Base de datos" en memoria: lista de mensajes
messages = []


def replicate_to_neighbors(message):
    """Envía el mensaje a cada nodo vecino. Si un vecino está caído, lo ignora
    y sigue con los demás (esto es la tolerancia a fallos)."""
    for neighbor in NEIGHBORS:
        try:
            requests.post(f"{neighbor}/replicate", json=message, timeout=2)
        except requests.exceptions.RequestException as e:
            print(f"[{NODE_NAME}] No se pudo replicar a {neighbor}: {e}")


@app.route("/health", methods=["GET"])
def health():
    """Endpoint simple para saber si el nodo está vivo."""
    return jsonify({"status": "ok", "node": NODE_NAME}), 200


@app.route("/messages", methods=["POST"])
def post_message():
    """Recibe un mensaje nuevo del cliente y lo guarda."""
    data = request.get_json(silent=True)

    if not data or "user" not in data or "text" not in data:
        return jsonify({"error": "Se requiere 'user' y 'text' en el body"}), 400

    message = {
        "id": str(uuid.uuid4()),
        "user": data["user"],
        "text": data["text"],
        "timestamp": datetime.utcnow().isoformat(),
        "origin_node": NODE_NAME,
    }

    messages.append(message)
    print(f"[{NODE_NAME}] Mensaje guardado: {message}")

    # Replicar el mensaje a los demás nodos
    replicate_to_neighbors(message)

    return jsonify(message), 201


@app.route("/replicate", methods=["POST"])
def replicate_message():
    """Recibe un mensaje ya creado por otro nodo y lo guarda, sin volver
    a replicarlo (evita el bucle infinito entre nodos)."""
    message = request.get_json(silent=True)

    if not message or "id" not in message:
        return jsonify({"error": "Mensaje inválido"}), 400

    # Evitar duplicados si el mensaje ya llegó antes
    if not any(m["id"] == message["id"] for m in messages):
        messages.append(message)
        print(f"[{NODE_NAME}] Mensaje replicado recibido: {message}")

    return jsonify({"status": "replicated"}), 200


@app.route("/messages", methods=["GET"])
def get_messages():
    """Devuelve todos los mensajes guardados en este nodo."""
    return jsonify({"node": NODE_NAME, "messages": messages}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
