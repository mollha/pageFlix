$(document).ready(function() {
    let current_book = null;
    let rating_box = $('#rating-box');
    let rating_feedback = $('#rating-feedback');
    let select_box = $('#search-input');
    const urlParams = new URLSearchParams(window.location.search);
    let user = urlParams.get('user');

    function createRatingComponent(rating_val, title, book_id){
        let my_div = document.createElement("div");
        my_div.setAttribute("data-book", book_id);
        my_div.setAttribute("data-title", title);
        my_div.style = "min-height: 40px";
        my_div.className = "row already-rated-book";

        let title_div = document.createElement("div");
        title_div.className = "col-9 d-flex";
        let inner_p = document.createElement("p");
        inner_p.style = "font-weight: bold; font-size: 13px";
        inner_p.className = "rated-title my-auto";
        inner_p.innerHTML = title;
        title_div.appendChild(inner_p);
        my_div.appendChild(title_div);

        let star_div = document.createElement("div");
        star_div.className = "col-2 d-flex";
        star_div.style = "margin: 0; padding:0";
        let inner_p_2 = document.createElement("p");
        inner_p_2.style = "font-weight:bold; color: #fcba03";
        inner_p_2.className = "rated-star my-auto";
        inner_p_2.innerHTML = rating_val + '<span class="fa fa-star checked" aria-hidden="true"></span>';
        star_div.appendChild(inner_p_2);
        my_div.appendChild(star_div);

        let bin_div = document.createElement("div");
        bin_div.className = "col-1 justify-content-center";
        bin_div.style = "margin: 0; padding:0";
        let bin_icon = document.createElement("i");
        bin_icon.className = "far fa-trash-alt delete-button";
        bin_icon.setAttribute("data-book", book_id);
        bin_div.appendChild(bin_icon);
        my_div.appendChild(bin_div);
        return my_div;
    }

    let initiateRatingDelete = function(){
        // delete rating
        let book_id = this.getAttribute("data-book");
        // $('#central-modal').modal('show');
        // delete rating
        $.ajax({
        data : {
            book_id : book_id,
            user_id: user
        },
        type : 'POST',
        url : '/deleterating',
        success: function(response){
            // remove now from position
            $('.already-rated-book[data-book="' + book_id + '"]').remove();
        }
        });
    };

    function openBookRating(user_id, book_id){
        $.ajax({
			type : 'GET',
			url : '/getbook',
            data: {
			    user_id: user,
                book_id: book_id
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response);
			}
		});
    }


    function populateAlreadyRated(user_id){
        document.getElementById("ratings-window").innerHTML = '';
        $.ajax({
			type : 'GET',
			url : '/getalluserratings',
            data: {
			    user_id: user_id,
            },
			success: function(response){
			    if(response){
                    for(let i = 0; i < response.length; i ++){
                        let book_id = response[i][0][0];
                        let book_rating = response[i][1];   // might need to use ParseInt
                        let book_title = response[i][0][3];
                        let component = createRatingComponent(book_rating, book_title, book_id);
                        document.getElementById("ratings-window").appendChild(component);
                    }
                        const buttons = document.querySelectorAll(".delete-button");
                        for (let button of buttons) {
                            button.addEventListener('click', initiateRatingDelete);
                        }
			    }
			    else{
			        document.getElementById('no-rating').innerHTML = 'This user has not provided any ratings!';
                }
            }
		});
    }
    populateAlreadyRated(user);

    function populateUserField(user_id){
        document.getElementById('user-id-box').innerHTML = 'User '+ user_id;
    }

    function remove_rating_style(){
        document.getElementById('rating-feedback').innerHTML = '';
        rating_box.val('');
        rating_box.css("box-shadow", 'None');
    }

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
        document.getElementById('rating-box').innerHTML = response.rating;
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
        remove_rating_style();
        $.ajax({
			type : 'GET',
			url : '/getbook',
            data: {
			    user_id: user_id,
                book_id: book_id
            },
            contenttype: "application/json",
			success: function(response){
			    console.log('interesting...');
			    console.log(response);
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
			    render_ratings(response);
            }
		});
    }

    $('#refreshIcon').on('click', function(event){
        remove_rating_style();
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
			    render_ratings(response);
            }
		});
    }

    // When a book is clicked, the rating box is shown
    $('.img-border').on('click', function(event) {
        let input = this.parentNode.parentNode.parentNode.querySelector('#input_row input');
        input.focus();
	});

     $('.already-rated-book').on('click', function(event) {
         console.log('hi');
         openBookRating(this.parentNode.getAttribute("data-book"), user);
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
            remove_rating_style();
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
                remove_rating_style();
                get_random_book('0');
            }
        }
        });
    });

    get_random_book('1');
    get_all_books();
    populateUserField(user);


});