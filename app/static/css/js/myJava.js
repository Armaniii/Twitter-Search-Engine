var search = "";
var input = document.getElementById("submit");
var listItems = document.getElementById("list-items");
var taskData = "";

function myFunction() {
    this.search = document.getElementById("searchVal").value
}

function handle(e) {
    address = document.getElementById("searchVal").value;
    if (e.keyCode === 13) {
        myFunction();
        // openInNewTab("http://www.google.com/search?q=" + this.search);

    }
    return false;
}

// function openInNewTab(url) {
//     var win = window.open(url, '_blank');
//     win.focus();
// }