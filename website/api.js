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
    card = '<div class="col-md-4">' +
              '<div class="card card-blog">' +
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
              '</div>' +
            '</div>';
  } else if (type === 'tweet') {
    card = '<div class="col-md-4">' +
              '<blockquote class="twitter-tweet">' +
                '<a href="' + link + '"></a>' +
              '</blockquote>' +
            '</div>';
  } else if (type === 'reddit') {
    card = '<div class="col-md-4">' +
              '<div class="card">' +
                '<blockquote class="reddit-card" data-card-created=&quot;2023-02-02T16:19:41.554663+00:00&quot;>' +
                  '<a href="' + link + '">' + title + '</a> from ' +
                  '<a href="https://www.reddit.com/r/technology/">technology</a>' +
                '</blockquote>' +
                '<script async src="https://embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script>' +
              '</div>' +
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
    }
  ];

  var cardHtml = '';
  for (var i = 0; i < newsList.length; i++) {
    var newsItem = newsList[i];
    cardHtml += createCard(newsItem.title, newsItem.image, newsItem.description, newsItem.link, newsItem.type);

    // Add a row div and a new column every 3 cards
    if (i % 3 === 0) {
      cardHtml += '</div></div><div class="row"><div class="col-md-4">';
    }
  }

  // If the number of cards is not a multiple of 3, close the last row div
  if (newsList.length % 3 !== 0) {
    cardHtml += '</div></div>';
  }

  // Display the cards
  var cardContainer = document.getElementById('card-container');
  cardContainer.innerHTML = cardHtml;
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


