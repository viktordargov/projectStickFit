function confirmDeletion() {
            if (confirm("Are you sure you want to delete all workout history? This action cannot be undone.")) {
                document.getElementById('delete-form').submit();
            }
        }