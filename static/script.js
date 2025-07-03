// get the HTML element
const video = document.getElementById('video');
const generateBtn = document.getElementById('Generate');

navigator.mediaDevices.getUserMedia({ video: true }) // ask the navigator to acces to the webcam
    .then(stream => { // if we have the webcam 
        video.srcObject = stream; // tell balise video to show this stream  
    })
    .catch(err => { // if no access to the webcam 
        console.error('Error access to the webcam :', err); // error 
    });
