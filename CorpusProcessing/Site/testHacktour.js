
var frame = document.getElementById("newsFrame");
if (!frame || true){
	var css = document.createElement('link');
	css.href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css";
	css.rel="stylesheet";
	css = document.createElement('link');
	css.href="http://www.cs.us.es/~lvalencia/cursos/IAE2017/style.css";
	css.rel="stylesheet";
	document.getElementsByTagName('head')[0].appendChild(css);

	var jq = document.createElement('script');
	jq.src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js";
	document.getElementsByTagName('head')[0].appendChild(jq);

	var counter=1;
	console.log("Recargado archivo completo");
	var currentNews;		
	function refreshNews(news){
		console.log("Refrescar noticias")
		currentNews = news;
		
		if (news && news.length){
			$("#news").html("");
			venueNews = news[0]['VenueNews'];
			for (i = 0; i < venueNews.length; i++){
				header = venueNews[i]['VenueNew']['NewHeader'];
				subject = venueNews[i]['VenueNew']['NewSubject'];
				var dt = '<dt>' + header + '</dt>';
				var dd = '<dd>' + subject + '</dd>';
				var cad = dt + dd;
				$("#news").append(cad);
				$("#news").append("<hr><br>");
			}
		}
		
		if (!$("#myModal").is(":visible"))
			$("#myTrigger").click();
		//$("#refresh").remove();
		$(".ratel-chat-message-content > img").remove();
	}
					
	function loadJQuery(){

		var waitForLoad = function () {
			if (typeof jQuery != "undefined") {
				console.log("jquery loaded..");
				
				jq = document.createElement('script');
				jq.src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js";
				document.getElementsByTagName('head')[0].appendChild(jq);

				jq = document.createElement('script');
				jq.src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js";
				document.getElementsByTagName('head')[0].appendChild(jq);
				
				$('body').css('background','url(http://www.cs.us.es/~lvalencia/cursos/IAE2017/fondo-hacktour.png)');

				$('body').css('background-size','cover');
				$('body').css('background-opacity','0.4');
				
				frame = document.getElementById("newsFrame");
				if (!frame)
					
				$('body').append('<div id="newsFrame">');
				$.get("http://www.cs.us.es/~lvalencia/cursos/IAE2017/part.html", function(data){
					console.log("bueno...");
				  $('#newsFrame').html(data);
				  setTimeout(
				  function() 
				  {
					$("#myModal").draggable({
						handle: ".modal-header"
					});
					$("#myModal").on('hidden.bs.modal', function () {
						$(this).data('bs.modal', null);
					});
				  }, 500);
				});
			} else {
				console.log("jquery not loaded..");
				window.setTimeout(waitForLoad, 500);
			}
		};
		
		window.setTimeout(waitForLoad, 1000);   
	}


	loadJQuery();

}