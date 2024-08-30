import json
import logging
logger = logging.getLogger()
import os
import uuid
import re
import secrets
import markdown
from flask import Flask, request, session, jsonify, render_template, send_file
from datetime import timedelta
from vo.problem import Problem
from vo.method import Method
from vo.experiment import  Experiment
from vo.ideate import ideate
from vo.review_result import ReviewResult

from mvp.server.utils import validate_arxiv_url, save_content_to_file
from vo.paper_data import Paper, load_paper_from_file, load_paper_from_dict
from utils_tool import init_logging
from args_tool import get_args

args = get_args()

config = {
    "USER_DATA_DIR": "user_data/",
    "Paper_DATA_DIR": "user_data/all_paper",
}

target_tab_list = ["problem", 'method', 'experiment', 'ideate']
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
# Set session lifetime to 31 days
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

# 存储用户数据
user_data = {}    

# 存储当前每一阶段最新的数据
current_data = {"paper": None, "problem": None, "method": None, "experiment": None, "ideate": None}


def load_json_from_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def load_test_sample_data(demo_file):
    data = load_json_from_file(demo_file)
    test_sample_data = {}
    for tab, result_key, feedback_key in zip(
        ["problem", "method", "experiment", "ideate"],
        ["problem_result", "method_result", "exp_result", "ideate_result"],
        ["problem_gpt_feedback_result", "method_gpt_feedback_result", "exp_gpt_feedback_result", "ideate_gpt_feedback_result"]
    ):
        if tab == "problem":
            llm_result = Problem.load_from_string(data[result_key])
            gpt_feedback_result = ReviewResult.load_from_string(data[feedback_key])
        elif tab == "method":
            llm_result = Method.load_from_string(data[result_key])
            gpt_feedback_result = ReviewResult.load_from_string(data[feedback_key])
        elif tab == "experiment":
            llm_result = Experiment.load_from_string(data[result_key])
            gpt_feedback_result = ReviewResult.load_from_string(data[feedback_key])
        elif tab.lower() == "ideate":
            llm_result = ideate.load_from_string(data[result_key])
            gpt_feedback_result = ReviewResult.load_from_string(data[feedback_key])
        else:
            raise ValueError(f"Unknown tab: {tab}")

        test_sample_data[tab] = {
            "llm_result": llm_result,
            "gpt_feedback_result": gpt_feedback_result
        }
    return test_sample_data



test_sample_data = load_test_sample_data(
    "user_data/demo_0830/paper_2310.08129/final_result.json"
)


def gen_tab_data(session_id, tab, human_feedback=None):
    # llm_result, cur_gpt_feedback_result = f"tab:{tab} test_llm_result", f"tab:{tab} test_gpt_feedback_result"
    llm_result = Problem(
        problem = f"tab: {tab} test llm result",
        rationale=f"tab: {tab} test llm rationale",
    )
    cur_gpt_feedback_result = ReviewResult(
        review = f"tab: {tab} test review",
        feedback = f"tab: {tab} test feedback",
        rating = f"tab: {tab} test rating",
    )
    cur_ideate = ideate(
        title=f"tab:{tab} test title", abstract=f"tab:{tab} test abstract"
    )

    tab_data = test_sample_data.get(tab, None)
    if tab_data is not None:
        assert isinstance(tab_data, dict)
        llm_result, cur_gpt_feedback_result = tab_data["llm_result"], tab_data["gpt_feedback_result"]
    else:
        if tab == 'ideate':
            # import pdb;
            # pdb.set_trace()
            llm_result = cur_ideate
    user_data[session_id][f'last_{tab.lower()}'] = llm_result
    user_data[session_id][f'last_{tab.lower()}_gpt_feedback'] = cur_gpt_feedback_result
    return llm_result, cur_gpt_feedback_result

# Turn json to markdown
def parse_to_markdown(input_list):
    # Initialize an empty string for Markdown content
    markdown_content = ""

    # Regular expression to find titles and abstracts
    pattern = re.compile(r'title:\s*{([^}]*)}\s*abstract:\s*{([^}]*)}')

    for item in input_list:
        # Find all matches in the current string
        matches = pattern.findall(item)

        for match in matches:
            title, abstract = match
            markdown_content += f"### Title\n{title}\n\n### Abstract\n{abstract}\n\n"

    return markdown_content

def parse_to_html(input_list, target_paper = None):
    # Initialize an empty string for HTML content
    html_content = ""

    # Regular expression to find titles and abstracts
    pattern = re.compile(r'title:\s*{([^}]*)}\s*abstract:\s*{([^}]*)}')

    for item in input_list:
        # Find all matches in the current string
        matches = pattern.findall(item)

        for match in matches:
            title, abstract = match
            if title == target_paper.title:
                continue
            html_content += f"<h3>Title</h3>\n<p>{title}</p>\n<h3>Abstract</h3>\n<p>{abstract}</p>\n"
    return html_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    session_id = session.get('session_id')
    query = request.form.get('query')
    # TODO: 这里还是只处理arxiv url，后续可以考虑直接处理文本
    flag, msg = validate_arxiv_url(query)
    if not flag:
        result = {
            'title': msg,
            'abstract': msg,
            'flag': 0
        }
    else:
        paper_id = query.split('/')[-1]
        paper_data_dir = os.path.join(config['Paper_DATA_DIR'], paper_id)
        input_paper_file = os.path.join(paper_data_dir, "input_paper.json")
        paper_info = load_paper_from_file(input_paper_file)
        user_data[session_id]['paper_info'] = paper_info
        result = {
            'title': paper_info.title,
            'abstract': paper_info.abstract,
            'rag_result': None,
            'flag': 1
        }
        current_data['paper'] = result
    return jsonify(result)

@app.route('/continue', methods=['GET'])
def continue_tab():
    session_id = session.get('session_id')
    tab = request.args.get('tab').lower()
    if tab.lower() in target_tab_list:
        iter_times = user_data[session_id].get(f'{tab.lower()}_iter_times', 0)
        llm_result, gpt_feedback = gen_tab_data(session_id, tab, human_feedback=None)
        # Store latest data to allow later tab switching
        current_data[tab] = [llm_result, gpt_feedback]
        iter_times += 1
        user_data[session_id][f'{tab.lower()}_iter_times'] = iter_times
        # import pdb;pdb.set_trace()
        if tab.lower() == 'ideate':
            last_problem = user_data[session_id].get('last_problem', None)
            last_method = user_data[session_id].get('last_method', None)
            last_experiment = user_data[session_id].get('last_experiment', None)
            last_ideate = user_data[session_id].get('last_ideate', None)
            # Generate and export the final content

            content = {
                'title': f'{last_ideate.title}',
                'abstract': f'{last_ideate.abstract}',
                'problem': markdown.markdown(last_problem.get_result()),
                'method': markdown.markdown(last_method.get_result()),
                'experiment': markdown.markdown(last_experiment.get_result()),
            }
            print('<<<<<<<<<<<<<<<<<<')
            print(content)
            print('<<<<<<<<<<<<<<<<<<')
        else:
            content = {
                'title': f'{tab.capitalize()}',
                'content': markdown.markdown(llm_result.get_result()),
                'rag_result': user_data[session_id].get('rag_result', None),
                'rationale': markdown.markdown(llm_result.get_rationale()),
                'gpt_feedback_review': markdown.markdown(gpt_feedback.get_review()),
                'gpt_feedback_content': markdown.markdown(gpt_feedback.get_feedback()),
                'gpt_feedback_rating': markdown.markdown(gpt_feedback.get_rating()),
            }
    else:
        # Generate content for the next tab
        content = {
            'title': f'{tab.capitalize()} Content',
            'content': f'This is {tab} content',
            'rationale':  f'This is {tab} content rationale',
            'gpt_feedback_review': f'This is {tab} content gpt_feedback_review',
            'gpt_feedback_content': f'This is {tab} content gpt_feedback_content',
            'gpt_feedback_rating': f'This is {tab} content gpt_feedback_rating',
        }
    return jsonify(content)


@app.route('/content', methods=['GET'])
def content():
    session_id = session.get('session_id')
    tab = request.args.get('tab')
    if tab.lower() in target_tab_list:
        if current_data[tab] == None:
            llm_result, gpt_feedback = gen_tab_data(session_id, tab, human_feedback=None)
            current_data[tab] = [llm_result, gpt_feedback]
        else:
            llm_result, gpt_feedback = current_data[tab]
            if tab.lower() == 'ideate':
                session_id = session.get('session_id')
                last_problem = user_data[session_id].get('last_problem', None)
                last_problem_gpt_feedback = user_data[session_id].get('last_problem_gpt_feedback', None)
                last_method = user_data[session_id].get('last_method', None)
                last_method_gpt_feedback = user_data[session_id].get('last_method_gpt_feedback', None)
                last_experiment = user_data[session_id].get('last_experiment', None)
                last_experiment_gpt_feedback = user_data[session_id].get('last_experiment_gpt_feedback', None)
                last_ideate = user_data[session_id].get('last_ideate', None)
                # Generate and export the final content
                content = {
                    'title': f'{last_ideate.title}',
                    'abstract': f'{last_ideate.abstract}',
                    'problem': markdown.markdown(last_problem.get_result()),
                    'method': markdown.markdown(last_method.get_result()),
                    'experiment': markdown.markdown(last_experiment.get_result()),
                }
            else:
                content = {
                    'title': f'{tab.capitalize()}',
                    'content': markdown.markdown(llm_result.get_result()),
                    'rag_result': user_data[session_id].get('rag_result', None),
                    'rationale': markdown.markdown(llm_result.get_rationale()),
                    'gpt_feedback_review': markdown.markdown(gpt_feedback.get_review()),
                    'gpt_feedback_content': markdown.markdown(gpt_feedback.get_feedback()),
                    'gpt_feedback_rating': markdown.markdown(gpt_feedback.get_rating()),
                }
    else:
        # Generate content for the next tab
        content = {
            'title': current_data['paper']['title'],
            'content': current_data['paper']['abstract'],
            'rag_result': user_data[session_id].get('rag_result', None),
            'rationale':  f'This is {tab} content rationale',
            'gpt_feedback_review': f'This is {tab} content gpt_feedback_review',
            'gpt_feedback_content': f'This is {tab} content gpt_feedback_content',
            'gpt_feedback_rating': f'This is {tab} content gpt_feedback_rating',
        }
    return jsonify(content)

@app.route('/regenerate', methods=['POST'])
def regenerate():
    session_id = session.get('session_id')
    feedback = request.json.get('feedback')
    tab = request.args.get('tab')
    # Regenerate content based on the feedback
    if tab.lower() in target_tab_list:
        iter_times = user_data[session_id].get(f'{tab.lower()}_iter_times', 0)
        llm_result, gpt_feedback  = gen_tab_data(session_id, tab, human_feedback=feedback)
        # Store latest data to allow later tab switching
        current_data[tab] = [llm_result, gpt_feedback]
        content = {
            'title': f'{tab.capitalize()} Content After Feedback, Iter time:{iter_times}',
            'content': llm_result.get_result(),
            'rationale': llm_result.get_rationale(),
            'gpt_feedback_review': gpt_feedback.get_review(),
            'gpt_feedback_content': gpt_feedback.get_feedback(),
            'gpt_feedback_rating': gpt_feedback.get_rating(),
        }
        iter_times += 1
        user_data[session_id][f'{tab.lower()}_iter_times'] = iter_times
    else:
        content = {
            'title': f'{tab.capitalize()} Content After Feedback',
            'content': f'This is {tab} content after feedback: {feedback}',
            'rationale': f'This is {tab} content rationale after feedback: {feedback}',
            'gpt_feedback_review': f'This is {tab} content gpt_feedback_review',
            'gpt_feedback_content': f'This is {tab} content gpt_feedback_content',
            'gpt_feedback_rating': f'This is {tab} content gpt_feedback_rating',
        }

    return jsonify(content)

@app.route('/export', methods=['GET'])
def export():
    session_id = session.get('session_id')
    last_problem = user_data[session_id].get('last_problem', None)
    last_method = user_data[session_id].get('last_method', None)
    last_experiment = user_data[session_id].get('last_experiment', None)
    last_ideate = user_data[session_id].get('last_ideate', None)
    # Generate and export the final content
    content = f"""### Title\n{last_ideate.title}\n### Abstract\n{last_ideate.abstract}\n### Problem\n{last_problem.get_result()}\n### Method\n{last_method.get_result()}\n### Experiment\n{last_experiment.get_result()}"""
    with open('mvp/backend/output.txt', 'w') as f:
        print(content)
        f.write(content)
    return send_file('output.txt', as_attachment=True)


@app.before_request
def before_request():
    session.permanent = True
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    session_id = session['session_id']
    if session_id not in user_data:
        user_data[session_id] = {}

if __name__ == '__main__':
    init_logging(log_dir='log')
    app.run(debug=True, host='0.0.0.0', port=5001)