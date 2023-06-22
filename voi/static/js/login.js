$("#loginButton").click(function(){
    let email = $("#email").val();
    let password = $("#password").val();

    $.ajax({
        method: "POST",
        url: "/api/v1/user/login",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "email": email,
            "password": password
        }),
        success: function(result){
            console.log(1)
            localStorage.setItem("token", result.access);
            localStorage.setItem("refresh_token", result.refresh);
            top.location.href = "/";
        },
        error: function(request){
            if (request.responseJSON.email || request.responseJSON.password){
                $("#fieldEmpy").css("display", "flex");
            }
            if (request.status == 401 || request.responseJSON.detail){
                $("#wrongEmailOrPassword").css("display", "flex");
            }
        }
    });
});