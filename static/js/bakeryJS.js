function openOverlay() {
    document.getElementById("message_overlay").style.width = "fit-content";
}

function closeOverlay() {
    document.getElementById("message_overlay").style.width = "0";
}

function onload_outOfStock() {
    $.ajax({
        url: "/main.py",
        context: document.body
    }).done(function( o ) {
        // check if stock == 0

    })
}
