$("#enable_user").click((event) => {
    let user_id = event.target.dataset.id;
    let data_url = "enable_user?user_id="+user_id;
    $.get({url: data_url, success: (result) => {
        if (result.success) {
            
            toastr["success"]("Enabled User");
            window.location.reload();
        } 
      }})
});

$("#delete_user").click((event) => {
    let user_id = event.target.dataset.id;
    let data_url = "delete_user?user_id="+user_id;
    $.get({url: data_url, success: (result) => {
        if (result.success) {
            
            toastr["success"]("Deleted user");
            window.location.reload();
        } 
      }})
});

$(".role-edit-select").click((event) => {
    console.log(event.target.dataset);
    let role_id = event.target.dataset.id;
    let user_id = event.target.dataset['userId'];
    let data_url = "change_role?user_id="+user_id+"&role_id="+role_id;
    $.get({url: data_url, success: (result) => {
        if (result.success) {
            
            toastr["success"]("Change Role");
            window.location.reload();
        } else {
            toastr["success"]("Failed to update role");
        }
      }})
})