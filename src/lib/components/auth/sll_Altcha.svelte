<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import type { i18n as I18n } from 'i18next';
	import type { Readable } from 'svelte/store';
	import type { AltchaWidgetElement } from 'altcha';
	import { WEBUI_API_BASE_URL } from '$lib/constants';

	export let payload = '';
	const i18n = getContext<Readable<I18n>>('i18n');
	let widget: AltchaWidgetElement;
	let loaded = false;
	let failed = false;

	const load = async () => {
		failed = false;
		try {
			await import('altcha/i18n');
			loaded = true;
		} catch {
			failed = true;
		}
	};

	onMount(() => {
		void load();
		return () => {
			payload = '';
		};
	});

	export const reset = () => {
		payload = '';
		widget?.reset();
		void widget?.verify();
	};

	const stateChange = (event: CustomEvent<{ state: string; payload?: string }>) => {
		payload = event.detail.state === 'verified' ? (event.detail.payload ?? '') : '';
	};
</script>

<div class="sll-altcha mt-4 text-left text-sm" style="--altcha-max-width: 100%;">
	{#if loaded}
		<altcha-widget
			bind:this={widget}
			challenge={`${WEBUI_API_BASE_URL}/auths/altcha/challenge`}
			language={$i18n.language}
			auto="onload"
			display="standard"
			on:statechange={stateChange}
		></altcha-widget>
	{:else if failed}
		<p role="alert">{$i18n.t('Unable to load signup verification.')}</p>
		<button type="button" class="mt-1 underline" on:click={load}>{$i18n.t('Retry')}</button>
	{:else}
		<p role="status">{$i18n.t('Loading signup verification...')}</p>
	{/if}
</div>

<style>
	.sll-altcha {
		color-scheme: light;
	}

	:global(.dark) .sll-altcha {
		color-scheme: dark;
	}
</style>
