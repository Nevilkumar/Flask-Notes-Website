function deletenote(noteid){
    console.log('sdfjadfj')
    fetch('/delete-note/', {
        method:'POST',
        body: JSON.stringify({noteid:noteid}),
    }).then((_res) => {
        window.location.href = "/";
    })
}