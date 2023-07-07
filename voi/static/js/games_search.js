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

url = window.location.href.split('?')[1];

$.ajax({
    method: "GET",
    url: `/api/v1/games/search/?${url}`,
    success: function(result){
        if(result.results == ""){
            $("#errorGameNotFound").css("display", "inline");
            $("#genereFilter").css("display", "none")
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

$.ajax({
    method: "GET",
    url: "/api/v1/games/genere-list",
    success: function(result){
        generes = result;
        $.each(generes, function(index){
            
            let genereName = generes[index]["genere_name"];
            let genereId = generes[index]["id"];

            editedGenereName = genereName.toLowerCase().replace("_", " ")

            $("#genereCheckbox").append(
                `
                <input class='genere_checkbox' type='checkbox' id='genere_${genereId}'>
                <label class='genere_name' for='genere_${genereId}"\'>${editedGenereName}</label><br>
                `
            );
            var urlParams = new URLSearchParams(window.location.search);
            let urlGenereParams = urlParams.getAll("genere");

            $.each(urlGenereParams, function(i){
                if(genereId == urlGenereParams[i]){
                    ($(`#genere_${genereId}`).attr("checked", true));
                }
            });

            $(`#genere_${genereId}`).click(function(){
                nowUrl = window.top.location.href;
                genereParam = generes[index]["id"];
                param = `&genere=${genereParam}`
                if($(`#genere_${genereParam}`)[0].checked == true){
                    newUrl = nowUrl + param;
                    window.top.location.href = newUrl;
                }

                if($(`#genere_${genereParam}`)[0].checked == false){
                    oldUrl = nowUrl.replace(param, "");
                    window.top.location.href = oldUrl;
                }
            });

            $("#genereFilterButton").click(function(){
                $("#genereCheckbox").show(300);
                $("#genereFilterButton").css("display", "none");
            });

            $("#exitFromCheckbox").click(function(){
                $("#genereCheckbox").hide(300);
                setTimeout(
                    function(){
                        $("#genereFilterButton").css("display", "inline");
                    },
                    300
                );
            });
        });
    }
});

