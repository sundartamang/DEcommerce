var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log("ProductId : ",productId,"action :",action)
        console.log("User :",user)

        if(user === 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}
// for AnonymouUser
function addCookieItem(productId,action){
    console.log("USer is not log in..")
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <=0){
            delete cart[productId]
        }
    }
    console.log("Cart : ",cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}
// for log in user
function updateUserOrder(productId,action){
    console.log("User is authenticated. sendng data..")
    var url = '/update-item/'

    fetch(url,{
        method: 'POST',
        headers :{
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken
        },
        body : JSON.stringify({'productId':productId,'action':action})
    })
    .then((response)=>{
        response.json()
    })
    .then((data) =>{
        console.log("Data: ",data)
        location.reload()
    })
}