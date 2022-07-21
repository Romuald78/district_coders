
function send_user_code() {
    // get the console
    var console_view = document.getElementById("console_view");
    console_view.innerHTML = '';

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
        // clear the console and populate it
        console_view.appendChild(title.body);
        console_view.appendChild(time_stamp.body);
        console_view.appendChild(html_out.body);
        console_view.appendChild(html_err.body);
        console_view.appendChild(err_msg.body);

        display_result_stat();
    });
}

// display languages stat and last solve code
function display_result_stat() {
    var language_stats = document.getElementById("languages_stats");
    language_stats.innerHTML = '';
    var solve_code = document.getElementById("languages_solve_code");
    solve_code.innerHTML = '';

    var formElement = document.getElementById("user_form");
    const data = new URLSearchParams(new FormData(formElement));
    fetch('/exercise/stats_get/', {
        method: 'post',
        body: data,
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {

        // refreshing languages stats
        for (const [key,value] of Object.entries(json.languages)) {
            // adding language name
            var li_lang = document.createElement("li");
            li_lang.appendChild(document.createTextNode(value.name));
            language_stats.appendChild(li_lang);

            // adding stats list into li_lang
            var ul_lang_stat = document.createElement("ul");

            var li_result_test = document.createElement("li");
            var li_result_train = document.createElement("li");

            li_result_test.appendChild(document.createTextNode(value.result_test + "% of success in test mode"));
            li_result_train.appendChild(document.createTextNode(value.result_train + "% of success in train mode"));

            ul_lang_stat.appendChild(li_result_test);
            ul_lang_stat.appendChild(li_result_train);

            li_lang.appendChild(ul_lang_stat);
        }

        // refreshing user solve code
        console.log(json.testresult);
        for (const item of json.testresult) {
            if (item.testresult_obj.solve_percentage > 0) {
                var li_solution = document.createElement("li");
                li_solution.appendChild(document.createTextNode(item.lang_obj.name))
                solve_code.appendChild(li_solution);

                // adding stats list into li_lang
                var ul_details = document.createElement("ul");

                var li_nb_try = document.createElement("li");
                var li_solvetime = document.createElement("li");
                var li_solve_per = document.createElement("li");
                var li_solve_code = document.createElement("li");

                li_nb_try.appendChild(document.createTextNode("nb try: " + item.testresult_obj.nb_test_try));
                li_solvetime.appendChild(document.createTextNode("solve time: " + item.testresult_obj.solve_time));
                li_solve_per.appendChild(document.createTextNode("solve at: " + item.testresult_obj.solve_percentage + "%"));
                li_solve_code.appendChild(document.createTextNode("solve code: "));
                pre_solve_code = document.createElement("pre");
                div_solve_code = document.createElement("div");
                div_solve_code.classList.add("code");
                div_solve_code.appendChild(document.createTextNode(item.testresult_obj.solve_code))
                // div_solve_code.id = "console_view";
                pre_solve_code.appendChild(div_solve_code);
                li_solve_code.appendChild(pre_solve_code);

                ul_details.appendChild(li_nb_try);
                ul_details.appendChild(li_solvetime);
                ul_details.appendChild(li_solve_per);
                ul_details.appendChild(li_solve_code);

                solve_code.appendChild(ul_details);
            }
        }
    });
}
