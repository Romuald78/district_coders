
function send_email_confirm() {
    var formElement = document.getElementById("user_form");
    const data = new URLSearchParams(new FormData(formElement));
    // const data = new URLSearchParams();
    // data.append("user_id", document.getElementById("user_id").value);
    fetch('/accounts/email_change_send/', {
        method: 'post',
        body: data,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        // if email sending succeed
        if (json.exit_code === 0) {
            var stat = document.getElementById("stat")
            stat.innerText = ''
            stat.appendChild(document.createTextNode("Email successfully sent !"));
            setTimeout(() => {
                stat.innerText = ''
            }, 5000);
        }

        console.log(json);
    });
}

