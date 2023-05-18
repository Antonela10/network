document.addEventListener('DOMContentLoaded', function() {

    var like_buttons = document.querySelectorAll('.like-button');

    like_buttons.forEach(function (like_button) {
        like_button.addEventListener('click', function(e) {
            const button_one = e.target;
            button_clicked = button_one.parentNode;
            const post_liked_id = button_clicked.dataset.liked;
            const post_liked = button_clicked.parentNode;

            var likes_number = button_clicked.querySelector("#likes-number");

            var request_user = post_liked.querySelector("#request-user");

            if (button_one.style.color == 'red') {
                button_one.style.color = 'grey';
                // button_clicked.style.border = 'none';
                // button_clicked.style.outline = 'none';
            } else {
                button_one.style.color = 'red';
                // button_clicked.style.border = 'none';
                // button_clicked.style.outline = 'none';
            }

            fetch('/like/' + post_liked_id, {
                method: 'PUT',
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken").value,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    'id': post_liked_id,
                })
            })
            .then(response => response.json())
            .then(data => {
                likes_number.textContent = data.likes;
            })
        })
    })
})