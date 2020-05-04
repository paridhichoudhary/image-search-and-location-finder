var current_pic = "";
var current_pic_name = "";
$(document).ready(function () {
    // Init
    console.log( "ready!" );
    $('#results').hide();
    $('class-prediction').hide();
    // Upload Preview
    });

$('img').click(function (e) {
    console.log("Inherent function called");
    $('img.highlight').not(e.target).removeClass('highlight');
    $(this).toggleClass('highlight');
    url = $(this).attr('href');
    current_pic=$(this).attr('src');
    console.log(current_pic);
    current_pic_name=$(this).attr('src').split("/")[3];
    console.log(current_pic_name);
});



// Predict
$('#btn-find-location').click(function () {
        $.post( "/postmethod", {
        javascript_data: current_pic
    });
   $.ajax({
        type: 'POST',
        url: '/displayClassText',
        contentType: false,
        cache: false,
        processData: false,
        async: true,
        success: function (data) {
                $('#class-prediction').show();
                $('#image-results-section').hide();
                console.log(data+" class");
                $('#class-label').show();
                var class_text = document.getElementById("class-label");
                data = data.charAt(0).toUpperCase() + data.substring(1)
                class_text.innerHTML = "Possible object in image : " + data.bold();
                $('#results').show();
                $('#search-label').show();
                var search_text = document.getElementById("search-label");
                if (data=="people"){
                    search_text.innerHTML = "Sorry, we cannot find location for an image from this class!<br>";
                }
                else{
                    search_text.innerHTML = "Top 3 "+data.toLowerCase()+" images from Iceland that were closest to this picture and their locations are:";
                }
        },
    });
    // Make prediction by calling api /predictVGG16
    $.ajax({
        type: 'POST',
        url: '/findLocation',
        contentType: false,
        cache: false,
        processData: false,
        async: true,
        success: function (data) {
//                $('#results').show();
            if (data=="||"){
                console.log('People Class!');
            }
            else{
                results = data.split("|");
                first_image_results = results[0].split(",");
                first_image_city = first_image_results[1];
                first_image_state = first_image_results[2];
                second_image_results = results[1].split(",");
                second_image_city = second_image_results[1];
                second_image_state = second_image_results[2];
                third_image_results = results[2].split(",");
                third_image_city = third_image_results[1];
                third_image_state = third_image_results[2];
                // Get and d isplay the result
                $('#results').show();
//                $('#class-label').hide();
                $('#results').fadeIn(600);
                $('#image-results-section').show();
                var now = new Date();
                var fig_1_img = document.getElementById("result-1-img");
                fig_1_img.src = "static/images/result_"+current_pic_name.split(".")[0]+"_0.png?" + now.getTime();
                console.log(fig_1_img.src)
                var fig_1_caption = document.getElementById("result-1-caption");
                fig_1_caption.innerHTML = first_image_city+",<br/>"+first_image_state;
                var fig_2_img = document.getElementById("result-2-img");
                fig_2_img.src = "static/images/result_"+current_pic_name.split(".")[0]+"_1.png?" + now.getTime();
                var fig_2_caption = document.getElementById("result-2-caption");
                fig_2_caption.innerHTML = second_image_city+",<br/>"+second_image_state;
                var fig_3_img = document.getElementById("result-3-img");
                fig_3_img.src = "static/images/result_"+current_pic_name.split(".")[0]+"_2.png?" + now.getTime();
                var fig_3_caption = document.getElementById("result-3-caption");
                fig_3_caption.innerHTML = third_image_city+",<br/>"+third_image_state;
                console.log('Model Success!');
            }
        },
    });
});
