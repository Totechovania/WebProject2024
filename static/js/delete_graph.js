function delete_graph() {


    if  (confirm( "Вы уверены, что хотите удалить график?" )){
        let del_btn = document.getElementById('delete_graph_btn');
        del_btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>'

        let xmlhttp__delete_graph = new XMLHttpRequest();

        xmlhttp__delete_graph.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                del_btn.innerHTML = 'Удалить';
                window.location.href = '/profile';
            } else if (this.readyState == 4 && this.status == 404) {
                alert("Error: " + this.responseText);
                del_btn.innerHTML = 'Удалить';
            }
        }
        xmlhttp__delete_graph.open("DELETE", "/api/delete_graph/" + graph_id, true);
        xmlhttp__delete_graph.send();
    }
}