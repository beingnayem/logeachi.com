
// for increasing the cart product quantity
$('.qty-plus').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: '/cart/pluscart/',
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

// for dicreasing the cart product quantity
$('.qty-minus').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: '/cart/minuscart/',
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

