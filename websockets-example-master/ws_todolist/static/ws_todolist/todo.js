function updateList(items) {
    // Removes the old to-do list items
    var list = document.getElementById("todo-list");
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }

    // Parses the response to get a list of JavaScript objects for 
    // the items.

    // Adds each new todo-list item to the list
    for (var i = 0; i < items.length; i++) {
        // Extracts the item id and text from the response
        var id = items[i]["pk"];  // pk is "primary key", the id
        var itemText = items[i]["fields"]["text"];
        var ipAddr   = items[i]["fields"]["ip_addr"]
  
        // Builds a new HTML list item for the todo-list item
        var newItem = document.createElement("li");
        newItem.innerHTML = "<button onclick='deleteItem("+id+")'>X</button> " +
                            sanitize(itemText) +
                            ' <span class="details">' +
                            "(id=" + id + ", ip_addr=" + ipAddr + ")" +
                            '</span>';

        // Adds the todo-list item to the HTML list
        list.appendChild(newItem);
    }
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    var errorElement = document.getElementById("error");
    errorElement.innerHTML = message;
}

function displayMessage(message) {
    var errorElement = document.getElementById("message");
    errorElement.innerHTML = message;
}

function displayResponse(response) {
    if ("error" in response) {
        displayError(response.error);
    } else if ("message" in response) {
        displayMessage(response.message);
    } else {
        displayMessage("Unknown response");
    }
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function addItem() {
    var itemTextElement = document.getElementById("item");
    var itemTextValue   = itemTextElement.value;

    // Clear input box and old error message (if any)
    itemTextElement.value = '';
    displayError('')

    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var response = JSON.parse(req.responseText);
        displayResponse(response);
    }

    req.open("POST", "/ws_todolist/add-item", true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());

}

function deleteItem(id) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var response = JSON.parse(req.responseText);
        displayResponse(response);
    }

    req.open("POST", "/ws_todolist/delete-item/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());
}

window.onload = function() {
    // Create a new WebSocket.
    var socket = new WebSocket("ws://" + window.location.host + "/test/");

    // Handle any errors that occur.
    socket.onerror = function(error) {
        displayMessage("WebSocket Error: " + error);
    }

    // Show a connected message when the WebSocket is opened.
    socket.onopen = function(event) {
        displayMessage("WebSocket Connected");
    }


    // Handle messages sent by the server.
    socket.onmessage = function(event) {
        var items = JSON.parse(event.data);
        updateList(items);
    }

    // Show a disconnected message when the WebSocket is closed.
    socket.onclose = function(event) {
        displayMessage("WebSocket Disconected");
    }
}

