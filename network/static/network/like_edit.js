function edit(id){

    // get relevant parameters
    let element = document.getElementById(`edit-${id}`);
    let edit_button = document.getElementById(`btn-edit-${id}`);
    let save_button = document.getElementById(`btn-save-${id}`);
    let current_text = element.innerHTML;

    // change edit button to save via display style
    edit_button.style.display = "none";
    save_button.style.display = "block";

    // create a new element -> textarea
    var edit_field = document.createElement('textarea'); 
    edit_field.class = "form-control";
    edit_field.value = current_text;
    edit_field.cols = 75;
    edit_field.id = element.id;

    element.replaceWith(edit_field)
}

function save(id){

    // get relevant parameters
    let element = document.getElementById(`edit-${id}`);
    let edit_button = document.getElementById(`btn-edit-${id}`);
    let save_button = document.getElementById(`btn-save-${id}`);
    let new_text = element.value;

    // fetch new text to back-end
    fetch(`/save/${id}`,{
        method: 'POST',
        body: JSON.stringify({
            new_text : new_text
        })
    });

    // create new element for text and replace with the old one
    let new_element = document.createElement('span');
    new_element.innerHTML = new_text;
    new_element.id = element.id;

    element.replaceWith(new_element)  
    
    // toggle back to edit button
    edit_button.style.display = "block";
    save_button.style.display = "none";
}

function like(id){

    // get relevant parameters
    let like_text = document.getElementById(`btn-like-${id}`);
    let like_count = document.getElementById(`like-count-${id}`);
    let total_likes = document.getElementById('total_likes');

    // check, set status and toggle like/unlike
    if (like_text.innerHTML == "like"){
        like_status = true;
        like_text.innerHTML = "unlike";
    }   
    else {
        like_status = false;
        like_text.innerHTML = "like";
    }

    // fetch likes status to back-end
    fetch(`/like/${id}`,{
        method: 'PUT',
        body: JSON.stringify({
            like : like_status
        })
    })
    // change innerHTML with updated data
    .then(response => response.json())
    .then(data => {
        like_count.innerHTML = data['likes'],
        total_likes.innerHTML = "Likes: " + data['total_likes']
    });
}