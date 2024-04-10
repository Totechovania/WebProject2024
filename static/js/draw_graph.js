function draw() {
    let btn = document.getElementById('draw_btn');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>'
    btn.disabled = true;
    let height = document.getElementById('img_height').value;
    if (!height) height = document.getElementById('img_height').placeholder;
    let width = document.getElementById('img_width').value;
    if (!width) width = document.getElementById('img_width').placeholder;
    let center_x = document.getElementById('center_x').value;
    if (!center_x) center_x = document.getElementById('center_x').placeholder;
    let center_y = document.getElementById('center_y').value;
    if (!center_y) center_y = document.getElementById('center_y').placeholder;
    let pixel_per_unit = document.getElementById('pixel_per_unit').value;
    if (!pixel_per_unit) pixel_per_unit = document.getElementById('pixel_per_unit').placeholder;

    let formulas = [];
    for (let i = 0; i < id_count; i++) {
        let elem = document.getElementById(`input${i}`);
        if (elem.value) formulas.push(elem.value);
    }

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('graph_img').src ="data:image/png;base64," +  this.responseText;
            btn.innerHTML = 'Draw';
            btn.disabled = false;
        }
    };

    xmlhttp.open("POST", "/draw", true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send( JSON.stringify({height, width, center_x, center_y, pixel_per_unit, formulas}) );

}