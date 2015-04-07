var friends = [], enemies = [];
process.argv.slice(2).forEach(function(value, index) {
    var data = { index: index, strength: parseInt(value.substring(1)) };
    if(value[0] === 'F') {
        friends.push(data);
    } else {
        enemies.push(data);
    }
});

function weaknessCompare(a, b) {
    return (a.strength > b.strength) ? -1 : ((a.strength < b.strength) ? 1 : 0);
}

friends.sort(weaknessCompare);
enemies.sort(weaknessCompare);

if(friends.length > 0) {
    var strongest = friends[0];
    for(var i = 0; i < enemies.length; i++) {
        var enemy = enemies[i];
        if(enemy.strength + 1 < strongest.strength) {
            strongest.target = enemy.index;
            break;
        }
    };
}
if(friends.length > 1) {
    friends[1].target = friends[friends.length - 1].index;
}

console.log(friends.map(function(friend) {
    return friend.index + ',' + (friend.target || friend.index);
}).join(' '));