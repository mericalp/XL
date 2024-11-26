// static/js/notification.js
console.log('Initializing WebSocket...');
const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
const socketUrl = `${ws_scheme}://${window.location.host}/ws/notifications/`;  // Keep ws/ prefix from URLs
console.log('Connecting to:', socketUrl);

const notificationSocket = new WebSocket(socketUrl);

notificationSocket.onopen = function(e) {
    console.log('WebSocket connection established');
};

notificationSocket.onmessage = function(e) {
    console.log('Message received:', e.data);
    const data = JSON.parse(e.data);
    if (data.type === 'notification') {
        toastr.warning(data.message);
    }
};

notificationSocket.onerror = function(e) {
    console.error('WebSocket error:', e);
};