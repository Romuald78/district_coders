
function send_email_confirm() {
    var formElement = document.getElementById("user_form");
    const data = new URLSearchParams(new FormData(formElement));
    // const data = new URLSearchParams();
    // data.append("user_id", document.getElementById("user_id").value);
    fetch('/accounts/sendemailconfirmation/', {
        method: 'post',
        body: data,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        var stat = document.getElementById("stat")
        stat.innerText = ''
        stat.appendChild(document.createTextNode("Email successfully sent !"));
        setTimeout(() => {
            stat.innerText = ''
        }, 8000);
        console.log(json);
    });
}

