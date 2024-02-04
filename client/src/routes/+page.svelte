<script lang="ts">
	enum senderType {
		user = 'user',
		bot = 'bot'
	}
	let messages: { sender: senderType; content: string }[] = [];
	let inputValue = '';

	function sendMessage() {
		if (!inputValue.trim()) return;
		const newMessage = { sender: senderType.user, content: inputValue };
		messages = [...messages, newMessage];

		const botResponse = { sender: senderType.bot, content: `Professor Ferdman: ${inputValue}` };
		messages = [...messages, botResponse];
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
