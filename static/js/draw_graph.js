function draw() {
    let btn = document.getElementById('draw_btn');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>'

    let graphs_params = get_graph_params();

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('graph_img').src ="data:image/png;base64," +  this.responseText;
            btn.innerHTML = 'Draw';
        } else if (this.readyState == 4 && this.status == 400) {
            alert("Error: " + this.responseText);
            btn.innerHTML = 'Draw';
        }
    };

    xmlhttp.open("POST", "/api/draw", true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send( JSON.stringify(graphs_params) );

}
