<template>
  <div class="bg-gray-100 min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-blue-600 text-white py-4 shadow-lg">
      <h1 class="text-center text-2xl font-bold">ERP Anomaly Detection</h1>
      <p class="text-center text-sm mt-1">
        Chat with AI to detect anomalies in ERP transactions
      </p>
    </header>

    <!-- Chat Container -->
    <main class="flex-1 overflow-y-auto p-4">
      <div class="max-w-3xl mx-auto">
        <!-- Chat Messages -->
        <div class="flex flex-col space-y-4">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="[
              'p-3 rounded-lg text-sm max-w-[70%]',
              message.isUser
                ? 'bg-blue-100 self-end text-blue-800 ml-auto pr-3 pl-8'
                : 'bg-gray-200 text-gray-800 mr-auto pl-3 pr-8',
            ]"
          >
            <div
              v-if="!message.isUser"
              v-html="formatMessage(message.text)"
            ></div>
            <div v-else>{{ message.text }}</div>
          </div>
        </div>
      </div>
    </main>

    <!-- Input Form -->
    <footer class="bg-gray-200 py-4">
      <div class="max-w-3xl mx-auto flex items-center space-x-4">
        <input
          v-model="prompt"
          class="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring focus:ring-blue-300"
          placeholder="Ask something about ERP anomaly detection..."
        />
        <button
          @click="sendMessage"
          class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      prompt: "",
      messages: [], // History of messages
    };
  },
  methods: {
    async sendMessage() {
      if (!this.prompt.trim()) return;

      // Add user message to chat history
      this.messages.push({ text: this.prompt, isUser: true });

      try {
        // Send prompt to backend API
        const response = await axios.post("http://127.0.0.1:5001/generate", {
          prompt: this.prompt,
        });

        console.log("Response:", response.data);

        // Add AI response to chat history
        this.messages.push({ text: response.data.response, isUser: false });

        // Clear the input field
        this.prompt = "";
      } catch (error) {
        console.error("Error:", error);
        this.messages.push({
          text: "Something went wrong. Please try again later.",
          isUser: false,
        });
      }
    },
    formatMessage(text) {
      // Convert plain text to HTML
      return text
        .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>") // Bold
        .replace(/\* ([^*]+)/g, "<li>$1</li>") // Bullet list
        .replace(/(?:\r\n|\r|\n)/g, "<br>") // Line breaks
        .replace(/- ([^*]+)/g, "<li>$1</li>"); // Handle additional bullet formats
    },
  },
};
</script>

<style scoped>
.chat-message {
  max-width: 70%;
  word-wrap: break-word;
  margin-bottom: 10px;
  line-height: 1.5;
}

.user-message {
  border-radius: 20px 20px 0 20px;
  animation: slideFromRight 0.3s ease;
}

.ai-message {
  border-radius: 20px 20px 20px 0;
  animation: slideFromLeft 0.3s ease;
}

@keyframes slideFromRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideFromLeft {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
