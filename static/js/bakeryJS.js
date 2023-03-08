function openOverlay() {
    document.getElementById("message_overlay").style.width = "fit-content";
    document.getElementById("message_overlay").style.opacity = "100%";
    document.getElementById("hideOver").style.opacity = "100%";
}

function closeOverlay() {
    document.getElementById("message_overlay").style.width = "0";
    document.getElementById("message_overlay").style.opacity = "0%";
    document.getElementById("hideOver").style.opacity = "0%";
}

//function onload_outOfStock() {
//     $.ajax({
//        url: "/main.py",
//        context: document.body
//     }).done(function( o ) {
// check if stock == 0
//
//     })
// }
