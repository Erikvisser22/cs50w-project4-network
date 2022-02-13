function follow(id){
    follow_text = document.getElementById('btn-follow')
    followers_count = document.getElementById('followers_count')

    if (follow_text.innerHTML == "Follow"){
        follow_status = true;
        follow_text.innerHTML = "Unfollow";
    }   
    else {
        follow_status = false;
        follow_text.innerHTML = "Follow";
    }
    
    fetch(`/profile/${id}`,{
        method : 'PUT',
        body : JSON.stringify({
            follow : follow_status,
            follow_id : id
        })
    })
    .then(response => response.json())
    .then(data => {
        followers_count.innerHTML = "Followers: " + data['followers_count']
    });

}