marked.use({
    mangle: false,
    headerIds: false
});
  
$(".toggle-button").click(function(){
    $(".navbar-links").toggleClass('active');
    $(".navbar-search").toggleClass('active');
});

$("#navbarSearchButton").click(function(){
    searchInput = $("#searchInput").val();
    top.location.href = `/games/search/?name=${searchInput}`;
});

$(".profile").css("display", "none");

var prefix = "Bearer";
var token = localStorage.getItem("token");

if (token){
    $("#loginLi").empty();
    $("#registerLi").empty();
    $("#profile").css("display", "block");
}

var oldTitle;
var oldBody;
var oldScreenshot;
var oldTypeId;

var screenshotOnDelete = [];

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}

handbookId = window.location.href.split("/")[5];
  
$.ajax({
    method: "GET",
    url: `/api/v1/handbook/${handbookId}`,
    success: function(result){
        var handbook = result["handbook"];
        oldTitle = handbook["title"];
        oldBody = handbook["body"];
        oldScreenshot = handbook["screenshot"];
        oldTypeId = handbook["type"]["id"];
        if (oldScreenshot != ""){
            $("#oldScreenshot").css("display", "grid");
            $.each(oldScreenshot, function(index){
                var file_url = oldScreenshot[index]["file_url"];
                var screenshotId = oldScreenshot[index]["id"];
                var isDelete = oldScreenshot[index]["is_delete"];
                if(isDelete == true){
                    return;
                }
                $("#oldScreenshot").append(
                    `<input type="checkbox" id="screenshot_${screenshotId}" class="screenshot-checkbox">
                    <label for="screenshot_${screenshotId}"><img src="/media/${file_url}" class="old-screenshot"></label>`
                );
                $(`#screenshot_${screenshotId}`).click(function(){
                    if($(`#screenshot_${screenshotId}`)[0].checked == true){
                        screenshotOnDelete.push(screenshotId);
                    }
                    if($(`#screenshot_${screenshotId}`)[0].checked == false){
                        var removeItem = screenshotOnDelete.indexOf(screenshotId);
                        screenshotOnDelete.splice(removeItem, 1);
                    }
                });
                $(".screenshot-checkbox").click(function(){
                    if($(".screenshot-checkbox:checked").length > 0){
                        $("#deleteScreenshot").css("display", "inline");
                    }
                    if($(".screenshot-checkbox:checked").length <= 0){
                        $("#deleteScreenshot").css("display", "none");
                    }
                });
            });
        }
        $(`#types`).val(oldTypeId);
        $("#handbookTitle").attr("value", oldTitle);
        $("#handbookBody").append(oldBody);
        $("#previewHandbookBody").append(marked.parse(oldBody));
        
    },
    error: function(request, status, error){
        if (request.responseJSON.error_handbook_not_found){
            $("#errorHandbookNotFound").css("display", "inline");
            $("#handbook").css("display", "none");
            setTimeout(
                function(){
                    window.location.href = "/";
                },
                2500
            );
        }
    }
});
  
$.ajax({
    method: "GET",
    url : "/api/v1/handbook/handbook-type-list",
    success: function(result){
        var types = result;
        $.each(types, function(index){
            var typeId = types[index]['id'];
            var typeName = types[index]['type_name'];
            $("#types").append(
                `<option value="${typeId}">${typeName.toLowerCase()}</option>`
            );
        });
        $(`#types`).val(oldTypeId);
    }
});
  
$("#addStrong").click(function(){
    $("#handbookBody").val( $("#handbookBody").val() + "**strong text**" ).trigger("input");
});

$("#addEm").click(function(){
    $("#handbookBody").val( $("#handbookBody").val() + "*emphasized text*" ).trigger("input");
});

$("#addLink").click(function(){
    $("#handbookBody").val( $("#handbookBody").val() + "[link name](url)" ).trigger("input");
});

$("#handbookBody").on("input", function(){
    $("#previewHandbookBody").empty();
    text = $("#handbookBody").val();
    $("#previewHandbookBody").append(marked.parse(text));
});

$("#handbookTitle").add("#handbookBody").add("#types").on('input change', function(){
    if($("#handbookTitle").val() == "" || $("#handbookBody").val() == "" || $('#types').find(":selected").val() == ""){
        $("#saveHandbook").css("display", "none");
        return;
    }
    $("#saveHandbook").css("display", "inline");
  
    if($("#handbookTitle").val() == oldTitle && $("#handbookBody").val() == oldBody && $('#types').find(":selected").val() == oldTypeId){
        $("#saveHandbook").css("display", "none");
        return;
    }
    $("#saveHandbook").css("display", "inline");
});
  
$("#saveHandbook").click(function(){    
    var updateTitle = $("#handbookTitle").val();
    var updateBody = $("#handbookBody").val();
    var updateTypeId = $('#types').find(":selected").val();
    var updateTypeName = $('#types').find(":selected").text();
    
    $.ajax({
        method: "PUT",
        url: `/api/v1/handbook/edit/${handbookId}`,
        headers: { 'Authorization': `${prefix} ${token}` },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "title": updateTitle,
            "body": updateBody,
            "type": {
                "id": updateTypeId,
                "type_name": updateTypeName
            }
        }),
        success: function(result){
            location.reload();
            return;
        },
        error: function(request, status, error){
            if (request.responseJSON.error_handbook_not_found){
                $("#errorHandbookNotFound").css("display", "inline");
                $("#handbook").css("display", "none");
                setTimeout(
                    function(){
                        window.location.href = "/";
                    },
                    2500
                );
            }
            if (request.responseJSON.error_user_id){
                $("#errorUserId").css("display", "inline");
                $("#handbook").css("display", "none");
                setTimeout(
                    function(){
                        window.location.href = "/";
                    },
                    2500
                );
            }
            if (request.responseJSON.error_handbook_type_not_allowed){
                $("#errorHandbookTypeNotAllowed").css("display", "inline");
            }
            if (request.responseJSON.error_field_empty){
                $("#errorHandbookFieldEmpty").css("display", "inline");
            }
            if (request.status == 401){
                window.location.href = "/";
            }
        }
    });
});
  
$("#uploadScreeshot").on("input", function(){
    if ($("#uploadScreeshot").val() == null){
        $("#saveScreenshot").css("display", "none");
        return;
    }
    $("#saveScreenshot").css("display", "inline");
    maxAllowedCountFile = 15 - document.getElementsByClassName("screenshot-checkbox").length;
    countFile = document.getElementById("uploadScreeshot").files.length;
    allCountFile = document.getElementById("uploadScreeshot").files.length + document.getElementsByClassName("screenshot-checkbox").length;
    if (countFile > maxAllowedCountFile){
        $("#errorMoreThanLimitFile").css("display", "block");
        $("#saveScreenshot").css("display", "none");
        $("#errorMoreThanLimitFile").text(`More than 15 files: ${allCountFile}`);
        return;
    }

    $("#saveScreenshot").attr("disabled", false);
    $("#errorMoreThanLimitFile").text("");
});
  
$("#deleteScreenshot").click(function(){
    $.ajax({
        method: "DELETE",
        url: `/api/v1/handbook/delete-screenshot/${handbookId}`,
        headers: { 'Authorization': `${prefix} ${token}` },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "id": screenshotOnDelete,
        }),
        success: function(result){
            location.reload();
            return;
        },
        error: function(request, status, error){
            if(request.responseJSON.error_field_empty){
                $("#errorDeleteScreenshotFieldEmpty").css("display", "inline");
            }
            if(request.responseJSON.error_screenshot_not_found){
                $("#errorScreenshotNotFound").css("display", "inline");
            }
            if(request.responseJSON.error_screenshot_already_delete){
                $("#errorScreenshotAlreadyDelete").css("display", "inline");
            }
            if (request.status == 401){
                window.location.href = "/";
            }
        }   
    });
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
            location.reload();
        },
        error: function(request, status, error){
            if (request.responseJSON.error_handbook_not_found){
                $("#errorHandbookNotFound").css("display", "inline");
                $("#handbook").css("display", "none");
                setTimeout(
                    function(){
                        window.location.href = "/";
                    },
                    2500
                );
            }  
            if(request.responseJSON.error_field_empty){
                $("#errorFileFieldEmpty").css("display", "block");
            }
            if (request.responseJSON.error_file_size){
                $("#errorFileSize").css("display", "block");
            }
            if (request.responseJSON.error_file_ext){
                $("#errorFileExt").css("display", "block");
            }
            if (request.status == 401){
                window.location.href = "/";
            }
        }
    });
});

$("#deleteButton").click(function(){
    $("#deleteButton").css("display", "none");
    $("#confirmDelete").css("display", "block");
});
  
$("#yesButton").click(function(){
    $.ajax({
        method: "DELETE",
        url: `/api/v1/handbook/delete/${handbookId}`,
        headers: { 'Authorization': `${prefix} ${token}` },
        success: function(result){
            $("#successDeleteHandbook").css("display", "block");
            $("#handbook").css("display", "none")
            setTimeout(
                    function(){
                        window.location.href = "/";
                    },
                    3000
            );
        },
        error: function(request, status, error){
            if (request.responseJSON.error_handbook_not_found){
                $("#errorHandbookNotFound").css("display", "inline");
                $("#handbook").css("display", "none");
                setTimeout(
                    function(){
                        window.location.href = "/";
                    },
                    2500
                );
            }
            if (request.responseJSON.error_user_id){
                $("#errorUserId").css("display", "inline");
                $("#handbook").css("display", "none");
                setTimeout(
                    function(){
                        window.location.href = "/";
                    },
                    2500
                );
            }
            if (request.status == 401){
                window.location.href = "/";
            }
        }
    });
});

$("#noButton").click(function(){
    $("#confirmDelete").css("display", "none");
    $("#deleteButton").css("display", "inline");
});