<script>
  import axios from "axios";

  const apiUrl = "http://localhost:8000";
  let data = null;
  let taskId = "";
  let intervalId = null;

  let errorText = null;
  let status = null;

  let current_progress_item = 1;
  let total_progress_item = 0;
  let progress_percentage = 0;
  let iteration_count = 0;

  const check_task_status = () => {
    let getTaskStatusUrl = `${apiUrl}/result/${taskId}`;
    axios
      .get(getTaskStatusUrl)
      .then((response_result) => {
        console.log(response_result);
        const taskStatus = response_result.data.status;
        if (response_result.data.response != null) {
          current_progress_item = response_result.data.response.current + 1;
          total_progress_item = response_result.data.response.total;
          progress_percentage = response_result.data.response.progress;
        }
        if (taskStatus === "COMPLETED") {
          clearInterval(intervalId);
          data = response_result.data.data.content;
          status = "COMPLETED";
        } else if (taskStatus === "FAILED") {
          clearInterval(intervalId);
          errorText = response_result.data.error;
          status = "FAILED";
        } else {
          status = "PROCESS";
        }
      })
      .catch((error) => {
        clearInterval(intervalId);
        status = "FAILED";
        errorText = error;
      });
  };

  const get_data = () => {
    axios
      .get(`${apiUrl}/long-process/${iteration_count}`)
      .then((response) => {
        taskId = response.data.task_id;
        if (taskId == undefined) {
          data = response.data.data;
          status = "COMPLETED";
          return;
        } else intervalId = setInterval(check_task_status, 1000);
      })
      .catch((error) => {
        status = "FAILED";
        errorText = error.response.data.error;
      });
  };
</script>

<main>
  <div class="data">
    <input class="form-control" type="text" bind:value={iteration_count} />
    <button type="button" class="btn btn-primary w-100 mt-2" on:click={get_data}
      >Submit</button
    >
    {#if status === "PROCESS"}
      <div class="status mt-2">
        {#if progress_percentage === 0}
          <p>there is a lot of users, you are in list. Please wait...</p>
        {:else}
          <div class="progress mt-2">
            <div
              class="progress-bar"
              role="progressbar"
              aria-valuenow={progress_percentage.toFixed(2)}
              aria-valuemin="0"
              aria-valuemax="100"
              style="width: {progress_percentage.toFixed(2)}%"
            >
              {current_progress_item} : {total_progress_item} || {progress_percentage.toFixed(
                2
              )}%
            </div>
          </div>
        {/if}
      </div>
    {/if}
    {#if status === "COMPLETED"}
      <div class="status">
        <p>{data}</p>
      </div>
    {/if}
    {#if status === "FAILED"}
      <div class="status">
        <p>FAILED</p>
        <p>{errorText}</p>
      </div>
    {/if}
  </div>
</main>
