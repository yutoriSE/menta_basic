//オーダー追加処理
addOrder.addEventListener('click',async () => {
    if(itemCode.value == ""){
        alert("商品コードを入力してください");
    }else if(itemNum.value == ""){
        alert("個数を入力してください");
    }else{
    
        if(await eel.add_order(itemCode.value, itemNum.value)()){
            alert("商品コードが間違っています");
        }else{
            itemCode.value = "";
            document.getElementById("itemNum").value = "";
        }
    }
});

//会計ボタン押下処理
checkout.addEventListener('click', (e) => {
    eel.view_order_item_info();
    chengeTotalAmountText();
});

//支払いボタン押下時の処理
pay.addEventListener('click',async () => {
    let tamount = await eel.get_total_amount()();
    //オーダーがあるか判定
    if(Number(tamount) == 0){
        alert("オーダーがありません")
    }else{
        if(paymentAmount.value == ""){
            alert("お支払い金額を入力してください");
        }else{
            eel.calc_payment(paymentAmount.value);
            chengeReturnAmountText();
            eel.export_receipt();
        }
    }
});

//ログ表示
eel.expose(view_log_js)
function view_log_js(text){
    log.value += text + "\n";
}

//総額をセット
async function chengeTotalAmountText(){
    let tamount = await eel.get_total_amount()();
    document.getElementById("totalAmount").innerText = tamount+"円" ;  
}

//おつりをセット
async function chengeReturnAmountText(){
    let ramount = await eel.get_return_amount()();
    if (Number(ramount) > 0){
        document.getElementById("returnAmount").innerText = ramount+"円";
    }
}

//ページ遷移
function link(target) {
    window.location.href=target;
}

//販売履歴のHTML更新
async function historyLoad() {
    let data = await eel.get_history()();
    var historyMain = document.getElementById("historyMain");
    
    //リストのクリア
    while(historyMain.firstChild){
        historyMain.removeChild(historyMain.firstChild);
    }
    
    historyMain.insertAdjacentHTML('beforeend', '<h3>販売履歴一覧</h3>');
    historyMain.insertAdjacentHTML('beforeend', '<table class="table" id="historyTable">')
    historyMain.insertAdjacentHTML('beforeend', '</table>');

    let table = document.getElementById('historyTable');

    var index = 1;
    for(var d of data){
        let newRow = table.insertRow();
        let newCell = newRow.insertCell();
        let newText = document.createTextNode(String(index++));
        newCell.appendChild(newText);

        newCell = newRow.insertCell();
        newText = document.createTextNode(d);
        newCell.appendChild(newText);
    }

    
}

//コンテンツ切替
historyNav.addEventListener('click', () => {
    
    //navberのavtive切替
    let pnav = document.getElementById("posNav");
    pnav.classList.remove("active");
    let hnav = document.getElementById("historyNav");
    hnav.classList.add("active");


    //posの操作
    var element = document.getElementById("posMain");
    state = element.style.display;

    if(state == "inline"){
        element.setAttribute("style","display:none");
    }
    //historyの操作
    var element = document.getElementById("historyMain");
    state = element.style.display;

    if(state == "none"){
        historyLoad()
        element.setAttribute("style", "display:inline");
    }
});

//コンテンツ切替
posNav.addEventListener('click', () => {

    //navberのavtive切替
    let pnav = document.getElementById("posNav");
    pnav.classList.add("active");
    let hnav = document.getElementById("historyNav");
    hnav.classList.remove("active");    

    //posの操作
    var element = document.getElementById("posMain");
    state = element.style.display;

    if(state == "none"){
        element.setAttribute("style", "display:inline");
    }
    //historyの操作
    var element = document.getElementById("historyMain");
    state = element.style.display;

    if(state == "inline"){
        element.setAttribute("style","display:none");
   }
});