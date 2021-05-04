//pythonからリスト受け取って、HTMLタグ追加していく処理

try{
    window.onload = function loadHistory(){
        alert("test")
        let data = await eel.get_history()();
        for(var d of data){
            historyBody.insertAdjacentHTML('afterbegin', '<p>'+d+'</p>');
        }
    }
} catch(error){
    console.error(error)
}

//ページ遷移
function link(target) {
    window.location.href=target;
}