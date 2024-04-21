function save_news(news_id, card_id) {
    let title = document.getElementById('card_title_input' + card_id).value;
    let content = document.getElementById('news_text_input' + card_id).value;
    let graph_id = document.getElementById('news_graph_select' + card_id).value;

    let xmlhttps_save_news = new XMLHttpRequest();
    let req = {
        'title': title,
        'content': content,
        'graph_id': graph_id
    }
    xmlhttps_save_news.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            location.reload();
        }
    }
    xmlhttps_save_news.open("POST", "/api/update_news/" + news_id, true);
    xmlhttps_save_news.setRequestHeader("Content-type", "application/json", );
    xmlhttps_save_news.send(JSON.stringify(req));
}