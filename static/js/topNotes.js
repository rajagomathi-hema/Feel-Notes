document.addEventListener("DOMContentLoaded", () => {

    const radios = document.querySelectorAll(".reaction-radio");
    const topNoteText = document.getElementById("topNoteText");

    radios.forEach(radio => {
        radio.addEventListener("change", async () => {
            const emoji = radio.dataset.emoji;

            try {
                const res = await fetch(`/note/topnote/${emoji}`);
                const data = await res.json();

                if (!data || !data.note || !data.note.content) {
                    topNoteText.textContent = "No note found for this reaction.";
                    return;
                }

                topNoteText.textContent = data.note.content;


            } catch (err) {
                topNoteText.textContent = "Error loading the note.";
            }
        });
    });
});

