document.addEventListener('DOMContentLoaded', function() {

    // Disable the post button (prevent from posting empty posts)
    document.querySelector("#post_button").disabled = true;

    post_form = document.querySelector("#post-form");
    post_form.onkeyup = () => {
        if (post_form.value.length > 0) {
            document.querySelector("#post_button").disabled = false;
        } else {
            document.querySelector("#post_button").disabled = true;
        }
    };

    var all_posts = document.querySelector("#all-posts");
    all_posts.addEventListener('click', (event) => {
        if (event.target.tagName === 'BUTTON') {
            const button = event.target;
            const post_id = button.dataset.post; // post id
            const post = button.parentNode;
            const post_body = post.querySelector('.post-body');
            const input_div = post.querySelector('.input-div');

            if (button.textContent === 'Edit') {
                input_div.style.display = 'block';
                var input = document.createElement('input');
                input.type = 'text';
                input.value = post_body.textContent;
                input.setAttribute('class', 'edited_input_value');
                input_div.appendChild(input);
                post_body.style.display = 'none';
                button.textContent = 'Save';
            } else if (button.textContent === 'Save') {
                const new_input = post.querySelector('.edited_input_value').value;

                fetch('/edit/' + post_id, {
                    method: 'PUT',
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken").value,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        'postBody': new_input,
                    })
                })
                .then(response => response.json())
                .then(data => {
                    post_body.textContent = data.postBody;
                    input_div.removeChild(input_div.firstElementChild);
                    post_body.style.display = 'block';
                    button.textContent = 'Edit';
                })
            }
            
        }
    })
})