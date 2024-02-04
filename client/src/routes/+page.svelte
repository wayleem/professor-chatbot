<script lang="ts">
  import { onMount } from 'svelte';
  import type { senderType } from './senderType'; // Assuming you have this type defined elsewhere

  let messages: { sender: senderType; content: string; tag?: string }[] = [];
  let inputValue = '';

  async function sendMessage() {
    if (!inputValue.trim()) return;
    const newMessage = { sender: 'user', content: inputValue };
    messages = [...messages, newMessage];

    try {
      const response = await fetch('http://localhost:5000/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue }),
      });

      if (response.ok) {
        const { response: botResponse, tag } = await response.json();
        messages = [...messages, { sender: 'bot', content: `Professor Ferdman: ${botResponse}`, tag }];
      } else {
        console.error('Error getting response:', await response.text());
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }

    inputValue = ''; // Reset input field after sending message
  }

  // Helper function to determine message text color based on tag
  const getMessageClass = (tag?: string) => {
    switch (tag) {
      case 'PositiveExcuse':
        return 'text-green-700';
      case 'NegativeExcuse':
        return 'text-red-700';
      default:
        return ''; // No additional class for other types of messages
    }
  };
</script>

<div class="p-4">
  <div class="mb-4 h-96 overflow-y-auto bg-white shadow rounded-lg p-4">
    {#each messages as { sender, content, tag }}
      <div class={`p-2 ${sender === 'user' ? 'text-right' : 'text-left'} ${getMessageClass(tag)}`}>
        {content}
      </div>
    {/each}
  </div>
  <input
    class="w-full p-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
    type="text"
    bind:value={inputValue}
    on:keypress={(e) => e.key === 'Enter' && sendMessage()}
    placeholder="Type your message here..."
  />
</div>
