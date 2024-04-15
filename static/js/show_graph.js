function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length === 1 ? "0" + hex : hex;
}
function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}


let xmlhttp_show_graph = new XMLHttpRequest();
xmlhttp_show_graph.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        let graph = JSON.parse(this.responseText).graph;
        let graph_param = graph.function;
        graph_param = graph_param.replace(/'/g, '"');
        graph_param = JSON.parse(graph_param);

        let name = graph.name;
        let graph_name = document.getElementById("graph_name");
        graph_name.value = name;

        let pryvate = graph.private;
        let graph_privacy = document.getElementById("graph_privacy");
        if (pryvate) {graph_privacy.value = "private"} else graph_privacy.value = "public";

        let width = graph_param.width;
        let img_width = document.getElementById("img_width");
        img_width.value = width;

        let height = graph_param.height;
        let img_height = document.getElementById("img_height");
        img_height.value = height;

        let center_x_val = graph_param.center_x;
        let center_x_elem = document.getElementById("center_x");
        center_x_elem.value = center_x_val;

        let center_y_val = graph_param.center_y;
        let center_y_elem = document.getElementById("center_y");
        center_y_elem.value = center_y_val;

        let pixel_per_unit_val = graph_param.pixel_per_unit;
        let pixel_per_unit_elem = document.getElementById("pixel_per_unit");
        pixel_per_unit_elem.value = pixel_per_unit_val;


        let formulas_val = graph_param.formulas;
        let colors_val = graph_param.colors;

        for ( let i = 0; i < formulas_val.length; i++) {
            let hex_color = rgbToHex(colors_val[i][0], colors_val[i][1], colors_val[i][2]);
            add_formula(formulas_val[i], hex_color);
        }



        }

    else if (this.readyState == 4 && this.status == 404) {
        alert("Error: " + this.responseText);
    }
};
xmlhttp_show_graph.open("GET", "/api/open_graph/" + graph_id, true);
xmlhttp_show_graph.send();

