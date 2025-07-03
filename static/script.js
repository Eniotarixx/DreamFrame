// get the HTML element
const video = document.getElementById('video');
const generateBtn = document.getElementById('Generate');

navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 512 }, height: { ideal: 512 } } }) // ask the navigator to acces to the webcam with a resolution of 512x512 if possible > ideal 
    .then(stream => { // if we have the webcam 
        video.srcObject = stream; // tell balise video to show this stream  
    })
    .catch(err => { // if no access to the webcam 
        console.error('Error access to the webcam :', err); // error 
    });
