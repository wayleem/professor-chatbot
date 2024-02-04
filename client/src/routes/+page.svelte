<script lang="ts">
	import minus from '../assets/MINUS.png';
	import bad from '../assets/BAD.png';
	import neutral from '../assets/NEUTRAL.png';
	import good from '../assets/GOOD.png';
	import f_grade from '../assets/F.png';
	import d_grade from '../assets/D.png';
	import c_grade from '../assets/C.png';
	import b_grade from '../assets/B.png';
	import a_grade from '../assets/A.png';
	import plus_mp3 from '../assets/PLUS.mp3';
	import minus_mp3 from '../assets/MINUS.mp3';
	import music from '../assets/bgmusic.mp3';
	import { afterUpdate, onMount } from 'svelte';

	const gradeImageMap = {
		A: a_grade,
		B: b_grade,
		C: c_grade,
		D: d_grade,
		F: f_grade
	};

	let messages: { sender: string; content: string; tag?: string }[] = [];
	let inputValue = '';
	let points = 0;
	let moodImageSrc = bad;
	let gradeSrc = gradeImageMap['F'];
	let deduction = false;
	let gain = false;
	let countdown = 100;
	let gameEnded = false;
	let plus_sound: HTMLAudioElement;
	let minus_sound: HTMLAudioElement;
	let bg_music: HTMLAudioElement;

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
		countdown = 100;
		gameEnded = false;
		messages = [];
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
		bg_music.play();
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
					{ sender: 'bot', content: `Professor Stark: ${botResponse}`, tag }
				];
				if (points_change < 0) {
					minus_sound.play();
					deduction = true;
					setTimeout(() => {
						deduction = false;
					}, 2000);
				} else if (points_change > 0) {
					plus_sound.play();
					gain = true;
					setTimeout(() => {
						gain = false;
					}, 2000);
				}

				points += points_change;
				if (points >= 90) {
					gradeSrc = gradeImageMap['A'];
				} else if (points >= 70) {
					gradeSrc = gradeImageMap['B'];
				} else if (points >= 50) {
					gradeSrc = gradeImageMap['C'];
				} else if (points >= 30) {
					gradeSrc = gradeImageMap['D'];
				} else {
					gradeSrc = gradeImageMap['F'];
				}
			} else {
				console.error('Error getting response:', await response.text());
			}
		} catch (error) {
			console.error('Fetch error:', error);
		}

		inputValue = '';
	}

	const negativeTags = [
		'CovidExcuse',
		'MentalHealth',
		'TrafficExcuse',
		'Oversleep',
		'SickExcuse',
		'TechnicalExcuse',
		'OtherCourses',
		'SugarCoat',
		'Threat',
		'PoorExcuse'
	];

	const getMessageClass = (tag?: string) => {
		if (tag === 'SeriousExcuse') return 'text-green-700';
		if (tag && negativeTags.includes(tag)) {
			return 'text-red-700';
		}
		return '';
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

<div class="flex flex-col p-4">
	<audio src={plus_mp3} bind:this={plus_sound} />
	<audio src={minus_mp3} bind:this={minus_sound} />
	<audio src={music} preload="auto" bind:this={bg_music} />
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
	<div class="flex flex-row self-center">
		<img class="lg:w-[24vw] md:w-[30vw] w-[24vw]" alt="grade" src={gradeSrc} />
		<img
			class={`lg:w-[24vw] md:w-[30vw] w-[24vw] ${flipImage ? 'scale-x-[-1]' : ''}`}
			alt="mood"
			src={moodImageSrc}
		/>
	</div>
</div>
