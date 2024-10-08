#!/usr/bin/env python

# mypy: ignore-errors
import torch
from trainer import load_model
from sklearn.metrics import classification_report

def classify_text(model, tokenizer, text, config):
    model.eval()
    encoding = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        return_token_type_ids=False,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )

    device = next(model.parameters()).device
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1)

    # 結果の取得
    predicted_class_id = logits.argmax().item()
    predicted_class = config.id_to_category[predicted_class_id]
    confidence = probabilities[0][predicted_class_id].item()

    # すべてのクラスの確率を取得
    all_probabilities = probabilities[0].cpu().numpy()
    class_probabilities = {config.id_to_category[i]: prob for i, prob in enumerate(all_probabilities)}

    # トークン化されたテキストの取得
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])

    # 注意重みの取得（最後の層の最初のヘッドを使用）
    attention_weights = outputs.attentions[-1][0, 0, 0].cpu().numpy()

    return {
        'text': text,
        'predicted_class': predicted_class,
        'confidence': confidence,
        'class_probabilities': class_probabilities,
        'tokens': tokens,
        'attention_weights': attention_weights
    }

test_reports = [
    # 起動障害
    {"text": "スマートフォンの電源ボタンを長押ししても反応がありません。", "category": "起動障害"},
    {"text": "ノートパソコンを開いても、ファンの音はするものの画面が点灯しません。", "category": "起動障害"},
    {"text": "タブレットが突然シャットダウンし、再起動を繰り返しています。", "category": "起動障害"},

    # 表示障害
    {"text": "ディスプレイの右半分が突然真っ暗になりました。", "category": "表示障害"},
    {"text": "画面全体がピンク色に変色し、正常な色が表示されません。", "category": "表示障害"},
    {"text": "モニターに縦縞の線が入り、画像が歪んで見えます。", "category": "表示障害"},

    # 音声障害
    {"text": "ヘッドホンを接続しても音が左側からしか聞こえません。", "category": "音声障害"},
    {"text": "スピーカーから雑音が constant に出続けています。", "category": "音声障害"},
    {"text": "音楽再生時に音が途切れ途切れになります。", "category": "音声障害"},

    # 操作障害
    {"text": "スマートフォンの画面の一部分だけタッチ操作が効かなくなりました。", "category": "操作障害"},
    {"text": "マウスのダブルクリックが認識されなくなりました。", "category": "操作障害"},
    {"text": "キーボードの特定のキーを押すと、別の文字が入力されてしまいます。", "category": "操作障害"},

    # 接続障害
    {"text": "Bluetoothイヤホンとペアリングできません。", "category": "接続障害"},
    {"text": "特定のウェブサイトにだけアクセスできません。", "category": "接続障害"},
    {"text": "外付けHDDを接続してもPCに認識されません。", "category": "接続障害"},

    # バッテリー問題
    {"text": "フル充電しても30分程度しか使用できません。", "category": "バッテリー問題"},
    {"text": "バッテリー残量が50%から急に0%になり、シャットダウンします。", "category": "バッテリー問題"},
    {"text": "充電中にバッテリーが異常に熱くなります。", "category": "バッテリー問題"},

    # ソフトウェア障害
    {"text": "新しいアプリをインストールしようとすると、毎回エラーが発生します。", "category": "ソフトウェア障害"},
    {"text": "特定のソフトウェアを起動すると、ブルースクリーンが表示されます。", "category": "ソフトウェア障害"},
    {"text": "システムのアップデート後、一部のアプリケーションが動作しなくなりました。", "category": "ソフトウェア障害"},

    # ハードウェア障害
    {"text": "ノートパソコンのヒンジが壊れて、蓋が閉じられなくなりました。", "category": "ハードウェア障害"},
    {"text": "DVDドライブからディスクが取り出せなくなりました。", "category": "ハードウェア障害"},
    {"text": "プリンターの給紙ローラーが動かず、用紙を吸い込みません。", "category": "ハードウェア障害"}
]

if __name__ == "__main__":
    # モデルをロード
    model, tokenizer, config = load_model(True)

    predictions = []
    true_labels = []

    for report in test_reports:
        result = classify_text(model, tokenizer, report["text"], config)
        print()
        print(f"入力テキスト: {result['text']}")
        print(f"予測されたカテゴリ: {result['predicted_class']}")
        print(f"信頼度: {result['confidence']:.4f}")
        print("\nすべてのカテゴリの確率:")
        print_string = "  "
        for category, prob in sorted(result['class_probabilities'].items(), key=lambda x: x[1], reverse=True):
            print_string += f"{category}: {prob:.4f}, "
        print(print_string)

        print("\nトークン化されたテキスト:")
        print_string = "  "
        for token, weight in zip(result['tokens'], result['attention_weights']):
            if token != '[PAD]':
                print_string += f"{token}: {weight:.4f}, "
        print(print_string)

        predictions.append(result['predicted_class'])
        true_labels.append(report['category'])

    # モデル評価
    model.eval()
    print(classification_report(true_labels, predictions))