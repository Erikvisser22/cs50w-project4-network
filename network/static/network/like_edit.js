function edit(id){

    let element = document.getElementById(`edit-${id}`);
    let edit_button = document.getElementById(`btn-edit-${id}`);
    let save_button = document.getElementById(`btn-save-${id}`);

    edit_button.style.display = "none";
    save_button.style.display = "block";

    let current_text = element.innerHTML;


    var edit_field = document.createElement('textarea'); 
    edit_field.class = "form-control";
    edit_field.value = current_text;
    edit_field.cols = 75;
    edit_field.id = element.id;

    element.replaceWith(edit_field)
}

function save(id){

    let element = document.getElementById(`edit-${id}`);
    let edit_button = document.getElementById(`btn-edit-${id}`);
    let save_button = document.getElementById(`btn-save-${id}`);

    let new_text = element.value;

    fetch(`/save/${id}`,{
        method: 'POST',
        body: JSON.stringify({
            new_text : new_text
        })
    });

    let new_element = document.createElement('span');
    new_element.innerHTML = new_text;
    new_element.id = element.id;

    element.replaceWith(new_element)    
    edit_button.style.display = "block";
    save_button.style.display = "none";
}

function like(id){

    let like_text = document.getElementById(`btn-like-${id}`);
    let like_count = document.getElementById(`like-count-${id}`)

    if (like_text.innerHTML == "like"){
        like_status = true;
        like_text.innerHTML = "unlike";
    }   
    else {
        like_status = false;
        like_text.innerHTML = "like";
    }
    
    fetch(`/like/${id}`,{
        method: 'PUT',
        body: JSON.stringify({
            like : like_status
        })
    })
    .then(response => response.json())
    .then(data => {
        like_count.innerHTML = data['likes']
    });
}