from googletrans import Translator

translator = Translator()

text = input("翻訳する日本語テキストを入力してください＞")
print(translator.translate(text, dest="en").text)
