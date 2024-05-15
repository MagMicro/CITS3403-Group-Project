var selectedTags = [];

function updateTagsField() {
    document.querySelector('#tags').value = selectedTags.join(',');
}

document.querySelectorAll('.tag-button').forEach(item => {
    item.addEventListener('click', event => {
        if (selectedTags.includes(item.dataset.tag)) {
            selectedTags = selectedTags.filter(tag => tag !== item.dataset.tag);
            item.classList.remove('selected');
            item.style.backgroundColor = 'rgb(255, 255, 255)';
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

