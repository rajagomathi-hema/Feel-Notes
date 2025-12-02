
document.addEventListener("DOMContentLoaded", function () {
    let emojiList = []
    let countList = []
    const emojiLabels = {
        "😊": "Happy 😊",
        "😍": "Loved 😍",
        "😢": "Sad 😢",
        "😡": "Angry 😡",
        "😂": "Funny 😂"
    };

    fetch('/note/analytics')
        .then(response => response.json())
        .then(responseData => {
            if (responseData.status == "success") {
                let reactionTotals = responseData.reactionTotals
                for (let emoji in reactionTotals) {
                    countList.push(reactionTotals[emoji])
                    emojiList.push(emojiLabels[emoji])
                }


                console.log(emojiList, countList)

                // === Mood Pie Chart ===
                const data = {
                    labels: emojiList,
                    datasets: [{
                        data: countList,
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

                console.log(data)

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
                console.log(config)
                new Chart(ctx, config);
            } else {
                throw new Error(data.message);

            }
        })
        .catch(err => {
            alert(err)
        })
});