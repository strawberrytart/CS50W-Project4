document.addEventListener("DOMContentLoaded", function(){
    
    // let querySelector fail silently if editProfileButton is not found on the page
    const saveButton = document.querySelector('#saveEditProfile');
    if (saveButton){
        // disable the saveButton
        saveButton.disabled = true;
    }

    // If user releases a key in the bio textarea, allow user to submit the form
    const editBio = document.querySelector('#edit_bio');
    if (editBio){
        editBio.onkeyup = function(){
            console.log(this)
            saveButton.disabled = false;
        }
    }
    
    //If user attached an image file, allow user to submit the form
    const profilePic = document.getElementById('id_profile_image')
    if (profilePic){
        profilePic.addEventListener('change', function() {
            const fileInput = this;
            if (fileInput.files.length > 0) {
            console.log('File attached:', fileInput.files[0]);
            saveButton.disabled = false;

            } else {
            console.log('No file attached');
            saveButton.disabled = true;
            }
        });
    }
    
    //When the follow-buttons are clicked, depending on the text execute unfollow or follow 
    const followButton = document.querySelectorAll('#follow-button');
    if (followButton){
        followButton.forEach(function(button){
            button.addEventListener('click', function(){
                if (button.innerHTML === "Unfollow"){
                    unfollow(button.dataset.id, button)
                }
                else if (button.innerHTML === "Follow"){
                    follow(button.dataset.id, button)
                }
            })
        })
    }
});

//Send a PUT request to the path /follow/${profile_id}
function follow(profile_id, button){
    fetch(`/follow/${profile_id}`,{
        method: 'PUT',
        body: JSON.stringify({
            action : "follow"
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result["error"]){
            console.log(result["error"])
        }
        else{
            //If there is not error, update the following or follower count without refreshing the page
            const followingCount = document.querySelector('#following-count')
            if (followingCount){
                followingCount.innerHTML = result["following"]
            }

            const followerCount = document.querySelector('#follower-count')
            if (followerCount){
                followerCount.innerHTML = result["followers"]
            }
            button.innerHTML = "Unfollow";
            button.classList.add('unfollow');
        }
    })
}

//Send a PUT request to /follow/${profile_id}
function unfollow(profile_id, button){
    // Using fetch API to make asynchronous request to the server
    fetch(`/follow/${profile_id}`,{
        method: 'PUT',
        // Sending JSON data in the request body
        body: JSON.stringify({
            action : "unfollow"
        })
    })
    // Handling the response from the server as JSON
    .then(response => response.json())
    .then(result => {
        if (result["error"]){
            console.log(result["error"])
        }
        else{
            //If there is not error, update the following or follower count without refreshing the page
            const followingCount = document.querySelector('#following-count')
            if (followingCount){
                followingCount.innerHTML = result["following"]
            }

            const followerCount = document.querySelector('#follower-count')
            if (followerCount){
                followerCount.innerHTML = result["followers"]
            }
            button.innerHTML = "Follow";
            button.classList.remove('unfollow')
        }
    })
}
