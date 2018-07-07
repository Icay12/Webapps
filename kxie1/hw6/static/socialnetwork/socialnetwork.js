/**
 * Created by icay on 23/02/2018.
 */

// Sends a new request to update the to-do list


function getUpdates() {
    var list = $("#post_list");
    var max_time = list.data("creation_time")
    $.get("/socialnetwork/get_changes/" + max_time)
        .done(function(data) {
            list.data('max-time', data['max-time']);
            for (var i = 0; i < data.posts.length; i++) {
                var post = data.posts[i];
                var new_post = $(post.html);
                new_post.data("post-id", post.id);

                list.prepend("<hr class='featurette-divider'>");
                list.prepend("<p id=total_"+post.id+"></p>");
                list.prepend("<p>Comments:</p>");


                list.prepend(new_post);

            }


        });
}


function getPostList() {
    $.ajax({
        url: "/socialnetwork/get-list-json",
        dataType : "json",
        success: updatePostList
    });
}

function updatePostList(posts) {
    // Removes the old to-do list items
    $("li").remove();

    // Adds each new todo-list item to the list
    $(posts).each(function() {
        // var name = this.fields.user
        // var id = this.fields.id
        // window.alert(id)
        $("#post-list").append(
            '<li style="width : 500px" class="card" id="ipost">' +
                '<a href= /socialnetwork/otherprofile/' + this.fields.name +'> <h5 class="card-header">' +this.fields.name+'</h5></a>' +
                '<h7 class="card-header">' + this.fields.creation_time + '</h7>' +
                '<p class="card-body">' + this.fields.post + '</p>' +
                '<h7>Comments:</h7>' +
                '<textarea style="width:400px;height:50px" class="card" id= "newComment'+ this.pk +'" name = "newComment" placeholder="Give some comment..."></textarea>' +
                "<button onclick='addComment(" + this.pk + ")'>submit</button>" +
            "</li>"
        );

        getCommentList(this.pk)
    });
}


function getCommentList(post_id) {
    // var id = post_id
    // var ull = "/socialnetwork/get-comment-list-json/"+id
    // window.alert(ull)
    $.ajax({
        url: "/socialnetwork/get-comment-list-json",
        data: "post_id="+post_id,
        dataType : "json",
        success: updateCommentList
    });
}


function updateCommentList(comments) {
    $("lii").remove();

    $(comments).each(function() {

        $("#comment-list").append(
            '<lii style="width : 450px" class="card">' +
                '<a href= /socialnetwork/otherprofile/' + this.fields.user +'> <h7 class="card-header">' +this.fields.user+ + this.fields.date + '</h7></a>' +
                '<p class="card-body">' + this.fields.text + '</p>' +
            "</lii>"
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
    window.alert(message);
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

function addPost() {
    var postTextElement = $("#newPost");
    var postTextValue   = postTextElement.val();

    // Clear input box and old error message (if any)
    postTextElement.val('');
    displayError('');
    // console.log(postTextValue)

    $.ajax({
        url: "/socialnetwork/create",
        type: "POST",
        data: "newPost="+postTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updatePostList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}


function addComment(post_id) {
    var commentTextElement = $("#newComment"+post_id);
    var commentTextValue   = commentTextElement.val();

    // Clear input box and old error message (if any)
    commentTextElement.val('');
    displayError('');
    window.alert(commentTextValue)

    $.ajax({
        url: "/socialnetwork/addcomment",
        type: "POST",
        data: "newComment="+commentTextValue+"&post_id="+post_id+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updatePostList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

// function deletePost(id) {
//     $.ajax({
//         url: "/jquery-todolist/delete-item/"+id,
//         type: "POST",
//         data: "csrfmiddlewaretoken="+getCSRFToken(),
//         dataType : "json",
//         success: updateList
//     });
// }

// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getPostList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getPostList, 5000);

