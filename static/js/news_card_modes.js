function edit_news_mode(card_id) {
    document.getElementById('card_title' + card_id).hidden = true;
    document.getElementById('news_title_input_container' + card_id).hidden = false;
    document.getElementById('card_title_input' + card_id).value = document.getElementById('card_title' + card_id).innerHTML;

    document.getElementById('news_text' + card_id).hidden = true;
    document.getElementById('news_text_input_container' + card_id).hidden = false;
    document.getElementById('news_text_input' + card_id).value = document.getElementById('news_text' + card_id).innerHTML;

    document.getElementById('del_btn' + card_id).hidden = true;
    document.getElementById('edit_btn' + card_id).hidden = true;

    document.getElementById('cancel_btn' + card_id).hidden = false;
    document.getElementById('save_btn' + card_id).hidden = false;

    document.getElementById('news_graph_select' + card_id).hidden = false;

    generate_select_options(card_id);
}

function normal_news_mode(card_id) {
    document.getElementById('card_title' + card_id).hidden = false;
    document.getElementById('news_title_input_container' + card_id).hidden = true;

    document.getElementById('news_text' + card_id).hidden = false;
    document.getElementById('news_text_input_container' + card_id).hidden = true;

    document.getElementById('del_btn' + card_id).hidden = false;
    document.getElementById('edit_btn' + card_id).hidden = false;

    document.getElementById('cancel_btn' + card_id).hidden = true;
    document.getElementById('save_btn' + card_id).hidden = true;

    document.getElementById('news_graph_select' + card_id).hidden = true;

    select_graph(card_id, Number(document.getElementById('graph_id_label' + card_id).innerHTML));
}