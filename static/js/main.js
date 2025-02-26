console.log('Привет')

document.getElementById("likeButton").addEventListener('click', post_like)

function post_like(event) {
    event.preventDefault()
    url = document.getElementById("likeButton").getAttribute('href')
    url = 'http://127.0.0.1:8000' + url

    fetch(url)
    .then(response => {
        return response.json()
    })
    .then(data => {
        document.getElementById("likesCount").textContent=`Лайки ${data.likes}`;

        //скрой кнопку лайка
        document.getElementById("likeButton").style.display = 'none'
        // покажи кнопку снять лайк, заполненное сердечко
        document.getElementById("unlikeButton").style.display = ''
    })
}


document.getElementById("unlikeButton").addEventListener('click', post_unlike)

function post_unlike(event) {
    event.preventDefault()
    url = document.getElementById("unlikeButton").getAttribute('href')
    url = 'http://127.0.0.1:8000' + url

    fetch(url)
    .then(response => {
        return response.json()
    })
    .then(data => {
        document.getElementById("likesCount").textContent=`Лайки ${data.likes}`;

        //скрой кнопку снять лайк
        document.getElementById("unlikeButton").style.display = 'none'
        // покажи кнопку лайк
        document.getElementById("likeButton").style.display = ''
    })
}


$(".col-sm-6").on('submit', '#commentForm', function(event){

  event.preventDefault()
  let form = $("#commentForm")
  let url = form.attr('action')

  $.ajax({
    type: 'POST',
    url: url,
    data: form.serialize(),
    success: function(data){
        if (data.is_valid === true){
            $('#comments').replaceWith(data.comments)
            $('#commentForm').trigger('reset')
        }
        else {
            $('#commentForm').replaceWith(data.form)
        }
    }
  })
});