$("#registrateButton").click(function(){
    let email = $("#email").val();
    let password = $("#password").val();
    let confirmPassword = $("#confirmPassword").val();
    let username = $("#username").val();
    let dateOfBirth = $("#dateOfBirth").val();
    
    if (confirmPassword !== password){
        $("#wrongPasswordConfirm").css("display", "flex");
        return;
    }

    $("#registrateButton").attr("disabled", true);
    
    $.ajax({
        method: "POST",
        url: "/api/v1/user/register",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
        "email": email,
        "password": password,
        "username": username,
        "date_of_birth": dateOfBirth
        }),
        success: function(result){
            $(".register-form").css("display", "none");
            $(".activate-text").css("display", "flex");
        },
        error: function(request, status, error){
            $("#registrateButton").attr("disabled", false);
            if(request.responseJSON.error_field_empty){
                $("#fieldEmpy").css("display", "flex");
            }
            if(request.responseJSON.error_email_exist){
                $("#emailExist").css("display", "flex");
            }
        }
    });
});