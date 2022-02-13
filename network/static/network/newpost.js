
document.addEventListener('DOMContentLoaded', function() {

    // set eventlistener for a new post
    document.querySelector('#post_form').addEventListener('submit', new_post);

});

function new_post() {

    // fetch new post data to back-end
    fetch(`new_post` , {
        method: 'POST',
        body: JSON.stringify({
            text: document.querySelector('#postTextarea').value
        })
    });
};

    


