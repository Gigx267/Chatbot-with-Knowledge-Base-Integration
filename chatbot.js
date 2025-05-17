const { Configuration, OpenAIApi } = require('openai');
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

// Initialize OpenAI (replace with your API key)
const configuration = new Configuration({
    apiKey: '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',
});
const openai = new OpenAIApi(configuration);

// Chat history
let chatHistory = [];

async function chatWithAI() {
    console.log("AI Chatbot: Hello! Type 'quit' to exit.");

    while (true) {
        const userInput = await new Promise(resolve => {
            readline.question('You: ', resolve);
        });

        if (userInput.toLowerCase() === 'quit') {
            console.log("Chatbot: Goodbye!");
            readline.close();
            return;
        }

        // Add user message to history
        chatHistory.push({ role: 'user', content: userInput });

        try {
            // Get AI response
            const response = await openai.createChatCompletion({
                model: 'gpt-3.5-turbo',
                messages: [
                    { role: 'system', content: 'You are a helpful assistant.' },
                    ...chatHistory
                ],
                temperature: 0.7,
            });

            const aiResponse = response.data.choices[0].message.content;
            console.log(`Chatbot: ${aiResponse}`);

            // Add AI response to history
            chatHistory.push({ role: 'assistant', content: aiResponse });

            // Limit history to prevent excessive tokens
            if (chatHistory.length > 10) {
                chatHistory = chatHistory.slice(-10);
            }

        } catch (error) {
            console.error('Error communicating with OpenAI:', error.message);
            console.log("Chatbot: I'm having trouble responding. Please try again.");
        }
    }
}

// Start the chat
chatWithAI();