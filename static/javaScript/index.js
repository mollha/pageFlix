$(document).ready(function() {
	$('#userInput').on('change', function(event) {
		$.ajax({
			data: {
				userID: $('#userInput').val(),
			},
			type: 'POST',
			url: '/checkuser',
			success: function (response) {
				if (response) {
					alert('hi');
					document.getElementById("userInput").style.border = "9px solid yellow";
				}
			}
		});
	});

	$('#form').on('submit', function(event) {
		$.ajax({
			data : {
				name : $('#userInput').val(),
			},
			type : 'POST',
			url : '/process',
			success: function(response){
				if(response){
					window.location.replace("/welcome");
				}

			}
		});
		alert($('#userInput').val());
		event.preventDefault(); // HTML automatically tries to post the form, we therefore manually stop this
		// $("html").load("/view");
	});

	$('#refreshIcon').on('click', function(event) {
		$.ajax({
			type : 'GET',
			url : '/getuser',
			success: function(response){
			    $("#userInput").val(response);
            }
		});
	});

});