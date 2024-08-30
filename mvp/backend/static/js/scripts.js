let currentTab = 'paper';
let nextTab = 'problem';
let progress = 0;


function disableButton(button_name) {
    const button = document.getElementById(button_name);
    button.disabled = true;
}

function enableButton(button_name) {
    const button = document.getElementById(button_name);
    button.disabled = false;
}

function search() {
    const query = document.getElementById('query').value;
//    const file = document.getElementById('file-upload').files[0];
    const formData = new FormData();
    formData.append('query', query);
//    if (file) {
//        formData.append('file', file);
//    }

    fetch('/search', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.flag == 1){
            enableButton('continue-tab');
            // enableButton('regenerate-tab');
            enableButton('paper-tab');
            currentTab = 'problem';
            progress += 20;
        }
        document.getElementById('result').innerHTML = `<h1>${data.title}</h1><p>${data.abstract}</p>`;
        document.getElementById('gpt_feedback').innerHTML = `<h1>RELATED PAPERS</h1><p>${data.rag_result}</p>`;
        document.getElementById('paper-tab').classList.add('active');
        document.getElementById('progress').style.width = `${progress}%`;
    });
}

function showTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(`${tab}-tab`).classList.add('active');

    // Fetch and display content for the selected tab
    fetch(`/content?tab=${tab}`, {
        method: 'GET'
    })
    .then(response => {
        // if (!response.ok) {
        //     throw new Error('Network response was not ok');
        // }
        return response.json();
    })
    .then(data => {
        if (currentTab == 'paper'){
            document.getElementById('result').innerHTML = `<h1>${data.title}</h1><p>${data.content}</p>`;
//            document.getElementById('gpt_feedback').innerHTML = `<h1>RELATED PAPERS</h1><p>${data.rag_result}</p>`;
        }
        if (currentTab == 'problem' || currentTab == 'method' || currentTab == 'experiment'){
            document.getElementById('result').innerHTML = `<h1>${data.title}</h1><p>${data.content}</p><h1>Rationale</h1><p>${data.rationale}</p>`; 
            document.getElementById('gpt_feedback').innerHTML = `<h1>GPT FEEDBACK</h1><h2>Review</h2><p>${data.gpt_feedback_review}</p><h2>FeedBack</h2><p>${data.gpt_feedback_content}</p><h2>Rating</h2><p>${data.gpt_feedback_rating}</p>`;
        }
        if (currentTab == 'ideate'){
            document.getElementById('result').innerHTML = `<h1>Ideate</h1><h2>Title</h2><p>${data.title}</p><h2>Abstract</h2><p>${data.abstract}</p><h2>problem</h2><p>${data.problem}</p><h2>method</h2><p>${data.method}</p><h2>experiment</h2><p>${data.experiment}</p>`;
            document.getElementById('gpt_feedback').innerHTML = ``;
        }
                
        
    })
    .catch(error => {
        console.error('Error fetching content:', error);
        document.getElementById('result').innerHTML = `<p>Error fetching content: ${error.message}</p>`;
    });
}

function continueTab() {
    disableButton('continue-tab');
    document.getElementById('loading').style.display = 'block'; // Show loading spinner
    

    fetch(`/continue?tab=${nextTab}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none'; // Hide loading spinner
        enableButton('continue-tab');
        enableButton(nextTab + '-tab');
        enableButton('export-tab');
        enableButton('regenerate-tab');

        if (nextTab == 'problem' || nextTab == 'method' || nextTab == 'experiment'){
            document.getElementById('result').innerHTML = `<h1>${data.title}</h1><p>${data.content}</p><h1>Rationale</h1><p>${data.rationale}</p>`; 
            document.getElementById('gpt_feedback').innerHTML = `<h1>GPT FEEDBACK</h1><h2>Review</h2><p>${data.gpt_feedback_review}</p><h2>FeedBack</h2><p>${data.gpt_feedback_content}</p><h2>Rating</h2><p>${data.gpt_feedback_rating}</p>`;
        }
        if (nextTab == 'ideate'){
            document.getElementById('result').innerHTML = `<h1>Ideate</h1><h2>Problem</h2><p>${data.problem}</p><h2>Title</h2><p>${data.title}</p><h2>Abstract</h2><p>${data.abstract}</p><h2>Method</h2><p>${data.method}</p><h2>Experiment</h2><p>${data.experiment}</p>`;
            document.getElementById('gpt_feedback').innerHTML = ``;
        }

        // if(currentTab != 'ideate')
        // document.getElementById('result').innerHTML = `<h1>${data.title}</h1><p>${data.content}</p><h1>Rationale</h1><p>${data.rationale}</p>`;
        // else if (currentTab == 'ideate')
        // document.getElementById('result').innerHTML = `<h1>Ideate</h1><h2>Title</h2><p>${data.content}</p><h2>Abstract</h2><p>${data.rationale}</p>`;

        // if(currentTab != 'paper' || currentTab != 'ideate')
        // document.getElementById('gpt_feedback').innerHTML = `<h1>GPT FEEDBACK</h1><h2>Review</h2><p>${data.gpt_feedback_review}</p><h2>FeedBack</h2><p>${data.gpt_feedback_content}</p><h2>Rating</h2><p>${data.gpt_feedback_rating}</p>`;

        

        // Move to next tab
        document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
        document.getElementById(`${nextTab}-tab`).classList.add('active');
        progress += 20;
        document.getElementById('progress').style.width = `${progress}%`;
        currentTab = nextTab;
        if (nextTab === 'paper') nextTab = 'problem';
        else if (nextTab === 'problem') nextTab = 'method';
        else if (nextTab === 'method') nextTab = 'experiment';
        else if (nextTab === 'experiment') nextTab = 'ideate';
        else if (nextTab === 'ideate') nextTab = 'ideate';
    });
}

function regenerate() {
    const feedback = document.getElementById('human-feedback').value;
    document.getElementById('loading').style.display = 'block'; // Show loading spinner
    fetch(`/regenerate?tab=${currentTab}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ feedback })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none'; // Hide loading spinner
        document.getElementById('result').innerHTML = `<h1>${data.title}</h1><p>${data.content}</p><h1>Rationale</h1><p>${data.rationale}</p>`;
        if(currentTab != 'paper' || currentTab != 'ideate')
        document.getElementById('gpt_feedback').innerHTML = `<h1>GPT FEEDBACK</h1><h2>Review</h2><p>${data.gpt_feedback_review}</p><h2>FeedBack</h2><p>${data.gpt_feedback_content}</p><h2>Rating</h2><p>${data.gpt_feedback_rating}</p>`;
    });
}

function exportContent() {
    fetch('/export', {
        method: 'GET'
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'research_agent_output.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    });
}

//function updateProgress() {
//    const progressPercentage = (${currentTab} / (tabs.length - 1)) * 100;
//    progress.style.width = `${progressPercentage}%`;
//
//    const progressPercentage = 0;
//    if (currentTab === 'paper') progressPercentage = 20;
//else if (currentTab === 'problem') progressPercentage = 40;
//else if (currentTab === 'method') progressPercentage = 60;
//else if (currentTab === 'experiment') progressPercentage = 80;
//else if (currentTab === 'ideate') progressPercentage = 100;
//}