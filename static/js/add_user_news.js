let xmlhttps_add_user_news = new XMLHttpRequest();
xmlhttps_add_user_news.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let news_container = document.getElementById('news_container');
        let new_elem = document.createElement('div');
        new_elem.innerHTML = generate_news_card(JSON.parse(this.responseText), 1);
        news_container.appendChild(new_elem);
    }
}
xmlhttps_add_user_news.open("GET", "/api/open_news/1", true);
xmlhttps_add_user_news.send()