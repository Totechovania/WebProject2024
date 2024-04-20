function delete_news(news_id) {
    if  (confirm( "Вы уверены, что хотите удалить публикацию?" )){
        let xmlhttps_delete_news = new XMLHttpRequest();
        xmlhttps_delete_news.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                location.reload();
            }
        }
        xmlhttps_delete_news.open("DELETE", "/api/delete_news/" + news_id, true);
        xmlhttps_delete_news.send();
    }
}