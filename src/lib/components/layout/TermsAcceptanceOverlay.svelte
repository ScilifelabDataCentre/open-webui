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
					OpenLLM is a pilot service run by SciLifeLab Data Centre providing access to
					open-weight large language models.
				</p>
			</div>

			<div class="px-6 py-6 sm:px-8">
				<div
					class="max-h-[52vh] overflow-y-auto rounded-[1.5rem] border border-black/10 bg-gray-50/80 p-5 text-sm leading-6 text-gray-700 dark:border-white/10 dark:bg-white/5 dark:text-gray-200"
				>
					<h2 class="text-base font-semibold text-black dark:text-white">What is this?</h2>
					<p class="mt-2">
						OpenLLM is a pilot service run by SciLifeLab Data Centre providing access to
						open-weight large language models (LLMs) hosted on infrastructure controlled by
						SciLifeLab. The service offers both a chat interface (Open WebUI) and API endpoints.
						The pilot runs during spring 2026 with a limited group of users.
					</p>
					<p class="mt-2">
						Our primary focus is enabling API-based access so that LLMs can be embedded in
						research workflows, automation pipelines, and agentic tools. The chat interface is
						available as a convenience, but the pilot is not optimized for users who only need a
						ChatGPT-style experience.
					</p>
					<p class="mt-2">
						The goal is to learn what use cases SciLifeLab-hosted LLMs can realistically support,
						what infrastructure and expertise are needed, and what a future production service
						could look like.
					</p>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">
						What you can use it for
					</h2>
					<ul class="mt-2 list-disc space-y-2 pl-5">
						<li>Embedding LLMs in research workflows and pipelines via the API</li>
						<li>Prototyping agentic tools and automations</li>
						<li>
							Working with data that should not leave SciLifeLab-controlled infrastructure (e.g.
							internal code, non-public datasets, or information containing personal data that is
							not patient/healthcare data)
						</li>
						<li>Evaluating open-weight models for your specific research or platform needs</li>
					</ul>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">
						What you should not use it for
					</h2>
					<ul class="mt-2 list-disc space-y-2 pl-5">
						<li>Processing patient data or data classified above "internal" sensitivity</li>
						<li>
							Any use case that requires guaranteed uptime, latency, or throughput; this is a
							pilot, not a production service
						</li>
						<li>Heavy sustained workloads that could degrade the service for other pilot users</li>
						<li>
							Anything that violates Swedish law, EU regulations, SciLifeLab policies, ethical
							review board or research ethics committee decisions, or your university's own
							policies
						</li>
					</ul>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">
						Where does the data live?
					</h2>
					<p class="mt-2">
						All models run on infrastructure controlled by SciLifeLab Data Centre, deployed on the
						KTH Kubernetes cluster and SafeSpring cloud, located in Sweden. Your prompts and outputs
						are processed on this infrastructure and are not sent to any third-party provider. We do
						not train models on your data.
					</p>
					<p class="mt-2">
						We may collect anonymized usage metrics (request counts, token volumes, latency) to
						evaluate the pilot. We do not log prompt content beyond what is needed for debugging
						during the pilot period.
					</p>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">
						What we do and do not promise
					</h2>
					<p class="mt-2 font-semibold text-black dark:text-white">We do:</p>
					<ul class="mt-2 list-disc space-y-2 pl-5">
						<li>Provide access to a curated set of small and medium-size open-weight LLMs</li>
						<li>Make a reasonable effort to keep the service available during the pilot</li>
						<li>Actively collect your feedback to shape future decisions</li>
					</ul>
					<p class="mt-4 font-semibold text-black dark:text-white">We do not:</p>
					<ul class="mt-2 list-disc space-y-2 pl-5">
						<li>Guarantee availability, performance, or specific model versions</li>
						<li>Commit to continuing the service beyond the pilot period</li>
						<li>Provide support equivalent to a production service</li>
					</ul>

					<h2 class="mt-5 text-base font-semibold text-black dark:text-white">Feedback</h2>
					<p class="mt-2">
						Your input is the most valuable output of this pilot. Please share feedback, use cases,
						issues, and ideas at
						<a class="underline" href="mailto:serve@scilifelab.se">serve@scilifelab.se</a>
						or through the channels provided to you when you joined the pilot.
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
