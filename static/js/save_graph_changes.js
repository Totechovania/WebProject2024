function save_graph_changes() {
    let sc_btn = document.getElementById('save_graph_changes_btn');
    sc_btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>'

    let name = document.getElementById('graph_name').value;
    if (!name) name = document.getElementById('graph_name').placeholder;
    let private = (document.getElementById('graph_privacy').value === "private");
    let graphs_params = get_graph_params();

    let xmlhttp_save_graph_changes = new XMLHttpRequest();
    xmlhttp_save_graph_changes.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            sc_btn.innerHTML = 'Сохранить изменения';
        } else if (this.readyState == 4 && this.status == 400) {
            alert("Error: " + this.responseText);
            sc_btn.innerHTML = 'Сохранить изменения';
        }
    }

    xmlhttp_save_graph_changes.open("PUT", "/api/update_graph/" + graph_id, true);
    xmlhttp_save_graph_changes.setRequestHeader("Content-type", "application/json");
    xmlhttp_save_graph_changes.send( JSON.stringify({name, private, graphs_params}) );
}