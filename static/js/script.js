function changeKeyColor(key, color) {
    const keyElement = document.getElementById(key)
    if (keyElement) {
        keyElement.style.backgroundColor = color;
        if (color == "white") {
            keyElement.removeAttribute("style");
        }
    } else {
        console.log("key not faund: " + key);
    }
}

goal = NaN

function getLastColor() {
    fetch("/get_last_color")
        .then(response => response.json())
        .then(data => {
            const key = data.key;
            const color = data.color;
            temp = data.goal;
            if (temp != goal) {
                goal = temp;
                d = new Date();
                $("#note").attr("src", "static/images/current.png?t="+d.getTime());
            }
            if (key && color) {
                console.log("yipee " + key + ", " + color);
                changeKeyColor(key, color);
            }
        })
}


function updateDiv()
{ 
    $( "#imgDiv" ).load(window.location.href + " #imgDiv" );
}

setInterval(getLastColor, 100);