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

var url = window.location.href.split("?")[1];
$.ajax({
    method: "GET",
    url: `/api/v1/handbook/handbook-list/?${url}`,
    success: function(result){
        var handbook = result.results;

        if (handbook == ""){
            $("#errorHandbookNotFound").css("display", "inline")
        }

        $.each(handbook, function(index){

            var title = handbook[index]["title"];
            var handbookId = handbook[index]["id"];

            $("#handbookList").append(
                `
                <a href='/handbook/${handbookId}'>
                    <div class='handbook'>
                        <p class='handbook-name'>${title}</p>
                    </div>
                </a>
                `
            );
        });

        var nextPage = result.next;
        var previousPage = result.previous;
        if(result.previous){
            var previousPage = result.previous.split("?")[1];
            $(".pagination").append(
                `<button class="previousPage">&#10094</button><br>`
            );
            $(".previousPage").click(function(){
                top,location.href = `/handbook/handbook-list/?${previousPage}`;
            });
        }
        if(result.next){
            var nextPage = result.next.split("?")[1];
            $(".pagination").append(
                `<button class="nextPage">&#10095</button><br>`
            );
            $(".nextPage").click(function(){
                top,location.href = `/handbook/handbook-list/?${nextPage}`;
            });
        }
    }
});