document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll(".edit-button").forEach(function(button){
        button.addEventListener("click", function(){
            //Get the post id
            const post_id = button.dataset.id
            //Get the element that holds the post content
            const post_content_field = document.querySelector(`#post-content-${post_id}`)
            //Get the post content text
            const post_content= document.querySelector(`#post-content-${post_id}`).innerHTML
            // Create a div for the editForm
            const editForm = document.createElement("div");
            editForm.classList.add("col")
            //Create a button for saving the form
            const saveButton = document.createElement("button");
            //set attribute, and classes, and set icon to innerHTML
            saveButton.setAttribute('form', `edit-post${post_id}`);
            saveButton.setAttribute('type', 'submit');
            saveButton.classList.add("update-button")
            saveButton.innerHTML = `<i class="bi bi-floppy-fill"></i>`

            //Create a div for cancel button
            const cancelButton = document.createElement("div");
            cancelButton.classList.add("text-center")
            cancelButton.innerHTML = `<button class="cancel-button"><i class="bi bi-x-circle-fill"></i></button>`

            //put the form into the editForm div
            editForm.innerHTML = 
            `<form id="edit-post${post_id}">
            <textarea required rows="4" cols="75" id="edit-post" class="form-control" name="content">${post_content}</textarea>
            </form>`
            //put the cancelButton inside the editForm,put it after the form
            editForm.append(cancelButton)

            //Replace the edit button with save button
            button.replaceWith(saveButton);
            //Replace the post content with EditForm
            post_content_field.replaceWith(editForm);

            //Get the text area and focus it, put the cursor at the end of the text
            const editField = editForm.querySelector("#edit-post");
            editField.focus();
            editField.setSelectionRange(post_content.trim().length, post_content.trim().length);
            
            //If the edit form is submitted, 
            editForm.querySelector("form").onsubmit = function(){
                const new_post_content = editField.value.trim();
                // Check of the length of the new content is less than 280
                if (0 < new_post_content.length <= 280) {
                    editPost(new_post_content, post_id, post_content_field, button, editForm, saveButton);
                } else {
                    console.log("Invalid post length.");
                }
                return false;
            }
            //If the cancel button is clicked, put back the edit button and post content
            editForm.querySelector(".cancel-button").onclick = function(){
                editForm.replaceWith(post_content_field);
                saveButton.replaceWith(button);
            }


        })
    });

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


function editPost(new_post_content, post_id, post_content_field, button, editForm, saveButton){
    fetch(`/editpost/${post_id}`,{
        method: 'PUT',
        body: JSON.stringify({
            "content": new_post_content
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result["error"]){
            console.log(result["error"])
        }
        else{
            //Change the original post body content to the new content
            post_content_field.innerHTML = new_post_content;
            //Put back the post body and edit button
            editForm.replaceWith(post_content_field);
            saveButton.replaceWith(button);
        }
    })
}


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

