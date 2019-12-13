document.addEventListener('DOMContentLoaded', function(){
	$("#formSubmit").on('click', function(event){
		window.location.replace("/welcome");
	});

	$.ajax({
			type : 'GET',
			url : '/getnewid',
			success: function(response){
				document.getElementById("userInput").setAttribute("placeholder", response);
            }
		});

});