<script lang="ts">
	import minus from '../assets/MINUS.png';
	import bad from '../assets/BAD.png';
	import neutral from '../assets/NEUTRAL.png';
	import good from '../assets/GOOD.png';
	import plus_mp3 from '../assets/PLUS.mp3';
	import minus_mp3 from '../assets/MINUS.mp3';
	import music from '../assets/bgmusic.mp3';
	import { afterUpdate, onMount } from 'svelte';

	let messages: { sender: string; content: string; tag?: string }[] = [];
	let inputValue = '';
	let points = 0;
	let moodImageSrc = bad;
	let deduction = false;
	let gain = false;
	let countdown = 10;
	let gameEnded = false;

	function startCountdown() {
		const timer = setInterval(() => {
			countdown -= 1;
			if (countdown <= 0) {
				clearInterval(timer);
				gameEnded = true;
			}
		}, 1000);
	}

	function restartGame() {
		points = 0;
		countdown = 60;
		gameEnded = false;
		startCountdown();
	}

	$: {
		if (deduction) {
			moodImageSrc = minus;
		} else if (gain) {
			moodImageSrc = good;
		} else if (points >= 90) {
			moodImageSrc = good;
		} else if (points >= 65 && points < 90) {
			moodImageSrc = neutral;
		} else {
			moodImageSrc = bad;
		}
	}

	onMount(() => {
		startCountdown();
		const interval = setInterval(() => {
			flipImage = !flipImage;
		}, 500);

		return () => {
			clearInterval(interval);
		};
	});

	async function sendMessage() {
		if (!inputValue.trim()) return;
		const newMessage = { sender: 'user', content: inputValue };
		messages = [...messages, newMessage];

		try {
			const response = await fetch('http://localhost:5000/api', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: inputValue })
			});

			if (response.ok) {
				const { response: botResponse, tag, points_change } = await response.json();
				messages = [
					...messages,
					{ sender: 'bot', content: `Professor Ferdman: ${botResponse}`, tag }
				];
				if (points_change < 0) {
					deduction = true;
					setTimeout(() => {
						deduction = false;
					}, 2000);
				} else if (points_change > 0) {
					gain = true;
					setTimeout(() => {
						gain = false;
					}, 2000);
				}

				points += points_change;
			} else {
				console.error('Error getting response:', await response.text());
			}
		} catch (error) {
			console.error('Fetch error:', error);
		}

		inputValue = '';
	}

	const getMessageClass = (tag?: string) => {
		switch (tag) {
			case 'PositiveExcuse':
				return 'text-green-500';
			case 'NegativeExcuse':
				return 'text-red-500';
			default:
				return '';
		}
	};
	function scrollToBottom(node: HTMLElement) {
		afterUpdate(() => {
			node.scrollTop = node.scrollHeight;
		});
		return {
			update() {
				node.scrollTop = node.scrollHeight;
			}
		};
	}
	let flipImage = false;
</script>

<div class="flex flex-col p-4 h-screen overscroll-none">
	<div class="mb-4">
		<p class="text-center font-black text-red-500 text-xl">
			{countdown} SECONDS UNTIL GRADES ARE FINALIZED
		</p>
	</div>
	<div class="mb-4 h-96 overflow-y-auto bg-white shadow rounded-lg p-4" use:scrollToBottom>
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
	{#if gameEnded}
		<div
			class="fixed flex flex-col top-0 left-0 w-full h-full bg-gray-900 bg-opacity-75 flex items-center justify-center z-10"
		>
			<h1 class="text-8xl mb-4 text-red-500">YOU FAILED</h1>
			<button
				class="px-6 py-3 bg-blue-500 text-white rounded focus:outline-none"
				on:click={restartGame}
			>
				RETAKE THE COURSE
			</button>
		</div>
	{/if}
	<img
		class={`w-[32vw] self-center ${flipImage ? 'scale-x-[-1]' : ''}`}
		alt="mood"
		src={moodImageSrc}
	/>
</div>
