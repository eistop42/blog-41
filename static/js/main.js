
// document.getElementById("likeButton").addEventListener('click', post_like)
// document.getElementById("unlikeButton").addEventListener('click', post_unlike)

// function post_like(event) {
//     event.preventDefault()
//     url = document.getElementById("likeButton").getAttribute('href')
//     url = 'http://127.0.0.1:8000' + url
//     console.log(url)

//     fetch(url)
//     .then(response => {
//         return response.json()
//     })
//     .then(data => {
//         document.getElementById("likesCount").textContent=`Лайки ${data.likes}`;
//         document.getElementById("likeButton").style.display = 'none'
//         document.getElementById("unlikeButton").style.display = 'show'
//     })
// }


// function post_like(event) {
//     event.preventDefault()
//     url = document.getElementById("likeButton").getAttribute('href')
//     url = 'http://127.0.0.1:8000' + url
//     console.log(url)

//     fetch(url)
//     .then(response => {
//         return response.json()
//     })
//     .then(data => {
//         document.getElementById("likesCount").textContent=`Лайки ${data.likes}`;
//         document.getElementById("likeButton").style.display = 'none'
//         document.getElementById("unlikeButton").style.display = ''
//     })
// }



// function post_unlike(event) {
//     event.preventDefault()
//     url = document.getElementById("unlikeButton").getAttribute('href')
//     url = 'http://127.0.0.1:8000' + url
//     console.log(url)

//     fetch(url)
//     .then(response => {
//         return response.json()
//     })
//     .then(data => {
//         document.getElementById("likesCount").textContent=`Лайки ${data.likes}`;
//         document.getElementById("unlikeButton").style.display = 'none'
//         document.getElementById("likeButton").style.display = ''
//     })
// }



$(document).ready(function () {
    $("#likeButton").on("click", postLike);
    $("#unlikeButton").on("click", postUnlike);

    function postLike(event) {
        event.preventDefault();
        let url = "http://127.0.0.1:8000" + $("#likeButton").attr("href");
        console.log(url);

        $.get(url, function (data) {
            $("#likesCount").text(`Лайки ${data.likes}`);
            $("#likeButton").hide();
            $("#unlikeButton").show();
        });
    }

    function postUnlike(event) {
        event.preventDefault();
        let url = "http://127.0.0.1:8000" + $("#unlikeButton").attr("href");
        console.log(url);

        $.get(url, function (data) {
            $("#likesCount").text(`Лайки ${data.likes}`);
            $("#unlikeButton").hide();
            $("#likeButton").show();
        });
    }


    $("#commentForm").submit(function (event) {
        event.preventDefault();  // Предотвращаем стандартную отправку формы

        var form = $(this);
        var url = form.attr("action");

        $.ajax({
            url: url,
            type: "POST",
            data: form.serialize(),  // Сериализуем данные формы
            success: function (data) {
                // Если успешно:
                $("#comments").prepend(data.comment);  // Добавляем новый комментарий
                form[0].reset();  // Очищаем форму
                $("#errors").empty();  // Очищаем блок с ошибками
            },
            error: function (xhr) {
                // Если ошибка:
                let errorHtml = JSON.parse(xhr.responseText).errors // Ошибки, переданные с сервера
                $("#errors").html(errorHtml);  // Вставляем ошибки в блок
            }
        });
    }); 
});