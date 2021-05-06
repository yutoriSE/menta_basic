//結果出力
eel.expose(view_log_js);
function view_log_js(text){
    result.value += text + "\n";
}

//Enterキー押下時に翻訳実行
targetText.addEventListener('keypress', (e) => {
    if(e.keyCode == 13){
        var target = targetText.value;
        var select = selectLangage.value;

        result.value = "";

        if(select == 1){
            eel.translate_to_english(target);
        }else{
            eel.translate_to_japanese(target);
        }
    }
});