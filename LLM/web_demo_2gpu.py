from transformers import AutoModel, AutoTokenizer
import gradio as gr
import mdtex2html

from typing import Dict, Tuple, Union, Optional
from utils import load_model_on_gpus


#import torch
#torch.cuda.set_device(1)

def fix_configure_device_map() -> Dict[str, int]:
    # transformer.word_embeddings 占用1层
    # transformer.final_layernorm 和 lm_head 占用1层
    # transformer.layers 占用 28 层
    # 总共30层分配到num_gpus张卡上

    num_trans_layers = 28

    # bugfix: 在linux中调用torch.embedding传入的weight,input不在同一device上,导致RuntimeError
    # windows下 model.device 会被设置成 transformer.word_embeddings.device
    # linux下 model.device 会被设置成 lm_head.device
    # 在调用chat或者stream_chat时,input_ids会被放到model.device上
    # 如果transformer.word_embeddings.device和model.device不同,则会导致RuntimeError
    # 因此这里将transformer.word_embeddings,transformer.final_layernorm,lm_head都放到第一张卡上
    device_map = {'transformer.word_embeddings': 0,
                  'transformer.final_layernorm': 0, 'lm_head': 0}

    # GPU0 - 6GB; GPU1 - 12GB
    # 将前8个Transformer layers 放置在GPU0上，其他的放置在GPU1上
    gpu0_layers = 8
    gpu1_layers = num_trans_layers - gpu0_layers
    gpu_target = 0
    for i in range(num_trans_layers):
        if i >= gpu0_layers:
            gpu_target = 1
        device_map[f'transformer.layers.{i}'] = gpu_target

    return device_map

# chatglm2-b6和chatglm-6b结构有所不同,参考chatglm-6b的device_map修改
def fix_configure_device_map_v2() -> Dict[str, int]:
    # transformer.layers 占用 28 层
    # 总共30层分配到num_gpus张卡上

    num_trans_layers = 28

    device_map = {'transformer.embedding.word_embeddings': 0,
                  'transformer.rotary_pos_emb': 0,
                  'transformer.encoder.final_layernorm': 0,
                  'transformer.output_layer': 0,
                  'lm_head': 0}

    # GPU0 - 6GB; GPU1 - 12GB
    # 将前8个Transformer layers 放置在GPU0上，其他的放置在GPU1上
    gpu0_layers = 8
    gpu1_layers = num_trans_layers - gpu0_layers
    gpu_target = 0
    for i in range(num_trans_layers):
        if i >= gpu0_layers:
            gpu_target = 1
        device_map[f'transformer.encoder.layers.{i}'] = gpu_target

    return device_map

model_path = "../chatglm2-6b-model"
print("Load mode: "+model_path)

#tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
#model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)


if "chatglm2" in model_path:
    model = load_model_on_gpus(model_path, num_gpus=2, device_map=fix_configure_device_map_v2())
else:
    model = load_model_on_gpus(model_path, num_gpus=2, device_map=fix_configure_device_map())


model = model.eval()
#print(model)

"""Override Chatbot.postprocess"""


def postprocess(self, y):
    if y is None:
        return []
    for i, (message, response) in enumerate(y):
        y[i] = (
            None if message is None else mdtex2html.convert((message)),
            None if response is None else mdtex2html.convert(response),
        )
    return y


gr.Chatbot.postprocess = postprocess


def parse_text(text):
    """copy from https://github.com/GaiZhenbiao/ChuanhuChatGPT/"""
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>"+line
    text = "".join(lines)
    return text


def predict(input, chatbot, max_length, top_p, temperature, history):
    chatbot.append((parse_text(input), ""))
    for response, history in model.stream_chat(tokenizer, input, history, max_length=max_length, top_p=top_p,
                                               temperature=temperature):
        chatbot[-1] = (parse_text(input), parse_text(response))       

        yield chatbot, history


def reset_user_input():
    return gr.update(value='')


def reset_state():
    return [], []


with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">ChatGLM</h1>""")

    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10).style(
                    container=False)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("Submit", variant="primary")
        with gr.Column(scale=1):
            emptyBtn = gr.Button("Clear History")
            max_length = gr.Slider(0, 4096, value=2048, step=1.0, label="Maximum length", interactive=True)
            top_p = gr.Slider(0, 1, value=0.7, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0, 1, value=0.95, step=0.01, label="Temperature", interactive=True)

    history = gr.State([])

    submitBtn.click(predict, [user_input, chatbot, max_length, top_p, temperature, history], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)

demo.queue().launch(share=True, inbrowser=True)
