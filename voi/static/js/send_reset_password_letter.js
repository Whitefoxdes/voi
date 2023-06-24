$("#sendLetter").click(function(){
    let email = $("#email").val()
    $("#sendLetter").attr("disabled", true);
    $("#sendLetter").css("cursor", "default");
    $.ajax({
        method: "POST",
        url:"/api/v1/user/send-reset-password-letter",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "email": email,
        }),
        success:function(result){
            $(".success").css("display", "inline");
            $(".send-letter-form").css("display", "none");
        },
        error: function(request, status, error){
            $("#sendLetter").attr("disabled", false);
            $("#sendLetter").css("cursor", "pointer");
            if(request.responseJSON.error){
                $("#errorRequestFieldEmpty").css("display", "block");
            }
            if(request.responseJSON.error_not_found_email){
                $("#errorNotFoundEmail").css("display", "block");
            }
        }
    });
});