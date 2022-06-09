const tweetElement = document.getElementById("tweets")

tweetElement.innerHTML = "<h1>Tweet 1</h1>"

const xhr = new XMLHttpRequest()
const method = 'GET'
const url = "/tweet"
const responseType = "json"


xhr.responseType = responseType
console.log(xhr.responseType)
xhr.open(method,url)
xhr.onload = function(){
    const serverResponse = xhr.response
    const listItems = serverResponse.response
    let docTweet = []
    let i
    
    for(i=0;i<listItems.length;i++){
        console.log(i);
        console.log(listItems[i]);
        
        let current = "<div class='mb-4'><h1>" + listedItems[i].id + "</h1>" + "<p>" + listedItems[i].text + "</p></div>"
        docTweet += current;
    }
    tweet.innerHTML = docTweet;
}
xhr.send()