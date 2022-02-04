async function search(e) {
    try {
        e.preventDefault();
        let searchForm = document.getElementById('searchForm')
        let form = new FormData(searchForm);

        let artist_p = document.querySelector('#artist_p')
        let album_p = document.querySelector('#album_p')
        let album_img = document.querySelector('#album_img')
        artist_p.innerText = "Getting results...please wait"
        album_p.innerText = ''
        album_img.style.visibility='hidden'

        let response = await fetch('/search', {method:'POST', body:form})
        let data = await response.json();
    
        let artist_input = document.querySelector('#artist_input')
        let album_input = document.querySelector('#album_input')
        let image_input = document.querySelector('#image_input')
        
        let ignore_artist = document.querySelector('#ignore_artist')
        let ignore_album = document.querySelector('#ignore_album')
        let ignore_img = document.querySelector('#ignore_img')
        let music_link = document.querySelector('#music_link')
        
        let artist_name = data.topalbums.album[0].artist.name
        let album_name = data.topalbums.album[0].name
        let a_img = data.topalbums.album[0].image[3]['#text']
        // let top_album = data.topalbums.album[0]
        // let album_link = data.topalbums.album[0].url
        
        album_img.style.visibility="visible"
        album_img.src = a_img
        artist_p.innerHTML = `<strong>Artist:</strong> ${artist_name}`
        album_p.innerHTML = `<strong>Album:</strong> ${album_name}`
        music_link.href = `https://www.youtube.com/results?search_query=${artist_name} ${album_name}`
        music_link.innerText = 'Listen Here'

        artist_input.value = artist_name
        ignore_artist.value = artist_name
        album_input.value = album_name
        ignore_album.value = album_name
        image_input.value = a_img
        ignore_img.value = a_img
    } 
    catch (error) {
        artist_p.innerText = "No artists found. Please try again."
        album_p.innerText = ''
        let album_img = document.querySelector('img')
        album_img.style.visibility="hidden"
        console.log(error)
    }
}