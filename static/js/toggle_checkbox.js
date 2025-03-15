console.log("Toggle checkbox script loaded");
document.addEventListener("DOMContentLoaded", function () {
  // Get all checkboxes in the checklist
  const checkboxes = document.querySelectorAll(
    '#checklist .todo-item .todo-content input[type="checkbox"]'
  );

  const success_message = document.querySelector(".success_message");
  const error_message = document.querySelector(".error_message");

  if (success_message) {
    setTimeout(() => {
      success_message.style.display = "none";
    }, 2000);
  }

  if (error_message) {
    setTimeout(() => {
      error_message.style.display = "none";
    }, 2000);
  }
  console.log("Checkboxes:", checkboxes);
  // Add event listener to each checkbox
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      const taskId = this.value;
      const isCompleted = this.checked;

      console.log("Task ID:", taskId);

      // Send AJAX request to update task status
      updateTaskStatus(taskId, isCompleted);
    });
  });

  // Function to send AJAX request
  function updateTaskStatus(taskId, isCompleted) {
    fetch(`/task/toggle/${taskId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify({ completed: isCompleted }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Task updated:", data);
      })
      .catch((error) => {
        console.error("Error updating task:", error);
        // Revert checkbox state if there was an error
        const checkbox = document.getElementById(taskId);
        if (checkbox) {
          checkbox.checked = !isCompleted;
        }
      });
  }
});
