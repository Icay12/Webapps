// Sends a new request to update the to-do list
function getList() {
    $.ajax({
        url: "/jquery-todolist/get-list-json",
        dataType : "json",
        success: updateList
    });
}

function updateList(items) {
    // Removes the old to-do list items
    $("li").remove();

    // Adds each new todo-list item to the list
    $(items).each(function() {
        $("#todo-list").append(
            "<li><button onclick='deleteItem("+this.pk+")'>X</button> " +
                    sanitize(this.fields.text) +
                    ' <span class="details">' +
                    "(id=" + this.pk + ", ip_addr=" + this.fields.ip_addr + ")" +
                    "</span></li>"
        );
    });
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
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
    var itemTextElement = $("#item");
    var itemTextValue   = itemTextElement.val();

    // Clear input box and old error message (if any)
    itemTextElement.val('');
    displayError('');

    $.ajax({
        url: "/jquery-todolist/add-item",
        type: "POST",
        data: "item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

function deleteItem(id) {
    $.ajax({
        url: "/jquery-todolist/delete-item/"+id,
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: updateList
    });
}

// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getList, 5000);
