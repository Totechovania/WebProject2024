let xmlhttps_add_user_news = new XMLHttpRequest();
let news_card_id = 0
xmlhttps_add_user_news.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let news_container = document.getElementById('news_container');
        let usr_news = JSON.parse(this.responseText);
        for (let i = 0; i < usr_news.length; i++) {
            let new_elem = document.createElement('div');
            new_elem.innerHTML = generate_news_card(usr_news[i], news_card_id);
            news_container.appendChild(new_elem);
            news_card_id++;
        }

    }
}
xmlhttps_add_user_news.open("GET", "/api/user_news/" + usr_id, true);
xmlhttps_add_user_news.send()