<script lang="ts">
  import { onMount } from 'svelte';
  import type { GlobalInterface } from '../../utils/interface';
  import { API_URL } from '../../utils/contants';

  let data: GlobalInterface | null = null;
  let error: string | null = null;

  onMount(async () => {
    try {
      const response = await fetch(`${API_URL}/second`);
      if (!response.ok) {
        throw new Error(`Error fetching data: ${response.statusText}`);
      }
      data = await response.json(); // Assuming the response is JSON
    } catch (err: unknown) {
      error = err instanceof Error ? err.message : 'An unknown error occurred';
    }
  });
</script>

{#if error}
  <p style="color: red;">Error: {error}</p>
{:else if data}
  <div>
    <h1>{data.title}</h1>
    <p>{data.subtitle} Visit <a href="/">Home page </a></p>
  </div>
{:else}
  <p>Loading...</p>
{/if}

<style>
  /* Add your styles here */
</style>
