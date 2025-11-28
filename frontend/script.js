// kmrl-chatbot/frontend/script.js

const API_URL = "http://127.0.0.1:8000/api/ask/";

// Function to add a message to the chat window
function addMessage(sender, text, isError = false) {
    const chatWindow = document.getElementById('chat-window');
    const messageDiv = document.createElement('div');
    
    // Simple styling classes based on sender
    let className = 'message ';
    if (sender === 'User') className += 'user';
    else if (sender === 'Chatbot') className += 'chatbot';
    else className += 'system';
    if (isError) className += ' error';

    messageDiv.className = className;
    messageDiv.textContent = `${sender}: ${text}`;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to bottom
}

// Function to display source documents
function displaySources(sources) {
    const sourcesList = document.getElementById('sources-list');
    sourcesList.innerHTML = ''; // Clear previous sources

    if (sources && sources.length > 0) {
        sources.forEach((source, index) => {
            const listItem = document.createElement('li');
            
            // Take a clean snippet and escape newlines for display
            const snippet = source.content.substring(0, 100).replace(/\n/g, ' ') + '...'; 
            
            listItem.innerHTML = `
                <strong>${index + 1}. ${source.doc_name}</strong> (Distance: ${source.similarity.toFixed(4)})<br>
                Snippet: ${snippet}
            `;
            sourcesList.appendChild(listItem);
        });
    } else {
        sourcesList.innerHTML = '<li>No relevant sources found in the database.</li>';
    }
}

// Main function to send the query to Django API
async function sendQuery() {
    const inputField = document.getElementById('query-input');
    const query = inputField.value.trim();

    if (!query) return;

    // Display user query
    addMessage('User', query);
    inputField.value = ''; // Clear input
    
    // Clear sources while processing
    document.getElementById('sources-list').innerHTML = '';

    try {
        addMessage('System', 'Querying Local LLM (Processing on CPU, please wait)...');
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Send the query in the exact format Django expects
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        
        // --- CRITICAL FINAL FIX: Clean the repeated text ---
        const fullAnswer = data.answer;
        
        // 1. Regex to find the known garbage patterns (Answer: repetition, or eslint garbage) 
        // and replace everything from that point with an empty string.
        const cleanedGarbage = fullAnswer.replace(/(Answer:.*|^-eslint-disable-next-line.*)/s, '').trim(); 

        // 2. Ensure the answer isn't empty, then display
        const cleanAnswer = cleanedGarbage || "I cannot retrieve a clean answer from the model.";
        
        // Display LLM Answer
        addMessage('Chatbot', cleanAnswer);
        
        // Display Sources
        displaySources(data.sources);

    } catch (error) {
        console.error('Fetch Error:', error);
        addMessage('System', `Connection Error: ${error.message}. Ensure Django server is running!`, true);
        displaySources([]);
    }
}

// Optional: Basic event listener for Enter key
document.getElementById('query-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendQuery();
    }
});