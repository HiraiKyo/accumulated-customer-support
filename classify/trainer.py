#!/usr/bin/env python

# mypy: ignore-errors
import os
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import BertForSequenceClassification, BertJapaneseTokenizer, BertConfig
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from config import Config
from samples.text import trouble_reports
import argparse

class TroubleReportDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def train_bert_classifier(model, tokenizer, trouble_reports, config, num_epochs=5, batch_size=16, learning_rate=2e-5):
    # データの準備
    texts = [report['text'] for report in trouble_reports]
    labels = [config.category_to_id[report['category']] for report in trouble_reports]

    # データの分割
    train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

    # データセットとデータローダーの作成
    train_dataset = TroubleReportDataset(train_texts, train_labels, tokenizer, max_length=128)
    val_dataset = TroubleReportDataset(val_texts, val_labels, tokenizer, max_length=128)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # デバイスの設定
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # オプティマイザーの設定
    optimizer = AdamW(model.parameters(), lr=learning_rate)

    # トレーニングループ
    for epoch in range(num_epochs):
        model.train()
        for batch in train_dataloader:
            optimizer.zero_grad()
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

        # 評価
        model.eval()
        val_preds = []
        val_true = []

        with torch.no_grad():
            for batch in val_dataloader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)

                outputs = model(input_ids, attention_mask=attention_mask)
                _, preds = torch.max(outputs.logits, dim=1)

                val_preds.extend(preds.cpu().tolist())
                val_true.extend(labels.cpu().tolist())

        print(f"Epoch {epoch + 1}/{num_epochs}")
        print(classification_report([config.id_to_category[i] for i in val_true], [config.id_to_category[i] for i in val_preds]))

    return model, tokenizer

def save_model(model, tokenizer, config: Config):
    if not os.path.exists(config.trained_dir):
        os.makedirs(config.trained_dir)
    model.save_pretrained(f"{config.trained_dir}")
    tokenizer.save_pretrained(f"{config.trained_dir}")
    torch.save(config.category_to_id, os.path.join(config.trained_dir, 'category_mapping.pt'))

def load_model(trained = False):
    config = Config()
    # モデルの読み込み
    model = None
    tokenizer = None
    if trained is True:
        model_config = BertConfig.from_pretrained(Config.bert_pretrained_model)
        model_config.output_attentions = True
        model_config.num_labels = len(config.categories)
        model = BertForSequenceClassification.from_pretrained(f"{config.trained_dir}", config=model_config)
        tokenizer = BertJapaneseTokenizer.from_pretrained(f"{config.trained_dir}")
        config.category_to_id = torch.load(os.path.join(config.trained_dir, 'category_mapping.pt'))
        config.id_to_category = {id: category for category, id in config.category_to_id.items()}
    else:
        model_config = BertConfig.from_pretrained(Config.bert_pretrained_model)
        model_config.output_attentions = True
        model_config.num_labels = len(config.categories)
        model = BertForSequenceClassification.from_pretrained(Config.bert_pretrained_model, config=model_config)
        tokenizer = BertJapaneseTokenizer.from_pretrained(Config.bert_pretrained_tokenizer)

    return model, tokenizer, config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--trained', type=bool, default=None)

    trained = parser.parse_args().trained

    # 前回モデルのロード
    model, tokenizer, config = load_model(trained)
    # 訓練データ
    reports = trouble_reports
    # モデルのトレーニング
    model, tokenizer = train_bert_classifier(model, tokenizer, reports, config)
    # モデルの保存
    save_model(model, tokenizer, config)
