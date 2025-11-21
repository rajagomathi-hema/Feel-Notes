const saveContainer = document.getElementById('saveContainer');

document.addEventListener('DOMContentLoaded', () => {
    fetch('/save/getAll')
        .then(response => response.json())
        .then(saveData => {
            if (saveData.status == "success") {

                saveContainer.innerHTML = ''

                let data = saveData.data
                let savedNoteList = []

                data.forEach(savedNote => {

                    let button = savedNote.note.content.length > 200 ? `
                        <button type="button" style="font-size: inherit;"
                        class="btn btn-link p-0 text-decoration-none text-primary read-more-btn">
                        Read more
                        </button>
                    ` : '';

                    let savedNoteSnippet = `
                        <div class="col-md-6">
                            <div class="card h-100 note-card shadow-sm">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-2 text-center">
                                            <span class="fs-3">${savedNote.note.mood}</span>
                                        </div>

                                        <div class="col-10">
                                            <p class="text-muted truncated-text mb-1" style="font-size: inherit;">
                                                ${savedNote.note.content}
                                            </p>

                                            ${button}

                                            <button class="btn btn-outline-danger btn-sm float-end delete-btn" data-id="${savedNote.id}">
                                                Delete
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `

                    savedNoteList.push(savedNoteSnippet);
                });

                saveContainer.innerHTML = savedNoteList.join('')

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

                let deleteBtn = document.querySelectorAll('.delete-btn');

                deleteBtn.forEach(btn => {
                    btn.addEventListener('click', () => {

                        let saveNoteId = btn.dataset.id;


                        fetch(`/save/delete?id=${saveNoteId}`, {
                            method: 'DELETE'
                        })
                            .then(res => res.json())
                            .then(result => {
                                if (result.status === "success") {
                                    btn.closest('.col-md-6').remove();
                                }
                                else {
                                    throw new Error(result.message);
                                }
                            })
                            .catch(err => alert(err));
                    });
                });
            } else {
                throw new Error(saveData.message);
            }
        })
        .catch(err => {
            alert(err)
        })
})














