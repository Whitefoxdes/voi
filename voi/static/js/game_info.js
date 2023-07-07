$(".toggle-button").click(function(){
    $(".navbar-links").toggleClass('active');
    $(".navbar-search").toggleClass('active');
});

$(".profile").css("display", "none");

let token = localStorage.getItem("token");

if (token){
    $("#loginLi").empty();
    $("#registerLi").empty();
    $("#profile").css("display", "block");
}

$("#navbarSearchButton").click(function(){
    searchInput = $("#searchInput").val();
    top.location.href = `/games/search/?name=${searchInput}`;
});

gameId = window.location.href.split("/")[4];

$.ajax({
    method: "GET",
    url: `/api/v1/games/${gameId}`,
    success: function(result){
        $("#handbook").append(
            `<a href="/handbook/handbook-list/?game=${gameId}" id="allHandbook">All handbook</a><br>`
        )
        if(token){
            $("#handbook").append(
                `<a href="/handbook/create/${gameId}" id="createNewHandbook">Create new handbook</a>`
            );
        }
        game = result.game;
        $("#gameName").append(
            `
            <p class='name'>${game["name"]}</p>
            `
        );
        screenshot = game["screenshot"];
        $.each(screenshot, function(index){
            $("#screenshotList").append(
                `
                <img class='screenshot' id='screenshot_${index}' src="/media/${screenshot[index]["file_url"]}">
                `
            );
            $("#curentScreenshot").attr("src", $(`#screenshot_0`).attr("src"));
            
            $(`#screenshot_${index}`).hover(function(){
                $("#curentScreenshot").attr("src", $(`#screenshot_${index}`).attr("src"));
            });

        });
    },
    error: function(request, status, error){
        if (request.responseJSON.error_game_not_found){
            $("#errorGameNotFound").css("display", "inline");
            $("#gameName").css("display", "none");
            $("#gameScreenshot").css("display", "none");
        }
    }
});