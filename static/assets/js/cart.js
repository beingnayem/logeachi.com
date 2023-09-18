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



