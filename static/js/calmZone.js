const emojis = ["🌙", "⭐", "✨", "💫", "🌟", "💛", "💜", "💖", "🤍", "🤎"];
const quotes = [
    "“Peace begins with a smile.”",
    "“Let your worries drift away.”",
    "“You are light and calm.”",
    "“Happiness grows where peace lives.”",
    "“Breathe in sunshine, exhale stress.”",
    "“Choose calm, choose joy.”",
    "“You deserve peace and happiness.”"
];

const quoteEl = document.getElementById('quote');
const releaseBtn = document.getElementById('releaseBtn');

const releaseText = document.getElementById('releaseText');

// 🌿 Change quote every few seconds
setInterval(() => {
    quoteEl.style.opacity = 0;
    setTimeout(() => {
        quoteEl.textContent = quotes[Math.floor(Math.random() * quotes.length)];
        quoteEl.style.opacity = 1;
    }, 1000);
}, 6000);

// 🕊️ Handle Release button click
releaseBtn.addEventListener('click', () => {
    const text = thoughtInput.value.trim();
    if (text) {
        releaseText.textContent = "💭 " + text + " 💭";
        releaseText.style.display = "block";
        releaseText.classList.add("fade-away");

        for (let i = 0; i < 5; i++) createFloatingEmoji();

        setTimeout(() => {
            releaseText.style.display = "none";
            releaseText.classList.remove("fade-away");
            thoughtInput.value = "";
        }, 2000);
    } else {
        releaseText.textContent = "💛 Write something to release...";
        releaseText.style.display = "block";
        setTimeout(() => releaseText.style.display = "none", 1500);
    }
});

// 🌼 Floating emoji creation
function createFloatingEmoji() {
    const emoji = document.createElement("div");
    emoji.classList.add("float-emoji");
    emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    emoji.style.left = Math.random() * 100 + "%";
    emoji.style.animationDuration = (Math.random() * 6 + 8) + "s";
    emoji.style.fontSize = Math.random() * 12 + 20 + "px";
    document.body.appendChild(emoji);
    setTimeout(() => emoji.remove(), 13000);
}

// 🌈 Background emoji floating slowly
setInterval(createFloatingEmoji, 1800);



const zoneForm = document.getElementById("zoneForm");

zoneForm.addEventListener('submit', (e) => {
    e.preventDefault()

    const thoughtInput = document.getElementById("thoughtInput").value

    const data = { "content": thoughtInput }

    fetch("/calmZone/new", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status == "success") {
                alert(data.message)
                zoneForm.reset()
                location.reload()
            } else {
                throw new Error(data.message);

            }
        })
        .catch(err => {
            alert(err)
        })

})