$(".toggle-button").click(function () {
    $(".navbar-links").toggleClass('active');
    $(".navbar-search").toggleClass('active');
});

$("#profileTop").click(function () {
    $(".profile-fields").toggleClass('active');
    $(".safety-fields").removeClass('active');
});

$("#safetyTop").click(function () {
    $(".safety-fields").toggleClass('active');
    $(".profile-fields").removeClass('active');
});

let oldUsername;
let oldEmail;
let oldDateOfBirth;
$("#editUsername").add("#editDateOfBirth").on('input', function(){
    
    if($("#editUsername").val() == "" || $("#editDateOfBirth").val() == ""){
        $("#saveProfile").css("display", "none");
        return;
    }
    
    if($("#editUsername").val() == oldUsername && $("#editDateOfBirth").val() == oldDateOfBirth){
        $("#saveProfile").css("display", "none");
        return;
    }
    $("#saveProfile").css("display", "inline");
});

$("#changeUserAvatar").on('input', function(){

    if($("#changeUserAvatar").val() == null){
        $("#saveUserAvatar").css("display", "none");
        return;
    }
    $("#saveUserAvatar").css("display", "inline");
});

$("#editEmail").on('input', function(){
    if($("#editEmail").val() == oldEmail){
        $("#saveEmail").css("display", "none");
        return;
    }
    $("#saveEmail").css("display", "inline");
});
$("#changePassword").on('input', function(){
    if($("#changePassword").val() == ""){
        $("#savePassword").css("display", "none");
        return;
    }
    $("#savePassword").css("display", "inline");
});

let refresh_token = localStorage.getItem('refresh_token');
let prefix = "Bearer";
let token;
$.ajax({
        method: "POST",
        url: "/api/v1/user/token-refresh",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "refresh": refresh_token
        }),
        success: function (result) {
            token = result.access;
            $.ajax({
                    method: "GET",
                    url: "/api/v1/user/profile",
                    headers: { 'Authorization': `${prefix} ${token}` },
                    success: function (result) {
                        oldUsername = result.data_profile["username"];
                        oldDateOfBirth = result.data_profile["date_of_birth"];
                        oldEmail = result.data_user["email"];
                        isStaff = result.data_user["is_staff"];
                        
                        if(isStaff == true){
                            $("#addNewGameLi").append(
                                `
                                <a class="add-new-game" id="addNewGame" href="/games/add-new-game">Add new game</a>
                                `
                            );
                        }

                        $("#username").append(`${result.data_profile["username"]}`);
                        
                        $("#editUsername").val(result.data_profile["username"]);
                        $("#editDateOfBirth").val(result.data_profile["date_of_birth"]);
                        $("#editEmail").val(result.data_user["email"]);
                        if(result.data_profile["user_avatar"]){
                            $("#userAvatar").attr("src", `/media/${result.data_profile["user_avatar"]}`);
                        }
                    },
            });
        },
        error: function(){
            localStorage.removeItem("token")
            localStorage.removeItem("refresh_token")
            top.location.href = "/user/login";
        }
});

$("#saveProfile").click(function(){
    let newUsername = $("#editUsername").val();
    let newDateOfBirth = $("#editDateOfBirth").val();
    $.ajax({
        method: "PUT",
        url: "/api/v1/user/edit-profile",
        headers: { 'Authorization': `${prefix} ${token}` },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "username": newUsername,
            "date_of_birth": newDateOfBirth
        }),
        success: function(){
            location.reload();
            return;
        },
        error: function(request, status, error){
            if(request.responseJSON.error);
                $("#errorProfile").css("display", "block");
                return;
        }
    });
});
$("#saveUserAvatar").click(function(){
    let newUserAvatar = document.getElementById("changeUserAvatar").files[0];
    let formData = new FormData();
    formData.append("file_url", newUserAvatar);
    $.ajax({
        method: "PUT",
        url: "/api/v1/user/user-avatar-upload",
        headers: { 'Authorization': `${prefix} ${token}` },
        contentDisposition: "attachment;filename=image",
        processData: false,
        contentType: false,
        data: formData,
        success: function(){
            location.reload();
            return;
        },
        error: function(request, status, error){
            if(request.responseJSON.error_file_size){
                $("#errorFileSize").css("display", "block");
                return;
            }
            if(request.responseJSON.error_file_ext){
                $("#errorFileExt").css("display", "block");
                return;
            }
        }
    });
});

$("#saveEmail").click(function(){
    let newEmail = $("#editEmail").val();
    let confirmIdentityPassword = $("#confirmIdentityPassword").val();
    $.ajax({
        method: "PUT",
        url: "/api/v1/user/edit-email",
        headers: { 'Authorization': `${prefix} ${token}` },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "email": newEmail,
            "password": confirmIdentityPassword
        }),
        success: function(){
            location.reload();
            return;
        },
        error: function(request, status, error){
            if(request.responseJSON.error){
                $("#errorEmail").css("display", "block");
                return;
            }

            if(request.responseJSON.error_email_exist){
                $("#errorEmailExist").css("display", "block");
                return;
            }

            if(request.responseJSON.error_confirm_identity_password){
                $("#errorWrongConfirmIdentityPassword").css("display", "block");
                return;
            }
        }
    });
});

$("#savePassword").click(function(){
    let email = $("#editEmail").val();
    let oldPassword = $("#oldPassword").val();
    let newPassword = $("#changePassword").val();
    let confirmPassword = $("#confirmPassword").val();

    if(confirmPassword !== newPassword){
        $("#errorWrongConfirmPassword").css("display", "block");
        return;
    }

    $.ajax({
        method: "PUT",
        url: "/api/v1/user/change-password",
        headers: { 'Authorization': `${prefix} ${token}` },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "password": newPassword,
            "old_password": oldPassword,
            "email": email
        }),
        success: function(){
            location.reload();
            return;
        },
        error: function(request, status, error){
            if(request.responseJSON.error){
                $("#errorPassword").css("display", "block");
                return;
            }
            if(request.responseJSON.error_old_password){
                $("#errorOldPassword").css("display", "block");
                return;
            }
        }
    });
});

$("#logOut").click(function(){
    localStorage.clear();
    top.location.href = "/";
});

$("#navbarSearchButton").click(function(){
    searchInput = $("#searchInput").val();
    top.location.href = `/games/search/?name=${searchInput}&is_active=true&page=1`;
});