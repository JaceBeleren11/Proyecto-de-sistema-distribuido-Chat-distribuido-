from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Nombre de este nodo (útil ya en la sesión 3 cuando haya varios)
NODE_NAME = os.environ.get("NODE_NAME", "Nodo A")

# "Base de datos" en memoria: lista de mensajes
messages = []


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
        "id": len(messages) + 1,
        "user": data["user"],
        "text": data["text"],
        "timestamp": datetime.utcnow().isoformat(),
        "node": NODE_NAME,
    }

    messages.append(message)
    print(f"[{NODE_NAME}] Mensaje guardado: {message}")

    return jsonify(message), 201


@app.route("/messages", methods=["GET"])
def get_messages():
    """Devuelve todos los mensajes guardados en este nodo."""
    return jsonify({"node": NODE_NAME, "messages": messages}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
