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

$('.remove-btn').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: '/cart/removecart/',
        data: {
            pk: id
        },
        success: function(data){
            document.getElementById("total_ammount").innerText = data.total_ammount;
            document.getElementById("total_cost").innerText = data.total_cost;
            eml.parentNode.parentNode.parentNode.remove();
        }
    });
});





