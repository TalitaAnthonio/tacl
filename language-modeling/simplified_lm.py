
# use open-ai gpt for gpt2 
# other models: xlnet-base-uncased, openai-gpt, gpt2, transfo-xl-wt103 (but very slow)
# ValueError: `num_return_sequences` has to be smaller or equal to `num_beams`.


from transformers import pipeline, set_seed, XLNetConfig, XLNetTokenizer, XLNetLMHeadModel,  OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
import json 
import torch 
import pdb 
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


# load the model 
model =  OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', cache_dir="../../model")
tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt', cache_dir="../../model")

# set parameters
num_return_sequences = 100 
num_beams = 100 
reference_length = 1 

# example text to predict 
text_to_predict = "If you want to make an appointment, check the number. Call "

# tokenize the text 
tokenized_text =  tokenizer.tokenize(text_to_predict)

# if the length is bigger or equal than 512, then take the tokenized_text[-512:] from left to right. 
if len(tokenized_text) >= 512: 

    inputs = tokenizer.encode(text_to_predict, add_special_tokens=False, return_tensors="pt") 


    inputs_truncated = inputs.tolist()[0]

    truncate_point = (512-reference_length) * -1 
    inputs_truncated = inputs_truncated[truncate_point:]
    

    # tensor([[ 645,  512,  823,  485,  925,  531, 7785,  240, 2457,  481, 2253,  239,1370]])
    inputs = torch.tensor(inputs_truncated, dtype=torch.int64).unsqueeze(0)

    # encoded inputs: 'if you want to make an appointment, check the number. call'
    encoded_inputs = tokenizer.decode(inputs[0])
    prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))


    # if using a gpu, then send the model to the device. 
    if device!='cpu': 
        outputs = model.generate(inputs, max_length=inputs.size()[1]+reference_length, num_return_sequences=num_return_sequences, num_beams=num_return_sequences)
        model.to(device)

    else: 
        outputs = model.generate(inputs, max_length=inputs.size()[1]+reference_length, num_return_sequences=num_return_sequences, num_beams=num_beams)

else: 

    inputs = tokenizer.encode(text_to_predict, add_special_tokens=False, return_tensors="pt") 
    encoded_inputs = tokenizer.decode(inputs[0])

    prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))


    print("tokenized_text length", len(tokenized_text))
    print("prompt length:", prompt_length)

    if device != 'cpu': 
        outputs = model.generate(inputs, max_length=inputs.size()[1]+reference_length, num_return_sequences=num_return_sequences, num_beams=num_return_sequences)
        model.to(device)

    else: 
        outputs = model.generate(inputs, max_length=inputs.size()[1]+reference_length, num_return_sequences=num_return_sequences, num_beams=num_beams)

# map the encoded indices of the predicted tokens to the tokens. 
results = {"generated_texts": [tokenizer.decode(outputs[i])[prompt_length:] for i in range(len(outputs))], "tokenized_in_model": encoded_inputs}

print(results)

