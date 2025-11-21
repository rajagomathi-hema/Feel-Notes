const noteForm = document.getElementById("Notes");

noteForm.addEventListener('submit', (e) => {
    e.preventDefault()

    const note = document.getElementById("note").value
    const mood = document.querySelector('input[name="emoji"]:checked').value


    const data = { "content": note, "mood": mood }

    fetch("/note/new", {
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
                noteForm.reset()
                location.reload()
            } else {
                throw new Error(data.message);

            }
        })
        .catch(err => {
            alert(err)
        })

})


const noteContainer = document.getElementById('noteContainer')

document.addEventListener('DOMContentLoaded', () => {
    fetch('/note/getAll')
        .then(response => response.json())
        .then(notesData => {
            if (notesData.status == "success") {
                noteContainer.innerHTML = ''
                let data = notesData.data
                let noteList = []
                data.forEach(note => {

                    let button = note.content.length > 200 ? `
                        <button type="button" style="font-size: inhert;"
                            class="btn btn-link p-0 text-decoration-none text-primary read-more-btn">
                            Read more
                        </button>
                    `: ''

                    let noteSnippet = `
                        <div class="col-md-6">
                            <div class="card h-100 note-card shadow-sm">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-2 text-center">
                                            <span class="fs-3">${note.mood}</span>
                                        </div>
                                        <div class="col-10">
                                            <p class="text-muted truncated-text mb-1" style="font-size: inhert;">
                                                ${note.content}
                                            </p>

                                            ${button}
                                        </div>
                                    </div>

                                    <div class="d-flex justify-content-between mt-3 pt-2 border-top">
                                        <div class="d-flex align-items-center">
                                            <button class="btn border-0 fs-4 p-0">😀</button>
                                            <span class="count"></span>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <button class="btn border-0 fs-4 p-0">😍</button>
                                            <span class="count"></span>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <button class="btn border-0 fs-4 p-0">😒</button>
                                            <span class="count"></span>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <button class="btn border-0 fs-4 p-0">😘</button>
                                            <span class="count"></span>
                                        </div>
                                        
                                        <div class="d-flex align-items-center">
                                            <button class="btn saveBtn border-0 p-0" data-id="${note.id}"><i style='color: var(--primary) !important' class="fs-4 ${note.isSaved? 'bi bi-bookmark-fill': 'bi bi-bookmark'}"></i></button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `
                    noteList.push(noteSnippet)
                });

                noteContainer.innerHTML = noteList.join('')

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

                let saveBtn = document.querySelectorAll(".saveBtn");

                saveBtn.forEach(btn => {
                    btn.addEventListener('click', () => {

                        let noteId = btn.dataset.id;


                        fetch(`/save/new?id=${noteId}`)
                            .then(res => res.json())
                            .then(result => {
                                if (result.status === "saved") {
                                    btn.querySelector('i').classList.remove('bi-bookmark');
                                    btn.querySelector('i').classList.add('bi-bookmark-fill');
                                }
                                else if (result.status === "unsaved") {
                                    btn.querySelector('i').classList.remove('bi-bookmark-fill');
                                    btn.querySelector('i').classList.add('bi-bookmark');
                                }
                                else{
                                    throw new Error(result.message);
                                    
                                }
                            })
                            .catch(err => alert(err));
                    });
                });

                
            } else {
                throw new Error(notesData.message);

            }
        })
        .catch(err => {
            alert(err)
        })
})