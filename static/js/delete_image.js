function deleteImage(postId) {
    if (!confirm("Are you sure you want to delete this image?")) {
        return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch(deletePostUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({image_id: postId})
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                document.getElementById(`image-${postId}`).remove();
                location.reload();
            }
        })
        .catch(error => console.error("Error:", error));
}

