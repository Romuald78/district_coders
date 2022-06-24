const readline = rl.default;

var interf = readline.createInterface(process.stdin, null, null);

var lines = []

function read_line(){
    return lines.shift();
}

interf.on('line', function (received) {
    console.log("|"+received+"|");
    lines.push(received);
});

interf.on('close', function () {

