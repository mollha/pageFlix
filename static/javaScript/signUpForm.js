document.addEventListener('DOMContentLoaded', function(){
	$("#formSubmit").on('click', function(event){
		let user_box = document.getElementById("userInput");
		let user_id = user_box.getAttribute('placeholder');
		$.ajax({
			data : {
            	user_id : user_id
        	},
			type : 'POST',
			url : '/createuser',
			success: function(response){
				window.location.replace("/welcome?user=" + response);
            }
		});
	});

	$.ajax({
			type : 'GET',
			url : '/getnewid',
			success: function(response){
				document.getElementById("userInput").setAttribute("placeholder", response);
            }
		});

});