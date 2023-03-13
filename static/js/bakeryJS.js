function openOverlay() {
    document.getElementById("message_overlay").style.width = "fit-content";
    document.getElementById("message_overlay").style.opacity = "100%";
    document.getElementById("hideOver").style.opacity = "100%";
    document.getElementById("message_overlay").style.height = "40px";
}

function closeOverlay() {
    document.getElementById("message_overlay").style.width = "0px";
    document.getElementById("message_overlay").style.opacity = "0%";
    document.getElementById("hideOver").style.opacity = "0%";
    document.getElementById("message_overlay").style.height = "20px";
}
