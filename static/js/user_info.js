xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let responce = JSON.parse(this.responseText);
        alert(this.responseText, responce["name"]);
        document.getElementById('user_img').src = "data:image/png;base64," + responce['img'];
        document.getElementById('user_name').innerHTML = responce["name"];
        document.getElementById('user_email').innerHTML = responce["email"];
        document.getElementById('user_created_date').innerHTML = responce['created_date'];
        document.getElementById('user_about').innerHTML = responce['about'];
    }
}
xmlhttp.open("GET", "/api/user_info", true);
xmlhttp.send()