import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8080, type=int)
    parser.add_argument("--device", default="cuda", type=str)
    parser.add_argument("--encoder",default="ViT-B/16",type=str)
    parser.add_argument("--vector_dir",help="directory of stored vector embeddings",default="",type=str)
    parser.add_argument("--search_dir",help="directory to perform image search",default="",type=str)
    args = parser.parse_args()

    return args