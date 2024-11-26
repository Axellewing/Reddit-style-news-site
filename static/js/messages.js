document.addEventListener("DOMContentLoaded", function() {
    const messageModal = document.getElementById("messageModal");
    if (messageModal) {
        const modalInstance = new bootstrap.Modal(messageModal);
        modalInstance.show();
    }
});