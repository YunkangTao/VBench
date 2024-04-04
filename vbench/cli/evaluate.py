import torch
import os
from vbench import VBench
from datetime import datetime

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
def register_subparsers(subparser):
    parser = subparser.add_parser('evaluate')
    parser.add_argument(
        "--output_path",
        type=str,
        default='./evaluation_results/',
        help="output path to save the evaluation results",
    )
    parser.add_argument(
        "--full_json_dir",
        type=str,
        default=f'{CUR_DIR}/../VBench_full_info.json',
        help="path to save the json file that contains the prompt and dimension information",
    )
    parser.add_argument(
        "--videos_path",
        type=str,
        required=True,
        help="folder that contains the sampled videos",
    )
    parser.add_argument(
        "--dimension",
        nargs='+',
        required=True,
        help="list of evaluation dimensions, usage: --dimension <dim_1> <dim_2>",
    )
    parser.add_argument(
        "--load_ckpt_from_local",
        type=bool,
        required=False,
        help="whether load checkpoints from local default paths (assuming you have downloaded the checkpoints locally",
    )
    parser.add_argument(
        "--read_frame",
        type=bool,
        required=False,
        help="whether directly read frames, or directly read videos",
    )
    parser.add_argument(
        "--custom_input",
        action="store_true",
        required=False,
        help="whether use custom input prompt or vbench prompt"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=False,
        help="""Specify the input prompt
        If not specified, filenames will be used as input prompts
        *Mutually exclusive to --prompt_file.
        """
    )
    parser.add_argument(
        "--prompt_file",
        type=str,
        required=False,
        help="""Specify the path of the file that contains prompt lists,
        If not specified, filenames will be used as input prompts.
        *Mutually exclusive to --prompt.
        """
    )
    parser.set_defaults(func=evaluate)

def evaluate(args):
    print(f'args: {args}')

    device = torch.device("cuda")
    my_VBench = VBench(device, args.full_json_dir, args.output_path)
    
    print(f'start evaluation')
    
    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    prompt = []
    
    if args.prompt_file != "" and len(args.prompt) != 0:
        raise Exception("--prompt_file and --prompt cannot be used together")

    elif args.prompt_file:
        with open(args.prompt_file, 'r') as f:
            prompt = [line.strip() for line in f.readlines()]
    elif args.prompt:
        prompt = [args.prompt]
    
    my_VBench.evaluate(
        videos_path = args.videos_path,
        name = f'results_{current_time}',
        prompt_list=prompt,
        dimension_list = args.dimension,
        local=args.load_ckpt_from_local,
        read_frame=args.read_frame,
        custom_prompt=args.custom_input,
    )
    print('done')
