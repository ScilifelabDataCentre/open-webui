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
		class="fixed inset-0 z-1000 flex items-center justify-center bg-white/80 p-4 text-black backdrop-blur-md dark:bg-black/80 dark:text-white"
	>
		<div
			class="w-full max-w-3xl rounded-[2rem] border border-black/10 bg-white/95 shadow-2xl dark:border-white/10 dark:bg-gray-900/95"
		>
			<div class="border-b border-black/10 px-6 py-5 dark:border-white/10 sm:px-8">
				<div
					class="text-xs font-semibold uppercase tracking-[0.18em] text-gray-500 dark:text-gray-400"
				>
					SciLifeLab OpenLLM Policy
				</div>
				<h1 class="mt-2 text-2xl font-semibold sm:text-3xl">Review and accept to continue</h1>
				<p class="mt-2 max-w-2xl text-sm leading-6 text-gray-600 dark:text-gray-300">
					Please review the policy below before continuing. By accepting, you confirm that you
					understand the pilot nature of the service and agree to use it in accordance with the
					rules set out here.
				</p>
			</div>

			<div class="px-6 py-6 sm:px-8">
				<div
					class="max-h-[52vh] overflow-y-auto rounded-[1.5rem] border border-black/10 bg-gray-50/80 p-5 text-sm leading-6 text-gray-700 dark:border-white/10 dark:bg-white/5 dark:text-gray-200"
				>
					<p>
						SciLifeLab OpenLLM is a pilot project where we are currently assessing the technical and
						infrastructure setup. We currently do not have a use policy because we have not yet
						settled on the technical setup and have not yet carried out assessments required to
						establish expected confidentiality, integrity, and availability of our service and user
						content. Keep in mind that we do not guarantee that this pilot will become a production
						grade service at this point. We will create and publish a clear use policy and describe
						expectations once it is possible and before we move on to offering a production grade
						service.
					</p>
					<p class="mt-4">
						In the meantime, please keep in mind that this service is for testing purposes and:
					</p>
					<ul class="mt-3 list-disc space-y-3 pl-6">
						<li>
							Do not send any text, data, or code that requires any level of confidentiality above
							publicly available information (in other words, do not send things that are not public
							information or where the information would not be allowed to be made public);
						</li>
						<li>
							Do not expect any guaranteed integrity, uptime, latency, or throughput; Keep in mind
							that this is a pilot and it can be shut down at any time;
						</li>
						<li>
							Do not use the service for anything that violates the requirements or policies from
							your own university (employer), the Swedish law, the EU regulations, SciLifeLab
							policies, ethical review board or research ethics committee decisions, etc.
						</li>
					</ul>
					<p class="mt-4">
						Please get acquainted with our documentation and follow announcements: <a
							class="break-words font-medium text-blue-600 underline underline-offset-2 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
							href="https://openllm.scilifelab.se/docs/">https://openllm.scilifelab.se/docs/</a
						>
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
