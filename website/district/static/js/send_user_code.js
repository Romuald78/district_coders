
function send_user_code() {
    var formElement = document.getElementById("user_form");
    const data = new URLSearchParams(new FormData(formElement));
    fetch('/exercise/inspect/', {
        method: 'post',
        body: data,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        // parse string to HtML
        var parser     = new DOMParser();
	    var title      = parser.parseFromString(json.title, 'text/html');
	    var html_out   = parser.parseFromString(json.stdout, 'text/html');
	    var html_err   = parser.parseFromString(json.stderr, 'text/html');
        var err_msg    = parser.parseFromString(json.err_msg, 'text/html');
        var time_stamp = parser.parseFromString(json.time_stamp, 'text/html');
        // get the console, clear and populate it
        var console_view = document.getElementById("console_view");
        console_view.innerHTML = '';
        console_view.appendChild(title.body);
        console_view.appendChild(time_stamp.body);
        console_view.appendChild(html_out.body);
        console_view.appendChild(html_err.body);
        console_view.appendChild(err_msg.body);
    });
}

