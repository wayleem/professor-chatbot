<script lang="ts">
	enum senderType {
		user = 'user',
		bot = 'bot'
	}
	let messages: { sender: senderType; content: string }[] = [];
	let inputValue = '';

	// ... other code

	async function sendMessage() {
		if (!inputValue.trim()) return;
		const newMessage = { sender: senderType.user, content: inputValue };
		messages = [...messages, newMessage];

		const response = await fetch('http://localhost:5000/api', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ message: inputValue })
		});

		if (response.ok) {
			const responseData = await response.json();
			const botResponse = {
				sender: senderType.bot,
				content: `Professor Ferdman: ${responseData.response}`
			};
			messages = [...messages, botResponse];
		} else {
			console.error('Error getting response:', await response.text());
		}

		inputValue = '';
	}
</script>

<div class="p-4">
	<div class="mb-4 h-96 overflow-y-auto bg-white shadow rounded-lg p-4">
		{#each messages as { sender, content }, index}
			<div class="{sender === 'user' ? 'text-right' : 'text-left'} p-2">
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
