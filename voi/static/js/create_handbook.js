$(".toggle-button").click(function(){
    $(".navbar-links").toggleClass('active');
    $(".navbar-search").toggleClass('active');
});

$(".profile").css("display", "none");

var prefix = "Bearer";
var token = localStorage.getItem("token");

if (token){
    $("#loginLi").empty();
    $("#registerLi").empty();
    $("#profile").css("display", "block");
}

$("#navbarSearchButton").click(function(){
    searchInput = $("#searchInput").val();
    top.location.href = `/games/search/?name=${searchInput}`;
});
    
$.ajax({
    method: "GET",
    url : "/api/v1/handbook/handbook-type-list",
    success: function(result){
        types = result;
        $.each(types, function(index){
            var typeId = types[index]['id'];
            var typeName = types[index]['type_name'];
            $("#types").append(
                `<option value="${typeId}">${typeName.toLowerCase()}</option>`
            );
        });
    }
});

$("#addStrong").click(function(){
    $("#handbookBody").val( $("#handbookBody").val() + "**strong text**" );
});

$("#addEm").click(function(){
    $("#handbookBody").val( $("#handbookBody").val() + "*emphasized text*" );
});

$("#addLink").click(function(){
    $("#handbookBody").val( $("#handbookBody").val() + "[link name](url)" );
});

$("#handbookBody").on("input", function(){
    $("#previewHandbookBody").empty();
    text = $("#handbookBody").val();
    $("#previewHandbookBody").append(marked.parse(text));
});

$("#saveNewHandbook").click(function(){
    var title = $("#handbookTitle").val();
    var body = $("#handbookBody").val();
    var gameId = window.location.href.split("/")[5];
    var typeId = $('#types').find(":selected").val();
    var typeName = $('#types').find(":selected").text();
    $.ajax({
        method: "POST",
        url: `/api/v1/handbook/create/${gameId}`,
        headers: { 'Authorization': `${prefix} ${token}` },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "title": title,
            "body": body,
            "type": {
                "id": typeId,
                "type_name": typeName
            }
        }),
        success: function(result){
            var handbookId =  result.handbook_id;
            $("#uploadScreenshotForHandbook").css("display", "block");
            $("#createHandbook").css("display", "none");
        
            $("#uploadScreeshot").on("input", function(){
                if ($("#uploadScreeshot").val() == null){
                    $("#saveScreenshot").css("display", "none");
                    return;
                }
                $("#saveScreenshot").css("display", "inline");
                
                if (document.getElementById("uploadScreeshot").files.length > 15){
                    $("#errorMoreThanLimitFile").css("display", "block");
                    $("#saveScreenshot").attr("disabled", true);
                    $("#errorMoreThanLimitFile").text(`More than 15 files: ${document.getElementById("uploadScreeshot").files.length}`);
                    return;
                }
            
                $("#saveScreenshot").attr("disabled", false);
                $("#errorMoreThanLimitFile").text("");
            });
            $("#saveScreenshot").click(function(){
                var formData = new FormData();
                $.each(document.getElementById("uploadScreeshot").files, function(index){
                    screenshot = document.getElementById("uploadScreeshot").files[index];
                    formData.append("file_url", screenshot);
                });
                $.ajax({
                    method: "POST",
                    url: `/api/v1/handbook/upload-screenshot-for-handbook/${handbookId}`,
                    headers: { 'Authorization': `${prefix} ${token}` },
                    contentDisposition: "attachment;filename=image",
                    processData: false,
                    contentType: false,
                    data: formData,
                    success: function(result){
                        $("#successMessage").css("display", "block");
                        $("#uploadScreenshotForHandbook").css("display", "none");
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
        }
    });
});