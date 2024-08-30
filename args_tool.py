import argparse


def get_args():
    parser = argparse.ArgumentParser(description="命令行中传入的参数")

    # 添加参数
    parser.add_argument('--test_data', type=str, required=False, default='test_data/research_agent_test_data.json', help='输入的数据')
    parser.add_argument('--model', type=str, required=False, default='deepseek', help='基座模型')
    parser.add_argument('--llm_try_times', type=int, required=False, default=3, help='llm失败最多尝试次数')
    parser.add_argument('--review_times', type=int, required=False, default=1, help='review agent迭代优化的次数，这里利用reflextion的feedback来优化效果')
    parser.add_argument('--offline', type=int, required=False, default=1, help='offline模式在失败后，会读取本地文件加载已经完成的llm调用，不需要重新调用')
    parser.add_argument('--project_dir', type=str, required=False, default='user_data/test_project_openai', help='项目输出目录')
    parser.add_argument('--step', type=int, required=False, default=0, help='全局计数器')
    parser.add_argument('--download_arxiv_paper_by_wget', type=str, required=False, default="0", help='是否用wget下载arxiv文档，1:是，0:否')
    parser.add_argument('--use_rag_result', type=str, required=False, default="1", help='是否用利用rag结果，1:是，0:否')
    parser.add_argument('--use_proxies', type=str, required=False, default="0", help='是否利用代理下载arxiv文章（没开代理下载arxiv可能非常慢），1:是，0:否')


    # 解析参数
    args = parser.parse_args()

    # 这里可以添加您的代码来处理这些参数
    print(args)
    return args

if __name__ == "__main__":
    get_args()
    # python args.py --base_bge_model path/to/base/model --ft_bge_model path/to/ft/model --train_file path/to/train/file --valid_file path/to/valid/file --test_file path/to/test/file --train_features_save_path path/to/train/features --valid_features_save_path path/to/valid/features --model_ckpt_save_path path/to/model/ckpt