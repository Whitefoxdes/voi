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

url = window.location.href.split('?')[1];
$.ajax({
    method: "GET",
    url: `/api/v1/games/all-games/?${url}`,
    success: function(result){
        if(result.results == ""){
            $("#errorGameNotFound").css("display", "inline");
        }
        var game = result.results;

        $.each(game, function(index){
            var name = game[index]["name"];
            var gameId = game[index]["id"];
            
            $("#gamesList").append(
                `
                <a href='/games/${gameId}'>
                    <div class="game">
                        <p class="game-name">${name}</p>
                    </div>
                </a>
                `
            );
        });
        if(result.previous){
            var previousPage = result.previous.split("?")[1];
            $(".pagination").append(
                `<button class="previousButton">&#10094</button><br>`
            );
            $(".previousButton").click(function(){
                top,location.href = `/games/search/?${previousPage}`;
            });
        }
        if(result.next){
            var nextPage = result.next.split("?")[1];
            $(".pagination").append(
                `<button class="nextButton">&#10095</button><br>`
            );
            $(".nextButton").click(function(){
                top,location.href = `/games/search/?${nextPage}`;
            });
        }
    }
});

$("#navbarSearchButton").click(function(){
    searchInput = $("#searchInput").val();
    top.location.href = `/games/search/?name=${searchInput}&is_active=true&page=1`;
});