$(document).ready(function() {
    let current_book = null;
    let rating_box = $('#rating-box');
    let rating_feedback = $('#rating-feedback');
    let select_box = $('#search-input');

    function render_ratings(response){
        let avg_rating = Math.round(parseInt(response.avg_rating));
        const checked_star = '<span class="fa fa-star'+' checked'+'"></span>';
        const unchecked_star = '<span class="far fa-star"></span>';
        let html_stars = checked_star.repeat(avg_rating) + unchecked_star.repeat(5 - avg_rating);
        document.getElementById('avg-rating-p').innerHTML = 'Avg. rating: '
            + html_stars + ' ' + response.avg_rating;

        current_book = response;
        let year = '<strong>Year: </strong>' + Math.round(parseInt(response.year)).toString();
        document.getElementById('title_h1').innerHTML = response.title;
        document.getElementById('year_p').innerHTML = year;
        document.getElementById('author_p').innerHTML = '<strong>Author: </strong>' + response.authors;
        document.getElementById('genre_p').innerHTML = '<strong>Genre: </strong>' + response.genres;
        $('.img-border .book-img').attr("src", response.image_path);
    }

    function reset_selection(){
        $('#search-input').get(0).selectedIndex = 0;
    }

    function invalid_input(element){
		element.css("box-shadow", "0 0 10px rgb(255, 0, 0)");
	    rating_feedback.css("color", 'red');
    }

	function valid_input(element) {
		element.css("box-shadow", "0 0 10px rgb(0, 255, 63)");
		rating_feedback.css("color", "green");
    }

    function get_all_books(){
        // delete all books first
        $.ajax({
			type : 'GET',
			url : '/allbooks',
			success: function(response){
			    let html_text = '<option disabled selected value> -- Select a title -- </option>\n';
			    for (let i = 0; i < response.length; i++) {
			        html_text += '<option value="' + response[i][0] + '">' + response[i][3] + '</option>'
                }
			    document.getElementById('search-input').innerHTML = html_text;
            }
		});
    }

    select_box.on('change', function(event){
        user_id = 0;
        book_id = select_box.val();
        rating_box.val('');
        rating_box.css("box-shadow", 'None');
        $.ajax({
			type : 'GET',
			url : '/getbook',
            data: {
			    user_id: user_id,
                book_id: book_id
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response);
			}
		});
    });


    function get_random_book(user_id){
        reset_selection();
        $.ajax({
			type : 'GET',
			url : '/randombook',
            data: {
                user_id: user_id
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response)
            }
		});
    }

    $('#refreshIcon').on('click', function(event){
        get_random_book('0');
    });


    function get_book(book_name){
        book_name = book_name || "hello";
        // Need to get a book from its title
        $.ajax({
			type : 'GET',
			url : '/getbook',
            data: {
                book_name: book_name
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response)
            }
		});
    }

    // When a book is clicked, the rating box is shown
    $('.img-border').on('click', function(event) {
        let input = this.parentNode.parentNode.parentNode.querySelector('#input_row input');
        input.focus();
	});


    // $('#refreshIcon').on('click', function(event){
    //     rating_box.css("box-shadow", 'None');
    //     document.getElementById('rating-feedback').innerHTML = '';
    //     // Need to get a new book
    //     // [author, year, title...
    //     rating_box.val('');
    //     get_book('');
    // });


    rating_box.on('change', function(event){
        // validate
        let val = rating_box.val();
        if(val){
            if(Number.isNaN(val)){
                document.getElementById('rating-feedback').innerHTML = 'Rating must be a number from 1 to 5';
                invalid_input(rating_box);
            }
            else{
                let int_val = parseInt(val);
                if(int_val >= 1 && int_val <= 5){
                    document.getElementById('rating-feedback').innerHTML = '';
                    valid_input(rating_box);
                }
                else{
                    invalid_input(rating_box);
                    document.getElementById('rating-feedback').innerHTML = 'Rating must be a number from 1 to 5';
                }
            }
        }
        else{
            document.getElementById('rating-feedback').innerHTML = '';
            rating_box.css("box-shadow", 'None');
        }
    });

    $('#submit-circle').on('click', function(event) {
        $.ajax({
        data : {
            rating : rating_box.val()
        },
        type : 'POST',
        url : '/updaterating',
        success: function(response){
            if(response){
                document.getElementById('rating-feedback').innerHTML = response;
                invalid_input(rating_box);
            }
            else{
                document.getElementById('rating-feedback').innerHTML = '';
                rating_box.css("box-shadow", 'None');
                rating_box.val('');
                get_random_book('0');
            }
        }
        });
    });


    get_random_book('1');
    get_all_books();

});