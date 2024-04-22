# !/usr/bin/env python3
"""
==== No Bugs in code, just some Random Unexpected FEATURES ====
┌─────────────────────────────────────────────────────────────┐
│┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐│
││Esc│!1 │@2 │#3 │$4 │%5 │^6 │&7 │*8 │(9 │)0 │_- │+= │|\ │`~ ││
│├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┤│
││ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │{[ │}] │ BS  ││
│├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤│
││ Ctrl │ A │ S │ D │ F │ G │ H │ J │ K │ L │: ;│" '│ Enter  ││
│├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────┬───┤│
││ Shift  │ Z │ X │ C │ V │ B │ N │ M │< ,│> .│? /│Shift │Fn ││
│└─────┬──┴┬──┴──┬┴───┴───┴───┴───┴───┴──┬┴───┴┬──┴┬─────┴───┘│
│      │Fn │ Alt │         Space         │ Alt │Win│   HHKB   │
│      └───┴─────┴───────────────────────┴─────┴───┘          │
└─────────────────────────────────────────────────────────────┘

测试训练好的模型。

Author: pankeyu
Date: 2023/01/11
"""
from typing import List

import torch
from rich import print
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def inference(
    model, 
    tokenizer, 
    sentences: List[str],
    device: str,
    batch_size=16,
    max_seq_len=128
    ) -> List[int]:
    """
    Args:
        model (_type_): _description_
        tokenizer (_type_): _description_
        sentences (List[str]): _description_
        batch_size (int, optional): _description_. Defaults to 16.
        max_seq_len (int, optional): _description_. Defaults to 128.

    Returns:
        List[int]: [laebl1, label2, label3, ...]
    """
    res = []
    for i in range(0, len(sentences), batch_size):
        batch_sentence = sentences[i:i+batch_size]
        ipnuts = tokenizer(
            batch_sentence,
            truncation=True,
            max_length=max_seq_len,
            padding='max_length',
            return_tensors='pt'
        )
        output = model(
            input_ids=ipnuts['input_ids'].to(device),
            token_type_ids=ipnuts['token_type_ids'].to(device),
            attention_mask=ipnuts['attention_mask'].to(device),
        ).logits
        output = torch.argmax(output, dim=-1).cpu().tolist()
        res.extend(output)
    return res


if __name__ == '__main__':
    device = 'cuda:0'                                                  # 指定GPU设备
    saved_model_path = 'checkpoints/94ai/model_best'       # 训练模型存放地址
    tokenizer = AutoTokenizer.from_pretrained(saved_model_path) 
    model = AutoModelForSequenceClassification.from_pretrained(saved_model_path) 
    model.to(device).eval()

    sentences = [
        '[0:43.320,0:45.490]  哦，好的好的，可以可以好。',
        '喂，你好，我这边是分期乐的客户经理啊，啊，就您之前是有在我们平台有借过款的，您这边手机上是还有分期乐APP吗',
    ]
    res = inference(model, tokenizer, sentences, device)
    print('res: ', res)