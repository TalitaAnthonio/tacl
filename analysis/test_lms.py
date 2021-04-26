from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer
import torch
import pdb 
from transformers import BigBirdTokenizer, BigBirdForPreTraining, XLNetLMHeadModel, XLNetTokenizer

model_path='xlnet-base-cased'
model =   XLNetLMHeadModel.from_pretrained(model_path, cache_dir="../../model")
tokenizer = XLNetTokenizer.from_pretrained(model_path, cache_dir="../../model")


#tokenizer = BigBirdTokenizer.from_pretrained('google/bigbird-roberta-base')
#model = BigBirdForPreTraining.from_pretrained('google/bigbird-roberta-base')

#model =  OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', cache_dir="../../model")
#tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt', cache_dir="../../model")

inputs = tokenizer("The capital of France is ", return_tensors="pt")['input_ids']

outputs = model.generate(inputs, max_length=inputs.size(1)+2, num_return_sequences=10, num_beams=10)

print(outputs) 
for output in outputs: 
    encoded = tokenizer.decode(output)
    print(encoded)