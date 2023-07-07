$(".toggle-button").click(function(){
    $(".navbar-links").toggleClass('active');
    $(".navbar-search").toggleClass('active');
});

$("#navbarSearchButton").click(function(){
    searchInput = $("#searchInput").val();
    top.location.href = `/games/search/?name=${searchInput}`;
});

$(".profile").css("display", "none");

let token = localStorage.getItem("token");

if (token){
    $("#loginLi").empty();
    $("#registerLi").empty();
    $("#profile").css("display", "block");
}

if(isAuthenticated()){
    userId = parseJWT(token)["user_id"];
}

handbookId = window.location.href.split("/")[4];
$.ajax({
    method: "GET",
    url: `/api/v1/handbook/${handbookId}`,
    success: function(result){
        var handbook = result["handbook"];
        var author = result["handbook"]["author"]["profile"]["username"];
        var authorId = result["handbook"]["author"]["id"];
        var title = handbook["title"];
        var body = handbook["body"];
        var screenshot = handbook["screenshot"];
        if (screenshot){
            $.each(screenshot, function(index){
                var file_url = screenshot[index]["file_url"];
                $("#handbookScreenshot").append(
                    `<img class='screenshot' src='/media/${file_url}' id='screenshot_${index}'>`
                );
                $(`#screenshot_${index}`).click(function(){
                    window.open(`/media/${file_url}`);
                });
            });
        }
        $("#author").append(author);
        $("#title").append(title);
        $("#body").append(marked.parse(body));
        if(userId == authorId){
            $("#editHandbook").append(
                `<a href="/handbook/edit/${handbookId}">Edit handbook</a>`
            )
        }
    },
    error: function(request, status, error){
        if (request.responseJSON.error_handbook_not_found){
            $("#errorHandbookNotFound").css("display", "inline");
            $("#handbook").css("display", "none");
        }
    }
});