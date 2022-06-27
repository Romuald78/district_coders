
const interf = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

var lines = []

function read_line(){
    return lines.shift();
}

interf.on('line', function (received) {
    //console.log("|"+received+"|");
    lines.push(received);
});

interf.on('close', function () {

