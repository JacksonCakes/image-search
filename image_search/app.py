from flask import Flask, render_template , request , jsonify
from PIL import Image
import numpy as np
import re
import torch
from io import BytesIO
import base64
import clip
import torch
import torch.nn.functional as F
from utils.utils import load_embeddings
app = Flask(__name__)
device = None 
args = None 
model, preprocess = None
embeddings = None 
@app.route('/')
def home():
	return render_template('./index.html')

@app.route('/imgSearch' , methods=['POST'])
def search_img():
	img_data = re.sub('^data:image/.+;base64,', '', request.form['imageBase64'])
	img_raw = Image.open(BytesIO(base64.b64decode(img_data)))
	with torch.no_grad():
		target = model.encode_image(preprocess(img_raw)).unsqueeze(0).to(device)
	top_img = compute_similarity(target,embeddings)
	return jsonify({'htmlresponse': render_template('./response.html', filenames=top_img)}) 


def compute_similarity(target,vector_dict):
	res = set()
	max_sim = float('-inf')
	for name,embedding in vector_dict.items():
		cos_sim = F.cosine_similarity(embedding,target)
		if cos_sim >= max_sim:
			extension = name.split(".")[1].upper()
			extension = "JPEG" if extension != "PNG" else extension
			img = Image.open(args.search_dir+name)
			img_byte_arr = BytesIO()
			img.save(img_byte_arr, format=extension)
			encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
			res.add((name,encoded_img))
			max_sim = cos_sim
	return res

def main(opt):
	global device
	global args
	global model
	global preprocess
	global embeddings
	args = opt
	device = args.device
	model, preprocess = clip.load(args.encoder, device=device)
	embeddings = load_embeddings(args.vector_dir)
	app.run(debug = True,use_reloader=False)