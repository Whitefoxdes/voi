var userActivationUuid = window.location.href.split("/")[5];
$.ajax({
    method: "PUT",
    url: `/api/v1/user/activate-user/${userActivationUuid}`,
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    success: function(){
        $("#activate").css("display", "block");
        setTimeout(function() {
            top.location.href = "{% url 'user_view:login' %}";
        }, 3000);
    },
    error: function(request, status, error){
        if (request.responseJSON.error_user){
            $("#error").css("display", "block");
            setTimeout(function() {
                top.location.href = "/";
            }, 3000);
        }
    }
});