<script lang="ts">
	import DOMPurify from 'dompurify';
	import { marked } from 'marked';

	import { getAdminDetails, getLogoutRedirectUrl, userSignOut } from '$lib/apis/auths';
	import { onMount, tick, getContext } from 'svelte';
	import { config } from '$lib/stores';

	const i18n = getContext('i18n');

	let adminDetails = null;

	// SciLifeLab change start: registration questionnaire redirect.
	// The registration_questionnaire Event Function (openllm-setup) reports whether
	// this pending user still has to answer it. A full page load is needed because
	// the Function serves the form outside the SPA. Any failure, including a
	// missing Function, keeps the normal pending overlay. See SCILIFELAB_README.md.
	const redirectToQuestionnaire = async () => {
		try {
			const res = await fetch('/api/v1/registration-questionnaire/status', {
				method: 'POST',
				credentials: 'same-origin',
				headers: { Authorization: `Bearer ${localStorage.token}` }
			});
			if (res.ok && (await res.json())?.required === true) {
				window.location.replace('/auth/registration-questionnaire');
			}
		} catch (err) {
			console.error(err);
		}
	};
	// SciLifeLab change end

	onMount(async () => {
		// SciLifeLab change start: registration questionnaire redirect.
		redirectToQuestionnaire();
		// SciLifeLab change end
		adminDetails = await getAdminDetails(localStorage.token).catch((err) => {
			console.error(err);
			return null;
		});
	});
</script>

<div class="fixed w-full h-full flex z-999">
	<div
		class="absolute w-full h-full backdrop-blur-lg bg-white/10 dark:bg-gray-900/50 flex justify-center"
	>
		<div class="m-auto pb-10 flex flex-col justify-center">
			<div class="max-w-md">
				<div
					class="text-center dark:text-white text-2xl font-normal z-50"
					style="white-space: pre-wrap;"
				>
					{#if ($config?.ui?.pending_user_overlay_title ?? '').trim() !== ''}
						{$config.ui.pending_user_overlay_title}
					{:else}
						{$i18n.t('Account Activation Pending')}<br />
						{$i18n.t('Contact Admin for WebUI Access')}
					{/if}
				</div>

				<div
					class=" mt-4 text-center text-sm dark:text-gray-200 w-full"
					style="white-space: pre-wrap;"
				>
					{#if ($config?.ui?.pending_user_overlay_content ?? '').trim() !== ''}
						{@html DOMPurify.sanitize(
							marked.parse(($config?.ui?.pending_user_overlay_content ?? '').replace(/\n/g, '<br>'))
						)}
					{:else}
						{$i18n.t('Your account status is currently pending activation.')}{'\n'}{$i18n.t(
							'To access the WebUI, please reach out to the administrator. Admins can manage user statuses from the Admin Panel.'
						)}
					{/if}
				</div>

				{#if adminDetails}
					<div class="mt-4 text-sm font-normal text-center">
						<div>{$i18n.t('Admin')}: {adminDetails.name} ({adminDetails.email})</div>
					</div>
				{/if}

				<div class=" mt-6 mx-auto relative group w-fit">
					<button
						class="relative z-20 flex px-5 py-2 rounded-full bg-white border border-gray-100 dark:border-none hover:bg-gray-100 text-gray-700 transition font-normal text-sm"
						on:click={async () => {
							location.href = '/';
						}}
					>
						{$i18n.t('Check Again')}
					</button>

					<button
						class="text-xs text-center w-full mt-2 text-gray-400 underline"
						on:click={async () => {
							const res = await userSignOut().catch((err) => {
								console.error(err);
								return null;
							});
							localStorage.removeItem('token');
							location.href = getLogoutRedirectUrl(res?.redirect_url);
						}}>{$i18n.t('Sign Out')}</button
					>
				</div>
			</div>
		</div>
	</div>
</div>
