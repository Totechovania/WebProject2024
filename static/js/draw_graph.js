function draw() {
    let btn = document.getElementById('draw_btn');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>'

    let graphs_params = get_graph_params();

    var xmlhttp_draw_graph = new XMLHttpRequest();
    xmlhttp_draw_graph.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('graph_img').src ="data:image/png;base64," +  this.responseText;
            btn.innerHTML = 'Draw';
        } else if (this.readyState == 4 && this.status == 400) {
            alert("Error: " + this.responseText);
            btn.innerHTML = 'Draw';
        }
    };

    xmlhttp_draw_graph.open("POST", "/api/draw", true);
    xmlhttp_draw_graph.setRequestHeader("Content-type", "application/json");
    xmlhttp_draw_graph.send( JSON.stringify(graphs_params) );

}
