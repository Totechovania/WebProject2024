let xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let responce = JSON.parse(this.responseText);
        if (responce.img) document.getElementById('user_img').src = "data:image/png;base64," + responce.img;
        if (responce.name) document.getElementById('user_name').innerHTML = responce.name;
        if (responce.email) document.getElementById('user_email').innerHTML = responce.email;
        if (responce.created_date) document.getElementById('user_created_date').innerHTML = responce.created_date;
        if (responce.about) document.getElementById('user_about').innerHTML = responce.about;
    }
}
xmlhttp.open("GET", "/api/user_info", true);
xmlhttp.send()