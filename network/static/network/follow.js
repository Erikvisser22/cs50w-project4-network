function follow(id){

    // get relevant parameters
    follow_text = document.getElementById('btn-follow')
    followers_count = document.getElementById('followers_count')

    // check, set status and toggle follow/unfollow
    if (follow_text.innerHTML == "Follow"){
        follow_status = true;
        follow_text.innerHTML = "Unfollow";
    }   
    else {
        follow_status = false;
        follow_text.innerHTML = "Follow";
    }
    
    // fetch follow status and id to back-end
    fetch(`/profile/${id}`,{
        method : 'PUT',
        body : JSON.stringify({
            follow : follow_status,
            follow_id : id
        })
    })
    // update followers count from response data
    .then(response => response.json())
    .then(data => {
        followers_count.innerHTML = "Followers: " + data['followers_count']
    });

}