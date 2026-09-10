# Proyecto-de-sistema-distribuido-Chat-distribuido-
# NodeMesh — Chat distribuido

Proyecto integrador de Sistemas Distribuidos: un chat construido sobre varios nodos independientes que se reparten la carga, replican mensajes entre sí y siguen funcionando aunque uno de ellos falle.

## Equipo
- Luis Guillermo Mejenes Chacon 1 — Nodo A
- Jorge Enrique Soberanes Espinosa 2 — Nodo B
- Angelo Mendoza Garcia 3 — Nodo C
- Diego Alonso Lopez Ballesta 4 — Nodo D
- Diego Angel Vazquez Contreras 5 — Nodo E

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

Imagen del diagrama aqui <--------------------------------------------

- El **cliente** puede conectarse a cualquiera de los 5 nodos.
- Cada **nodo** corre en su propio puerto (5001–5005) o contenedor.
- Los nodos **replican los mensajes entre sí** para mantener la misma información.
- Si un nodo se apaga, el sistema **sigue funcionando** con los nodos restantes.

### Configuración de entorno

<img width="1483" height="762" alt="Captura de pantalla 2026-09-10 183323" src="https://github.com/user-attachments/assets/ec973602-14c2-4b3c-b0e1-276670913526" />

## Cómo correr el proyecto
...
