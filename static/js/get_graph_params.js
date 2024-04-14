function get_graph_params() {

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
    let colors = [];
    for (let i = 0; i < id_count; i++) {
        let elem = document.getElementById(`input${i}`);
        if (elem) {
            formulas.push(elem.value);
            colors.push(document.getElementById(`color_input${i}`).value);
        }
    }

    return {height, width, center_x, center_y, pixel_per_unit, formulas, colors}
}
