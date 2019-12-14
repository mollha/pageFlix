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
			success: function(){
				setTimeout(function () {
					window.location.replace("/welcome?user=" + user_id);
					}, 5000);
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