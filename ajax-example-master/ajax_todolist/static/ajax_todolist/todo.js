// Sends a new request to update the to-do list
function getList() {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var items = JSON.parse(req.responseText);
        updateList(items);
    }

    req.open("GET", "/ajax-todolist/get-list-json", true);
    req.send(); 
}

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
        if (Array.isArray(response)) {
            updateList(response);
        } else {
            displayError(response.error);
        }
    }

    req.open("POST", "/ajax-todolist/add-item", true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());

}

function deleteItem(id) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var items = JSON.parse(req.responseText);
        updateList(items);
    }

    req.open("POST", "/ajax-todolist/delete-item/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());
}

// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getList, 5000);
