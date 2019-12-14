document.addEventListener("DOMContentLoaded", function(){

let user_box = $('#userInput');

	function invalid_input(element){
		element.css("box-shadow", "0 0 10px rgb(255, 0, 0)");
	}

	function valid_input(element) {
		element.css("box-shadow", "0 0 10px rgb(0, 255, 63)");
	}

	function check_valid_name(){
		$.ajax({
			data: {
				userID: user_box.val()
			},
			type: 'POST',
			url: '/checkuser',
			success: function (response) {
				if (response) {
					valid_input(user_box);
				}
				else{
					invalid_input(user_box);
				}
				return response;
			}
		});
	}

	user_box.on('change', function(event) {
		if(user_box.val()){
			check_valid_name();
		}
		else{
			user_box.css('box-shadow','none');
		}
	});

	// When the user ID form is submitted, POST input to /process and if the user ID exists, redirect to welcome page
	$('#form').on('submit', function(event) {
		$.ajax({
			data: {
			userID: user_box.val()
			},
			type: 'POST',
			url: '/checkuser',
			success: function (response) {
				if (response) {
					valid_input(user_box);
					window.location.replace("/welcome?user=" + user_box.val());
				}
				else{
					invalid_input(user_box);
				}
				return response;
			}
		});
		// HTML automatically tries to post the form, we therefore manually stop this
		event.preventDefault();
	});


	// When refresh icon is clicked, include a random valid user ID and color the box shadow green
	$('#refreshIcon').on('click', function(event) {
		$.ajax({
			type : 'GET',
			url : '/getuser',
			success: function(response){
			    $("#userInput").val(response);
			    valid_input(user_box)
            }
		});
	});

});