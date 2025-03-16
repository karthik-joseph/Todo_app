// Update form handling
function initializeUpdateForm() {
  const updateForm = document.getElementById("updateForm");
  if (updateForm) {
    updateForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(this);
      fetch(this.action, {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            document.getElementById("successPopup").classList.add("show");
          } else {
            throw new Error("Failed to update task");
          }
        })
        .catch((error) => {
          alert("Error: " + error.message);
          window.location.href = "/task";
        });
    });
  }
}

function redirectToTasks() {
  window.location.href = "/task";
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  initializeUpdateForm();
});
