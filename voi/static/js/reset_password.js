$("#saveNewPassword").click(function(){

    var resetPasswordUuid = window.location.href.split("/")[5];

    let newPassword = $("#newPassword").val();
    let confirmPassword= $("#confirmPassword").val();

    if(confirmPassword !== newPassword){
        $("#errorConfirmPassword").css("display", "block");
        return;
    }
    $.ajax({
        method: "PUT",
        url: `/api/v1/user/reset-password/${resetPasswordUuid}`,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "password": newPassword,
        }),
        success: function(result){
            $(".reset-password-form").css("display", "none");
            $("#success").css("display", "inline");
            setTimeout(function(){
                top.location.href = "/user/login";
            }, 3000);
        },
        error: function(request, status, error){
            if(request.responseJSON.error){
                $("#errorRequestFieldEmpty").css("display", "block");
            }
            if(request.responseJSON.error_url){
                $("#errorURL").css("display", "block")
                setTimeout(function(){
                    top.location.href = "/user/login"
                }, 4000);
            }
        }
    });
});