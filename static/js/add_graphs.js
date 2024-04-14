let xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let graphs = JSON.parse(this.responseText)['graphs'];
        for (let i = 0; i < graphs.length; i++) {
            let graph = graphs[i];
            let id = graph['id'];
            let name = graph['name'];
            let preview = graph['preview'];


        }
    }
};
xmlhttp.open("GET", "/api/user_graphs/" + usr_id, true);
xmlhttp.send();

