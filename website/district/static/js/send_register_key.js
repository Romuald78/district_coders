function display_user_groups() {
    fetch('/accounts/my_groups/', {
        method: 'get'
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        // populate the page to display groups
        var ul = document.getElementById("groups");
        ul.innerHTML = '';

        for (const [key,value] of Object.entries(json)) {
            // adding group name
            var li_gn = document.createElement("li");
            li_gn.appendChild(document.createTextNode(value.group_obj.name));
            ul.appendChild(li_gn);

            // adding members list of the group
            var li_mem = document.createElement("li");
            li_mem.appendChild(document.createTextNode("membres :"));
            ul.appendChild(li_mem);

            var ul_mem = document.createElement("ul");
            // adding user's name
            value.group_users.forEach(username => {
                var li_user = document.createElement("li");
                li_user.appendChild(document.createTextNode(username));
                ul_mem.appendChild(li_user);
            })
            ul.appendChild(ul_mem);
        }

        // console.log(JSON.stringify(json));
    });
}

function send_register_key() {
    var formElement = document.getElementById("register_form");
    const data = new URLSearchParams(new FormData(formElement));
    fetch('/accounts/group_register/', {
        method: 'post',
        body: data,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        var console_view = document.getElementById("register_result");
        console_view.innerHTML = '';

        var err_p = document.createElement("p");
        err_p.classList.add("infobox");
        if (json.exit_code !== 0) {
            err_p.appendChild(document.createTextNode(json.err_msg[1]));
            if (json.exit_code == 9) {
                err_p.classList.add("warning");
            } else {
                err_p.classList.add("error");
            }
        } else {
            err_p.appendChild(document.createTextNode("New group registration ok"));
            err_p.classList.add("ok");
            // refresh display
            display_user_groups();

            // clear register_key text field
            var register_key_field = document.getElementById("register_key");
            register_key_field.value = "";
        }
        console_view.appendChild(err_p);

        // console.log(JSON.stringify(json));
    });
}