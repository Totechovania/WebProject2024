function generate_news_card(info, card_id) {
    console.log(info)
    let news_info = info.news
    let user_info = info.user
    let graph_info = info.graph




    let user_name_element_str = `<img src="data:image/png;base64,${user_info.avatar}" class="img-fluid rounded-circle border" alt="Card image" style="width: 40px; height: 40px;">
                            <a class="navbar-brand text-dark" href="/profile/${user_info.id}">${user_info.name}</a>
                            <label class="text-secondary">${news_info.updated_date} </label>`

    let news_element_str = `<div class="container-fluid">
                                    <h4 class="card-title" id="card_title${card_id}">${news_info.title}</h4>
                                    
                                    <div class="form-floating pb-3" hidden="hidden" id="news_title_input_container${card_id}">
                                       <input type="text" class="form-control" id="card_title_input${card_id}">
                                       <label for="card_title_input${card_id}">Заголовок</label>
                                    </div>
                                    
                                    <p class="card-text text-break" id="news_text${card_id}">
                                        ${news_info.content}
                                    </p> 
                                    
                                    <div class="form-floating pb-3" hidden="hidden" id="news_text_input_container${card_id}">
                                       <textarea class="form-control" id="news_text_input${card_id}" style="height: fit-content"></textarea>
                                       <label for="news_text_input${card_id}">Текст</label>
                                    </div>
                                    
                                    
                                    <select class="form-select" id="news_graph_select${card_id}" hidden="hidden" onchange="select_graph(${card_id}, document.getElementById('news_graph_select${card_id}').value)">  
                                    </select>
                                    
                                    <select class="form-select" id="news_privacy_select${card_id}" hidden="hidden">
                                        <option value="private">Приватный</option>
                                        <option value="public">Публичный</option>
                                    </select>
                                </div>`

    let privacy = graph_info.private ? "Приватный" : "Публичный";
    let graph_element_str = `<img class="card-img-top rounded-start-0" src="data:image/png;base64,${graph_info.preview}" alt="graph image" id="news_graph_img${card_id}">
                                    <div class="card-body">
                                      <label id="graph_id_label${card_id}" hidden="hidden">${graph_info.id}</label>
                                      <h5 class="card-title" id="news_graph_title${card_id}">${graph_info.name}</h5>
                                      <p class="card-text" id="news_graph_privacy${card_id}">${privacy}</p>
                                      <div class="d-flex flex-row justify-content-end">
                                        <a href="/graph/${graph_info.id}" class="btn btn-primary" id="news_graph_link${card_id}">Открыть</a>
                                      </div>
                                    </div>`


    return `<div class="d-flex flex-row p-1" id="news_card${card_id}">
                    <div class="card rounded-end-0">
                        <div class="card-header" id="card_header${card_id}">
                            ${user_name_element_str}
                        </div>
                        <div class="card-body p-1">
                                ${news_element_str}
                        </div>
                        <div class="card-footer d-flex flex-row justify-content-end p-1">
                            <div class="btn p-1 text-danger" onclick="delete_news(${news_info.id}, ${card_id})" id="del_btn${card_id}" ${news_info.user_id===cur_user_id ? '' : 'hidden="hidden"'}"  onclick= "delete_news(${news_info.id})" > Удалить</div>
                            <div class="btn p-1 text-secondary" onclick="edit_news_mode(${card_id})" id="edit_btn${card_id}" ${news_info.user_id===cur_user_id ? '' : 'hidden="hidden"'} > Редактировать</div>
                            <div class="btn p-1 text-secondary" hidden="hidden" id="cancel_btn${card_id}" onclick="normal_news_mode(${card_id})"> Отменить</div>
                            <div class="btn p-1 text-primary" hidden="hidden" id="save_btn${card_id}" onclick="save_news(${news_info.id}, ${card_id})"> Сохранить</div>
                        </div>  
                    </div>
                    <div class="card rounded-start-0" style="width: 200px">
                        ${graph_element_str}
                    </div>
                  </div>`
}
