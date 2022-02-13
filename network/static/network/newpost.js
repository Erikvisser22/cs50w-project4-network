
document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#post_form').addEventListener('submit', new_post);

});

function new_post() {

    fetch(`new_post` , {
        method: 'POST',
        body: JSON.stringify({
            text: document.querySelector('#postTextarea').value
        })
    })
}

    


