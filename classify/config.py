from samples.category import trouble_categories

class Config(dict):
    categories = trouble_categories
    # カテゴリを数値にマッピング
    category_to_id = {category: id for id, category in enumerate(categories)}
    id_to_category = {id: category for category, id in category_to_id.items()}

    bert_pretrained_tokenizer = "tohoku-nlp/bert-large-japanese-v2"
    bert_pretrained_model = 'tohoku-nlp/bert-large-japanese-v2'

    trained_dir = "models"
    trained_tokenizer = "bert_trouble_report_tokenizer"
    trained_model = "bert_trouble_report_classifier.pth"