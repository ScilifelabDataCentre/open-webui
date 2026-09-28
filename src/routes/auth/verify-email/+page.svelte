<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { verifyEmail } from '$lib/apis/auths';
	import { WEBUI_NAME } from '$lib/stores';

	let status: 'loading' | 'success' | 'error' = 'loading';

	onMount(async () => {
		const token = $page.url.searchParams.get('token');
		if (!token) {
			status = 'error';
			return;
		}

		try {
			await verifyEmail(token);
			status = 'success';
		} catch {
			status = 'error';
		}
	});
</script>

<svelte:head>
	<title>Verify email · {$WEBUI_NAME}</title>
</svelte:head>

<main
	class="flex min-h-screen items-center justify-center bg-white px-6 text-center text-gray-900 dark:bg-black dark:text-white"
>
	<div class="w-full max-w-md">
		{#if status === 'loading'}
			<p class="text-lg">Verifying your email address…</p>
		{:else if status === 'success'}
			<h1 class="text-2xl font-medium">Email verified</h1>
			<p class="mt-3 text-sm text-gray-600 dark:text-gray-400">
				You can now sign in to {$WEBUI_NAME}.
			</p>
			<a class="mt-6 inline-block underline" href="/auth">Go to sign in</a>
		{:else}
			<h1 class="text-2xl font-medium">This verification link is invalid or expired</h1>
			<p class="mt-3 text-sm text-gray-600 dark:text-gray-400">
				Return to sign in and request a new verification email.
			</p>
			<a class="mt-6 inline-block underline" href="/auth">Go to sign in</a>
		{/if}
	</div>
</main>
