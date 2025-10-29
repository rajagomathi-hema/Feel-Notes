document.addEventListener("DOMContentLoaded", function () {
    // Handle "Read more" logic
    document.querySelectorAll('.truncated-text').forEach(textEl => {
        const readMoreBtn = textEl.parentElement.querySelector('.read-more-btn');
        if (readMoreBtn && textEl.scrollHeight <= textEl.clientHeight + 2) {
            readMoreBtn.style.display = 'none';
        }
    });

    // Show modal dynamically
    const noteModal = new bootstrap.Modal(document.getElementById('noteModal'));
    const modalBody = document.getElementById('noteModalBody');

    document.querySelectorAll('.read-more-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const fullText = this.parentElement.querySelector('.truncated-text').textContent.trim();
            modalBody.textContent = fullText;
            noteModal.show();
        });
    });

    // === Mood Pie Chart ===
    const data = {
        labels: ["Happy 😀", "Loved 😍", "Sad 😢", "Angry 😡", "Excited 🤩"],
        datasets: [{
            data: [35, 25, 15, 10, 15],
            backgroundColor: [
                "#4CAF50",  // green (Happy)
                "#FF69B4",  // pink (Loved)
                "#2196F3",  // blue (Sad)
                "#FF5722",  // orange (Angry)
                "#FFD700"   // yellow (Excited)
            ],
            borderColor: "#fff",
            borderWidth: 2
        }]
    };

    const config = {
        type: "pie",
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        font: { size: 13 }
                    }
                }
            }
        }
    };

    const ctx = document.getElementById("moodChart").getContext("2d");
    new Chart(ctx, config);
});
