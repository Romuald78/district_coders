
function send_user_code() {
    console.log("ici bas");
    var formElement = document.getElementById("user_form");
    const data = new URLSearchParams(new FormData(formElement));
    fetch('./inspect', {
        method: 'post',
        body: data,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        // parse string to HtML
        var parser = new DOMParser();
	    var html_out = parser.parseFromString(json.stdout, 'text/html');
	    var html_err = parser.parseFromString(json.stderr, 'text/html');
        // get the console, clear and populate it
        var console_view = document.getElementById("console_view");
        console_view.innerHTML = ''
        console_view.appendChild(html_out.body);
        console_view.appendChild(html_err.body);
    });
}