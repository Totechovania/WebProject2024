let xmlhttp_get_graphs = new XMLHttpRequest();
xmlhttp_get_graphs.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        let graphs = JSON.parse(this.responseText)['graphs'];
        let graphs_container = document.getElementById('graphs_container');
        for (let i = 0; i < graphs.length; i++) {
            let graph = graphs[i];
            let id = graph['id'];
            let name = graph['name'];
            let preview = graph['preview'];

            graphs_container.innerHTML += `
                        <div class="p-2">
                        <div class="card" style="width: 300px;">
                            <img class="card-img-top" src="data:image/png;base64,${preview}" alt="Card image">
                            <div class="card-body">
                              <h4 class="card-title">${name}</h4>
                              <p class="card-text">aaaaaaaa</p>
                              <a href="/graph/${id}" class="btn btn-primary">Открыть</a>
                            </div>
                         </div>
                         </div>`
        }
    }
};
xmlhttp_get_graphs.open("GET", "/api/user_graphs/" + usr_id, true);
xmlhttp_get_graphs.send();

