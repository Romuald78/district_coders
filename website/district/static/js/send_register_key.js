function send_register_key() {
    var formElement = document.getElementById("register_form");
    const data = new URLSearchParams(new FormData(formElement));
    fetch('/accounts/register/', {
        method: 'post',
        body: data,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        // parse string to HtML
        var parser = new DOMParser();
        var html_out;
        if (json.exit_code !== 0) {
            html_out = parser.parseFromString("Oops, something went wrong", 'text/html');
        } else {
            html_out = parser.parseFromString("Added to a new group !", 'text/html');
        }
        var console_view = document.getElementById("register_result");
        console_view.innerHTML = '';
        console_view.appendChild(html_out.body);

        console.log(JSON.stringify(json));
    });
}