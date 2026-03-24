import pickle
import os
import torch

from excel_extract import process_text_pipeline

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'bilstm_traced.pt')
mapping_path = os.path.join(script_dir, 'mappings.pkl')

model = torch.jit.load(model_path, map_location=torch.device('cpu'))
model.eval()

with open(mapping_path, 'rb') as f:
    mappings = pickle.load(f)

word2idx = mappings['word2idx']
idx2tag = mappings['idx2tag']


def encode(sentence):
    unk = word2idx.get("<UNK>", 1)
    return [word2idx.get(str(w), unk) for w in sentence]


def predict(text):
    tokens = process_text_pipeline(text)

    encoded = torch.tensor([encode(tokens)])

    with torch.no_grad():
        logits = model(encoded)
        preds = logits.argmax(-1).squeeze(0)

    results = []
    for token, p in zip(tokens, preds):
        tag = idx2tag[p.item()]
        results.append({
            'token': token,
            'tag': tag
        })

    return results, tokens


def extract_entities(predictions):
    entities = []
    current_entity = None
    current_tokens = []

    for pred in predictions:
        tag = pred['tag']
        token = pred['token']

        if tag.startswith('B-'):
            if current_entity:
                entities.append({
                    'type': current_entity,
                    'value': ''.join(current_tokens),
                    'tokens': current_tokens.copy()
                })
            current_entity = tag[2:]
            current_tokens = [token]

        elif tag.startswith('I-'):
            if current_entity == tag[2:]:
                current_tokens.append(token)
            else:
                if current_entity:
                    entities.append({
                        'type': current_entity,
                        'value': ''.join(current_tokens),
                        'tokens': current_tokens.copy()
                    })
                current_entity = tag[2:]
                current_tokens = [token]
        else:
            if current_entity:
                entities.append({
                    'type': current_entity,
                    'value': ''.join(current_tokens),
                    'tokens': current_tokens.copy()
                })
                current_entity = None
                current_tokens = []

    if current_entity:
        entities.append({
            'type': current_entity,
            'value': ''.join(current_tokens),
            'tokens': current_tokens.copy()
        })

    return entities


def extract_entity_by_type(entities, entity_type):
    values = [entity['value'] for entity in entities if entity['type'] == entity_type]
    return ' '.join(values) if values else None


def extract_all_entities_by_type(entities):
    result = {}
    for entity in entities:
        entity_type = entity['type']
        if entity_type not in result:
            result[entity_type] = []
        result[entity_type].append(entity['value'])
    return {k: ' '.join(v) for k, v in result.items()}
