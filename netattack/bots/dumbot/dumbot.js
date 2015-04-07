var input = process.argv.splice(2);
var regexp = new RegExp(" ", "gm");
input = String(input).split(regexp);
var nodes = [];
var targets = [];
for(var i = 0; i < input.length; i++){
    if(input[i].charAt(0) == "F")
        nodes.push(i);
    else
        targets.push(i);
}
var result = "";
var length = nodes.length;
for(var i = 0; i < length; i++){
    if(targets.length>0)
        result += nodes.shift() + "," + targets.shift() + " ";
    else
        result += nodes.shift() + ",0 ";
}
console.log(result);