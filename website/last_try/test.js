var form = document.getElementById("my-form");
var button = document.getElementById("submit-id");
//button.addEventListener("click", showCards);

form.addEventListener("submit", function(event) {
  event.preventDefault(); // prevent the page from reloading
  showCards(); // call the showCards function to display the cards
});

function createCard(title, image, description, link, type) {
  var card = '';
  
  if (type === 'classic') {
    card =    '<div class="card card-blog">' +
                '<a href="' + link + '" target="_blank">' +
                  '<div class="card-image">' +
                    '<figure style="margin-bottom: 0">' +
                      '<img class="img" src="' + image + '" alt="">' +
                    '</figure>' +
                    '<div class="card-caption">' + title + '</div>' +
                    '<div class="ripple-cont"></div>' +
                  '</div>' +
                  '<div class="table">' +
                    '<h6 class="category text-info"><i class="fa fa-soundcloud"></i> Data Science</h6>' +
                    '<p class="card-description">' + description + '</p>' +
                  '</div>' +
                '</a>' +
              '</div>';
  } else if (type === 'tweet') {
    card =    '<blockquote class="twitter-tweet">' +
                '<a href="' + link + '"></a>' +
              '</blockquote>';

  } else if (type === 'reddit') {
    card =     '<div class="card">' +
                '<blockquote class="reddit-card" data-card-created=&quot;2023-02-02T16:19:41.554663+00:00&quot;>' +
                  '<a href="' + link + '">' + title + '</a> from ' +
                  '<a href="https://www.reddit.com/r/technology/">technology</a>' +
                '</blockquote>' +
                '<script async src="https://embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script>' +
              '</div>';
  }
  
  return card;
}

function showCards() {
  var newsList = [
    {
      title: 'The Era of Happy Tech Workers Is Over',
      image: 'https://source.unsplash.com/user/xteemu/800x600',
      description: 'The perks of working at a Silicon Valley firm are disappearing and unlikely to return. The current macroeconomic environment is forcing tech companies to optimize more for profit than growth.',
      link: 'https://archive.ph/xPIf3',
      type: 'classic'
    },
    {
      title: '',
      image: '',
      description: '',
      link: 'https://twitter.com/x/status/1635694897612173312',
      type: 'tweet'
    },
    {
      title: 'ChatGPT may be the fastest-growing consumer app in internet history, reaching 100 million users in just over 2 months, UBS report says',
      image: '',
      description: '',
      link: 'https://www.reddit.com/r/technology/comments/10ro9gi/chatgpt_may_be_the_fastestgrowing_consumer_app_in/?ref_source=embed&amp;ref=share',
      type: 'reddit'
    },
    {
      title: 'Next up for CRISPR: Gene editing for the masses?',
      image: 'https://source.unsplash.com/user/austindistel/800x600',
      description: 'Advances in CRISPR technology may soon make it possible for a vaccine that provides lifelong protection against heart disease. New forms of the technology, like prime editing, are broadening the scope of gene-editing treatments.',
      link: 'https://archive.ph/an4EL',
      type: 'classic'
    },
    {
    title: 'Netflix founder Reed Hastings steps down as co-CEO',
    image: 'http://adamthemes.com/demo/code/cards/images/blog01.jpeg',
    description: '',
    link: 'https://techcrunch.com/2023/01/19/netflix-founder-reed-hastings-steps-down-as-co-ceo/?utm_source=tldrnewsletter&guccounter=1',
    type: 'classic'
    },
    {
    title: '',
    image: '',
    description: '',
    link: 'https://twitter.com/AlphaSignalAI/status/1618026300421332993',
    type: 'tweet'
    }
  ];

  var cardHtml = '';
  for (var i = 0; i < newsList.length; i++) {
    var newsItem = newsList[i];
    cardHtml += createCard(newsItem.title, newsItem.image, newsItem.description, newsItem.link, newsItem.type);

    if (i === 2 || i === 5 || i === 8) {
      var id_col = 'col' + (Math.floor((i+1)/3)).toString();
      var cardContainer = document.getElementById(id_col);
      cardContainer.innerHTML = cardHtml;
      cardHtml = '';
    }
    if (i+1 === newsList.length) {
      if (cardHtml !== '') {
        var id_col = 'col' + (Math.floor((i+1)/3)+1).toString();
        var cardContainer = document.getElementById(id_col);
        cardContainer.innerHTML = cardHtml;
        cardHtml = '';
      }
    }
  }
  twttr.widgets.load();
  setTimeout(addListeners, 3000);
}

function addListeners() {
  const cards = document.querySelectorAll('.card, .card-blog, .twitter-tweet');

  cards.forEach(card => {
    card.addEventListener('click', event => {
      const clickedCard = event.target.closest('a');
      const cardTitle = clickedCard.querySelector('.card-caption').textContent;
      const cardImageSrc = clickedCard.querySelector('.img').getAttribute('src');
      const cardCategory = clickedCard.querySelector('.category').textContent;
      const cardDescription = clickedCard.querySelector('.card-description').textContent;
      
      console.log(`L'utilisateur a cliqué sur la card suivante :
      Titre : ${cardTitle}
      Image : ${cardImageSrc}
      Catégorie : ${cardCategory}
      Description : ${cardDescription}`);
    });
  });

  const reddits = document.querySelectorAll('.embedly-card');
  console.log(reddits);

  reddits.forEach(reddit => {
    reddit.addEventListener('click', event => {
      const clickedReddit = event.target;
      console.log(clickedReddit);
    });
  });

  const tweets = document.querySelectorAll('.twitter-tweet');
  const help = document.getElementById('twitter-widget-0');
  var parentWindow = help.contentWindow.parent;

  parentWindow.addEventListener('message', function(event) {
    console.log('received smh');
  })

  help.addEventListener("load", function() {
    console.log('test');
    var tweetDoc = help.contentDocument || help.contentWindow.document;
    var tweetLink = tweetDoc.querySelector(".tweet-link");

    tweetLink.addEventListener("click", function() {
      help.contentWindow.postMessage("User clicked on tweet!", "*");
    });
  });

  /*tweets.forEach(tweet => {
    var tweetDoc = tweet.contentWindow.document;
    tweetDoc.addEventListener('click', event => {
      const clickedTweet = event.target;
      console.log(clickedTweet);
    });
  });

  div_tweets = document.querySelectorAll('.twitterez');
  div_tweets.forEach(div_tweet => {
    div_tweet.addEventListener('click', event => {
      console.log('alors');
      const clickedTweet = event.target;
      console.log(clickedTweet);
    });
  });*/


  /*window.addEventListener('load', function() {
    // Get the tweet's iframe
    var tweetIframe = document.querySelector('.twitter-tweet > iframe');
    //console.log(tweetIframe)
    // Get the iframe's content window
    var tweetContentWindow = tweetIframe.contentWindow;
    // Add a click event listener to the body of the tweet
    tweetContentWindow.document.body.addEventListener('click', function() {
      // Handle the click event
      alert('You clicked the tweet!');
    });
  });*/

  /*const tests = document.querySelectorAll('#emb_fmdm35');
  tests.forEach(reddit => {
    reddit.addEventListener('click', event => {
      const clickedReddit = event.target;
      console.log(clickedReddit);
    });
  });*/

  /*cards.forEach(card => {
    card.addEventListener('click', event => {
      const clickedCard = event.target;
      console.log(clickedCard)
      console.log(`L'utilisateur a cliqué sur la card ${clickedCard.link}`);
    });
  });*/
}


/*
function showCards() {
  // get the container element
  var container = document.getElementById("card-container");
  container.innerHTML = "";

  // create a list of card data, such as an array of objects
  var cardData = [
    { title: "Card 1", body: "This is the body of card 1" },
    { title: "Card 2", body: "This is the body of card 2" },
    { title: "Card 3", body: "This is the body of card 3" }
  ];

  // loop through the card data and generate a card for each item
  for (var i = 0; i < cardData.length; i++) {
    // create a new card element
    var card = document.createElement("div");
    card.classList.add("card");

    // create the card header
    var header = document.createElement("div");
    header.classList.add("card-header");
    header.innerText = cardData[i].title;
    card.appendChild(header);

    // create the card body
    var body = document.createElement("div");
    body.classList.add("card-body");
    body.innerText = cardData[i].body;
    card.appendChild(body);

    // add the card to the container element
    if (container) {
      container.appendChild(card);
    } else {
      console.error("Container element not found");
    }
  }
}*/


