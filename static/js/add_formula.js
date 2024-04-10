let id_count = 0;
function add_formula() {
    var container = document.createElement("div");
    container.innerHTML = `<div class="d-flex flex-row  p-1 bg-light border-1" id="input${id_count}_container">
    <input type="text" id="input${id_count}">
    <button type="button" class="btn" onclick="document.getElementById('input${id_count}_container').remove()">delete</button>
    </div>`;
    document.getElementById("formulas").appendChild(container);
    document.getElementById(`input${id_count}`).focus();
    id_count += 1;
}
