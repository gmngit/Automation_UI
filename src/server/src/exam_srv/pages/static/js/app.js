const api_url = "/api/v1";
const per_page = "?per_page=9"
let srvModal

form_result_handlers = {
    "registration-form" : signUp,
    "login-form": signIn,
    "add-server-form": addServer,
    "server-list": fillServerList,
    "myself": fillMyself,
    "logout": logout,
}

window.onload = function(){
    console.log("Page ready!")

    // Находим все формы на странице
    const forms = document.querySelectorAll('form');

    // Для каждой формы добавляем обработчик на кнопку submit
    forms.forEach(form => {
      console.log("Add form handler:", form.id)
      form.addEventListener('submit', (event) => {
        event.preventDefault(); // Отменяем стандартное поведение формы
        // Вызываем метод send_post и передаем в него ссылку на форму
        send_post(form.action, new FormData(form), form.id);
        return false
      });
    });

    srv_form = document.getElementById("add-server-form")
    if (srv_form) {
        srvModal = new bootstrap.Modal('#addServerModal', {})
        addServerFormConfig()
        send_get(api_url+"/auth/user", [], 'myself')
        send_get(api_url+"/servers"+per_page, [], 'server-list')
        // let logout_btn = document.getElementById("logout-btn")
        // if (logout_btn){
        //     logout_btn.addEventListener("click", (event)=>{
        //         event.preventDefault();
        //         send_get("/auth/logout", [], 'logout')
        //     })
        // }
        let api_links = document.querySelectorAll(".api-btn")
        if (api_links){
            api_links.forEach(link=>{
                link.addEventListener("click", event=>{
                    event.preventDefault();
                    send_get(event.target.href, [], event.target.dataset.action)
                })
                
            })
        }
    }
}

async function send_post(endpoint, formData, form_name){
    console.log("Send post", form_name)
    headers = {}
    token = getCookie('access_token') || ""
    if (token != ""){
        headers = {
            "Authorization": "Bearer "+token
        }
    }
    let response = await fetch(endpoint, {
      method: 'POST',
      headers: headers,
      body: formData
    });
    switch (response.status) {
        case 200: //успешно
        case 201: //создано
            if (form_result_handlers[form_name]) {
                let json = await response.json();
                form_result_handlers[form_name](json)
            }
            break
        case 204: //No content
            if (form_result_handlers[handler]) {
                //let json = await response.json();
                form_result_handlers[form_name]({})
            }
            break
        case 401: //Требуется токен
        case 403: //Требуется токен
            setTimeout(()=>{
                    if (window.location['pathname'] != "/signin" && window.location['pathname'] != "/signup"){
                        window.location.replace("/signin")
                    }
                }, 3000)
        case 400:
        case 409: //Объект уже существует
            //TODO: показать сообщение об ошибке
        case 500: //ошибка сервера
            //TODO: показать сообщение об ошибке
        default:
            //TODO: показать сообщение об ошибке
            let json = await response.json();
            appendAlert(json["message"],"danger")
    }
}

async function send_get(endpoint, formData, handler){
    console.log("Send get", handler)
    headers = {}
    token = getCookie('access_token') || ""
    if (token != ""){
        headers = {
            "Authorization": "Bearer "+token
        }
    }
    let response = await fetch(endpoint, {
      method: 'GET',
      headers: headers,
    });
    switch (response.status) {
        case 200: //успешно
            if (form_result_handlers[handler]) {
                let json = await response.json();
                form_result_handlers[handler](json)
            }
            break
        case 204: //No content
            if (form_result_handlers[handler]) {
                //let json = await response.json();
                form_result_handlers[handler]({})
            }
            break
        case 404: //Not found
            break
        case 401: //Требуется авторизация
        case 403: //Требуется токен
            setTimeout(()=>{
                    if (window.location['pathname'] != "/signin" || window.location['pathname'] != "/signup"){
                        window.location.replace("/signin")
                    }
                }, 3000)
        case 400:
        case 409: //Объект уже существует
            //TODO: показать сообщение об ошибке
        case 500: //ошибка сервера
            //TODO: показать сообщение об ошибке
        default:
            //TODO: показать сообщение об ошибке
            let json = await response.json();
            appendAlert(json["message"],"danger", "page-alert")
    }
}


async function send_delete(endpoint, formData, handler){
    console.log("Send delete", handler)
    headers = {}
    token = getCookie('access_token') || ""
    if (token != ""){
        headers = {
            "Authorization": "Bearer "+token
        }
    }
    let response = await fetch(api_url+endpoint, {
      method: 'DELETE',
      headers: headers,
    });
    switch (response.status) {
        case 200: //успешно
            if (form_result_handlers[handler]) {
                let json = await response.json();
                form_result_handlers[handler](json)
            }
            break
        case 204: //No content
            if (form_result_handlers[handler]) {
                //let json = await response.json();
                form_result_handlers[handler]({})
            }
            break
        case 401: //Требуется авторизация
        case 403: //Требуется токен
            setTimeout(()=>{
                    if (window.location['pathname'] != "/signin" || window.location['pathname'] != "/signup"){
                        window.location.replace("/signin")
                    }
                }, 3000)
        case 400:
        case 409: //Объект уже существует
            //TODO: показать сообщение об ошибке
        case 500: //ошибка сервера
            //TODO: показать сообщение об ошибке
        default:
            //TODO: показать сообщение об ошибке
            let json = await response.json();
            appendAlert(json["message"],"danger", "page-alert")
    }
}


function signUp(result){
    //Пользователь зарегистрирован
    console.log(result)
    document.cookie = `access_token=${result['access_token']}`
    window.location.replace("/profile")
}

function signIn(result){
    //Пользователь авторизовался
    console.log(result)
    document.cookie = `access_token=${result['access_token']}`
    window.location.replace("/profile")
}

function addServer(result){
    //Пользователь добавил сервер
    console.log(result)
    send_get(api_url+"/servers"+per_page, [], 'server-list')
    srvModal.hide();
}


function appendAlert(message, type, alert_placeholder = 'form-alert'){
  const alertPlaceholder = document.getElementById(alert_placeholder)
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

function setServerName(elem){
    const name = document.getElementById('name')
    const cpu_value = document.getElementById('cpu').value
    //const ram_value = document.getElementById('ram').value
    let ram_value = 0
    document.getElementsByName("ram").forEach((elem)=>{
        if (elem.checked) {
            ram_value = elem.value
        }
    })
    const ssd_value = document.getElementById('ssd').value
    document.getElementById("ssd_value").innerHTML = ssd_value
    const geo_value = document.getElementById('location').value
    rand_name = ""
    for (let i=0; i<8; i++){
        rand_name += String.fromCharCode(Math.floor(Math.random()*25+65))
    }
    name.value = `${geo_value}-${cpu_value}CPU-${ram_value}RAM-${ssd_value}SSD-${rand_name}`
}

function setDeadline(elem){
    let period = parseInt(document.getElementById('period').value)
    let now = new Date()
    let month = now.getMonth()
    now.setMonth(month + period)
    const deadline = document.getElementById('deadline')
    deadline.value = `${now.getFullYear()}-${now.getMonth()+1}-${now.getDay()+1}`
}

function addServerFormConfig(){
    const form = document.getElementById('add-server-form')
    const inputs = form.querySelectorAll("input")
    inputs.forEach((elem)=>{
        if (['cpu', 'ram1', 'ram2', 'ram4', 'ram8', 'ram16', 'ssd', 'location'].indexOf(elem.id) != -1){
            elem.onchange = setServerName
        }
    })
    const selects = form.querySelectorAll("select")
    selects.forEach((elem)=>{
        if (elem.id == 'location'){
            elem.onchange = setServerName
        }else if (elem.id == 'period'){
            elem.onchange = setDeadline
        }
    })
    setServerName()
    setDeadline()
}

function getCookie(name){
    let cookies = document.cookie.split(";")
    for(let i=0; i<cookies.length; i++){
        elem = cookies[i].split("=")
        if (elem[0] == name){
            return elem[1]
        }
    }
    return null
}

function fillServerList(result){
    if (!result["items"]){
        send_get(api_url+"/servers"+per_page, [], 'server-list')
        return
    }
    const serverPlaceholder = document.getElementById('server-list')
    serverPlaceholder.innerHTML = ""
    if (result["items"]){
        for (let i=0; i<result['items'].length; i++){
            let item = result['items'][i]
            if (item['owner']['public_id'] == document.myself['public_id']){
                const wrapper = document.createElement('div')
                wrapper.className = "col-4 d-flex flex-column p-3"
                wrapper.innerHTML = [
                    `
                        <div class="card">
                            <div class="card-header">
                                <a href="${item['link']}" target="_blank">${item['name']}</a>
                            </div>
                            <div class="card-body">
                                <p class="card-text">
                                    ${item['cpu']} CPU<br>
                                    ${item['ram']} Gb RAM <br>
                                    ${item['ssd']} Gb SSD <br>
                                    ${item['location']}<br>
                                    <small>${item['time_remaining']}</small>
                                </p>
                            </div>
                            <div class="card-footer"><a href="#" class="btn del-server-btn  btn-outline-danger" data-srv-name='${item['name']}'>Удалить</a></div>
                        </div>
                    `
                ].join('')
                serverPlaceholder.append(wrapper)
            }
        }
    }

    if (result["links"]){
        let link_bar = document.getElementById("links_bar")
        link_bar.innerHTML = ""
        if(result["links"]["first"]){
            const wrapper = document.createElement('a')
            wrapper.className = "btn btn-outline-primary api-btn"
            wrapper.href = result["links"]["first"]
            wrapper.text = "«"
            wrapper.dataset.action = "server-list"
            link_bar.append(wrapper)
        }
        if(result["links"]["prev"]){
            const wrapper = document.createElement('a')
            wrapper.className = "btn btn-outline-primary api-btn"
            wrapper.href = result["links"]["prev"]
            wrapper.text = "‹"
            wrapper.dataset.action = "server-list"
            link_bar.append(wrapper)
        }
        if(result["links"]["self"]){
            const wrapper = document.createElement('a')
            wrapper.className = "btn btn-outline-primary api-btn"
            wrapper.href = result["links"]["self"]
            wrapper.text = result["page"]
            wrapper.dataset.action = "server-list"
            link_bar.append(wrapper)
        }
        if(result["links"]["next"]){
            const wrapper = document.createElement('a')
            wrapper.className = "btn btn-outline-primary api-btn"
            wrapper.href = result["links"]["next"]
            wrapper.text = "›"
            wrapper.dataset.action = "server-list"
            link_bar.append(wrapper)
        }
        if(result["links"]["last"]){
            const wrapper = document.createElement('a')
            wrapper.className = "btn btn-outline-primary api-btn"
            wrapper.href = result["links"]["last"]
            wrapper.text = "»"
            wrapper.dataset.action = "server-list"
            link_bar.append(wrapper)
        }
    }

    del_btns = document.querySelectorAll(".del-server-btn")
    if (del_btns){
        del_btns.forEach((elem)=>{
            elem.addEventListener("click", (event)=>{
                event.preventDefault();
                server_name = event.target.dataset.srvName
                if (confirm("Вы действительно хотите удалить сервер: "+server_name)){
                    send_delete(`/servers/${server_name}`, [], 'server-list')
                }

            })

        })
    }

    let api_links = document.querySelectorAll(".api-btn")
        if (api_links){
            api_links.forEach(link=>{
                link.addEventListener("click", event=>{
                    event.preventDefault();
                    send_get(event.target.href, [], event.target.dataset.action)
                })
                
            })
        }
}

function fillMyself(result){
    document.myself = result;
//    "email": "string",
//    "public_id": "string",
//    "admin": true,
//    "registered_on": "string",
//    "token_expires_in": "string"
    document.getElementById("user_email").innerHTML=result["email"]
}

function logout(result){
    window.location.replace("/signin")
}