let cur_user_graphs = {}

let xmlhttp_get_cur_usr_graphs = new XMLHttpRequest();
xmlhttp_get_cur_usr_graphs.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        let res = JSON.parse(this.responseText).graphs;
        for (let i = 0; i < res.length; i++) {
            cur_user_graphs[res[i]['id']] = res[i];
        }
    }
}
xmlhttp_get_cur_usr_graphs.open("GET", "/api/user_graphs/" + cur_user_id, true);
xmlhttp_get_cur_usr_graphs.send()

function generate_select_options(card_id) {
    let select_elem = document.getElementById('news_graph_select' + card_id);
    select_elem.innerHTML = '';
    for (let i = 0; i < Object.keys(cur_user_graphs).length; i++) {
        let id = Object.keys(cur_user_graphs)[i];
        let name = cur_user_graphs[id]['name'];
        select_elem.innerHTML += `<option value="${id}">${name}</option>`
    }
   select_elem.value = Number(document.getElementById('graph_id_label' + card_id).innerHTML)
}

function select_graph(card_id, graph_id) {
    let graph = cur_user_graphs[graph_id];
    document.getElementById('news_graph_img' + card_id).src = "data:image/png;base64," + graph['preview'];
    document.getElementById('news_graph_title' + card_id).innerHTML = graph['name'];
    document.getElementById('news_graph_privacy' + card_id).innerHTML = graph['private'] ? 'Приватный' : 'Публичный';
    document.getElementById("news_graph_link" + card_id).href = "/graph/" + graph_id;

}