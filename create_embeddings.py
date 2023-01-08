import argparse
import clip
import torch
from PIL import Image
import pickle

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--encoder", default="ViT-B/16",type=str)
    parser.add_argument("--output_format",help="embedding format, [.pkl,.npy]",default="pkl",type=str)
    parser.add_argument("--device", default="cuda", type=str)
    parser.add_argument("--input_dir", help="image directory", default="",type=str)
    parser.add_argument("--output_dir",help="embeddings output directory", default="", type=str)
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    model,preprocess = clip.load(args.encoder, device=args.device)
    if args.output_format == ".pkl":
        # store pkl in form of filename,embedding pair
        dict = {}
        for name in args.input_dir:
            with torch.no_grad():
                img = preprocess(Image.open(dir+name)).unsqueeze(0).to(args.device)
                embeddings = model.encode_image(img)
                dict[name] = embeddings

            with open(args.output_dir+"data.pkl", "wb") as f:
                pickle.dump(dict, f)
