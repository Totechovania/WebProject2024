function save_graph() {
    let btn = document.getElementById('save_graph_btn');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>'

    let name = document.getElementById('graph_name').value;
    if (!name) name = document.getElementById('graph_name').placeholder;
    let private = (document.getElementById('graph_privacy').value === "private");
    let graphs_params = get_graph_params();

    xmlhttp_save_graph = new XMLHttpRequest();
    xmlhttp_save_graph.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            btn.innerHTML = 'Сохранить';
        } else if (this.readyState == 4 && this.status == 400) {
            alert("Error: " + this.responseText);
            btn.innerHTML = 'Сохранить';
        }
    }
    xmlhttp_save_graph.open("POST", "/api/new_graph", true);
    xmlhttp_save_graph.setRequestHeader("Content-type", "application/json");
    xmlhttp_save_graph.send( JSON.stringify({name, private, graphs_params}) );
}