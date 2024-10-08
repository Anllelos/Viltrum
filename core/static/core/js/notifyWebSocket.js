
// Obtener el ID del usuario autenticado desde un script del backend (puedes usar una plantilla para obtenerlo dinámicamente)

// Crear la URL del WebSocket
const socketUrl = `ws://${window.location.host}/ws/notify/${userId}/`;

// Crear la conexión del WebSocket
const notificationSocket = new WebSocket(socketUrl);

// Cuando la conexión esté abierta
notificationSocket.onopen = function (e) {
    console.log("Conectado al WebSocket de notificaciones");
};

// Cuando llegue un mensaje del WebSocket
notificationSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data.message;

    // Añadir la notificación a la lista
    const notificationList = document.getElementById('notificationList');
    const newNotification = document.createElement('a');
    newNotification.textContent = message;
    notificationList.appendChild(newNotification);
};

// Cuando se cierre la conexión
notificationSocket.onclose = function (e) {
    console.log("Desconectado del WebSocket");
};

// En caso de error en el WebSocket
notificationSocket.onerror = function (e) {
    console.error("Error en el WebSocket", e);
};

// Manejar el envío de notificaciones (este ejemplo es para testeo)
