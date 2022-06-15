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
        console.log(json);
    });
}