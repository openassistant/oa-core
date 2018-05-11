// ---------------------
// Playing TTS in sync
// ---------------------
var sup1=0;
// play the specified text 
function playsyncronized(){


	if(!'speechSynthesis' in window){
		instructions.innerHTML = "Speech synthesis is not supported in this browser.  Sorry.";
		document.getElementById('ttsoptions').style.visibility = "hidden";
	}
	else {
		document.getElementById('ttsoptions').style.visibility = "visible";
		if(speechSynthesis.speaking){
			return;
		}
		var text = document.getElementById('texttospeakinput').value;
		// get the selected voice
		var voice = speechSynthesis.getVoices().filter(function(voice){
				return voice.name == voiceSelecter.value;
			})[0];

	    // Splitting each utterance up using punctuation is important.  Intra-utterance
	    // punctuation will add silence to the tts which looks bad unless the mouth stops moving
	    // correctly. Better to split it into separate utterances so play_for_duration will move when
	    // talking, and be on frame 0 when not. 

	    // split everything betwen deliminators [.?,!], but include the deliminator.
	    var substrings = text.match(/[^.?,!]+[.?,!]?/g);
	    for (var i = 0, l = substrings.length; i < l; ++i) {
	        var str = substrings[i].trim();

	        // Make sure there is something to say other than the deliminator
	        var numpunc = (str.match(/[.?,!]/g) || []).length;
	        if (str.length - numpunc > 0) {

	        	// suprisingly decent approximation for multiple languages.

	       		// if you change the rate, you would have to adjust
	            var speakingDurationEstimate = str.length * 50;
	            // Chinese needs a different calculation.  Haven't tried other Asian languages.
	            if (str.match(/[\u3400-\u9FBF]/)) {
	                speakingDurationEstimate = str.length * 200;
	            }

	            var msg = new SpeechSynthesisUtterance();

	            (function(dur){
                	msg.addEventListener('start', function(){
                		sup1.play_for_duration(dur);
	                })
                })(speakingDurationEstimate);

	            // The end event is too inacurate to use for animation,
	            // but perhaps it could be used elsewhere.  You might need to push 
	            // the msg to an array or aggressive garbage collection fill prevent the callback
	            // from firing.
	            //msg.addEventListener('end', function (){console.log("too late")}			                
	            
	            msg.text = str;
	            //change voice here
	            msg.voice = voice;

	            window.speechSynthesis.speak(msg);
	        }
	    }
	}
}

function init_talkr(){
// ----------------------
// Setup
// ----------------------

// Load the Gif
sup1 = new SuperGif({ gif: document.getElementById('exampleimg') } );
sup1.load(function(){

});


var instructions = document.getElementById('instructions');

// ----------------------
// Text to speech GUI
// ----------------------

// Code for the voice select element
var voiceSelecter = document.getElementById('voiceSelecter');
function getVoices() {
	if(voiceSelecter){
        voiceSelecter.innerHTML = "";
    	var voices = speechSynthesis.getVoices();
    	// iOS returns voices it doesn't let you use.
    	var bIsiOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    	var iOSVoiceSet = {};
    	if( bIsiOS ){ 
    		var array = ["Maged","Zuzana","Sara","Anna","Melina","Karen","Serena","Moira","Tessa","Samantha","Monica","Paulina","Satu","Amelie","Thomas","Carmit","Lekha","Mariska","Damayanti","Alice","Kyoko","Yuna","Ellen","Xander","Nora","Zosia","Luciana","Joana","Ioana","Milena","Laura","Alva","Kanya","Yelda","Ting-Ting","Sin-Ji","Mei-Jia"];
    		array.forEach(function(val){
    			iOSVoiceSet[val] = true;
    		});
    	}
    	voices.forEach(function(voice, i) {
    		// only some iOS voices are working, but they are all returned.
    		if( !bIsiOS || voice.name in iOSVoiceSet ){
    			var option = document.createElement('option');
    			option.value = voice.name;
    			option.innerHTML = voice.name;
    			if( voice.lang.substring(0,2) == "en" ){
    				voiceSelecter.insertBefore(option, voiceSelecter.firstChild);
    			}	else {
    				voiceSelecter.appendChild(option);
    			}
    		}
    	});
    }    
}
getVoices();
// Update the voices when they change (chrome loads asynchronously)
window.speechSynthesis.onvoiceschanged = function(e) {
  getVoices();
};


// ----------------------
// Load new GIFs
// ----------------------


var gifurlinput = document.getElementById('gifurlinput')
function loadNewGif(){
		var gifURL = gifurlinput.value;
    	if (gifURL.toLowerCase().indexOf(".gif") == -1) {
    		document.getElementById('giferrormessage').innerHTML = "Specify a gif file.";
    		return;
    	}
        function doesFileExist(urlToFile, success) {
            var xhr = new XMLHttpRequest();
            xhr.open('HEAD', urlToFile, true);
            xhr.onload = function(e) {
                if (xhr.status != "404") {
                    if (success) success(urlToFile);
                } else document.getElementById('giferrormessage').innerHTML = "That file was not found.";
            }
            xhr.onerror = function() {
                document.getElementById('giferrormessage').innerHTML  = "Error loading gif. Make sure the resource exists and has Access-Control-Allow-Origin headers.";
            };
            xhr.send();
        };

        function onFileExists() {
        	var imagecontainer = document.getElementById('imagecontainer')
        	imagecontainer.innerHTML = "";
            imgElement = document.createElement('img');
            imgElement.src = gifURL;
            imgElement.animatedSrc = gifURL;
            imgElement.setAttribute('rel:animated_src',gifURL);
            imgElement.setAttribute('rel:auto_play', 0);
            imagecontainer.appendChild(imgElement);
            instructions.innerHTML = "Please wait..."

            if(sup1){
                // free memory from previous SuperGif class.  The looping animation would
                // prevent the frames array from being garbage collected otherwise and memory
                // use would grow.
                sup1.destroy()
            }
            
            sup1 = new SuperGif({ gif: imgElement });
            sup1.load(function(){
            	instructions.innerHTML = "Click on the image below to hear the message."
            });
            document.getElementById('giferrormessage').innerHTML = "";
        }
        doesFileExist(gifURL, onFileExists)
}
if(gifurlinput)gifurlinput.addEventListener('input', loadNewGif) 

var imgurgifs = [
    "https://i.imgur.com/lLHEQ3F.gif", // mona
    "https://i.imgur.com/ork8hoP.gif", // lily
    "https://i.imgur.com/dS2yZ19.gif", // dog2
    "https://i.imgur.com/YpKsOQS.gif", // trump
    "https://i.imgur.com/FkEVxI6.gif", // washington
    "https://i.imgur.com/dvXw5bu.gif", // brunette
    "https://i.imgur.com/RLMkj1P.gif", // kiera
    "https://i.imgur.com/JwAmmkx.gif", // dog1 
    "https://i.imgur.com/vqVsazA.gif", // beiber
    "https://i.imgur.com/YphP1gi.gif" // portman
]
var imgurgifindex = 0;
var newgifbutton = document.getElementById("newgifbutton");
if(newgifbutton){
    newgifbutton.addEventListener("click", function(){
        imgurgifindex += 1;
        imgurgifindex = imgurgifindex % imgurgifs.length;
        gifurlinput.value = imgurgifs[imgurgifindex];  
        loadNewGif();
    })
}

document.addEventListener("keypress", function(e) {
    if (e.which == 13) {
        playsyncronized();
    }
});

};