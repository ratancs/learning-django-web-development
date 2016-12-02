$(".follow-btn").click(function () {
    var username = $(this).attr('username');
    var follow = $(this).attr('value') != "True";
    $.ajax({
        type: "POST",
        url:  "/user/"+username+"/",
        data: { username: username , follow : follow  },
        success: function () {
            window.location.reload();
        },
        error: function () {
            alert("ERROR !!");
        }
    })
});
