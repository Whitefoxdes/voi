$(".toggle-button").click(function(){
    $(".navbar-links").toggleClass('active');
    $(".navbar-search").toggleClass('active');
});
var prefix = "Bearer";
var token = localStorage.getItem("token");
$("#gameName").on("input", function(){
    if ($("#gameName").val() == ""){
        $("#saveGame").css("display", "none");
        return;
    }
    $("#saveGame").css("display", "inline");
});
$("#navbarSearchButton").click(function(){
    searchInput = $("#searchInput").val();
    top.location.href = `/games/search/?name=${searchInput}&is_active=true&page=1`
});
$("#saveGame").click(function(){
    $(".error").css("display", "none");
    var name = $("#gameName").val()
    $.ajax({
        method: "POST",
        url: "/api/v1/games/add-game",
        headers: { 'Authorization': `${prefix} ${token}` },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "name": name,
        }),
        success: function(result){
            $("#upload-screenshot-for-game").css("display", "block");
            $("#step").text("Step 2 of 2");
            $(".upload-screenshot-for-game").css("display", "block");
            $(".add-game").css("display", "none");
            var game_id = result.game_id;
            
            $("#uploadScreeshot").on("input", function(){
                if ($("#saveScreenshot").val() == null){
                    $("#saveScreenshot").css("display", "none");
                    return;
                }
                $("#saveScreenshot").css("display", "inline");
                
                if (document.getElementById("uploadScreeshot").files.length > 5){
                    $("#errorMoreThanLimitFile").css("display", "block");
                    $("#saveScreenshot").attr("disabled", true);
                    $("#errorMoreThanLimitFile").text(`More than 5 files: ${document.getElementById("uploadScreeshot").files.length}`);
                    return;
                }

                $("#saveScreenshot").attr("disabled", false);
                $("#errorMoreThanLimitFile").text("");
            });
            
            $("#saveScreenshot").click(function(){
                $(".error").css("display", "none");
                var formData = new FormData();
                $.each(document.getElementById("uploadScreeshot").files, function(index){
                    screenshot = document.getElementById("uploadScreeshot").files[index];
                    formData.append("file_url", screenshot);
                });
                $.ajax({
                    method: "PUT",
                    url: `/api/v1/games/upload-screenshot-for-game/${game_id}`,
                    headers: { 'Authorization': `${prefix} ${token}` },
                    contentDisposition: "attachment;filename=image",
                    processData: false,
                    contentType: false,
                    data: formData,
                    success: function(result){
                        $("#addNewGame").css("display", "block");
                        $("#saveScreenshot").attr("disabled", true);
                        setTimeout(
                            function(){
                                top.location.reload();
                            },
                            3000
                        );
                    },
                    error: function(request, status, error){
                        if(request.responseJSON.error_field_empty){
                            $("#errorFileFieldEmpty").css("display", "block");
                        }

                        if (request.responseJSON.error_file_size){
                            $("#errorFileSize").css("display", "block");
                        }

                        if (request.responseJSON.error_file_ext){
                            $("#errorFileExt").css("display", "block");
                        }
                    }
                });
            });
        },
        error: function(request, status, error){
            if (request.responseJSON.error_game_exist){
                $("#errorGameExist").css("display", "block");
            }

            if(request.responseJSON.error_field_empty){
                $("#errorNameFieldEmpty").css("display", "block");
            }
        }
    });
});