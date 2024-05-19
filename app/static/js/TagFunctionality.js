// Stores the tags currently selected by a user, submitted with poll form
const selectedTags = [];

function updateTagsField() {
    document.querySelector('#tags').value = selectedTags.join(',');
}
$(document).ready(() => {
    document.querySelectorAll('.tag-button').forEach(item => {
        item.addEventListener('click', event => {
            // If the tag clicked was already selected, deselect it
            if (selectedTags.includes(item.dataset.tag)) {
                selectedTags = selectedTags.filter(tag => tag !== item.dataset.tag);
                item.classList.remove('selected');
                item.style.backgroundColor = 'rgb(255, 255, 255)';
            // If the tag wasn't already selected, add it to the selected list
            } else {
                if (selectedTags.length < 3) {
                    selectedTags.push(item.dataset.tag);
                    item.classList.add('selected');
                    item.style.backgroundColor = 'rgba(0, 0, 0, 0.2)';
                }
            }
            updateTagsField();
        });
    });
});

