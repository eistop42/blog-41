console.log('Привет')

document.getElementById("likeButton").addEventListener('click', post_like)

function post_like(event) {
    event.preventDefault()
    url = document.getElementById("likeButton").getAttribute('href')
    url = 'http://127.0.0.1:8000' + url
    console.log(url)

    fetch(url)
    .then(response => {
        return response.json()
    })
    .then(data => {
        document.getElementById("likesCount").textContent=`Лайки ${data.likes}`;
    })
}