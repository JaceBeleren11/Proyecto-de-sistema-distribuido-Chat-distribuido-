# Proyecto-de-sistema-distribuido-Chat-distribuido-
# NodeMesh — Chat distribuido

Proyecto integrador de Sistemas Distribuidos: un chat construido sobre varios nodos independientes que se reparten la carga, replican mensajes entre sí y siguen funcionando aunque uno de ellos falle.

## Equipo
- Luis Guillermo Mejenes Chacon — Nodo A
- Jorge Enrique Soberanes Espinosa — Nodo B
- Angelo Mendoza Garcia — Nodo C
- Diego Alonso Lopez Ballesta — Nodo D
- Diego Angel Vazquez Contreras — Nodo E

## Stack tecnológico
- Python 3
- Flask
- Docker (para levantar los nodos como contenedores aislados)
- GitHub (control de versiones y entrega)
- Postman (pruebas de endpoints)
- ngrok (exponer un nodo a internet para pruebas de distribución geográfica real)
- LucidChart (diagrama de arquitectura)

## Sesión 1 — Diseño y arranque

### Preguntas de diseño

**¿Cuántos nodos tendrá el sistema?**
5 nodos, uno por cada integrante del equipo. Cada nodo es una instancia independiente del mismo servidor Flask, corriendo en su propio puerto (5001 a 5005) o contenedor Docker.

**¿Cómo se van a comunicar?**
Por HTTP/REST. Cuando un nodo recibe un mensaje nuevo de un cliente, lo replica hacia los otros 4 nodos mediante peticiones POST. El cliente puede conectarse a cualquiera de los 5 nodos indistintamente (transparencia de acceso).

**¿Qué pasa si uno falla?**
Los otros 4 nodos siguen funcionando con normalidad. Si la replicación hacia un nodo caído falla (timeout o connection error), esa excepción se captura y se ignora sin detener al nodo que envía el mensaje. Al volver a levantarse, el nodo caído puede solicitar el historial de mensajes a sus compañeros para ponerse al día.

### Diagrama de arquitectura

<img width="2114" height="1409" alt="Nodos de Diagrama Secuencial" src="https://github.com/user-attachments/assets/c95ff2ad-a442-4a7c-9fbd-d380dc5074f7" />

- El **cliente** puede conectarse a cualquiera de los 5 nodos.
- Cada **nodo** corre en su propio puerto (5001–5005) o contenedor.
- Los nodos **replican los mensajes entre sí** para mantener la misma información.
- Si un nodo se apaga, el sistema **sigue funcionando** con los nodos restantes.

### Configuración de entorno

<img width="1483" height="762" alt="Captura de pantalla 2026-09-10 183323" src="https://github.com/user-attachments/assets/ec973602-14c2-4b3c-b0e1-276670913526" />

## Cómo correr el proyecto
## Endpoints

| Método | Ruta         | Descripción                                              |
|--------|-------------|-----------------------------------------------------------|
| GET    | `/health`    | Verifica que el nodo está vivo                            |
| POST   | `/messages`  | Recibe un mensaje nuevo del cliente y lo replica al resto |
| GET    | `/messages`  | Devuelve todos los mensajes guardados en este nodo        |
| POST   | `/replicate` | Recibe un mensaje ya creado por otro nodo (uso interno)   |
| GET    | `/sync`      | Recupera el historial de los vecinos tras una caída       |

## Cómo correr un nodo

1. Instalar dependencias:
```bash
   cd "Nodo A"          # o Nodo B, C, D, E según corresponda
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
```

2. Correr el nodo indicando su nombre, puerto y la lista de vecinos (URLs de los otros 4 nodos):
```bash
   NODE_NAME="Nodo A" PORT=5001 NEIGHBORS="https://url-nodo-b.ngrok-free.app,https://url-nodo-c.ngrok-free.app,https://url-nodo-d.ngrok-free.app,https://url-nodo-e.ngrok-free.app" python app.py
```

3. Para pruebas entre computadoras distintas, exponer el nodo a internet con ngrok en una terminal aparte:
```bash
   ngrok http 5001
```
   Compartir la URL generada (`https://xxxx.ngrok-free.dev`) con el resto del equipo para que la usen en su propio `NEIGHBORS`.

## Cómo probar

- Con Postman: `POST /messages` a la URL de un nodo, luego `GET /messages` en otro nodo distinto para confirmar que el mensaje se replicó.
- Tolerancia a fallos: apagar un nodo (Ctrl+C), enviar un mensaje nuevo a otro nodo (debe funcionar sin errores), y verificar en los logs que el intento de replicar al nodo caído se ignoró sin detener el sistema.
- Recuperación: levantar de nuevo el nodo caído y hacer `GET /sync` para que recupere los mensajes que se perdió.

## Características de la Unidad I cubiertas

| Tema visto en clase          | Cómo aparece en el proyecto                                                                            |
|-------------------------------|------------------------------------------------------------------------------------                   |
| Concurrencia                  | Varios usuarios pueden mandar mensajes al mismo tiempo a distintos nodos                              |
| Transparencia de acceso       | El cliente puede conectarse a cualquiera de los nodos sin diferencia                                |
| Tolerancia a fallos           | Un nodo caído no detiene al resto (try/except en la replicación) + endpoint `/sync` para recuperación |
| Escalabilidad                 | Escalado horizontal: se pueden agregar más nodos sin tocar los existentes                             | 
| Modelo arquitectónico         | Cliente-servidor, con los servidores actuando también como pares entre sí                           |
| Modelo fundamental             | Procesos independientes (cada nodo) comunicados por red (HTTP), sin memoria compartida               |

## Limitaciones conocidas

- La sincronización (`/sync`) es manual, no automática al arrancar.
- Los mensajes se guardan en memoria (no en base de datos), así que si un nodo se reinicia y no hace `/sync`, pierde su historial local hasta que lo pide de nuevo.
- Las URLs de ngrok en el plan gratuito cambian en cada reinicio, por lo que `NEIGHBORS` debe actualizarse manualmente si algún nodo se reinicia.

## Prueba del sistema
Nodo A inicializado
<img width="960" height="1020" alt="Captura de pantalla 2026-09-15 190040" src="https://github.com/user-attachments/assets/a1f12ed6-5bf7-4e35-86e4-ee5513ef94b8" />
