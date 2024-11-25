document.addEventListener("DOMContentLoaded", function () {
    const messageModal = document.getElementById("messageModal");
    const shouldShowModal = {{ show_modal|yesno:"true,false" | safe }}; // Converts True/False to JS boolean

    if (messageModal && shouldShowModal) {
        const modalInstance = new bootstrap.Modal(messageModal);
        modalInstance.show();
    }
})