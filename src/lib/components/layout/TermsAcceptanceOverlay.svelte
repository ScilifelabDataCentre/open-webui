<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let show = false;
	export let loading = false;

	const dispatch = createEventDispatcher<{
		accept: void;
		signout: void;
	}>();
</script>

{#if show}
	<div
		class="fixed inset-0 z-[1000] flex items-center justify-center bg-white/80 p-4 text-black backdrop-blur-md dark:bg-black/80 dark:text-white"
	>
		<div
			class="w-full max-w-3xl rounded-[2rem] border border-black/10 bg-white/95 shadow-2xl dark:border-white/10 dark:bg-gray-900/95"
		>
			<div class="border-b border-black/10 px-6 py-5 dark:border-white/10 sm:px-8">
				<div
					class="text-xs font-semibold uppercase tracking-[0.18em] text-gray-500 dark:text-gray-400"
				>
					Terms and Conditions
				</div>
				<h1 class="mt-2 text-2xl font-semibold sm:text-3xl">Review and accept to continue</h1>
				<p class="mt-2 max-w-2xl text-sm leading-6 text-gray-600 dark:text-gray-300">
					This is a placeholder terms and conditions document for now. Acceptance is required once
					before accessing the application.
				</p>
			</div>

			<div class="px-6 py-6 sm:px-8">
				<div
					class="max-h-[52vh] overflow-y-auto rounded-[1.5rem] border border-black/10 bg-gray-50/80 p-5 text-sm leading-6 text-gray-700 dark:border-white/10 dark:bg-white/5 dark:text-gray-200"
				>
					<h2 class="text-base font-semibold text-black dark:text-white">
						1. Placeholder agreement
					</h2>
					<p class="mt-2">
						By continuing, you acknowledge that this is a temporary terms document used only to
						support the current sign-in flow.
					</p>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">2. Acceptable use</h2>
					<p class="mt-2">
						Use the system responsibly, do not attempt to disrupt service availability, and do not
						store or process content you are not authorized to handle.
					</p>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">3. Data handling</h2>
					<p class="mt-2">
						Data entered into the application may be stored, processed, logged, and reviewed by the
						system operator for operational, security, and support purposes.
					</p>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">4. No warranty</h2>
					<p class="mt-2">
						This placeholder agreement is provided as-is and may be replaced with a formal document
						later. Continued use after future updates may require renewed acceptance.
					</p>
				</div>

				<div class="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
					<button
						type="button"
						class="rounded-full border border-black/10 px-5 py-2.5 text-sm font-medium text-gray-700 transition hover:bg-black/5 disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10 dark:text-gray-200 dark:hover:bg-white/10"
						disabled={loading}
						on:click={() => dispatch('signout')}
					>
						Sign out
					</button>

					<button
						type="button"
						class="rounded-full bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-black/85 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-white dark:text-black dark:hover:bg-white/85"
						disabled={loading}
						on:click={() => dispatch('accept')}
					>
						{#if loading}
							Accepting...
						{:else}
							Accept and continue
						{/if}
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
