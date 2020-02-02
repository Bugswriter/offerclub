
$( document ).ready(function() {
    function changeTotal(mrp, real){
        $("#mrptotal").html("&#x20b9;"+ mrp);
        $("#realtotal").html("&#x20b9;"+ real);
    }
    // Adding to Cart
    $('.addtocart').click(function(){
    	var id = this.id;
        var amount = Number($(".quantity"+id).val());
        $("#"+id).toggleClass('btn-outline-info btn-danger');
        $("#"+id).html($(this).html() == 'Remove' ? 'Add to Cart' : 'Remove');

        if(amount < 1 || amount > 100){
            alert("Amount Must be in between 1 to 100");
            return;
        }
    	$.ajax({
    		url: '/addtocart',
    		type: "get",
    		data: {item_id: id, quantity: amount},
    		success: function(response){

                if (response.added){
                    if (response.veg){
                        var image = "<img src='/static/images/veg.png'> ";
                    }else{
                        var image = "<img src='static/images/nonveg.png'> ";
                    }
                    title = image + "&nbsp " + response.title;
                    quantity = " (" +response.quantity+ ")"
                    price = '<b class="float-right">&#x20b9;' + response.realprice*response.quantity;
                    row = "<li class='list-group-item' id=cart"+ response.id +">" + title + quantity  + price + "</li>";
                    $('#cart-list').append(row);
                }else{
                    var cartelement = "#cart"+response.id;
                    $(cartelement).remove(); 
                }
                changeTotal(response.mrptotal, response.realtotal);
            },
    		error: function(xhr) {
                alert("error happened");
    		}   
   		});
    });
});