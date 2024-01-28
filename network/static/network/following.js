document.addEventListener("DOMContentLoaded", function(){
    //When the heart button is clicked
    document.querySelectorAll('.heart').forEach(function(button){
        button.onclick = function(){
            //Get the post associated with the heart and the action
            const post_id = button.dataset.id;
            const action = button.dataset.action;

            // If the action is like, execute the like function
            if (action === "like"){
                like(post_id, action, button)
            }

            //If the action is unlike, execute the unlike function
            else if (action === "unlike"){
                like(post_id, action, button)
            }
        }
    });
})

function like(post_id,action,button){
    fetch(`/editpost/${post_id}`,{
        method: 'PUT',
        body: JSON.stringify({
            "action": action
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result["error"]){
            console.log(result["error"])
        }
        else{
            //Get the new like count
            const new_count = result["like_count"]
            //Update the like count
            document.querySelector(`#like-count-${post_id}`).innerHTML = new_count
            if (action === 'like'){
                //Change the action to unlike
                button.setAttribute('data-action', 'unlike')
                //Set the heart to red color
                button.classList.toggle('active');
            }
            else if (action === 'unlike'){
                //Change the action to like
                button.setAttribute('data-action', 'like')
                //Set the heart to blank
                button.classList.toggle('active');
            }
        }
    })
}