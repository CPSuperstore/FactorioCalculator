function flagError(id, errorMessage){
    var element = document.getElementById(id);
    var value = element.value;

    errorMessage = errorMessage || element.value;

    function clearError(){
        element.classList.remove("input-error");

        element.removeEventListener('click', clearError);
        element.value = value;
    }

    element.value = errorMessage;

    element.classList.add("input-error");
    element.addEventListener('click', clearError);
}

function isValidHttpUrl(string) {
    let url;

    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }

    return url.protocol === "http:" || url.protocol === "https:";
}

function dateify(date) {
    date = date.split("-")
    return new Date(parseInt(date[0])-1, date[1], date[2])
}

function numberPad(number, digits) {
    return Array(Math.max(digits - String(number).length + 1, 0)).join(0) + number;
}

function flash(message, messageType){
    messageType = messageType || "info";

    alertDisplay = document.getElementById("alertDisplay");

    alertDisplay.innerHTML += `
        <div class="alert alert-` + messageType + ` alert-dismissible">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            ` + message + `
        </div>
    `;
}

function getCSSVar(name){
    return getComputedStyle(document.body).getPropertyValue(name);
}
