// Calling backend with email and creating index, next getting chatlist chatlist 
const BASE_URL = "http://127.0.0.1:8000"

email = document.getElementById("email").value;
var indexData = new FormData();
indexData.append("email", email);

indexData.append("csrfmiddlewaretoken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
$.ajax({
    url: BASE_URL + "/getConnections",
    type: "POST",
    data: indexData,
    processData: false,
    contentType: false,
    success: function (response) {
        console.log(response)
        chat_data = response["connections"]
        // Index has been created now lets get chatlist
        make_chat_list(chat_data)
        // stop loader
        document.getElementById('loading').style.display = "none";
        // show toast
        document.getElementById("desc_correct").innerHTML = "All Contacts Fetched";
        launch_toast_correct();
    },
    error: function (error) {
        console.log(error);
        // stop loader
        document.getElementById('loading').style.display = "none";
        //show error toast
        document.getElementById("desc_correct").innerHTML = "Error! Please login again";
        launch_toast();
    }
});

// If enter is pressed in message input tab then this is used to handle that
const myInput = document.getElementById("message_send");
myInput.addEventListener("keydown", function (event) {
    if (event.keyCode === 13) {
        message_handler();
        event.preventDefault();
    }
});

// Setting username
document.getElementById("name").innerHTML = document.getElementById("shortname").value;

// This is used to create a user message
function append_user_message(message) {
    var message_div = document.createElement("div");
    message_div.className = "user_message";
    var name_dev = document.createElement("div");
    name_dev.className = "name_user_img";
    name_dev.innerHTML = document.getElementById("shortname").value;
    var message_Div = document.createElement("p");
    message_Div.innerHTML = message;
    message_div.appendChild(name_dev);
    message_div.appendChild(message_Div);
    var outer_div = document.getElementById("message_field_inner");
    outer_div.appendChild(message_div);
}

// This is used to create a message by bot
function append_sender_message(message, sender_name_short) {
    var message_div = document.createElement("div");
    message_div.className = "bot_message";
    var name_dev = document.createElement("div");
    name_dev.className = "name_user_img";
    name_dev.innerHTML = sender_name_short;
    var message_Div = document.createElement("p");
    message_Div.innerHTML = message;
    message_div.appendChild(name_dev);
    message_div.appendChild(message_Div);
    var outer_div = document.getElementById("message_field_inner");
    outer_div.appendChild(message_div);
}

// This is a message handler that gets message from user and then calls bot and then prints its message too
function message_handler() {
    var message = document.getElementById("message_send").value;
    document.getElementById("message_send").value = "";
    if (message != "") {
        append_user_message(message);
        chat(message);
    }
}



// Create chat list
function make_chat_list(chat_data) {
    document.getElementById('chat_list_data').value = JSON.stringify(chat_data);
    // Traversing data and making divs
    for (var i = 0; i < chat_data.length; i++) {
        var folder_file_div = document.createElement("div");
        folder_file_div.className = "folder_file";
        folder_file_div.id = chat_data[i]["id"];
        var img = document.createElement("img");
        img.src = "/static/images/user.png"
        var folder_file_name = document.createElement("div");
        folder_file_name.className = "folder_file_name";
        folder_file_name.innerHTML = chat_data[i]["username"];
        var p = document.createElement("p");
        p.className = "new_message"

        folder_file_div.appendChild(img)
        folder_file_div.appendChild(folder_file_name)
        folder_file_div.appendChild(p)
        // folder_file_div.appendChild(time_of_upload)
        folder_file_div.addEventListener('click', (function (chatId) {
            return function () {
                openChat(chatId);
            };
        })(chat_data[i]["id"]));
        document.getElementById("all_folders_and_files").appendChild(folder_file_div)
    }

}

// Open a particular chat


// Start new chat modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
function open_new_doc_modal() {
    modal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

var usermodal = document.getElementById("userModal");


// When the user clicks the button, open the modal 
function open_user_modal() {
    usermodal.style.display = "block";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal || event.target == usermodal) {
        modal.style.display = "none";
        usermodal.style.display = "none";
    }
}

function add_to_chatList(index_id, name, all_files) {
    var folder_file_div = document.createElement("div");
    folder_file_div.className = "folder_file";
    folder_file_div.id = index_id;
    var img = document.createElement("img");
    img.src = "/static/images/user.png"
    var folder_file_name = document.createElement("div");
    folder_file_name.className = "folder_file_name";
    folder_file_name.innerHTML = name;
    var p = document.createElement("p");
    p.className = "new_message"

    folder_file_div.appendChild(img)
    folder_file_div.appendChild(folder_file_name)

    folder_file_div.appendChild(p)
    folder_file_div.addEventListener('click', (function (chatId) {
        return function () {
            openChat(chatId);
        };
    })(index_id));
    document.getElementById("all_folders_and_files").appendChild(folder_file_div)
    var chat_data = document.getElementById("chat_list_data").value;
    chat_data = JSON.parse(chat_data);
    chat_data.push({ "index_id": index_id, "name": name, "all_files": all_files })
    document.getElementById("chat_list_data").value = JSON.stringify(chat_data);

}

function start_new_chat() {
    sender_email = document.getElementById("email").value;
    reciever_email = document.getElementById("new_chat_email").value;
    var formData = new FormData();
    formData.append("sender_email", sender_email);
    formData.append("reciever_email", reciever_email);
    formData.append("csrfmiddlewaretoken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
    $.ajax({
        url: BASE_URL + "/startNewChat",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            console.log(response)
            if (response["message"] == "Chat already started") {
                document.getElementById("desc").innerHTML = "Chat already started";
                launch_toast();
                document.getElementById("add_files_modal").style.display = "none";
            }
            else {
                reciever_name = response["reciever_name"]
                document.getElementById("chat_heading_name").innerHTML = reciever_name

                // Add to chat list
                add_to_chatList(response["reciever_id"], reciever_name, "")

                // Close modal
                document.getElementById("add_files_modal").style.display = "none";
            }
        },

        error: function (error) {
            console.log(error);
            // show error toast
            document.getElementById("desc").innerHTML = "User not Found";
            launch_toast();
            document.getElementById("add_files_modal").style.display = "none";
        }
    });
}

const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat?email="+email);
chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
};
chatSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
    active_chat = document.getElementById("active_chat").value
    if (active_chat == data["chat_id"]){
        append_sender_message(data["message"],data["short_name"])
    }
    else{
        // just indicate new message
        var div = document.getElementById(data["chat_id"])
        var p = div.querySelector("p")
        p.style.display = "block"

    }
    

};
function openChat(chat_id) {
    // getting chat history
    email = document.getElementById("email").value;
    $.ajax({
        url: BASE_URL + "/chatHistory?reciever_id=" + chat_id + "&sender_email=" + email,
        type: "GET",
        success: function (response) {
            console.log(response)
            // Chat list has been received
            chat_history_data = response["chat_history"]
            reciever_name = response["reciever_name"]
            document.getElementById("chat_heading_name").innerHTML = reciever_name
            // Calling make_history function
            make_chat_history(chat_history_data, chat_id)
        },
        error: function (error) {
            console.log(error);
        }
    });

    document.getElementById("chat_heading").style.display = "flex"
    document.getElementById("message_field_inner").innerHTML = ""

    // remove active_link from all other divs under the di with id all_folders_and_files
    var all_folders_and_files = document.getElementById("all_folders_and_files").children;
    for (var i = 0; i < all_folders_and_files.length; i++) {
        if (all_folders_and_files[i].id != chat_id) {
            all_folders_and_files[i].classList.remove("active_file")
        }
    }
    document.getElementById("active_chat").value = chat_id;
    document.getElementById(chat_id).classList.add("active_file");
    var div = document.getElementById(chat_id)
    var p = div.querySelector("p")
    p.style.display = "none"
}

// Create messages in chat history 
function make_chat_history(chat_history_data, chat_id) {
    for (var i = 0; i < chat_history_data.length; i++) {
        message = chat_history_data[i]["chat"]
        if (chat_history_data[i]["sender_id"] == chat_id) {
            append_sender_message(message, chat_history_data[i]["sender_name_short"])
        }
        else {
            append_user_message(message)
        }
    }
}


function chat(message) {
    var reciever_id = document.getElementById("active_chat").value;
    var email = document.getElementById("email").value;
    chatSocket.send(JSON.stringify({ message: message, reciever_id: reciever_id, email: email }));
}

function launch_toast() {
    var x = document.getElementById("toast")
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
}
function launch_toast_correct() {
    var x = document.getElementById("toast_correct")
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
}