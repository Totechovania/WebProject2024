function add_news() {
    console.log(cur_user_graphs);
    if (Object.keys(cur_user_graphs).length == 0) {
        alert("У вас нет ни одного графика");
        return;
    }
    let news_container = document.getElementById('news_container');
    let new_elem = document.createElement('div');
    let xmlhttps_get_cur_usr_info = new XMLHttpRequest();
    let info_template = {
        'news': {
            'title': 'Новая публикация',
            'content': '',
            'graph_id': Number(Object.keys(cur_user_graphs)[0]),
            'updated_date': '',
        },
        user: {},
        graph: {}
    }

    xmlhttps_get_cur_usr_info.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            info_template.user = JSON.parse(this.responseText);
            let xmlhttps_get_cur_graph_info = new XMLHttpRequest();
            xmlhttps_get_cur_graph_info.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    info_template.graph = JSON.parse(this.responseText).graph;
                    console.log(info_template);
                    new_elem.innerHTML = generate_news_card(info_template, news_card_id);
                    news_container.appendChild(new_elem);
                    edit_news_mode(news_card_id);
                    document.getElementById('card_title_input' + news_card_id).value = info_template.news.title;
                    let cancel_btn = document.getElementById('cancel_btn' + news_card_id);
                    const card_id = news_card_id;
                    cancel_btn.onclick = function () {
                        document.getElementById('news_card' + card_id).remove()
                    }
                    let submit_btn = document.getElementById('save_btn' + news_card_id);
                    submit_btn.innerHTML = "Опубликовать";
                    submit_btn.onclick = function () {
                        let req = {
                            'title': document.getElementById('card_title_input' + card_id).value,
                            'content': document.getElementById('news_text_input' + card_id).value,
                            'graph_id': info_template.news.graph_id,
                        }
                        let xmlhttps_new_news = new XMLHttpRequest();
                        xmlhttps_new_news.onreadystatechange = function () {
                            if (this.readyState == 4 && this.status == 200) {
                                location.reload();
                        }
                    }
                    xmlhttps_new_news.open("POST", "/api/new_news", true);
                    xmlhttps_new_news.setRequestHeader("Content-type", "application/json", );
                    xmlhttps_new_news.send(JSON.stringify(req));
                    }

                    news_card_id++;
            }}
            xmlhttps_get_cur_graph_info.open("GET", "/api/open_graph/" + info_template.news.graph_id, true);
            xmlhttps_get_cur_graph_info.send();
        }
    }
    xmlhttps_get_cur_usr_info.open("GET", "/api/user_info/" + cur_user_id, true);
    xmlhttps_get_cur_usr_info.send();
}