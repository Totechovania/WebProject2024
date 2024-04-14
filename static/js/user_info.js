if (cur_user_id != usr_id) {
    document.getElementById('redact_btn').hidden = true;
    document.getElementById('user_email').hidden = true;
    document.getElementById('user_email_label').hidden = true;
}
let xmlhttp_get_user_info = new XMLHttpRequest();
xmlhttp_get_user_info.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let responce = JSON.parse(this.responseText);
        if (responce.avatar) document.getElementById('user_avatar').src = 'data:image/png;base64,' + responce.avatar;
        if (responce.name) document.getElementById('user_name').innerHTML = responce.name;
        if (responce.email) document.getElementById('user_email').innerHTML = responce.email
        if (responce.created_date) document.getElementById('user_created_date').innerHTML = responce.created_date;
        if (responce.about) document.getElementById('user_about').innerHTML = responce.about;
    }
}
xmlhttp_get_user_info.open("GET", "/api/user_info/" + usr_id, true);
xmlhttp_get_user_info.send()