// custom javascript

(function() {
  console.log('Sanity Check!');
})();

function handleClick(type) {
  fetch('/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
      { task_type: type, latitude: 37.7749, longitude: 122.4194, elevation: 0 }
    ),
  })
  .then(response => response.json())
    .then(data => {
    console.log('Success:', data);
    getStatus(data.task_id)
  })
}

function getStatus(taskID) {
  fetch(`/tasks/${taskID}/status`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    console.log(res)
    const html = `
      <tr>
        <td>${res.task_id}</td>
        <td>${res.status}</td>
        <td>${res.result}</td>
      </tr>`;
    const newRow = document.getElementById('tasks').insertRow(0);
    newRow.innerHTML = html;

    const taskStatus = res.status;
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') {
      return false;
    }
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);
  })
  .catch(err => console.log(err));
}
