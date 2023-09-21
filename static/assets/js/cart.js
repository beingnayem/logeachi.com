$('.qty-plus').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: 'pluscart',
        data: {
            pk: id
        },
        success: function(data){
            console.log("data= ", data);
            eml.innerText = data.quantity;
            document.getElementById("total_ammount").innerText = data.total_ammount;
            document.getElementById("total_cost").innerText = data.total_cost;
        }
    });
});






// Rating Star JS
const starRating = document.querySelector('.singel-star-rating');
const ratingInputs = document.querySelectorAll('input[name="rating"]');
const starLabels = document.querySelectorAll('.singel-star-rating label');
let selectedRating = 0; // Initialize the selectedRating variable

ratingInputs.forEach((input, index) => {
    input.addEventListener('change', () => {
        // Remove the "selected" class from all labels
        starLabels.forEach(label => {
            label.classList.remove('selected');
        });

        // Add the "selected" class to labels up to the selected rating
        for (let i = 0; i <= index; i++) {
            starLabels[i].classList.add('selected');
        }

        // Update the selectedRating variable
        selectedRating = index + 1; // Rating values start from 1
        console.log(`Selected Rating: ${selectedRating}`);

        // Set the value attribute of the selected radio input
        input.value = selectedRating;

        // You can use the selectedRating value as needed (e.g., send it to the server)
    });
});







// Home Top Trending JS
$(document).ready(function() {
    // Add an event listener for category buttons
    $(".filter__btn").click(function() {
        var categoryId = $(this).data("category-id");

        // Hide all products
        $(".filter__item").hide();

        // Show products for the selected category
        if (categoryId === "all") {
            $(".filter__item").show();
        } else {
            $(".filter__item[data-category-id='" + categoryId + "']").show();
        }
    });
});