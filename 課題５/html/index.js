//オーダー追加処理
addOrder.addEventListener('click', () => {
    if(itemCode.value == ""){
        alert("商品コードを入力してください");
    }else if(itemNum.value == ""){
        alert("個数を入力してください");
    }else{
        eel.add_order(itemCode.value, itemNum.value);
        itemCode.value = "";
        document.getElementById("itemNum").value = "";
    }
});

//会計ボタン押下処理
checkout.addEventListener('click', (e) => {
    eel.view_order_item_info();
    chengeTotalAmountText();
});

//支払いボタン押下時の処理
pay.addEventListener('click', () => {
    if(paymentAmount.value == ""){
        alert("お支払い金額を入力してください");
    }else{
        eel.calc_payment(paymentAmount.value);
        chengeReturnAmountText();
        eel.export_receipt();
    }
});

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
    document.getElementById("returnAmount").innerText = ramount+"円" ;  
}
